"""What a card pairs with, and whether you can splash it.

Two questions the hover panel answers:

  AFFINITY - which of the ten archetypes wants this card most, and why.
  SPLASH   - can a deck outside its colours realistically run it.

Splash analysis needs pip counts, not just colour identity: {1}{R} and {R}{R}
are the same colour and completely different splash propositions. When a real
mana cost is available (Arena's database or Scryfall) the count is exact. When
it isn't -- every generated practice card, and real cards before the set file
lands -- this says so rather than inventing precision.
"""
from __future__ import annotations

import re
from typing import Optional

from .arenadb import CardInfo
from .model import Ratings

COLORS = "WUBRG"

# The whole of FRA's colour fixing.
#
# Correction (2026-09-21): an earlier version of this module said there was no
# enemy-colour dual at any rarity and built a shard/wedge distinction on it.
# That was wrong. There are TEN common duals, one for every pair -- the five
# allied "Annex" lands and the five enemy "Commons" lands, with identical text.
# Shards and wedges are equally supported, and the colour wheel does not enter
# into it. What does is the clause all ten share: they enter tapped unless you
# already control a planeswalker.
ANNEX = {"WU": "Fatehold Annex", "UB": "Theorix Annex", "BR": "Stingerquill Annex",
         "RG": "Konstrari Annex", "GW": "Vigorbloom Annex"}
COMMONS = {"WB": "Meticulous Commons", "UR": "Innovative Commons",
           "BG": "Formidable Commons", "RW": "Dedicated Commons",
           "GU": "Transformative Commons"}

# Rare slowlands: untapped from turn 3 with no planeswalker needed, so strictly
# better than the commons. These ARE allied-only -- the one place the wheel
# still matters.
SLOWLAND = {"WU": "Deserted Beach", "UB": "Shipwreck Marsh", "BR": "Haunted Ridge",
            "RG": "Rockfall Vale", "GW": "Overgrown Farmland"}

# Unconditional any-colour splash land, at common. Always tapped.
ROOM_OF_REFUGE = "Room of Refuge"

ALLIED = list(ANNEX)


def _key(pair) -> str:
    return "".join(sorted(set(pair), key=COLORS.index))


DUALS = {_key(k): v for k, v in list(ANNEX.items()) + list(COMMONS.items())}
SLOWLANDS = {_key(k): v for k, v in SLOWLAND.items()}


def dual_for(pair: str):
    """The common dual for this pair. Every pair has one."""
    return DUALS.get(_key(pair))


def slowland_for(pair: str):
    """The rare slowland for this pair, or None -- allied pairs only."""
    return SLOWLANDS.get(_key(pair))


def is_allied(pair: str) -> bool:
    return _key(pair) in SLOWLANDS


def annex_for(pair: str):
    """Kept for callers written against the old name; every pair has a dual now."""
    return dual_for(pair)


def three_color_lands(colors) -> list[dict]:
    """Every common dual available to a three-colour deck -- one per pair, so three."""
    cols = sorted(set(colors), key=COLORS.index)
    out = []
    for i in range(len(cols)):
        for j in range(i + 1, len(cols)):
            pair = cols[i] + cols[j]
            out.append({"pair": pair, "land": dual_for(pair),
                        "slowland": slowland_for(pair)})
    return out


def bridges_to(pair: str) -> list[dict]:
    """Every third colour this pair can add, and the two extra duals it brings.

    All three remaining colours are available -- each adds two duals that each
    share a colour with you, so neither is ever a dead draw.
    """
    cols = set(pair)
    out = []
    for c in COLORS:
        if c in cols:
            continue
        three = sorted(cols | {c}, key=COLORS.index)
        extra = [{"pair": x + c if COLORS.index(x) < COLORS.index(c) else c + x,
                  "land": dual_for(x + c)} for x in sorted(cols, key=COLORS.index)]
        slows = [d for d in (slowland_for(e["pair"]) for e in extra) if d]
        out.append({
            "color": c,
            "three": "".join(three),
            "land": " + ".join(e["land"] for e in extra),
            "lands": [e["land"] for e in extra],
            "pairs": [e["pair"] for e in extra],
            "slowlands": slows,
            # Kept so old callers that filter on "shard" keep working; every
            # option is now equally supported, so they all report as one.
            "kind": "shard",
            "shard": "".join(three),
            "nickname": "",
        })
    # A splash is better when the bridge colour also has a slowland with you.
    return sorted(out, key=lambda o: (-len(o["slowlands"]), o["color"]))


