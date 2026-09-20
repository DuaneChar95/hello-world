"""Playstyle profiling.

Two different things get confused in draft coaching, so this module keeps them
apart on purpose:

  STYLE  - a preference. You take cheap creatures, you commit early, you like
           blue. None of that is wrong. It is who you are at the table.
  LEAK   - a habit that costs you. Measured, not assumed: the average pick loss
           on picks that express a tendency, against picks that do not.

A tendency is only called a leak when the numbers say it costs something. Some
of your tendencies will turn out to be *earning* you points, and the report says
so rather than trying to sand you into a generic drafter.

Everything is computed from your own saved drafts. Small samples are labelled
as such instead of being dressed up as insight.
"""
from __future__ import annotations

import statistics
import textwrap
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from .arenadb import CardInfo
from .model import PoolState, Ratings, score_pack
from .session import load_drafts, DRAFT_DIR

COLORS = "WUBRG"


# --------------------------------------------------------------------------
# per-pick observation
# --------------------------------------------------------------------------

@dataclass
class Obs:
    """One pick, with everything needed to characterise it."""
    pack_no: int
    pick_no: int
    seen: list[CardInfo]
    taken: Optional[CardInfo]
    loss: float                      # model-best score minus taken score
    tags: set[str] = field(default_factory=set)

    @property
    def index(self) -> int:
        return (self.pack_no - 1) * 14 + self.pick_no


def _card_from(draft: dict, gid: int, ratings: Ratings) -> CardInfo:
    names, meta = draft.get("names", {}), draft.get("meta", {})
    m = meta.get(str(gid), {})
    name = names.get(str(gid), f"#{gid}")
    colors, rarity, cmc = m.get("colors", ""), m.get("rarity", ""), int(m.get("cmc") or 0)
    if not colors or not rarity:
        e = ratings.entry(name) or {}
        colors = colors or e.get("colors", "")
        rarity = rarity or e.get("rarity", "")
    return CardInfo(gid, name, colors, rarity, "", cmc, m.get("types", ""))


def observe(drafts: list[dict], ratings: Ratings) -> list[Obs]:
    """Replay every saved draft and tag each pick with what it expressed."""
    out: list[Obs] = []
    for d in drafts:
        pool = PoolState(mode=d.get("mode", "draft"))
        for rp in d.get("picks", []):
            ids = rp.get("pack", [])
            if len(ids) < 2:
                continue
            pack = [_card_from(d, g, ratings) for g in ids]
            scored = score_pack(pack, pool, ratings,
                                rp.get("pack_number", 1), rp.get("pick_number", 1))
            chosen_id = rp.get("chosen")
            taken = next((s.card for s in scored if s.card.grpid == chosen_id), None)
            if taken is None:
                continue
            by_adj = scored
            by_base = sorted(scored, key=lambda s: -s.base)
            tk = next(s for s in scored if s.card.grpid == chosen_id)
            o = Obs(rp.get("pack_number", 1), rp.get("pick_number", 1),
                    pack, taken, round(by_adj[0].score - tk.score, 2))

            # --- what did this pick express? ---------------------------
            if tk.card.grpid == by_base[0].card.grpid and tk.card.grpid != by_adj[0].card.grpid:
                o.tags.add("power_over_fit")
            if tk.card.grpid == by_adj[0].card.grpid and tk.card.grpid != by_base[0].card.grpid:
                o.tags.add("fit_over_power")
            if (taken.rarity or "").lower() in ("rare", "mythic"):
                better_cheap = [s for s in scored
                                if s.score > tk.score
                                and (s.card.rarity or "").lower() in ("common", "uncommon")]
                if better_cheap:
                    o.tags.add("rarity_chase")
            if taken.cmc and taken.cmc <= 2:
                o.tags.add("cheap")
            if taken.cmc and taken.cmc >= 5:
                o.tags.add("expensive")
            if any(t.startswith("removal") or t == "boardwipe" for t in ratings.tags(taken)):
                o.tags.add("interaction")
            if "creature" in (taken.types or "").lower():
                o.tags.add("creature")
            committed = pool.committed(ratings)
            tcols = ratings.card_colors(taken)
            if o.index > 5 and committed and tcols and not (tcols & committed):
                o.tags.add("off_color_late")
            if not tcols:
                o.tags.add("colorless")
            out.append(o)
            pool.add(taken)
    return out


