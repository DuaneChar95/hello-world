"""Pick scoring: turns the FRA guide's reasoning into a number plus reasons.

A pick score is: base card grade, adjusted for how well the card fits the pool
you have actually built so far, how late it is to still be speculating, what
your curve and interaction counts need, and which archetype your picks lean
toward. Every adjustment carries a human-readable reason so the overlay can
explain itself rather than just ranking.
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from .arenadb import CardInfo

COLORS = "WUBRG"
DATA = Path(__file__).resolve().parent.parent / "data"


# --------------------------------------------------------------------------

@dataclass
class Ratings:
    raw: dict

    @classmethod
    def load(cls, path: Optional[Path] = None) -> "Ratings":
        p = Path(path) if path else DATA / "fra_ratings.json"
        return cls(json.loads(Path(p).read_text(encoding="utf-8")))

    @property
    def cards(self) -> dict:
        return self.raw.get("cards", {})

    @property
    def archetypes(self) -> dict:
        return self.raw.get("archetypes", {})

    @property
    def color_scores(self) -> dict:
        return self.raw.get("color_scores", {})

    @property
    def confidence(self) -> str:
        return self.raw.get("confidence", "eval")

    @property
    def source(self) -> str:
        return self.raw.get("source", "")

    def entry(self, name: str) -> Optional[dict]:
        if not name:
            return None
        c = self.cards
        if name in c:
            return c[name]
        low = {k.lower(): v for k, v in c.items()}
        hit = low.get(name.lower())
        if hit:
            return hit
        # split / adventure / prepared cards print as "Front // Back"
        if "//" in name:
            return low.get(name.split("//")[0].strip().lower())
        return None

    def base_grade(self, card: CardInfo) -> tuple[float, str]:
        e = self.entry(card.name)
        if e and "grade" in e:
            return float(e["grade"]), "known"
        tg = self.raw.get("tag_grades", {})
        if e and e.get("tags"):
            best = max((tg.get(t, 0.0) for t in e["tags"]), default=0.0)
            if best:
                return best, "tag"
        by_rarity = {"mythic": 3.5, "rare": 3.2, "uncommon": 2.8, "common": 2.5, "basic": 0.0}
        r = by_rarity.get((card.rarity or "").lower())
        if r is not None:
            return r, "rarity"
        return 2.5, "unknown"

    def tags(self, card: CardInfo) -> list[str]:
        e = self.entry(card.name)
        return list(e.get("tags", [])) if e else []

    def note(self, card: CardInfo) -> str:
        e = self.entry(card.name)
        return e.get("note", "") if e else ""

    def card_colors(self, card: CardInfo) -> set[str]:
        cs = card.color_set()
        if cs:
            return cs
        e = self.entry(card.name)
        if e and e.get("colors"):
            return {c for c in e["colors"] if c in COLORS}
        return set()


# --------------------------------------------------------------------------

@dataclass
class PoolState:
    """What you have actually taken so far."""
    picks: list[CardInfo] = field(default_factory=list)
    mode: str = "draft"          # or "sealed"

    def add(self, c: CardInfo) -> None:
        self.picks.append(c)

    @property
    def n(self) -> int:
        return len(self.picks)

    def color_counts(self, ratings: Ratings) -> dict[str, int]:
        out = {c: 0 for c in COLORS}
        for c in self.picks:
            for col in ratings.card_colors(c):
                out[col] += 1
        return out

    def top_colors(self, ratings: Ratings, k: int = 2) -> list[str]:
        cc = self.color_counts(ratings)
        return [c for c, _ in sorted(cc.items(), key=lambda kv: -kv[1])][:k]

    def committed(self, ratings: Ratings) -> set[str]:
        """Colors you are genuinely in, not merely dabbling in."""
        cc = self.color_counts(ratings)
        ranked = sorted(cc.items(), key=lambda kv: -kv[1])
        out = {c for c, v in ranked[:2] if v >= 2}
        return out

    def archetype_lean(self, ratings: Ratings) -> list[tuple[str, float]]:
        """Score each archetype by color overlap and tag overlap."""
        cc = self.color_counts(ratings)
        tags: dict[str, int] = {}
        for c in self.picks:
            for t in ratings.tags(c):
                tags[t] = tags.get(t, 0) + 1
        out: list[tuple[str, float]] = []
        for pair, meta in ratings.archetypes.items():
            counts = [cc.get(c, 0) for c in pair]
            # Depth in both colours is what makes a lane; a 1-card splash is not
            # a second colour, so reward the thinner half explicitly.
            score = sum(counts) * 1.5 + min(counts) * 1.5
            score += sum(tags.get(w, 0) for w in meta.get("wants", [])) * 0.75
            score += (meta.get("draft" if self.mode == "draft" else "sealed", 7.0) - 7.0) * 0.8
            out.append((pair, score))
        out.sort(key=lambda kv: -kv[1])
        return out

    def curve(self) -> dict[int, int]:
        out: dict[int, int] = {}
        for c in self.picks:
            b = min(max(c.cmc, 1), 6)
            out[b] = out.get(b, 0) + 1
        return out

    def interaction_count(self, ratings: Ratings) -> int:
        n = 0
        for c in self.picks:
            t = ratings.tags(c)
            if any(x.startswith("removal") or x in ("boardwipe",) for x in t):
                n += 1
        return n

    def creature_count(self) -> int:
        return sum(1 for c in self.picks if "creature" in (c.types or "").lower())


# --------------------------------------------------------------------------

@dataclass
class Scored:
    card: CardInfo
    score: float
    base: float
    reasons: list[str]
    tags: list[str]
    note: str = ""

    @property
    def headline(self) -> str:
        return self.reasons[0] if self.reasons else ""


def _lateness(pack_no: int, pick_no: int, mode: str) -> float:
    """0.0 = pack 1 pick 1 (stay open), 1.0 = late (commit hard)."""
    if mode == "sealed":
        return 1.0
    seen = (max(pack_no, 1) - 1) * 14 + max(pick_no, 1)
    return min(1.0, max(0.0, (seen - 3) / 28.0))


def score_pack(pack: list[CardInfo], pool: PoolState, ratings: Ratings,
               pack_no: int = 1, pick_no: int = 1) -> list[Scored]:
    committed = pool.committed(ratings)
    lean = pool.archetype_lean(ratings)
    top_pair = lean[0][0] if lean else ""
    wants = set(ratings.archetypes.get(top_pair, {}).get("wants", []))
    late = _lateness(pack_no, pick_no, pool.mode)
    curve = pool.curve()
    interaction = pool.interaction_count(ratings)
    out: list[Scored] = []

    for card in pack:
        base, how = ratings.base_grade(card)
        score = base
        reasons: list[str] = []
        tags = ratings.tags(card)
        cols = ratings.card_colors(card)

        if how == "known":
            reasons.append(f"Rated {base:.1f}")
        elif how == "tag":
            reasons.append(f"~{base:.1f} from its tags (card not individually rated)")
        elif how == "rarity":
            reasons.append(f"~{base:.1f} placeholder from rarity - apply the rubric yourself")
        else:
            reasons.append("Unrated card - score it with the rubric")

        # --- colour fit -------------------------------------------------
        if cols:
            if committed:
                overlap = cols & committed
                if overlap and cols <= committed:
                    score += 0.45 * late
                    reasons.append(f"on-colour for {''.join(sorted(committed))}")
                elif overlap:
                    score += 0.15 * late
                    reasons.append("partly on-colour")
                else:
                    pen = 1.5 * late
                    score -= pen
                    reasons.append(f"off-colour (-{pen:.1f} at this point in the draft)")
            else:
                cs = ratings.color_scores
                bonus = (sum(cs.get(c, 7.0) for c in cols) / len(cols) - 7.0) * 0.12
                score += bonus
                if bonus > 0.05:
                    reasons.append("in a strong colour")
                elif bonus < -0.05:
                    reasons.append("in a weak colour")
        else:
            score += 0.1
            reasons.append("colourless - always castable")

        # --- archetype fit ----------------------------------------------
        hit = [t for t in tags if t in wants]
        if hit and top_pair:
            score += 0.3 + 0.1 * len(hit)
            meta = ratings.archetypes.get(top_pair, {})
            reasons.append(f"feeds {meta.get('name', top_pair)} ({', '.join(hit)})")

        # --- format-specific rules from the guide -----------------------
        if "threshold" in tags and top_pair != "UB":
            score -= 0.8
            reasons.append("threshold is near-dead outside U/B")
        if "burn_face" in tags and top_pair != "BR":
            score -= 0.4
            reasons.append("face damage is a trap outside a fast B/R")
        if any(t.startswith("removal") for t in tags) or "boardwipe" in tags:
            if interaction < 4:
                score += 0.35
                reasons.append(f"you only have {interaction} interaction - you want 4+")
        if "prepared" in tags and any(t.startswith("removal") for t in tags):
            score += 0.1
        if "empower3" in tags:
            if top_pair in ("UB", "WU"):
                score += 0.25
                reasons.append("empower surveil also fires your payoffs here")
            elif top_pair in ("RW", "BR"):
                score -= 0.2
                reasons.append("deferred value is weak when you're the beatdown")
        if "prepared" in tags:
            college = next((t for t in tags if t.startswith("prepared_")), "")
            in_college = college and college.split("_")[1] in \
                ratings.archetypes.get(top_pair, {}).get("name", "").lower()
            if in_college:
                score += 0.3
                reasons.append("in-college prepared - body plus a spell you want")
            elif college:
                reasons.append("out-of-college prepared - rate the body only")

        # --- curve ------------------------------------------------------
        if pool.mode == "draft" and card.cmc:
            b = min(max(card.cmc, 1), 6)
            have = curve.get(b, 0)
            if b == 2 and have < 5 and pool.n > 6:
                score += 0.2
                reasons.append(f"you have {have} two-drops - you want 5-6")
            elif b >= 5 and have >= 4:
                score -= 0.3
                reasons.append(f"you already have {have} cards at {b}+")

        out.append(Scored(card, round(score, 2), base, reasons, tags, ratings.note(card)))

    out.sort(key=lambda s: -s.score)
    return out


def pool_summary(pool: PoolState, ratings: Ratings) -> dict:
    lean = pool.archetype_lean(ratings)
    cc = pool.color_counts(ratings)
    top = lean[0] if lean else ("", 0.0)
    meta = ratings.archetypes.get(top[0], {})
    second = lean[1] if len(lean) > 1 else ("", 0.0)
    gap = top[1] - second[1]
    if pool.n < 4:
        verdict = "Too early to read - take the most powerful card."
    elif gap >= 4:
        verdict = f"Clearly in {meta.get('name', top[0])}. Commit and take playables."
    elif gap >= 1.5:
        verdict = f"Leaning {meta.get('name', top[0])}. Keep one foot open."
    else:
        verdict = "Genuinely open - let the next few picks decide."
    return {
        "picks": pool.n,
        "colors": {k: v for k, v in sorted(cc.items(), key=lambda kv: -kv[1]) if v},
        "top_pair": top[0],
        "top_name": meta.get("name", top[0]),
        "top_tag": meta.get("tag", ""),
        "tier": meta.get("tier", ""),
        "lean": lean[:3],
        "verdict": verdict,
        "interaction": pool.interaction_count(ratings),
        "creatures": pool.creature_count(),
        "curve": pool.curve(),
    }
