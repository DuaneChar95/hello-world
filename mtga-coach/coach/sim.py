"""Practice draft and sealed: a full pod you can play without Arena.

Seven bots sit with you. They keep colour counts and commit to lanes, so what
gets cut upstream actually dries up downstream -- which means signal reading is
a real skill here rather than a decoration. Packs pass left, right, left.

Advice is hidden while you pick, by default. A practice tool that shows you the
answer first is a reading exercise, not a draft. You get the verdict after the
pick instead, and the full review at the end.

Every practice draft is saved in the same format as a real one, so --review,
--playstyle and --quiz all work on them unchanged.
"""
from __future__ import annotations

import json
import random
import textwrap
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from .arenadb import CardInfo, CardResolver
from .cards import CardPool, SYNTH
from .model import PoolState, Ratings, score_pack
from .session import DraftSession, DRAFT_DIR

W = 76
PIP = {"W": "W", "U": "U", "B": "B", "R": "R", "G": "G"}
RAR = {"common": "c", "uncommon": "u", "rare": "R", "mythic": "M", "": "?"}


def sim_ratings(base: Ratings, pool: CardPool) -> Ratings:
    """A ratings object that knows the generated cards too."""
    raw = dict(base.raw)
    cards = dict(base.cards)
    for name, e in pool.ratings_overlay().items():
        cards.setdefault(name, e)
    raw["cards"] = cards
    return Ratings(raw)


# --------------------------------------------------------------------------
# bots
# --------------------------------------------------------------------------

class Bot:
    """Deliberately a bit worse than optimal, so lanes genuinely open up."""

    def __init__(self, seat: int, ratings: Ratings, rng: random.Random):
        self.seat = seat
        self.ratings = ratings
        self.rng = rng
        self.counts: dict[str, int] = {c: 0 for c in "WUBRG"}
        self.picks: list[CardInfo] = []

    def _commitment(self) -> float:
        return min(1.0, len(self.picks) / 12.0)

    def pick(self, pack: list[CardInfo]) -> CardInfo:
        top = sorted(self.counts.items(), key=lambda kv: -kv[1])
        main = {c for c, v in top[:2] if v >= 2}
        best, best_v = pack[0], -99.0
        for card in pack:
            g, _ = self.ratings.base_grade(card)
            cols = self.ratings.card_colors(card)
            v = g + self.rng.uniform(-0.35, 0.35)
            if cols:
                if main:
                    if cols <= main:
                        v += 1.1 * self._commitment()
                    elif cols & main:
                        v += 0.4 * self._commitment()
                    else:
                        v -= 1.4 * self._commitment()
                else:
                    v += 0.12 * sum(self.counts[c] for c in cols)
            if v > best_v:
                best, best_v = card, v
        self.picks.append(best)
        for c in self.ratings.card_colors(best):
            self.counts[c] += 1
        return best


# --------------------------------------------------------------------------
# display
# --------------------------------------------------------------------------

def fmt_card(c: CardInfo, ratings: Ratings, width: int = 30) -> str:
    cols = "".join(sorted(ratings.card_colors(c), key="WUBRG".index)) or "-"
    return (f"{c.name[:width]:<{width}} {cols:<2} {c.cmc or '-'}  "
            f"{RAR.get((c.rarity or '').lower(), '?')}")


def show_pack(pack: list[CardInfo], ratings: Ratings, pack_no: int, pick_no: int,
              coach: Optional[list] = None) -> None:
    print(f"\n{'-' * W}")
    print(f"  PACK {pack_no}  PICK {pick_no}   ({len(pack)} cards)")
    print(f"{'-' * W}")
    half = (len(pack) + 1) // 2
    for i in range(half):
        left = f"{i + 1:>2}. {fmt_card(pack[i], ratings, 28)}"
        j = i + half
        right = f"{j + 1:>2}. {fmt_card(pack[j], ratings, 28)}" if j < len(pack) else ""
        print(f"  {left:<43}{right}".rstrip())
    if coach:
        print(f"\n  coach: " + ", ".join(
            f"{s.card.name} {s.score:.1f}" for s in coach[:3]))