# --------------------------------------------------------------------------
# axes
# --------------------------------------------------------------------------

@dataclass
class Axis:
    key: str
    label: str
    left: str
    right: str
    value: float          # -1.0 .. +1.0, negative = left pole
    detail: str


def _bias(taken: int, seen: int, total_taken: int, total_seen: int) -> float:
    """How much more often a thing is taken than its share of what's offered."""
    if not total_taken or not total_seen or not seen:
        return 0.0
    took_share = taken / total_taken
    seen_share = seen / total_seen
    if seen_share <= 0:
        return 0.0
    return took_share / seen_share


def color_bias(obs: list[Obs], ratings: Ratings) -> dict[str, float]:
    taken_c: Counter = Counter()
    seen_c: Counter = Counter()
    tt = ss = 0
    for o in obs:
        for col in ratings.card_colors(o.taken):
            taken_c[col] += 1
            tt += 1
        for c in o.seen:
            for col in ratings.card_colors(c):
                seen_c[col] += 1
                ss += 1
    return {c: round(_bias(taken_c[c], seen_c[c], tt, ss), 2) for c in COLORS}


def commitment_point(drafts: list[dict], ratings: Ratings) -> Optional[float]:
    """Average pick number after which your top two colours stop changing."""
    points: list[int] = []
    for d in drafts:
        seq = []
        for rp in d.get("picks", []):
            cid = rp.get("chosen")
            if cid:
                seq.append(_card_from(d, cid, ratings))
        if len(seq) < 10:
            continue
        pairs = []
        run: Counter = Counter()
        for c in seq:
            for col in ratings.card_colors(c):
                run[col] += 1
            pairs.append(frozenset(x for x, _ in run.most_common(2)))
        final = pairs[-1]
        lock = len(pairs)
        for i in range(len(pairs) - 1, -1, -1):
            if pairs[i] != final:
                lock = i + 2
                break
            lock = i + 1
        points.append(lock)
    return round(statistics.mean(points), 1) if points else None


def build_axes(obs: list[Obs], drafts: list[dict], ratings: Ratings) -> list[Axis]:
    axes: list[Axis] = []
    if not obs:
        return axes

    # -- speed -------------------------------------------------------
    tk = [o.taken.cmc for o in obs if o.taken.cmc]
    sn = [c.cmc for o in obs for c in o.seen if c.cmc]
    if tk and sn:
        d = statistics.mean(sn) - statistics.mean(tk)      # positive = cheaper
        axes.append(Axis("speed", "Curve", "slow / top-heavy", "fast / cheap",
                         max(-1.0, min(1.0, d / 0.8)),
                         f"your picks average {statistics.mean(tk):.2f} mana against "
                         f"{statistics.mean(sn):.2f} for the cards you see "
                         f"({'cheaper' if d > 0 else 'more expensive'} by {abs(d):.2f})"))

    # -- power vs synergy --------------------------------------------
    p = sum(1 for o in obs if "power_over_fit" in o.tags)
    f = sum(1 for o in obs if "fit_over_power" in o.tags)
    if p + f >= 5:
        v = (p - f) / (p + f)
        axes.append(Axis("power", "Selection", "synergy first", "raw power first", v,
                         f"{p} picks took the strongest card over the better fit, "
                         f"{f} went the other way"))

    # -- commitment ---------------------------------------------------
    cp = commitment_point(drafts, ratings)
    if cp is not None:
        axes.append(Axis("commit", "Commitment", "commits early", "stays open late",
                         max(-1.0, min(1.0, (cp - 12) / 10.0)),
                         f"your final two colours settle around pick {cp:.0f} on average"))

    # -- interaction ---------------------------------------------------
    it = sum(1 for o in obs if "interaction" in o.tags)
    isn = sum(1 for o in obs for c in o.seen
              if any(t.startswith("removal") or t == "boardwipe" for t in ratings.tags(c)))
    if isn:
        b = _bias(it, isn, len(obs), sum(len(o.seen) for o in obs))
        axes.append(Axis("interaction", "Interaction", "avoids removal", "prioritises removal",
                         max(-1.0, min(1.0, (b - 1.0))),
                         f"you take removal {b:.2f}x as often as it appears in your packs"))

    # -- creatures ------------------------------------------------------
    ct = sum(1 for o in obs if "creature" in o.tags)
    csn = sum(1 for o in obs for c in o.seen if "creature" in (c.types or "").lower())
    if csn:
        b = _bias(ct, csn, len(obs), sum(len(o.seen) for o in obs))
        axes.append(Axis("creatures", "Board", "spell-leaning", "creature-leaning",
                         max(-1.0, min(1.0, (b - 1.0) * 2)),
                         f"you take creatures {b:.2f}x as often as they appear"))

    # -- risk -----------------------------------------------------------
    off = sum(1 for o in obs if "off_color_late" in o.tags)
    axes.append(Axis("risk", "Discipline", "stays in lane", "speculates late",
                     max(-1.0, min(1.0, off / max(len(obs), 1) * 8)),
                     f"{off} of {len(obs)} picks were off-colour after pick 5"))
    return axes


