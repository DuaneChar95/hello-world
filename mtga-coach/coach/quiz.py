"""Trainer. Two modes:

  drills  - concept questions about this format, playable before the set is out
  packs   - replays real packs from your own saved drafts and grades your pick

The packs mode is the one that actually moves your win rate, because it tests
you on the decisions you personally got wrong, with your real pool as context.
"""
from __future__ import annotations

import json
import random
import textwrap
from pathlib import Path
from typing import Optional

from .arenadb import CardInfo
from .model import PoolState, Ratings, score_pack
from .session import load_drafts, DRAFT_DIR

DATA = Path(__file__).resolve().parent.parent / "data"
PROFILE = Path.home() / ".mtga-coach" / "profile.json"

W = 74


def _wrap(s: str, indent: str = "     ") -> str:
    return "\n".join(textwrap.wrap(s, W, initial_indent=indent, subsequent_indent=indent))


def _ask(prompt: str) -> str:
    try:
        return input(prompt).strip()
    except (EOFError, KeyboardInterrupt):
        return "q"


def _load_profile() -> dict:
    try:
        return json.loads(PROFILE.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {"drills": {"seen": 0, "right": 0}, "packs": {"seen": 0, "right": 0}, "misses": {}}


def _save_profile(p: dict) -> None:
    PROFILE.parent.mkdir(parents=True, exist_ok=True)
    try:
        PROFILE.write_text(json.dumps(p, indent=1), encoding="utf-8")
    except OSError:
        pass


def run_drills(n: int = 10, seed: Optional[int] = None) -> None:
    data = json.loads((DATA / "drills.json").read_text(encoding="utf-8"))
    drills = data["drills"][:]
    rng = random.Random(seed)
    rng.shuffle(drills)
    drills = drills[:n]
    prof = _load_profile()
    right = 0

    print("\n" + "=" * W)
    print("  REALITY FRACTURE - CONCEPT DRILLS")
    print("  Answer with a number. 'q' quits.")
    print("=" * W)

    for i, d in enumerate(drills, 1):
        order = list(range(len(d["a"])))
        rng.shuffle(order)
        correct_pos = order.index(d["correct"])
        print(f"\n[{i}/{len(drills)}] {d['q']}\n")
        for j, oi in enumerate(order):
            print(f"   {j + 1}. {d['a'][oi]}")
        ans = _ask("\n  > ")
        if ans.lower().startswith("q"):
            break
        ok = ans.isdigit() and int(ans) - 1 == correct_pos
        if ok:
            right += 1
            print("\n  CORRECT.")
        else:
            print(f"\n  NO - the answer is {correct_pos + 1}. {d['a'][d['correct']]}")
            prof["misses"][d["q"][:60]] = prof["misses"].get(d["q"][:60], 0) + 1
        print(_wrap(d["why"]))
        print("-" * W)

    total = len(drills)
    prof["drills"]["seen"] += total
    prof["drills"]["right"] += right
    _save_profile(prof)
    print(f"\n  {right}/{total} this session.  "
          f"All time: {prof['drills']['right']}/{prof['drills']['seen']}")
    weak = sorted(prof["misses"].items(), key=lambda kv: -kv[1])[:3]
    if weak:
        print("\n  Concepts you keep missing:")
        for q, c in weak:
            print(f"    - {q}... (missed {c}x)")
    print()


def run_pack_quiz(ratings: Ratings, directory: Path = DRAFT_DIR,
                  n: int = 10, seed: Optional[int] = None,
                  hard_only: bool = False) -> None:
    """Replay real packs from your saved drafts and make you pick again."""
    drafts = load_drafts(directory)
    if not drafts:
        print(f"\nNo saved drafts in {directory}.")
        print("Run the overlay during a draft first - every pack you see is recorded.")
        print("In the meantime, try:  python run_overlay.py --drills\n")
        return

    rng = random.Random(seed)
    questions = []
    for d in drafts:
        names = d.get("names", {})
        meta = d.get("meta", {})
        pool = PoolState(mode=d.get("mode", "draft"))
        for rp in d.get("picks", []):
            pack = [CardInfo(g, names.get(str(g), f"#{g}"),
                             (meta.get(str(g)) or {}).get("colors", ""),
                             (meta.get(str(g)) or {}).get("rarity", ""), "",
                             int((meta.get(str(g)) or {}).get("cmc") or 0))
                    for g in rp.get("pack", [])]
            if len(pack) < 3:
                continue
            scored = score_pack(pack, pool, ratings,
                                rp.get("pack_number", 1), rp.get("pick_number", 1))
            chosen_id = rp.get("chosen")
            chosen = next((s for s in scored if s.card.grpid == chosen_id), None)
            loss = (scored[0].score - chosen.score) if chosen else 0.0
            if not hard_only or loss > 0.5:
                questions.append({
                    "pack_no": rp.get("pack_number", 1), "pick_no": rp.get("pick_number", 1),
                    "scored": scored, "pool_snapshot": list(pool.picks),
                    "you_took": chosen.card.name if chosen else None, "loss": round(loss, 2),
                })
            if chosen:
                pool.add(chosen.card)
            elif chosen_id:
                pool.add(CardInfo(chosen_id, names.get(str(chosen_id), f"#{chosen_id}")))

    if not questions:
        print("\nNo packs matched. Try without --hard.\n")
        return
    rng.shuffle(questions)
    questions = questions[:n]
    prof = _load_profile()
    right = 0

    print("\n" + "=" * W)
    print("  PACK QUIZ - your own drafts, replayed")
    print("  Pick a number. 'q' quits.")
    print("=" * W)

    for i, q in enumerate(questions, 1):
        pool_names = [c.name for c in q["pool_snapshot"]]
        print(f"\n[{i}/{len(questions)}]  Pack {q['pack_no']}, pick {q['pick_no']}")
        if pool_names:
            print(_wrap("Your pool: " + ", ".join(pool_names[-12:]), indent="  "))
        else:
            print("  Your pool: (empty - this is your first pick)")
        print()
        shown = q["scored"][:]
        rng.shuffle(shown)
        for j, s in enumerate(shown, 1):
            print(f"   {j:>2}. {s.card.name}")
        ans = _ask("\n  > ")
        if ans.lower().startswith("q"):
            break
        best = q["scored"][0]
        picked = None
        if ans.isdigit() and 1 <= int(ans) <= len(shown):
            picked = shown[int(ans) - 1]
        if picked and picked.card.grpid == best.card.grpid:
            right += 1
            print(f"\n  CORRECT - {best.card.name}")
        else:
            got = picked.card.name if picked else "(no answer)"
            print(f"\n  Model takes {best.card.name}  (you said {got})")
        print(_wrap("Why: " + "; ".join(best.reasons[:3])))
        if best.note:
            print(_wrap(best.note))
        if q["you_took"]:
            verdict = "matches the model" if q["loss"] <= 0.3 else f"cost about {q['loss']}"
            print(_wrap(f"In the real draft you took {q['you_took']} - {verdict}."))
        print("-" * W)

    total = len(questions)
    prof["packs"]["seen"] += total
    prof["packs"]["right"] += right
    _save_profile(prof)
    print(f"\n  {right}/{total} this session.  "
          f"All time: {prof['packs']['right']}/{prof['packs']['seen']}")
    print(f"\n  Reminder: the model is a pre-release prior ({ratings.confidence}), not data.")
    print("  Disagreeing with it is not automatically wrong - read the reason and judge.\n")
