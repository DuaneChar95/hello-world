"""Post-draft grading: what you took, what the model would have taken, and why.

The point is not the score. The point is the pattern across drafts -- whether
you consistently fight signals, under-draft interaction, or commit too late.
"""
from __future__ import annotations

from collections import Counter
from pathlib import Path
from typing import Optional

from .arenadb import CardInfo, CardResolver
from .model import PoolState, Ratings, score_pack
from .playstyle import build_profile, classify_pick, report as style_report
from .session import load_drafts, DRAFT_DIR


def _card(names: dict, gid: int, meta: Optional[dict] = None) -> CardInfo:
    m = (meta or {}).get(str(gid), {})
    return CardInfo(gid, names.get(str(gid), f"#{gid}"),
                    m.get("colors", ""), m.get("rarity", ""), "",
                    int(m.get("cmc") or 0), m.get("types", ""))


def regrade(draft: dict, ratings: Ratings, profile=None) -> dict:
    """Replay a saved draft through the current model."""
    names = draft.get("names", {})
    meta = draft.get("meta", {})
    pool = PoolState(mode=draft.get("mode", "draft"))
    rows = []
    for rp in draft.get("picks", []):
        pack = [_card(names, g, meta) for g in rp.get("pack", [])]
        if not pack:
            continue
        scored = score_pack(pack, pool, ratings, rp.get("pack_number", 1), rp.get("pick_number", 1))
        best = scored[0]
        chosen_id = rp.get("chosen")
        chosen = next((s for s in scored if s.card.grpid == chosen_id), None)
        loss = round(best.score - chosen.score, 2) if chosen else None
        verdict, vexp = classify_pick(scored, chosen_id, profile, ratings)
        rows.append({
            "style": verdict, "style_why": vexp,
            "pack": rp.get("pack_number", 1),
            "pick": rp.get("pick_number", 1),
            "took": chosen.card.name if chosen else "(unknown)",
            "took_score": chosen.score if chosen else None,
            "best": best.card.name,
            "best_score": best.score,
            "loss": loss,
            "why": best.reasons[:3],
            "rank": next((i + 1 for i, s in enumerate(scored) if s.card.grpid == chosen_id), None),
            "pack_size": len(scored),
        })
        if chosen:
            pool.add(chosen.card)
        elif chosen_id:
            pool.add(_card(names, chosen_id, meta))
    return {"rows": rows, "pool": pool}


def lessons(rows: list[dict], pool: PoolState, ratings: Ratings) -> list[str]:
    out: list[str] = []
    graded = [r for r in rows if r["loss"] is not None]
    if not graded:
        return ["Not enough recorded picks to grade."]

    losses = [r["loss"] for r in graded]
    avg = sum(losses) / len(losses)
    out.append(f"Average pick loss {avg:.2f} across {len(graded)} picks "
               f"({'tight' if avg < 0.25 else 'loose' if avg > 0.6 else 'reasonable'}).")

    agree = sum(1 for r in graded if r["rank"] == 1)
    out.append(f"You and the model agreed on {agree}/{len(graded)} picks "
               f"({100 * agree // len(graded)}%).")

    late_off = [r for r in graded
                if r["loss"] > 0.8 and (r["pack"] - 1) * 14 + r["pick"] > 10]
    if len(late_off) >= 3:
        out.append(f"{len(late_off)} late picks were well off the model's choice - "
                   "the usual cause is speculating on a lane after the point where "
                   "you should be taking playables.")

    early_loss = [r["loss"] for r in graded if (r["pack"] - 1) * 14 + r["pick"] <= 5]
    late_loss = [r["loss"] for r in graded if (r["pack"] - 1) * 14 + r["pick"] > 20]
    if early_loss and late_loss:
        e, l = sum(early_loss) / len(early_loss), sum(late_loss) / len(late_loss)
        if e > l + 0.3:
            out.append("Your early picks cost more than your late ones - you are "
                       "over-thinking pack 1. Early, just take the most powerful card.")
        elif l > e + 0.3:
            out.append("Your late picks cost more than your early ones - you are "
                       "staying open too long. Commit by around pick 5 of pack 1.")

    inter = pool.interaction_count(ratings)
    if inter < 4:
        caveat = ("" if ratings.confidence == "data" else
                  "  (Counted from the ratings file, which is still a pre-release prior and "
                  "does not yet know the set's removal - import 17Lands data to make this real.)")
        out.append(f"You finished with {inter} pieces of interaction. Every FRA deck wants 4+, "
                   "and instants are worth more here because they deny a prepared spell." + caveat)

    have_costs = any(c.cmc for c in pool.picks)
    if have_costs:
        curve = pool.curve()
        twos = curve.get(2, 0)
        if twos < 5 and pool.mode == "draft":
            out.append(f"Only {twos} two-drops. Target 5-6, and 7+ if you end up in R/W or B/R.")
        heavy = sum(v for k, v in curve.items() if k >= 5)
        if heavy > 5:
            out.append(f"{heavy} cards at five mana or more - that is a clunky deck in a format "
                       "where the aggro decks punish stumbles.")
    else:
        out.append("Curve not graded: this draft was recorded without mana costs "
                   "(Arena's card database was unreadable at the time).")

    lean = pool.archetype_lean(ratings)
    if lean:
        pair, _ = lean[0]
        meta = ratings.archetypes.get(pair, {})
        tier = meta.get("tier", "")
        out.append(f"You ended in {meta.get('name', pair)} ({pair}, tier {tier}, "
                   f"{meta.get('draft', '?')} draft score).")
        if tier == "C":
            out.append(f"{meta.get('name', pair)} is a C-tier lane. Ask whether it was open, "
                       "or whether you forced it.")

    worst = sorted(graded, key=lambda r: -(r["loss"] or 0))[:3]
    if worst and worst[0]["loss"] > 0.5:
        out.append("Biggest three leaks: " + "; ".join(
            f"P{r['pack']}p{r['pick']} took {r['took']} over {r['best']} (-{r['loss']})"
            for r in worst))
    return out