# --------------------------------------------------------------------------
# leaks: which tendencies actually cost something
# --------------------------------------------------------------------------

TENDENCY_LABELS = {
    "power_over_fit": "taking the strongest card over the better fit",
    "fit_over_power": "taking the synergy card over the strongest card",
    "rarity_chase": "taking a rare over a better-scoring common or uncommon",
    "off_color_late": "picking off-colour after pick 5",
    "cheap": "taking cheap cards",
    "expensive": "taking five-plus drops",
    "interaction": "taking removal",
    "creature": "taking creatures",
}


def leak_analysis(obs: list[Obs], min_n: int = 6) -> list[dict]:
    out = []
    overall = [o.loss for o in obs]
    if len(overall) < min_n * 2:
        return out
    for tag, label in TENDENCY_LABELS.items():
        with_t = [o.loss for o in obs if tag in o.tags]
        without = [o.loss for o in obs if tag not in o.tags]
        if len(with_t) < min_n or len(without) < min_n:
            continue
        a, b = statistics.mean(with_t), statistics.mean(without)
        out.append({"tag": tag, "label": label, "n": len(with_t),
                    "with": round(a, 2), "without": round(b, 2), "delta": round(a - b, 2)})
    out.sort(key=lambda r: -r["delta"])
    return out


# --------------------------------------------------------------------------
# profile
# --------------------------------------------------------------------------

@dataclass
class Profile:
    obs: list[Obs]
    axes: list[Axis]
    colors: dict[str, float]
    archetypes: Counter
    leaks: list[dict]
    n_drafts: int

    @property
    def n_picks(self) -> int:
        return len(self.obs)

    @property
    def confidence(self) -> str:
        if self.n_drafts < 3:
            return "provisional"
        if self.n_drafts < 10:
            return "emerging"
        return "established"

    def axis(self, key: str) -> Optional[Axis]:
        return next((a for a in self.axes if a.key == key), None)

    def label(self) -> str:
        """A short name for how you draft. Two traits, not a horoscope."""
        parts = []
        sp, pw, cm = self.axis("speed"), self.axis("power"), self.axis("commit")
        if cm and cm.value < -0.3:
            parts.append("Committed")
        elif cm and cm.value > 0.3:
            parts.append("Open")
        if pw and pw.value > 0.35:
            parts.append("Power")
        elif pw and pw.value < -0.35:
            parts.append("Synergy")
        if sp and sp.value > 0.35:
            parts.append("Aggro")
        elif sp and sp.value < -0.35:
            parts.append("Midrange")
        if not parts:
            return "Balanced Drafter"
        return " ".join(parts[:2]) + " Drafter"

    def favourite_colors(self, n: int = 2) -> list[str]:
        return [c for c, _ in sorted(self.colors.items(), key=lambda kv: -kv[1])[:n]]

    def avoided_colors(self) -> list[str]:
        return [c for c, v in sorted(self.colors.items(), key=lambda kv: kv[1]) if v < 0.75]