def show_pool(pool: PoolState, ratings: Ratings) -> None:
    from .model import pool_summary
    sm = pool_summary(pool, ratings)
    print(f"\n  POOL ({sm['picks']} cards)   " +
          "  ".join(f"{k}{v}" for k, v in sm["colors"].items()))
    by_col: dict[str, list[str]] = {}
    for c in pool.picks:
        key = "".join(sorted(ratings.card_colors(c), key="WUBRG".index)) or "C"
        by_col.setdefault(key, []).append(f"{c.name}({c.cmc or '-'})")
    for key in sorted(by_col, key=lambda k: (len(k), k)):
        print(textwrap.fill(f"  {key}: " + ", ".join(by_col[key]), W,
                            subsequent_indent="      "))
    print(f"  lean: {sm['top_name']} ({sm['top_pair']})  tier {sm['tier']}   "
          f"interaction {sm['interaction']}")
    print(f"  {sm['verdict']}")


# --------------------------------------------------------------------------
# deck building
# --------------------------------------------------------------------------

def build_deck(pool: PoolState, ratings: Ratings, size: int = 23) -> dict:
    lean = pool.archetype_lean(ratings)
    pair = lean[0][0] if lean else "WU"
    wanted = set(pair)
    playables = []
    for c in pool.picks:
        cols = ratings.card_colors(c)
        if cols and not cols <= wanted:
            continue
        g, _ = ratings.base_grade(c)
        playables.append((g, c))
    playables.sort(key=lambda t: -t[0])
    deck = [c for _, c in playables[:size]]
    curve: dict[int, int] = {}
    for c in deck:
        b = min(max(c.cmc or 3, 1), 6)
        curve[b] = curve.get(b, 0) + 1
    creatures = sum(1 for c in deck if "creature" in (c.types or "").lower())
    inter = sum(1 for c in deck
                if any(t.startswith("removal") or t == "boardwipe"
                       for t in ratings.tags(c)))
    return {"pair": pair, "deck": deck, "curve": curve, "creatures": creatures,
            "interaction": inter, "playable_count": len(playables),
            "meta": ratings.archetypes.get(pair, {})}


def grade_deck(d: dict, ratings: Ratings, mode: str = "draft") -> list[str]:
    out = []
    n = len(d["deck"])
    meta = d["meta"]
    out.append(f"Best build: {meta.get('name', d['pair'])} ({d['pair']}) - "
               f"{n} playables from {d['playable_count']} on-colour cards")
    if n < 23:
        out.append(f"SHORT: only {n} playables. You needed more on-colour picks - "
                   "in FRA there are ~14 commons per colour, so the back half of "
                   "packs will not bail you out.")
    twos = d["curve"].get(2, 0)
    target = 5 if mode == "draft" else 4
    if twos < target:
        out.append(f"Curve: {twos} two-drops, want {target}-6"
                   + (" (7+ in R/W or B/R)" if d["pair"] in ("RW", "BR") else ""))
    heavy = sum(v for k, v in d["curve"].items() if k >= 5)
    if heavy > 5:
        out.append(f"Curve: {heavy} cards at 5+. That is clunky.")
    if d["interaction"] < 4:
        out.append(f"Interaction: {d['interaction']}. Every FRA deck wants 4+, "
                   "and instants beat sorceries here because they deny a prepared spell.")
    if d["creatures"] < 14:
        out.append(f"Creatures: {d['creatures']}. Want 15-17.")
    lands = 17
    if d["pair"] == "RG" and heavy >= 4:
        lands = 18
        out.append("Heartwood ramp with a real top end - play 18 lands.")
    out.append(f"Lands: {lands}.   Curve: " +
               " ".join(f"{k}:{d['curve'].get(k, 0)}" for k in range(1, 7)))
    return out


