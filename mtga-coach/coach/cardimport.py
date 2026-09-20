"""Turn a real card list into the app's ratings file.

Accepts whatever you can get your hands on:

  * Scryfall search JSON  ({"object":"list","data":[...]}), one page or many
  * a bare JSON array of Scryfall card objects
  * an MTGJSON set file  ({"data":{"cards":[...]}})
  * a CSV with at least a name column

Tags are derived from oracle text, so the scorer understands real cards the
same way it understands the hand-written ones. Grades are a HEURISTIC, not
data -- rarity and card type with adjustments for removal, evasion and rate.
Any card already graded by hand keeps that grade, and 17Lands numbers imported
later overwrite everything.
"""
from __future__ import annotations

import csv
import json
import re
from pathlib import Path
from typing import Iterable, Optional

COLORS = "WUBRG"

# --- oracle-text patterns, in the order they are checked --------------------
PAT = [
    ("empower3",   r"empower jace ([3-9]|\d{2,})"),
    ("empower",    r"empower jace"),
    ("prepared",   r"\bprepare[ds]?\b"),
    ("threshold",  r"\bthreshold\b"),
    ("heartwood",  r"\bheartwood\b"),
    ("boardwipe",  r"destroy all creatures|each creature gets -\d+/-\d+|"
                   r"all creatures get -\d+/-\d+"),
    ("selfmill",   r"mill \w+ cards?\b(?!.*target (opponent|player))"),
    ("surveil",    r"\bsurveil\b"),
    ("scry",       r"\bscry\b"),
    ("lifegain",   r"\bgain \w+ life\b|\blifelink\b"),
    ("counters",   r"\+1/\+1 counter"),
    ("flying",     r"\bflying\b"),
    ("deathtouch", r"\bdeathtouch\b"),
    ("trample",    r"\btrample\b"),
    ("haste",      r"\bhaste\b"),
    ("prowess",    r"\bprowess\b"),
    ("sacrifice",  r"\bsacrifice (a|another|one)\b"),
    ("recursion",  r"return .* from your graveyard to (the battlefield|your hand)"),
    ("artifact",   r"\bartifact\b"),
    ("ramp",       r"search your library for a .*land|add \{[wubrgc]\}"),
]
REMOVAL = re.compile(
    r"destroy target creature|exile target creature|"
    r"deals? \d+ damage to target creature|target creature gets -\d+/-\d+|"
    r"destroy target (creature or planeswalker|permanent)", re.I)
BURN_FACE = re.compile(r"deals? \d+ damage to (target opponent|each opponent|"
                       r"target player|any target)", re.I)

# The five college prepared spells, identified by what the spell half does.
COLLEGE_PAT = [
    ("prepared_fatehold",    r"create a 2/2 .*token|token.*surveil"),
    ("prepared_theorix",     r"mill"),
    ("prepared_konstrari",   r"heartwood"),
    ("prepared_vigorbloom",  r"gain \w+ life|\+1/\+1 counter"),
    ("prepared_stingerquill", r"damage to (target opponent|each opponent|target player)"),
]


def _text_of(c: dict) -> str:
    parts = [c.get("oracle_text") or c.get("text") or ""]
    for f in c.get("card_faces") or []:
        parts.append(f.get("oracle_text") or f.get("text") or "")
    return "\n".join(p for p in parts if p).lower()


def _cost_of(c: dict) -> str:
    mc = c.get("mana_cost") or c.get("manaCost") or ""
    if not mc:
        faces = c.get("card_faces") or []
        if faces:
            mc = faces[0].get("mana_cost", "") or ""
    return mc


def _type_of(c: dict) -> str:
    t = c.get("type_line") or c.get("type") or ""
    if not t:
        faces = c.get("card_faces") or []
        if faces:
            t = faces[0].get("type_line", "")
    return t


def _colors_of(c: dict, cost: str) -> str:
    cols = c.get("colors")
    if cols is None:
        faces = c.get("card_faces") or []
        if faces:
            cols = faces[0].get("colors")
    if not cols:
        cols = re.findall(r"[WUBRG]", cost.upper())
    seen = {x for x in (cols or []) if x in COLORS}
    return "".join(c2 for c2 in COLORS if c2 in seen)


def derive_tags(c: dict) -> list[str]:
    text = _text_of(c)
    tline = _type_of(c).lower()
    cmc = int(float(c.get("cmc") or c.get("manaValue") or 0))
    tags: list[str] = []

    if "land" in tline:
        tags += ["land"]
        if re.search(r"add \{[wubrg]\}.*or.*\{[wubrg]\}|\{t\}: add \{[wubrg]\} or", text):
            tags.append("fixing")
        return tags

    if REMOVAL.search(text):
        tags.append("removal_instant_cheap" if ("instant" in tline and cmc <= 3)
                    else "removal")
    if BURN_FACE.search(text) and "creature" not in text.split("damage to")[0][-40:]:
        tags.append("burn_face")
    for tag, pat in PAT:
        if re.search(pat, text) and tag not in tags:
            tags.append(tag)
    if "prepared" in tags:
        for tag, pat in COLLEGE_PAT:
            if re.search(pat, text):
                tags.append(tag)
                break
    if "creature" in tline and cmc >= 5:
        tags.append("bigcreature")
    if "planeswalker" in tline:
        tags.append("planeswalker")
    if cmc <= 2 and "creature" in tline and ("haste" in tags or "prowess" in tags):
        tags.append("aggro")
    return tags


