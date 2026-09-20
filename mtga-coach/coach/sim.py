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
# engine - shared by the terminal and the window
# --------------------------------------------------------------------------

class DraftEngine:
    """The pod, as an explicit state machine so any UI can drive it.

    Call current_pack(), then pick(grpid), until done. The terminal loop and
    the Tk window are both thin shells over this.
    """

    def __init__(self, base_ratings: Ratings, seed: Optional[int] = None,
                 seats: int = 8, profile=None):
        self.rng = random.Random(seed)
        self.pool_gen = CardPool(base_ratings, seed=seed or 20261002)
        self.ratings = sim_ratings(base_ratings, self.pool_gen)
        self.resolver = CardResolver({c.info.grpid: c.info for c in self.pool_gen.all})
        self.session = DraftSession(self.resolver, self.ratings, mode="draft",
                                    profile=profile)
        self.profile = profile
        self.seats = seats
        self.bots = [Bot(i, self.ratings, self.rng) for i in range(1, seats)]
        self.pack_no = 0
        self.pick_no = 0
        self.packs: list[list[CardInfo]] = []
        self.done = False
        self._open_pack(1)

    # -- state ------------------------------------------------------
    def _open_pack(self, pack_no: int) -> None:
        self.pack_no = pack_no
        self.pick_no = 1
        self.packs = [[c.info for c in self.pool_gen.make_pack(self.rng)]
                      for _ in range(self.seats)]
        self._score()

    def _score(self) -> None:
        if self.packs and self.packs[0]:
            self.session.on_pack(self.pack_no, self.pick_no,
                                 [c.grpid for c in self.packs[0]])

    def current_pack(self) -> list[CardInfo]:
        return self.packs[0] if self.packs else []

    @property
    def scored(self):
        return self.session.current_scored

    @property
    def annotation(self) -> dict:
        return self.session.annotation or {}

    def feedback(self, grpid: int) -> dict:
        """What the model thinks of a pick, before it is committed."""
        scored = self.scored
        best = scored[0] if scored else None
        taken = next((s for s in scored if s.card.grpid == grpid), None)
        if best is None or taken is None:
            return {}
        out = {"taken": taken, "best": best,
               "loss": round(best.score - taken.score, 2)}
        if self.profile is not None:
            from .playstyle import classify_pick
            v, why = classify_pick(scored, grpid, self.profile, self.ratings)
            out["style"], out["style_why"] = v, why
        return out

    # -- advance ----------------------------------------------------
    def pick(self, grpid: int) -> None:
        if self.done:
            return
        self.session.on_pick(grpid)
        self.packs[0] = [c for c in self.packs[0] if c.grpid != grpid]
        for b in self.bots:
            p = self.packs[b.seat]
            if p:
                taken = b.pick(p)
                self.packs[b.seat] = [c for c in p if c.grpid != taken.grpid]
        direction = 1 if self.pack_no % 2 == 1 else -1
        self.packs = self.packs[-direction:] + self.packs[:-direction]
        self.pick_no += 1
        if self.pick_no > 14 or not self.packs[0]:
            if self.pack_no >= 3:
                self.done = True
                return
            self._open_pack(self.pack_no + 1)
        else:
            self._score()

    def finish(self) -> Optional[Path]:
        path = self.session.save()
        if path:
            _mark_simulated(path)
        return path


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
    lands = [c for c in pool.picks if "land" in (c.types or "").lower()]
    playables = []
    for c in pool.picks:
        if "land" in (c.types or "").lower():
            continue
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
            "lands": lands, "meta": ratings.archetypes.get(pair, {})}


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
    out += splash_lines(d, ratings)
    return out