def build_profile(ratings: Ratings, directory: Path = DRAFT_DIR,
                  real_only: bool = False) -> Optional[Profile]:
    drafts = load_drafts(directory, real_only=real_only)
    if not drafts:
        return None
    obs = observe(drafts, ratings)
    if not obs:
        return None
    arche: Counter = Counter()
    for d in drafts:
        pool = PoolState(mode=d.get("mode", "draft"))
        for nm in d.get("final_pool", []):
            e = ratings.entry(nm) or {}
            pool.add(CardInfo(0, nm, e.get("colors", ""), e.get("rarity", ""), "", 0))
        lean = pool.archetype_lean(ratings)
        if lean:
            arche[lean[0][0]] += 1
    return Profile(obs, build_axes(obs, drafts, ratings), color_bias(obs, ratings),
                   arche, leak_analysis(obs), len(drafts))


# --------------------------------------------------------------------------
# in-style vs stretch
# --------------------------------------------------------------------------

def style_fit(card: CardInfo, profile: Optional["Profile"], ratings: Ratings) -> float:
    """How much this card looks like something you normally take (0..1).

    Each component is weighted by how strongly that axis actually defines you.
    A drafter with no speed preference gets no speed signal, rather than a
    meaningless 0.5 diluting everything else. A genuinely balanced drafter
    therefore has no "usual pick" -- and the caller is expected to say so
    instead of inventing one.
    """
    if profile is None:
        return 0.5
    score = weight = 0.0

    cols = ratings.card_colors(card)
    if cols:
        b = statistics.mean([profile.colors.get(c, 1.0) for c in cols])
        w = min(1.0, abs(b - 1.0) * 3.0)
        score += max(0.0, min(1.0, 0.5 + (b - 1.0) * 1.2)) * w
        weight += w

    sp = profile.axis("speed")
    if sp and card.cmc:
        w = abs(sp.value)
        cheapness = max(0.0, min(1.0, (6 - card.cmc) / 5))
        score += (cheapness if sp.value > 0 else 1 - cheapness) * w
        weight += w

    inter = profile.axis("interaction")
    if inter and any(t.startswith("removal") or t == "boardwipe" for t in ratings.tags(card)):
        w = abs(inter.value)
        score += max(0.0, min(1.0, 0.5 + inter.value / 2)) * w
        weight += w

    cr = profile.axis("creatures")
    if cr and "creature" in (card.types or "").lower():
        w = abs(cr.value)
        score += max(0.0, min(1.0, 0.5 + cr.value / 2)) * w
        weight += w

    if weight < 0.15:            # no strong tendencies -> no opinion
        return 0.5
    return round(score / weight, 2)


def _pack_fits(scored, profile, ratings) -> dict[int, float]:
    return {s.card.grpid: style_fit(s.card, profile, ratings) for s in scored}


def annotate_pack(scored, profile: Optional["Profile"], ratings: Ratings,
                  stretch_window: float = 0.6) -> dict:
    """Mark the default pick and the best genuinely style-breaking alternative.

    A stretch pick is a card that is nearly as good as your default but is the
    kind of card you normally pass. It is offered as a *choice*, never as a
    correction -- taking it is how a drafter's range grows, and skipping it is
    not a mistake.

    Fit is judged against the rest of this pack, not an absolute scale, so a
    pack of cards you all like equally produces no stretch pick at all.
    """
    if not scored:
        return {"default": None, "stretch": None, "default_is_stretch": False, "fits": {}}
    if profile is None or profile.n_picks < 20:
        return {"default": scored[0], "stretch": None, "default_is_stretch": False,
                "fits": {s.card.grpid: 0.5 for s in scored}}
    fits = _pack_fits(scored, profile, ratings)
    default = scored[0]
    dfit = fits[default.card.grpid]
    vals = sorted(fits.values())
    spread = vals[-1] - vals[0]
    if spread < 0.12:
        return {"default": default, "stretch": None, "default_is_stretch": False, "fits": fits}
    margin = max(0.10, spread * 0.4)

    # The best card in the pack is itself one you would normally pass. That is
    # the more valuable warning than any alternative, so it wins.
    if dfit <= statistics.median(vals) - margin:
        return {"default": default, "stretch": None, "default_is_stretch": True, "fits": fits}

    near = [s for s in scored[1:] if default.score - s.score <= stretch_window]
    off = [s for s in near if fits[s.card.grpid] <= dfit - margin]
    stretch = min(off, key=lambda s: fits[s.card.grpid]) if off else None
    return {"default": default, "stretch": stretch, "default_is_stretch": False, "fits": fits}