# --------------------------------------------------------------------------
# the draft
# --------------------------------------------------------------------------

def _ask(prompt: str) -> str:
    try:
        return input(prompt).strip()
    except (EOFError, KeyboardInterrupt):
        return "q"


def run_draft(base_ratings: Ratings, seed: Optional[int] = None, seats: int = 8,
              coach: bool = False, auto: bool = False, feedback: bool = True,
              profile=None) -> Optional[Path]:
    rng = random.Random(seed)
    pool_gen = CardPool(base_ratings, seed=seed or 20261002)
    ratings = sim_ratings(base_ratings, pool_gen)
    resolver = CardResolver({c.info.grpid: c.info for c in pool_gen.all})
    session = DraftSession(resolver, ratings, mode="draft", profile=profile)
    bots = [Bot(i, ratings, rng) for i in range(1, seats)]

    print("=" * W)
    print("  PRACTICE DRAFT - Reality Fracture")
    print(f"  {seats}-player pod, 3 packs x 14 picks."
          f"  Cards marked {SYNTH} are generated placeholders.")
    print("  Enter a number to pick.  p = pool,  ? = rubric,  q = quit")
    print("=" * W)

    for pack_no in (1, 2, 3):
        packs = [[c.info for c in pool_gen.make_pack(rng)] for _ in range(seats)]
        direction = 1 if pack_no % 2 == 1 else -1
        for pick_no in range(1, 15):
            if not packs[0]:
                break
            session.on_pack(pack_no, pick_no, [c.grpid for c in packs[0]])
            scored = session.current_scored
            if auto:
                choice = scored[0].card
            else:
                while True:
                    show_pack(packs[0], ratings, pack_no, pick_no,
                              scored if coach else None)
                    a = _ask("\n  pick > ")
                    if a.lower().startswith("q"):
                        print("\n  quit - nothing saved.")
                        return None
                    if a.lower().startswith("p"):
                        show_pool(session.pool, ratings)
                        continue
                    if a.startswith("?"):
                        print()
                        for i, line in enumerate(ratings.raw.get("rubric", []), 1):
                            print(textwrap.fill(f"  {i}. {line}", W,
                                                subsequent_indent="     "))
                        continue
                    if a.isdigit() and 1 <= int(a) <= len(packs[0]):
                        choice = packs[0][int(a) - 1]
                        break
                    print("  ? enter a card number, or p / ? / q")

            if feedback and not auto:
                _pick_feedback(scored, choice, ratings, session, profile)
            session.on_pick(choice.grpid)
            packs[0] = [c for c in packs[0] if c.grpid != choice.grpid]

            for b in bots:
                p = packs[b.seat]
                if p:
                    taken = b.pick(p)
                    packs[b.seat] = [c for c in p if c.grpid != taken.grpid]
            packs = packs[-direction:] + packs[:-direction]

    print("\n" + "=" * W)
    print("  DRAFT COMPLETE")
    print("=" * W)
    show_pool(session.pool, ratings)
    d = build_deck(session.pool, ratings)
    print()
    for line in grade_deck(d, ratings):
        print(textwrap.fill("  " + line, W, subsequent_indent="    "))
    print("\n  Deck:")
    for c in sorted(d["deck"], key=lambda c: (c.cmc or 0, c.name)):
        print("   " + fmt_card(c, ratings))

    path = session.save()
    if path:
        _mark_simulated(path)
        print(f"\n  saved -> {path}")
        print("  Now run:  python run_overlay.py --review     (grades this draft)")
        print("            python run_overlay.py --playstyle  (updates your profile)")
    return path


