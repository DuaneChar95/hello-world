"""Resolve Arena grpIds to card names/colors/rarity.

Preferred source is Arena's own card database, which ships with the client as
Raw_CardDatabase_<hash>.mtga (a SQLite file). Column names have changed across
releases, so the schema is introspected rather than assumed.

Fallback is Scryfall's set-scoped search, which carries `arena_id`. That needs
internet but is small (one set, a few hundred cards).
"""
from __future__ import annotations

import glob
import json
import os
import platform
import re
import sqlite3
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Optional

CACHE_DIR = Path.home() / ".mtga-coach"
CACHE_FILE = CACHE_DIR / "cards.json"

COLOR_LETTERS = "WUBRG"


@dataclass
class CardInfo:
    grpid: int
    name: str
    colors: str = ""
    rarity: str = ""
    setcode: str = ""
    cmc: int = 0
    types: str = ""

    def color_set(self) -> set[str]:
        return {c for c in self.colors if c in COLOR_LETTERS}


# --------------------------------------------------------------------------
# Arena's own SQLite database
# --------------------------------------------------------------------------

def candidate_db_dirs() -> list[Path]:
    home = Path.home()
    sysname = platform.system()
    out: list[Path] = []
    if sysname == "Windows":
        for root in filter(None, [os.environ.get("ProgramFiles"),
                                  os.environ.get("ProgramFiles(x86)"),
                                  r"C:\Program Files", r"C:\Program Files (x86)"]):
            out.append(Path(root) / "Wizards of the Coast" / "MTGA" / "MTGA_Data" / "Downloads" / "Raw")
        out.append(home / "AppData" / "Local" / "Programs" / "MTGA" / "MTGA_Data" / "Downloads" / "Raw")
        for d in glob.glob(r"C:\Program Files*\Steam\steamapps\common\MTGA\MTGA_Data\Downloads\Raw"):
            out.append(Path(d))
    elif sysname == "Darwin":
        out.append(Path("/Applications/MTGA.app/Contents/Resources/Data/Downloads/Raw"))
        out.append(home / "Applications" / "MTGA.app" / "Contents" / "Resources" / "Data" / "Downloads" / "Raw")
    else:
        for p in (home / ".wine", home / ".local/share/Steam/steamapps/compatdata"):
            if p.exists():
                out += [Path(d) for d in glob.glob(str(p / "**/MTGA_Data/Downloads/Raw"), recursive=True)]
    return out


def find_card_db(explicit: Optional[str] = None) -> Optional[Path]:
    if explicit:
        p = Path(explicit).expanduser()
        return p if p.exists() else None
    newest, newest_mtime = None, -1.0
    for d in candidate_db_dirs():
        if not d.exists():
            continue
        for f in d.glob("Raw_CardDatabase_*.mtga"):
            try:
                m = f.stat().st_mtime
            except OSError:
                continue
            if m > newest_mtime:
                newest, newest_mtime = f, m
    return newest


def _cols(con: sqlite3.Connection, table: str) -> list[str]:
    try:
        return [r[1] for r in con.execute(f"PRAGMA table_info({table})")]
    except sqlite3.Error:
        return []


def _pick(cols: list[str], *wanted: str) -> Optional[str]:
    low = {c.lower(): c for c in cols}
    for w in wanted:
        if w.lower() in low:
            return low[w.lower()]
    return None


def _colors_from_cost(cost: object) -> str:
    """Arena encodes costs like 'o2oUoU' or '{2}{U}{U}'."""
    if not isinstance(cost, str):
        return ""
    found = {c for c in re.findall(r"[WUBRG]", cost.upper())}
    return "".join(c for c in COLOR_LETTERS if c in found)


def _cmc_from_cost(cost: object) -> int:
    if not isinstance(cost, str):
        return 0
    total = sum(int(n) for n in re.findall(r"\d+", cost))
    total += len(re.findall(r"[WUBRGC]", cost.upper()))
    return total