def three_color_plan(pair: str) -> dict:
    """How this two-colour deck should think about a third colour."""
    own = dual_for(pair)
    slow = slowland_for(pair)
    options = bridges_to(pair)
    base = "allied" if is_allied(pair) else "enemy"
    headline = f"{own} is your dual - every pair in FRA has one."
    if slow:
        headline += f" {slow} (rare) is the better version: untapped from turn 3, no planeswalker needed."
    advice = (
        "All three remaining colours are open, and each brings two duals that "
        "share a colour with you, so neither is ever a dead draw. The gate is "
        "not the colour wheel - it is the clause on all ten commons: they enter "
        "tapped unless a planeswalker is ALREADY on the battlefield. Want 3+ "
        "empower cards before you commit to a third colour, and two duals before "
        "you count the splash as live. " + ROOM_OF_REFUGE +
        " asks nothing at all - always tapped, any colour - and is often the "
        "right splash land for a single bomb."
    )
    return {"base": base, "own_land": own, "slowland": slow, "options": options,
            "headline": headline, "advice": advice}


# --------------------------------------------------------------------------
# pips
# --------------------------------------------------------------------------

def pip_counts(card: CardInfo) -> Optional[dict[str, int]]:
    """Coloured pips per colour, or None when the cost is unknown."""
    if not card.cost:
        return None
    sym = re.findall(r"[WUBRG]", card.cost.upper())
    if not sym:
        return {}
    out: dict[str, int] = {}
    for s in sym:
        out[s] = out.get(s, 0) + 1
    return out


def _pip_summary(card: CardInfo, ratings: Ratings) -> tuple[Optional[int], str]:
    """(total coloured pips, how certain we are)."""
    pc = pip_counts(card)
    if pc is not None:
        return sum(pc.values()), "exact"
    cols = ratings.card_colors(card)
    if not cols:
        return 0, "exact"
    # No cost string. Cheap single-colour cards are often double-pipped, but
    # that is a guess and gets labelled as one.
    return None, "unknown"


# --------------------------------------------------------------------------
# archetype affinity
# --------------------------------------------------------------------------

def archetype_affinity(card: CardInfo, ratings: Ratings) -> list[dict]:
    """Rank the ten archetypes by how much they want this card."""
    cols = ratings.card_colors(card)
    tags = set(ratings.tags(card))
    out: list[dict] = []
    for pair, meta in ratings.archetypes.items():
        pair_cols = set(pair)
        wants = set(meta.get("wants", []))
        score = 0.0
        why: list[str] = []

        if not cols:
            score += 2.0
            why.append("colourless - fits any deck")
        elif cols == pair_cols:
            score += 6.0
            why.append(f"exactly {pair}")
        elif cols <= pair_cols:
            score += 4.5
            why.append("on-colour")
        elif cols & pair_cols:
            score += 1.5
            why.append("half on-colour")

        hits = tags & wants
        if hits:
            score += 2.0 * len(hits)
            why.append("wants " + ", ".join(sorted(hits)))

        # format rules that override raw colour fit
        if "threshold" in tags and pair != "UB":
            score -= 3.0
            why.append("threshold is near-dead outside U/B")
        if "burn_face" in tags and pair != "BR":
            score -= 1.5
            why.append("face damage is a trap outside a fast B/R")
        if "empower3" in tags and pair in ("UB", "WU"):
            score += 1.0
            why.append("its surveil also fires this deck's payoffs")
        if "heartwood" in tags and pair == "RG":
            score += 1.0
            why.append("Heartwood is this deck's engine")

        if score > 0:
            out.append({"pair": pair, "name": meta.get("name", pair),
                        "tag": meta.get("tag", ""), "tier": meta.get("tier", ""),
                        "score": round(score, 1), "why": why})
    out.sort(key=lambda r: -r["score"])
    return out


def best_home(card: CardInfo, ratings: Ratings) -> Optional[dict]:
    a = archetype_affinity(card, ratings)
    return a[0] if a else None


# --------------------------------------------------------------------------
# splash
# --------------------------------------------------------------------------