def classify_pick(scored, taken_id: int, profile: Optional["Profile"],
                  ratings: Ratings) -> tuple[str, str]:
    """(verdict, explanation) for a pick that was actually made.

    "In style" means the card sat on the side of this pack you usually take,
    which is a comparison within the pack -- not a score against an ideal.
    """
    if not scored or profile is None or profile.n_picks < 20:
        return "unknown", ""
    tk = next((s for s in scored if s.card.grpid == taken_id), None)
    if tk is None:
        return "unknown", ""
    fits = _pack_fits(scored, profile, ratings)
    vals = sorted(fits.values())
    median = statistics.median(vals)
    spread = vals[-1] - vals[0]
    loss = scored[0].score - tk.score
    if spread < 0.12:
        return ("in style" if loss <= 0.3 else "in style, costly",
                "this pack did not split along your preferences")
    fit = fits[taken_id]
    typical = fit >= median
    if typical and loss <= 0.3:
        return "in style", "the pick you normally make, and a good one"
    if typical:
        return "in style, costly", (f"typical of you, but it cost {loss:.1f} against "
                                    f"{scored[0].card.name}")
    if loss <= 0.3:
        return "stretch", "outside your usual range and still strong - this is range-building"
    return "off profile", (f"neither your usual pick nor a strong one "
                           f"(-{loss:.1f} against {scored[0].card.name})")


# --------------------------------------------------------------------------
# report
# --------------------------------------------------------------------------

def _bar(v: float, width: int = 21) -> str:
    mid = width // 2
    pos = int(round(mid + v * mid))
    pos = max(0, min(width - 1, pos))
    cells = ["-"] * width
    cells[mid] = "|"
    cells[pos] = "O"
    return "".join(cells)


def report(profile: Optional[Profile], ratings: Ratings) -> str:
    if profile is None:
        return ("No saved drafts yet. Run the overlay through a draft and your "
                "playstyle builds itself.")
    L: list[str] = []
    W = 74
    L.append("=" * W)
    L.append(f"  PLAYSTYLE: {profile.label().upper()}")
    L.append(f"  {profile.n_drafts} drafts, {profile.n_picks} graded picks - "
             f"confidence: {profile.confidence}")
    L.append("=" * W)
    if profile.confidence == "provisional":
        L.append("  Fewer than 3 drafts. Treat everything below as a first sketch;")
        L.append("  most of it is still noise at this sample size.")
        L.append("")

    L.append("  HOW YOU DRAFT")
    L.append("  " + "-" * (W - 4))
    for a in profile.axes:
        L.append(f"  {a.label:<13}{a.left:>20} {_bar(a.value)} {a.right}".rstrip())
        L.append(textwrap.fill(a.detail, W - 6, initial_indent=" " * 15,
                               subsequent_indent=" " * 15))
    L.append("")

    L.append("  COLOURS - how often you take a colour vs how often you see it")
    L.append("  " + "-" * (W - 4))
    for c, v in sorted(profile.colors.items(), key=lambda kv: -kv[1]):
        verdict = ("strongly favoured" if v >= 1.3 else "favoured" if v >= 1.1 else
                   "avoided" if v <= 0.7 else "neutral")
        L.append(f"    {c}   {v:>4.2f}x   {verdict}")
    fav, avoid = profile.favourite_colors(), profile.avoided_colors()
    if fav:
        L.append(f"    -> you reach for {'/'.join(fav)}"
                 + (f" and steer away from {'/'.join(avoid)}" if avoid else ""))
    L.append("")

    if profile.archetypes:
        L.append("  WHERE YOU END UP")
        L.append("  " + "-" * (W - 4))
        for pair, n in profile.archetypes.most_common(5):
            meta = ratings.archetypes.get(pair, {})
            L.append(f"    {pair}  {meta.get('name', pair):<24} x{n}   "
                     f"tier {meta.get('tier', '?')}")
        L.append("")

    if profile.leaks:
        L.append("  TENDENCIES - measured cost, not opinion")
        L.append("  " + "-" * (W - 4))
        L.append("  (average pick loss when you do this, vs when you don't)")
        costly = [r for r in profile.leaks if r["delta"] > 0.15]
        earning = [r for r in profile.leaks if r["delta"] < -0.15]
        for r in costly[:3]:
            L.append(f"    COSTS  {r['label']}"[:W])
            L.append(f"           {r['with']} vs {r['without']} "
                     f"(+{r['delta']} per pick over {r['n']} picks)")
        for r in earning[:3]:
            L.append(f"    EARNS  {r['label']}")
            L.append(f"           {r['with']} vs {r['without']} "
                     f"({r['delta']} per pick over {r['n']} picks) - keep doing this")
        if not costly and not earning:
            L.append("    Nothing is measurably costing or earning you points yet.")
        L.append("")

    L.append("  WHAT WOULD SHAKE YOU UP")
    L.append("  " + "-" * (W - 4))
    for line in stretch_advice(profile, ratings):
        L.append(textwrap.fill(line, W - 4, initial_indent="    - ",
                               subsequent_indent="      "))
    L.append("")
    L.append(f"  Ratings source: {ratings.source}")
    return "\n".join(L)


