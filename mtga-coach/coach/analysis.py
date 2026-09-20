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

# The whole of FRA's colour fixing. Note what is NOT here: there is no
# enemy-colour dual at any rarity, and Heartwood adds {R} or {G} only.
ANNEX = {"WU": "Fatehold Annex", "UB": "Theorix Annex", "BR": "Stingerquill Annex",
         "RG": "Konstrari Annex", "GW": "Vigorbloom Annex"}
ALLIED = list(ANNEX)

# Contiguous arcs of the colour wheel. Each contains TWO allied pairs, so each
# gets two common Annexes. Wedges contain only one and are far worse supported.
SHARDS = {frozenset("WUB"): ("WUB", "Esper", ("WU", "UB")),
          frozenset("UBR"): ("UBR", "Grixis", ("UB", "BR")),
          frozenset("BRG"): ("BRG", "Jund", ("BR", "RG")),
          frozenset("RGW"): ("RGW", "Naya", ("RG", "GW")),
          frozenset("GWU"): ("GWU", "Bant", ("GW", "WU"))}


def shard_of(colors) -> Optional[tuple]:
    """(label, nickname, its two allied pairs) if these three colours form a
    contiguous arc of the wheel, else None -- a wedge, which FRA barely supports."""
    return SHARDS.get(frozenset(colors))

# The one colour that turns an enemy pair into a shard, making both of its
# Annexes into real duals instead of half-dead lands.
BRIDGE = {"WB": "U", "UR": "B", "BG": "R", "RW": "G", "GU": "W"}


def annex_for(pair: str) -> Optional[str]:
    key = "".join(sorted(pair, key=COLORS.index))
    for a, name in ANNEX.items():
        if "".join(sorted(a, key=COLORS.index)) == key:
            return name
    return None


def bridges_to(pair: str) -> list[dict]:
    """Which third colours this pair can reach on a common dual, and how."""
    cols = set(pair)
    out = []
    for allied, land in ANNEX.items():
        shared = cols & set(allied)
        extra = set(allied) - cols
        if len(shared) == 1 and len(extra) == 1:
            c = next(iter(extra))
            three = cols | {c}
            sh = shard_of(three)
            out.append({"color": c, "land": land, "shares": next(iter(shared)),
                        "kind": "shard" if sh else "wedge",
                        "shard": sh[0] if sh else "".join(sorted(three, key=COLORS.index)),
                        "nickname": sh[1] if sh else "",
                        "lands": list(sh[2]) if sh else [allied]})
    # A real shard reached by two different Annexes is one option, not two.
    merged: dict[str, dict] = {}
    for o in out:
        k = o["color"]
        if k in merged:
            merged[k]["land"] = merged[k]["land"] + " + " + o["land"]
        else:
            merged[k] = o
    ranked = sorted(merged.values(), key=lambda o: (o["kind"] != "shard", o["color"]))
    return ranked


def three_color_plan(pair: str) -> dict:
    """How this two-colour deck should think about a third colour."""
    key = "".join(sorted(pair, key=COLORS.index))
    allied = any("".join(sorted(a, key=COLORS.index)) == key for a in ANNEX)
    options = bridges_to(pair)
    if allied:
        return {
            "base": "allied", "own_land": annex_for(pair), "options": options,
            "headline": f"{annex_for(pair)} is your dual. Two third colours are one "
                        "common away.",
            "advice": "Each option below shares a colour with you, so that land is "
                      "never dead - it makes one of your main colours whether or "
                      "not you draw the splash card."}
    bridge = BRIDGE.get(key) or BRIDGE.get(pair)
    if bridge:
        lands = [o for o in options if o["color"] == bridge]
        sh = shard_of(set(pair) | {bridge})
        shard = f"{sh[0]} ({sh[1]})" if sh else "".join(
            sorted(set(pair) | {bridge}, key=COLORS.index))
        return {
            "base": "enemy", "own_land": None, "bridge": bridge, "shard": shard,
            "options": options,
            "headline": f"No dual exists for {key}. Adding {bridge} is what fixes it.",
            "advice": (f"{key} has no land in this set. But {bridge} turns you into "
                       f"{shard}, and then BOTH "
                       + " and ".join(sorted({
                           part for l in lands for part in l["land"].split(" + ")}))
                       + " become real duals instead of half-dead lands. Adding a "
                         "third colour here can improve your mana rather than "
                         "strain it - but only if you actually have the Annexes.")}
    return {"base": "unknown", "options": options, "headline": "", "advice": ""}



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