def load_from_arena_db(db_path: Path, setcode: Optional[str] = None) -> dict[int, CardInfo]:
    """Best-effort read of Arena's card database."""
    out: dict[int, CardInfo] = {}
    uri = f"file:{db_path}?mode=ro"
    con = sqlite3.connect(uri, uri=True)
    try:
        tables = [r[0] for r in con.execute("SELECT name FROM sqlite_master WHERE type='table'")]
        card_tbl = next((t for t in tables if t.lower() in ("cards", "card")), None)
        loc_tbl = next((t for t in tables if t.lower().startswith("localization")), None)
        if not card_tbl:
            return out
        c = _cols(con, card_tbl)
        grp = _pick(c, "GrpId", "grpid", "id")
        title = _pick(c, "TitleId", "Title_LocId", "NameLocId", "TitleID")
        cost = _pick(c, "CastingCost", "ManaCost", "Cost")
        rar = _pick(c, "Rarity", "RarityId")
        expn = _pick(c, "ExpansionCode", "Set", "SetCode")
        types = _pick(c, "Types", "CardTypes", "TypeLine")
        if not grp:
            return out

        names: dict[int, str] = {}
        if loc_tbl and title:
            lc = _cols(con, loc_tbl)
            loc_id = _pick(lc, "LocId", "Loc_Id", "id")
            text = _pick(lc, "enUS", "Formatted", "Loc", "Text", "enUs")
            lang = _pick(lc, "Langkey", "Language", "Lang")
            if loc_id and text:
                q = f"SELECT {loc_id}, {text} FROM {loc_tbl}"
                if lang:
                    q += f" WHERE {lang} IN ('en-US','enUS','EN','en')"
                try:
                    for lid, txt in con.execute(q):
                        if lid is not None and txt:
                            names.setdefault(int(lid), str(txt))
                except sqlite3.Error:
                    for lid, txt in con.execute(f"SELECT {loc_id}, {text} FROM {loc_tbl}"):
                        if lid is not None and txt:
                            names.setdefault(int(lid), str(txt))

        sel = [grp] + [x for x in (title, cost, rar, expn, types) if x]
        rows = con.execute(f"SELECT {', '.join(sel)} FROM {card_tbl}")
        idx = {name: i + 1 for i, name in enumerate(sel[1:])}
        rarity_map = {0: "", 1: "basic", 2: "common", 3: "uncommon", 4: "rare", 5: "mythic"}
        for row in rows:
            try:
                gid = int(row[0])
            except (TypeError, ValueError):
                continue
            nm = ""
            if title and row[idx[title]] is not None:
                nm = names.get(int(row[idx[title]]), "")
            ex = str(row[idx[expn]]) if expn and row[idx[expn]] else ""
            if setcode and ex and ex.upper() != setcode.upper():
                continue
            cst = row[idx[cost]] if cost else ""
            rv = row[idx[rar]] if rar else ""
            rarity = rarity_map.get(rv, str(rv).lower()) if isinstance(rv, int) else str(rv or "").lower()
            out[gid] = CardInfo(gid, nm or f"#{gid}", _colors_from_cost(cst), rarity, ex,
                                _cmc_from_cost(cst), str(row[idx[types]]) if types and row[idx[types]] else "")
    finally:
        con.close()
    return out


# --------------------------------------------------------------------------
# Scryfall fallback
# --------------------------------------------------------------------------

def load_from_scryfall(setcode: str) -> dict[int, CardInfo]:
    import urllib.request
    out: dict[int, CardInfo] = {}
    url = f"https://api.scryfall.com/cards/search?q=set%3A{setcode.lower()}&unique=prints"
    while url:
        req = urllib.request.Request(url, headers={"User-Agent": "mtga-coach/1.0", "Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=30) as r:
            data = json.load(r)
        for c in data.get("data", []):
            aid = c.get("arena_id")
            if not aid:
                continue
            out[int(aid)] = CardInfo(
                int(aid), c.get("name", ""), "".join(c.get("colors", []) or []),
                c.get("rarity", ""), (c.get("set") or "").upper(),
                int(c.get("cmc") or 0), c.get("type_line", ""))
        url = data.get("next_page") if data.get("has_more") else None
    return out


# --------------------------------------------------------------------------
# facade
# --------------------------------------------------------------------------

class CardResolver:
    def __init__(self, cards: Optional[dict[int, CardInfo]] = None):
        self.cards: dict[int, CardInfo] = cards or {}
        self.by_name = {c.name.lower(): c for c in self.cards.values() if c.name}

    def __len__(self) -> int:
        return len(self.cards)

    def get(self, grpid: int) -> CardInfo:
        c = self.cards.get(grpid)
        if c:
            return c
        return CardInfo(grpid, f"Unknown #{grpid}")

    def save(self, path: Path = CACHE_FILE) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps({str(k): asdict(v) for k, v in self.cards.items()}), encoding="utf-8")

    @classmethod
    def load_cached(cls, path: Path = CACHE_FILE) -> Optional["CardResolver"]:
        if not path.exists():
            return None
        try:
            raw = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            return None
        return cls({int(k): CardInfo(**v) for k, v in raw.items()})

    @classmethod
    def build(cls, setcode: Optional[str] = None, db_path: Optional[str] = None,
              allow_network: bool = False, refresh: bool = False, log=print) -> "CardResolver":
        if not refresh:
            cached = cls.load_cached()
            if cached and len(cached) > 100:
                log(f"card names: {len(cached)} from cache ({CACHE_FILE})")
                return cached
        db = find_card_db(db_path)
        if db:
            try:
                cards = load_from_arena_db(db, None)
                if cards:
                    r = cls(cards)
                    r.save()
                    log(f"card names: {len(cards)} from Arena database ({db.name})")
                    return r
            except sqlite3.Error as e:
                log(f"card names: Arena database unreadable ({e})")
        if allow_network and setcode:
            try:
                cards = load_from_scryfall(setcode)
                if cards:
                    r = cls(cards)
                    r.save()
                    log(f"card names: {len(cards)} from Scryfall ({setcode.upper()})")
                    return r
            except Exception as e:  # noqa: BLE001 - network/JSON, non-fatal
                log(f"card names: Scryfall lookup failed ({e})")
        log("card names: NONE resolved - the overlay will show grpIds and rubric advice only.")
        return cls({})
