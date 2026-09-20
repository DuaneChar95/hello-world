"""Draft state: assemble log events into a pool, and persist every draft."""
from __future__ import annotations

import json
import time
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Optional

from .arenadb import CardInfo, CardResolver
from .model import PoolState, Ratings, Scored, score_pack, pool_summary

DRAFT_DIR = Path.home() / ".mtga-coach" / "drafts"


@dataclass
class RecordedPick:
    pack_number: int
    pick_number: int
    pack: list[int]
    chosen: Optional[int] = None
    recommended: Optional[int] = None
    rec_score: float = 0.0
    chosen_score: float = 0.0


class DraftSession:
    """Turns a stream of PackEvent/PickEvent into advice and a saved record."""

    def __init__(self, resolver: CardResolver, ratings: Ratings, mode: str = "draft",
                 profile=None):
        self.resolver = resolver
        self.ratings = ratings
        self.profile = profile
        self.annotation: dict = {}
        self.pool = PoolState(mode=mode)
        self.current_pack: list[CardInfo] = []
        self.current_scored: list[Scored] = []
        self.pack_number = 0
        self.pick_number = 0
        self.history: list[RecordedPick] = []
        self._pending: Optional[RecordedPick] = None
        self._seen_packs: set[tuple] = set()
        self.started = time.time()
        self.draft_id = ""

    # -- ingest ---------------------------------------------------------
    def on_pack(self, pack_no: int, pick_no: int, card_ids: list[int], draft_id: str = "") -> bool:
        key = (pack_no, pick_no, tuple(card_ids))
        if key in self._seen_packs:
            return False
        self._seen_packs.add(key)
        if draft_id:
            self.draft_id = draft_id
        self.pack_number, self.pick_number = pack_no, pick_no
        self.current_pack = [self.resolver.get(i) for i in card_ids]
        self.current_scored = score_pack(self.current_pack, self.pool, self.ratings, pack_no, pick_no)
        self._annotate()
        best = self.current_scored[0] if self.current_scored else None
        self._pending = RecordedPick(
            pack_no, pick_no, list(card_ids),
            recommended=best.card.grpid if best else None,
            rec_score=best.score if best else 0.0,
        )
        return True

    def on_pick(self, card_id: int) -> bool:
        if self._pending is None or card_id not in self._pending.pack:
            # A pick we have no pack for (joined mid-draft) still grows the pool.
            if card_id > 10000:
                self.pool.add(self.resolver.get(card_id))
                return True
            return False
        self._pending.chosen = card_id
        chosen = next((s for s in self.current_scored if s.card.grpid == card_id), None)
        self._pending.chosen_score = chosen.score if chosen else 0.0
        self.history.append(self._pending)
        self.pool.add(self.resolver.get(card_id))
        self._pending = None
        self.current_pack = []
        self.current_scored = []
        self.annotation = {}
        return True

    def on_pool(self, card_ids: list[int]) -> None:
        """Sealed: the whole pool arrives at once."""
        self.pool = PoolState(mode="sealed")
        for i in card_ids:
            self.pool.add(self.resolver.get(i))
        self.current_pack = [self.resolver.get(i) for i in card_ids]
        self.current_scored = score_pack(self.current_pack, self.pool, self.ratings, 1, 1)
        self._annotate()

    def _annotate(self) -> None:
        from .playstyle import annotate_pack
        try:
            self.annotation = annotate_pack(self.current_scored, self.profile, self.ratings)
        except Exception:                                  # noqa: BLE001 - advice is optional
            self.annotation = {}

    # -- output ---------------------------------------------------------
    def summary(self) -> dict:
        return pool_summary(self.pool, self.ratings)

    def save(self, directory: Path = DRAFT_DIR) -> Optional[Path]:
        if not self.history:
            return None
        directory.mkdir(parents=True, exist_ok=True)
        stamp = time.strftime("%Y%m%d-%H%M%S", time.localtime(self.started))
        path = directory / f"draft-{stamp}.json"
        n = 1
        while path.exists():                 # two drafts in the same second
            path = directory / f"draft-{stamp}-{n}.json"
            n += 1
        names, meta = {}, {}
        for rp in self.history:
            for gid in rp.pack:
                if gid not in names:
                    ci = self.resolver.get(gid)
                    names[gid] = ci.name
                    meta[gid] = {"colors": ci.colors, "rarity": ci.rarity,
                                 "cmc": ci.cmc, "types": ci.types}
        payload = {
            "set": self.ratings.raw.get("set", ""),
            "mode": self.pool.mode,
            "draft_id": self.draft_id,
            "started": self.started,
            "picks": [asdict(h) for h in self.history],
            "names": {str(k): v for k, v in names.items()},
            "meta": {str(k): v for k, v in meta.items()},
            "final_pool": [c.name for c in self.pool.picks],
        }
        path.write_text(json.dumps(payload, indent=1), encoding="utf-8")
        return path


def load_drafts(directory: Path = DRAFT_DIR) -> list[dict]:
    if not directory.exists():
        return []
    out = []
    for f in sorted(directory.glob("draft-*.json")):
        try:
            out.append(json.loads(f.read_text(encoding="utf-8")) | {"_file": str(f)})
        except (OSError, ValueError):
            continue
    return out