def review_all(ratings: Ratings, directory: Path = DRAFT_DIR, limit: Optional[int] = None,
               real_only: bool = False) -> str:
    drafts = load_drafts(directory, real_only=real_only)
    if not drafts:
        return (f"No saved drafts in {directory}.\n"
                "Run the overlay during a draft and they will be recorded automatically.")
    if limit:
        drafts = drafts[-limit:]
    profile = build_profile(ratings, directory, real_only=real_only)
    lines: list[str] = []
    all_rows: list[dict] = []
    for d in drafts:
        res = regrade(d, ratings, profile)
        all_rows += [r for r in res["rows"] if r["loss"] is not None]
        lines.append("=" * 70)
        lines.append(f"{Path(d['_file']).name}  -  {d.get('mode', 'draft')}"
                     f"{'  (practice)' if d.get('simulated') else ''}  -  "
                     f"{len(res['rows'])} picks")
        lines.append("-" * 70)
        for r in res["rows"]:
            flag = "   " if (r["loss"] or 0) <= 0.3 else ("!! " if (r["loss"] or 0) > 0.8 else " * ")
            lines.append(f"{flag}P{r['pack']}p{r['pick']:<2}  took {r['took'][:26]:<26} "
                         f"model {r['best'][:26]:<26} "
                         + (f"-{r['loss']}" if r["loss"] else "="))
            if (r["loss"] or 0) > 0.8:
                lines.append(f"        why: {'; '.join(r['why'])}")
            if r.get("style") == "stretch":
                lines.append(f"        stretch: {r['style_why']}")
        lines.append("")
        for t in lessons(res["rows"], res["pool"], ratings):
            lines.append("  * " + t)
        lines.append("")

    if len(drafts) > 1 and all_rows:
        lines.append("=" * 70)
        lines.append(f"ACROSS {len(drafts)} DRAFTS")
        lines.append("-" * 70)
        avg = sum(r["loss"] for r in all_rows) / len(all_rows)
        lines.append(f"  Average pick loss {avg:.2f} over {len(all_rows)} picks.")
        passed = Counter()
        for r in all_rows:
            if (r["loss"] or 0) > 0.8:
                passed[r["best"]] += 1
        if passed:
            lines.append("  Cards you most often pass that the model wants: " +
                         ", ".join(f"{n} (x{c})" for n, c in passed.most_common(5)))
    if profile:
        stretches = [r for r in all_rows if r.get("style") == "stretch"]
        instyle = [r for r in all_rows if r.get("style", "").startswith("in style")]
        if all_rows:
            lines.append(f"  Style: {len(instyle)} picks were the pick you normally make, "
                         f"{len(stretches)} were outside your usual range and still strong.")
        lines.append("")
        lines.append(style_report(profile, ratings))
    else:
        lines.append("")
        lines.append(f"Ratings source: {ratings.source}")
    return "\n".join(lines)
