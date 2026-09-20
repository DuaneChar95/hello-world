"""Locate, tail and parse the MTG Arena Player.log.

Read-only. This module never writes to, injects into, or modifies the game.
It watches the log file Arena itself produces when 'Detailed Logs (Plugin
Support)' is enabled -- the same mechanism 17Lands and Untapped use.

Arena's log format has drifted across releases, so the parser here is
deliberately tolerant: it pulls every JSON object out of the stream and
classifies by which keys are present, rather than matching exact marker
strings. Unrecognised payloads can be dumped with --dump-unknown.
"""
from __future__ import annotations

import json
import os
import platform
import re
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable, Iterator, Optional

# --------------------------------------------------------------------------
# locating the log
# --------------------------------------------------------------------------

def candidate_log_paths() -> list[Path]:
    home = Path.home()
    sys = platform.system()
    out: list[Path] = []
    if sys == "Windows":
        appdata = os.environ.get("APPDATA")
        if appdata:
            low = Path(appdata).parent / "LocalLow" / "Wizards Of The Coast" / "MTGA"
            out += [low / "Player.log", low / "output_log.txt", low / "Player-prev.log"]
        out.append(home / "AppData" / "LocalLow" / "Wizards Of The Coast" / "MTGA" / "Player.log")
    elif sys == "Darwin":
        base = home / "Library" / "Logs" / "Wizards Of The Coast" / "MTGA"
        out += [base / "Player.log", base / "Player-prev.log"]
        out.append(home / "Library" / "Application Support" / "com.wizards.mtga" / "Player.log")
    else:  # Linux / Proton / Wine
        for pfx in (home / ".wine", home / ".local/share/Steam/steamapps/compatdata"):
            if pfx.exists():
                out += list(pfx.glob("**/LocalLow/Wizards Of The Coast/MTGA/Player.log"))
    return out


def find_log_path(explicit: Optional[str] = None) -> Optional[Path]:
    if explicit:
        p = Path(explicit).expanduser()
        return p if p.exists() else None
    for p in candidate_log_paths():
        try:
            if p.exists() and p.stat().st_size > 0:
                return p
        except OSError:
            continue
    return None


# --------------------------------------------------------------------------
# JSON extraction
# --------------------------------------------------------------------------

_OPENERS = "{["


def iter_json_blobs(text: str) -> Iterator[object]:
    """Yield every balanced JSON value embedded anywhere in `text`.

    Arena writes both single-line payloads and pretty-printed multi-line
    blocks, sometimes several per line, sometimes prefixed with markers like
    '[UnityCrossThreadLogger]==> Draft.Notify'. Scanning for balance handles
    all of those without knowing the markers.
    """
    i, n = 0, len(text)
    while i < n:
        ch = text[i]
        if ch not in _OPENERS:
            i += 1
            continue
        close = "}" if ch == "{" else "]"
        depth = 0
        j = i
        in_str = False
        esc = False
        while j < n:
            c = text[j]
            if in_str:
                if esc:
                    esc = False
                elif c == "\\":
                    esc = True
                elif c == '"':
                    in_str = False
            else:
                if c == '"':
                    in_str = True
                elif c in _OPENERS:
                    depth += 1
                elif c in "}]":
                    depth -= 1
                    if depth == 0:
                        break
            j += 1
        if depth == 0 and j < n and text[j] == close:
            chunk = text[i:j + 1]
            try:
                yield json.loads(chunk)
            except (ValueError, RecursionError):
                pass
            i = j + 1
        else:
            i += 1


def _unwrap_strings(obj: object, depth: int = 0) -> Iterator[object]:
    """Arena nests JSON inside JSON strings (payload / request / Payload)."""
    yield obj
    if depth > 3:
        return
    if isinstance(obj, dict):
        for v in obj.values():
            if isinstance(v, str) and len(v) > 2 and v.lstrip()[:1] in _OPENERS:
                try:
                    inner = json.loads(v)
                except ValueError:
                    continue
                yield from _unwrap_strings(inner, depth + 1)
            elif isinstance(v, (dict, list)):
                yield from _unwrap_strings(v, depth + 1)
    elif isinstance(obj, list):
        for v in obj[:50]:
            if isinstance(v, (dict, list)):
                yield from _unwrap_strings(v, depth + 1)


# --------------------------------------------------------------------------
# normalised events
# --------------------------------------------------------------------------

@dataclass
class PackEvent:
    pack_number: int
    pick_number: int
    card_ids: list[int]
    draft_id: str = ""
    source: str = ""

@dataclass
class PickEvent:
    card_id: int
    pack_number: int = 0
    pick_number: int = 0
    source: str = ""

@dataclass
class PoolEvent:
    card_ids: list[int]
    source: str = ""
    event_name: str = ""


def _ci(d: dict, *names) -> object:
    """Case-insensitive multi-key lookup."""
    if not isinstance(d, dict):
        return None
    lowered = {k.lower(): v for k, v in d.items() if isinstance(k, str)}
    for n in names:
        v = lowered.get(n.lower())
        if v is not None:
            return v
    return None