def heuristic_grade(c: dict, tags: list[str]) -> float:
    """A defensible starting grade. NOT data - 17Lands overwrites this."""
    tline = _type_of(c).lower()
    rarity = (c.get("rarity") or "").lower()
    cmc = int(float(c.get("cmc") or c.get("manaValue") or 0))
    g = {"mythic": 3.6, "rare": 3.3, "uncommon": 2.9, "common": 2.5}.get(rarity, 2.5)
    if "land" in tline:
        return 2.2 if "fixing" in tags else 0.0
    if "planeswalker" in tline:
        g += 0.7
    if "boardwipe" in tags:
        g += 0.5
    if "removal_instant_cheap" in tags:
        g += 0.7
    elif "removal" in tags:
        g += 0.4
    if "flying" in tags:
        g += 0.2
    if "deathtouch" in tags or "trample" in tags:
        g += 0.1
    if "prepared" in tags:
        g += 0.3
    if "empower3" in tags:
        g += 0.2
    if "threshold" in tags:
        g -= 0.1
    if "burn_face" in tags and "removal" not in tags:
        g -= 0.2
    if cmc >= 6:
        g -= 0.3
    if cmc <= 1 and "creature" in tline:
        g -= 0.2
    return round(max(0.0, min(5.0, g)), 2)


def load_cards(path: Path) -> list[dict]:
    """Read any of the accepted shapes into a flat list of card dicts."""
    raw = path.read_text(encoding="utf-8-sig")
    if path.suffix.lower() == ".csv":
        return list(csv.DictReader(raw.splitlines()))
    data = json.loads(raw)
    if isinstance(data, list):
        # a bare array, or a list of Scryfall pages
        if data and isinstance(data[0], dict) and data[0].get("object") == "list":
            out: list[dict] = []
            for page in data:
                out += page.get("data", [])
            return out
        return data
    if isinstance(data, dict):
        if data.get("object") == "list":
            return data.get("data", [])
        inner = data.get("data")
        if isinstance(inner, dict) and "cards" in inner:      # MTGJSON
            return inner["cards"]
        if isinstance(inner, list):
            return inner
        if "cards" in data:
            return data["cards"]
    raise ValueError(f"Could not find a card list in {path}")


def build_ratings(cards: Iterable[dict], base: dict, setcode: str = "FRA",
                  prune: bool = False) -> tuple[dict, dict]:
    """Merge a real card list into the ratings file. Hand grades win.

    Any hand-written card that the real list does not contain is reported: it
    is a name that was guessed wrong somewhere, and it would otherwise haunt
    the pool as a card that does not exist.
    """
    out = dict(base)
    existing = dict(base.get("cards", {}))
    before = set(existing)
    stats = {"seen": 0, "added": 0, "kept_hand_grade": 0, "skipped": 0,
             "unmatched": [], "pruned": 0}
    matched: set[str] = set()

    for c in cards:
        name = c.get("name") or c.get("Name") or ""
        if not name:
            stats["skipped"] += 1
            continue
        stats["seen"] += 1
        # Split/prepared cards print as "Front // Back"; key on the front.
        key = name.split("//")[0].strip()
        layout = (c.get("layout") or "").lower()
        if layout in ("token", "emblem", "art_series", "double_faced_token"):
            stats["skipped"] += 1
            continue
        cost = _cost_of(c)
        tline = _type_of(c)
        if "basic land" in tline.lower():
            stats["skipped"] += 1
            continue
        tags = derive_tags(c)
        entry = dict(existing.get(key, {}))
        hand = "grade" in entry and entry.get("source") != "auto"
        entry.update({
            "colors": _colors_of(c, cost),
            "rarity": (c.get("rarity") or "").lower(),
            "cost": cost,
            "cmc": int(float(c.get("cmc") or c.get("manaValue") or 0)),
            "types": tline,
            "tags": sorted(set(tags) | set(entry.get("tags", []))),
        })
        if hand:
            stats["kept_hand_grade"] += 1
        else:
            entry["grade"] = heuristic_grade(c, tags)
            entry["source"] = "auto"
        existing[key] = entry
        matched.add(key)
        stats["added"] += 1

    stats["unmatched"] = sorted(before - matched)
    if prune:
        for name in stats["unmatched"]:
            existing.pop(name, None)
        stats["pruned"] = len(stats["unmatched"])

    out["cards"] = existing
    out["set"] = setcode
    out["card_data"] = "real"
    out["confidence"] = "carddata"
    out["source"] = (f"Real {setcode} card list ({stats['added']} cards). "
                     f"Grades are heuristic except {stats['kept_hand_grade']} "
                     "hand-written ones. Import 17Lands data to replace them.")
    return out, stats