def stretch_advice(profile: Profile, ratings: Ratings) -> list[str]:
    """Concrete experiments, derived from the axes that are most lopsided."""
    out: list[str] = []
    avoid = profile.avoided_colors()
    if avoid:
        c = avoid[0]
        cs = ratings.color_scores.get(c, 7.0)
        out.append(f"You avoid {c} ({profile.colors[c]:.2f}x). It scores {cs} in this format - "
                   + ("that avoidance is well founded." if cs < 7.0 else
                      "force it once and see what you have been passing."))
    cm = profile.axis("commit")
    if cm and cm.value < -0.35:
        out.append("You commit early. Try one draft where you take the best card only "
                   "for five picks - early commitment is cheap insurance that costs "
                   "you the best decks.")
    elif cm and cm.value > 0.35:
        out.append("You stay open late. In FRA there are only ~14 commons per colour, so "
                   "the back half of packs is thin - try committing by pick 5 once.")
    pw = profile.axis("power")
    if pw and pw.value > 0.4:
        out.append("You take raw power over fit. Try one draft built strictly around the "
                   "college prepared commons and see whether the synergy deck beats "
                   "your goodstuff pile.")
    elif pw and pw.value < -0.4:
        out.append("You take synergy over power. Bombs win more limited games than "
                   "engines do - try taking the strongest card for all of pack 1.")
    sp = profile.axis("speed")
    if sp and sp.value > 0.4:
        out.append("You draft cheap. The slow decks (Theorix, Vigorbloom) are the two best "
                   "lanes here - one deliberately top-heavy draft would widen your range.")
    elif sp and sp.value < -0.4:
        out.append("You draft expensive. R/W Ajani's Army punishes exactly that; try it once "
                   "to feel how the aggro side of the format plays.")
    rare = next((r for r in profile.leaks if r["tag"] == "rarity_chase"), None)
    if rare and rare["delta"] > 0.2:
        out.append(f"Rare-chasing is costing you {rare['delta']} a pick. The best common in "
                   "the pack beats the fourth-best rare more often than it feels like.")
    lanes = profile.archetypes
    if lanes and len(lanes) >= 2:
        never = [p for p in ratings.archetypes if p not in lanes]
        if never:
            best = max(never, key=lambda p: ratings.archetypes[p].get("draft", 0))
            meta = ratings.archetypes[best]
            out.append(f"You have never ended in {meta.get('name', best)} ({best}), which is "
                       f"tier {meta.get('tier', '?')} at {meta.get('draft', '?')}. "
                       "That is the biggest blank on your map.")
    if not out:
        out.append("Your profile is balanced enough that nothing stands out as a stretch yet. "
                   "Draft more and this section gets sharper.")
    return out