def splash_lines(d: dict, ratings: Ratings) -> list[str]:
    """Whether a third colour is on the table, given the lands actually drafted."""
    from .analysis import three_color_plan, annex_for
    out: list[str] = []
    fixers = d.get("lands") or []
    plan = three_color_plan(d["pair"])
    own = plan.get("own_land")
    own_n = sum(1 for c in fixers if c.name == own) if own else 0
    if own_n:
        out.append(f"Fixing: {own_n}x {own} for your main pair.")
    if plan["base"] == "enemy":
        out.append(plan["headline"] + " " + plan["advice"].split(" - ")[0])
    for o in plan["options"]:
        if o["kind"] != "shard":
            continue
        have = [c for c in fixers if c.name in o["land"].split(" + ")]
        if len(have) >= 2:
            out.append(f"SPLASH LIVE: {len(have)} {o['land']} - {o['color']} is "
                       f"open to you ({o['shard']}"
                       + (f", {o['nickname']}" if o["nickname"] else "") +
                       "). Splash a bomb or premium removal only, never a 2-drop.")
        elif len(have) == 1:
            out.append(f"Splash possible: 1 {have[0].name}. One more and {o['color']} "
                       "is a real option.")
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
    eng = DraftEngine(base_ratings, seed, seats, profile)
    ratings = eng.ratings

    print("=" * W)
    print("  PRACTICE DRAFT - Reality Fracture")
    print(f"  {seats}-player pod, 3 packs x 14 picks."
          f"  Cards marked {SYNTH} are generated placeholders.")
    print("  Enter a number to pick.  p = pool,  i N = inspect card N,  "
          "? = rubric,  q = quit")
    print("=" * W)

    while not eng.done:
        pack = eng.current_pack()
        if not pack:
            break
        scored = eng.scored
        if auto:
            choice = scored[0].card
        else:
            choice = None
            while choice is None:
                show_pack(pack, ratings, eng.pack_no, eng.pick_no,
                          scored if coach else None)
                a = _ask("\n  pick > ")
                low = a.lower()
                if low.startswith("q"):
                    print("\n  quit - nothing saved.")
                    return None
                if low.startswith("p"):
                    show_pool(eng.session.pool, ratings)
                    continue
                if low.startswith("i"):
                    rest = a[1:].strip()
                    if rest.isdigit() and 1 <= int(rest) <= len(pack):
                        _inspect(pack[int(rest) - 1], ratings, scored)
                    else:
                        print("  ? use 'i 3' to inspect card 3")
                    continue
                if a.startswith("?"):
                    print()
                    for i, line in enumerate(ratings.raw.get("rubric", []), 1):
                        print(textwrap.fill(f"  {i}. {line}", W,
                                            subsequent_indent="     "))
                    continue
                if a.isdigit() and 1 <= int(a) <= len(pack):
                    choice = pack[int(a) - 1]
                else:
                    print("  ? enter a card number, or p / i N / ? / q")

        if feedback and not auto:
            _show_feedback(eng.feedback(choice.grpid))
        eng.pick(choice.grpid)

    print("\n" + "=" * W)
    print("  DRAFT COMPLETE")
    print("=" * W)
    show_pool(eng.session.pool, ratings)
    d = build_deck(eng.session.pool, ratings)
    print()
    for line in grade_deck(d, ratings):
        print(textwrap.fill("  " + line, W, subsequent_indent="    "))
    print("\n  Deck:")
    for c in sorted(d["deck"], key=lambda c: (c.cmc or 0, c.name)):
        print("   " + fmt_card(c, ratings))

    path = eng.finish()
    if path:
        print(f"\n  saved -> {path}")
        print("  Now run:  python run_overlay.py --review     (grades this draft)")
        print("            python run_overlay.py --playstyle  (updates your profile)")
    return path


def _inspect(card: CardInfo, ratings: Ratings, scored) -> None:
    from .analysis import hover_text
    sc = next((s for s in (scored or []) if s.card.grpid == card.grpid), None)
    print()
    for line in hover_text(card, ratings, sc).splitlines():
        print(textwrap.fill(line, W, initial_indent="  ",
                            subsequent_indent="    ") if line else "")


def _show_feedback(fb: dict) -> None:
    if not fb:
        return
    best, taken, loss = fb["best"], fb["taken"], fb["loss"]
    if loss <= 0.05:
        print(f"\n  + {taken.card.name} - agrees with the model.")
    else:
        print(f"\n  - {taken.card.name} ({taken.score:.2f}).  "
              f"Model: {best.card.name} ({best.score:.2f}), -{loss}")
        print(textwrap.fill("    why: " + "; ".join(best.reasons[:2]), W,
                            subsequent_indent="         "))
    if fb.get("style") and fb["style"] not in ("unknown", ""):
        print(f"    style: {fb['style']} - {fb['style_why']}")


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