def _as_ids(v: object) -> list[int]:
    """Accept [123,124], ['123','124'] or '123,124'."""
    out: list[int] = []
    if isinstance(v, str):
        parts = [p for p in re.split(r"[,\s]+", v) if p]
    elif isinstance(v, list):
        parts = v
    else:
        return out
    for p in parts:
        try:
            out.append(int(p))
        except (TypeError, ValueError):
            if isinstance(p, dict):
                gid = _ci(p, "grpId", "GrpId", "cardId", "id")
                try:
                    out.append(int(gid))  # type: ignore[arg-type]
                except (TypeError, ValueError):
                    pass
    return out


def _as_int(v: object, default: int = 0) -> int:
    try:
        return int(v)  # type: ignore[arg-type]
    except (TypeError, ValueError):
        return default


PACK_KEYS = ("DraftPack", "PackCards", "CardsInPack", "draftPack", "packCards")
POOL_KEYS = ("CardPool", "cardPool", "CardsInPool", "PoolCards")


def classify(obj: object):
    """Yield normalised events found anywhere inside a decoded payload."""
    for node in _unwrap_strings(obj):
        if not isinstance(node, dict):
            continue

        raw_pack = _ci(node, *PACK_KEYS)
        if raw_pack is not None:
            ids = _as_ids(raw_pack)
            if ids:
                pack_no = _as_int(_ci(node, "PackNumber", "SelfPack", "packNumber"), 0)
                pick_no = _as_int(_ci(node, "PickNumber", "SelfPick", "pickNumber"), 0)
                # Premier draft numbers packs 0-2 / picks 0-13; quick draft 1-3 / 1-14.
                if pack_no == 0:
                    pack_no = 1
                if pick_no == 0:
                    pick_no = 1
                did = _ci(node, "DraftId", "draftId", "EventName", "eventName") or ""
                yield PackEvent(pack_no, pick_no, ids, str(did), "log")
                continue

        raw_pool = _ci(node, *POOL_KEYS)
        if raw_pool is not None:
            ids = _as_ids(raw_pool)
            if len(ids) >= 40:          # a sealed pool, not a 15-card pack
                name = _ci(node, "InternalEventName", "EventName", "eventName") or ""
                yield PoolEvent(ids, "log", str(name))
                continue

        pick = _ci(node, "CardId", "PickGrpId", "GrpId", "cardId")
        if pick is not None and _ci(node, *PACK_KEYS) is None:
            cid = _as_int(pick, 0)
            # Arena grpIds are 5-6 digits; filter out small enum-ish values.
            if cid > 10000:
                yield PickEvent(cid,
                                _as_int(_ci(node, "PackNumber", "SelfPack"), 0),
                                _as_int(_ci(node, "PickNumber", "SelfPick"), 0),
                                "log")


def parse_text(text: str):
    """Classify every event in a blob of log text (used by --replay)."""
    for blob in iter_json_blobs(text):
        yield from classify(blob)


# --------------------------------------------------------------------------
# tailing
# --------------------------------------------------------------------------

class LogTailer:
    """Follow a log file, surviving the truncation Arena does on relaunch."""

    def __init__(self, path: Path, from_start: bool = False, poll: float = 0.7):
        self.path = Path(path)
        self.poll = poll
        self._fh = None
        self._pos = 0
        self._from_start = from_start

    def _open(self):
        self._fh = open(self.path, "r", encoding="utf-8", errors="replace")
        if self._from_start:
            self._pos = 0
        else:
            self._fh.seek(0, os.SEEK_END)
            self._pos = self._fh.tell()
        self._from_start = True   # after a rotation we want the whole new file

    def lines(self) -> Iterator[str]:
        while True:
            if self._fh is None:
                if not self.path.exists():
                    time.sleep(self.poll)
                    continue
                self._open()
            try:
                size = self.path.stat().st_size
            except OSError:
                self._fh = None
                continue
            if size < self._pos:                 # truncated -> reopen at 0
                try:
                    self._fh.close()
                except OSError:
                    pass
                self._fh = None
                self._pos = 0
                continue
            self._fh.seek(self._pos)
            chunk = self._fh.read()
            self._pos = self._fh.tell()
            if chunk:
                yield chunk
            else:
                time.sleep(self.poll)

    def events(self, on_unknown=None):
        """Yield normalised events as they appear. Buffers partial JSON."""
        buf = ""
        for chunk in self.lines():
            buf += chunk
            if len(buf) > 4_000_000:             # never let the buffer run away
                buf = buf[-1_000_000:]
            consumed_to = 0
            found = False
            for blob in iter_json_blobs(buf):
                found = True
                got = False
                for ev in classify(blob):
                    got = True
                    yield ev
                if not got and on_unknown is not None:
                    on_unknown(blob)
            if found:
                # Keep a tail window in case a JSON block is still being written.
                buf = buf[-200_000:] if len(buf) > 200_000 else buf
                # Drop everything up to the last closing brace we saw.
                last = max(buf.rfind("}"), buf.rfind("]"))
                if last > 0:
                    buf = buf[last + 1:]
            del consumed_to