def splash_advice(card: CardInfo, ratings: Ratings) -> dict:
    """Can a deck outside this card's colours actually cast it?"""
    cols = ratings.card_colors(card)
    pips, certainty = _pip_summary(card, ratings)
    pc = pip_counts(card)

    if not cols:
        return {"ease": "free", "headline": "Colourless - goes in any deck.",
                "detail": "No splash cost at all.", "homes": [],
                "certain": certainty == "exact"}

    if len(cols) >= 2:
        homes = [p for p in ratings.archetypes if set(p) & cols]
        return {
            "ease": "hard",
            "headline": f"Gold ({''.join(sorted(cols, key=COLORS.index))}) - "
                        "not a splash card.",
            "detail": "Needs both colours on curve. Only playable in a deck "
                      "already in one of them, and even then the second colour "
                      "has to be real, not a splash.",
            "homes": homes, "certain": certainty == "exact"}

    col = next(iter(cols))
    n = pc.get(col) if pc else None

    if n is not None and n >= 2:
        ease, head = "hard", f"{n} {col} pips - not splashable."
        detail = (f"Double-{col} means you need roughly 8-9 sources. That is a "
                  "main colour, not a splash.")
    elif n == 1:
        ease, head = "easy", f"Single {col} pip - a real splash candidate."
        detail = ("2-3 sources gets you there most games. Worth it for a bomb "
                  "or premium removal; not worth it for a body.")
    else:
        ease, head = "unknown", f"Single colour ({col}) - pip count unknown."
        detail = ("No mana cost in the card data yet, so this could be "
                  f"{{1}}{{{col}}} or {{{col}}}{{{col}}}. Cheap cards are more "
                  "often double-pipped. Import the real card list and this "
                  "becomes exact.")

    homes = [p for p in ratings.archetypes if col in p]
    extra = []
    if ease in ("easy", "unknown"):
        carriers = sorted({land for pair, land in ANNEX.items() if col in pair})
        if carriers:
            extra.append(f"Carried by {' or '.join(carriers)} - a common dual that "
                         f"makes {col} plus its partner, and enters untapped once "
                         "you control a planeswalker (a Jace token counts).")
        if col in "RG":
            extra.append("Heartwood tokens add {R} or {G}, so they pay for this "
                         "splash specifically. They do NOT fix any other colour.")
        if card.cmc and card.cmc >= 5:
            extra.append("At 5+ mana you will have drawn your splash source by "
                         "the time you can cast it, which makes the splash safer.")
        elif card.cmc and card.cmc <= 2:
            extra.append("A 2-drop you cannot reliably cast on turn 2 is not "
                         "doing its job - splash expensive cards, not cheap ones.")
    return {"ease": ease, "headline": head, "detail": detail, "homes": homes,
            "extra": extra, "certain": certainty == "exact"}


# --------------------------------------------------------------------------
# one block of text for a tooltip
# --------------------------------------------------------------------------

def hover_text(card: CardInfo, ratings: Ratings, scored=None) -> str:
    lines: list[str] = []
    cols = "".join(sorted(ratings.card_colors(card), key=COLORS.index)) or "C"
    rar = (card.rarity or "?").title()
    lines.append(f"{card.name}")
    lines.append(f"{cols}  ·  {card.cmc or '?'} mana  ·  {rar}"
                 + (f"  ·  {card.types}" if card.types else ""))
    note = ratings.note(card)
    if note:
        lines.append("")
        lines.append(note)
    if scored is not None:
        lines.append("")
        lines.append(f"Score {scored.score:.2f} in your current pool")
        for r in scored.reasons[:3]:
            lines.append(f"  · {r}")

    aff = archetype_affinity(card, ratings)
    if aff:
        lines.append("")
        lines.append("PAIRS BEST WITH")
        for a in aff[:3]:
            lines.append(f"  {a['pair']}  {a['name']} ({a['tag']}) — tier {a['tier']}")
            if a["why"]:
                lines.append(f"       {'; '.join(a['why'][:2])}")

    sp = splash_advice(card, ratings)
    lines.append("")
    lines.append("SPLASH")
    lines.append(f"  {sp['headline']}")
    lines.append(f"  {sp['detail']}")
    for e in sp.get("extra", []):
        lines.append(f"  {e}")
    return "\n".join(lines)