def _pick_feedback(scored, choice: CardInfo, ratings: Ratings,
                   session: DraftSession, profile) -> None:
    best = scored[0]
    taken = next((s for s in scored if s.card.grpid == choice.grpid), None)
    if taken is None:
        return
    loss = round(best.score - taken.score, 2)
    if loss <= 0.05:
        print(f"\n  + {choice.name} - agrees with the model.")
    else:
        print(f"\n  - {choice.name} ({taken.score:.2f}).  "
              f"Model: {best.card.name} ({best.score:.2f}), -{loss}")
        print(textwrap.fill("    why: " + "; ".join(best.reasons[:2]), W,
                            subsequent_indent="         "))
    if profile is not None:
        from .playstyle import classify_pick
        v, why = classify_pick(scored, choice.grpid, profile, ratings)
        if v not in ("unknown", ""):
            print(f"    style: {v} - {why}")


def _mark_simulated(path: Path) -> None:
    try:
        d = json.loads(path.read_text(encoding="utf-8"))
        d["simulated"] = True
        path.write_text(json.dumps(d, indent=1), encoding="utf-8")
    except (OSError, ValueError):
        pass


# --------------------------------------------------------------------------
# sealed
# --------------------------------------------------------------------------

def run_sealed(base_ratings: Ratings, seed: Optional[int] = None,
               packs: int = 6, auto: bool = False, profile=None) -> Optional[Path]:
    rng = random.Random(seed)
    pool_gen = CardPool(base_ratings, seed=seed or 20261002)
    ratings = sim_ratings(base_ratings, pool_gen)
    cards: list[CardInfo] = []
    for _ in range(packs):
        cards += [c.info for c in pool_gen.make_pack(rng)]

    print("=" * W)
    print("  PRACTICE SEALED - Reality Fracture")
    print(f"  {packs} packs, {len(cards)} cards. Build 40 with 17 lands.")
    print(f"  Cards marked {SYNTH} are generated placeholders.")
    print("=" * W)

    state = PoolState(mode="sealed")
    for c in cards:
        state.add(c)

    by_col: dict[str, list[CardInfo]] = {}
    for c in cards:
        key = "".join(sorted(ratings.card_colors(c), key="WUBRG".index)) or "C"
        by_col.setdefault(key, []).append(c)
    for key in sorted(by_col, key=lambda k: (len(k), k)):
        print(f"\n  --- {key} ({len(by_col[key])}) ---")
        for c in sorted(by_col[key], key=lambda c: -ratings.base_grade(c)[0]):
            print("   " + fmt_card(c, ratings))

    lean = state.archetype_lean(ratings)
    print("\n" + "-" * W)
    print("  Your call first. Which two colours, and why?")
    print("  Work the order: bombs -> the deck your bombs are in -> removal count.")
    if not auto:
        answer = _ask("\n  your build (e.g. 'UB') > ").upper()
    else:
        answer = ""
    print("-" * W)

    d = build_deck(state, ratings, size=23)
    if answer and len(answer) == 2 and all(ch in "WUBRG" for ch in answer):
        forced = PoolState(mode="sealed")
        for c in cards:
            cols = ratings.card_colors(c)
            if not cols or cols <= set(answer):
                forced.add(c)
        yours = build_deck(forced, ratings, size=23)
        print(f"\n  YOUR BUILD: {answer}")
        for line in grade_deck(yours, ratings, "sealed"):
            print(textwrap.fill("  " + line, W, subsequent_indent="    "))
        if yours["pair"] != d["pair"]:
            print(f"\n  The model would build {d['meta'].get('name', d['pair'])} "
                  f"({d['pair']}) instead:")
    else:
        print(f"\n  MODEL BUILD:")
    for line in grade_deck(d, ratings, "sealed"):
        print(textwrap.fill("  " + line, W, subsequent_indent="    "))
    print("\n  Deck:")
    for c in sorted(d["deck"], key=lambda c: (c.cmc or 0, c.name)):
        print("   " + fmt_card(c, ratings))
    print("\n  Top 3 archetype fits for this pool:")
    for pair, sc in lean[:3]:
        meta = ratings.archetypes.get(pair, {})
        print(f"    {pair}  {meta.get('name', pair):<22} "
              f"sealed {meta.get('sealed', '?')}  tier {meta.get('tier', '?')}")
    return None
