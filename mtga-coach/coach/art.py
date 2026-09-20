"""Card images.

Real cards get their real art from Scryfall, downloaded once and cached under
~/.mtga-coach/art/. Generated practice cards (marked with a degree sign) have no
art anywhere, so this hands the UI a spec to draw a card face instead -- clearly
a placeholder, never dressed up as a real card.

Pillow is optional. With it, JPEGs are fetched and scaled smoothly. Without it,
PNGs are fetched because Tk's own image loader only reads PNG and GIF, and
scaling falls back to integer subsampling.
"""
from __future__ import annotations

import re
import threading
import time
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Callable, Optional

from .arenadb import CardInfo
from .model import Ratings

ART_DIR = Path.home() / ".mtga-coach" / "art"
SYNTH_MARK = "°"
UA = {"User-Agent": "mtga-coach/1.0", "Accept": "*/*"}

try:
    from PIL import Image, ImageTk          # noqa: F401
    HAVE_PIL = True
except ImportError:
    HAVE_PIL = False

# Card-face tints for generated placeholders, by colour identity.
FACE = {
    "W": ("#F6F1DE", "#2A2620"), "U": ("#CBDDF2", "#16222E"),
    "B": ("#CDC8C6", "#1D1A19"), "R": ("#F3CCB8", "#33150C"),
    "G": ("#CBE0C6", "#132414"), "GOLD": ("#EADFAE", "#2E2508"),
    "C": ("#D8D8D8", "#222222"),
}


def is_generated(card: CardInfo) -> bool:
    return SYNTH_MARK in (card.name or "")


def slug(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")[:80]


def face_colors(card: CardInfo, ratings: Ratings) -> tuple[str, str]:
    cols = ratings.card_colors(card)
    if not cols:
        return FACE["C"]
    if len(cols) > 1:
        return FACE["GOLD"]
    return FACE[next(iter(cols))]


def placeholder_spec(card: CardInfo, ratings: Ratings) -> dict:
    """Everything needed to draw a card face, with no Tk involved."""
    from .analysis import best_home
    bg, fg = face_colors(card, ratings)
    home = best_home(card, ratings)
    tags = ratings.tags(card)
    return {
        "bg": bg, "fg": fg,
        "name": (card.name or "").replace(SYNTH_MARK, ""),
        "cost": card.cost or (f"{card.cmc}" if card.cmc else ""),
        "colors": "".join(sorted(ratings.card_colors(card), key="WUBRG".index)) or "C",
        "types": card.types or "",
        "rarity": (card.rarity or "").title(),
        "tags": ", ".join(tags[:3]),
        "home": f"{home['pair']} {home['name']}" if home else "",
        "generated": is_generated(card),
    }


class ArtCache:
    """Fetches and caches card images. Never blocks the UI thread."""

    def __init__(self, setcode: str = "fra", enabled: bool = True,
                 directory: Path = ART_DIR):
        self.setcode = setcode
        self.enabled = enabled
        self.dir = Path(directory)
        self.dir.mkdir(parents=True, exist_ok=True)
        self._missing: set[str] = set()
        self._lock = threading.Lock()
        self._last_fetch = 0.0

    def path_for(self, card: CardInfo) -> Path:
        ext = "jpg" if HAVE_PIL else "png"
        return self.dir / f"{slug(card.name)}.{ext}"

    def cached(self, card: CardInfo) -> Optional[Path]:
        p = self.path_for(card)
        return p if p.exists() and p.stat().st_size > 1000 else None

    def _urls(self, card: CardInfo) -> list[str]:
        version = "normal" if HAVE_PIL else "png"
        n = urllib.parse.quote(card.name)
        return [
            f"https://api.scryfall.com/cards/named?exact={n}&set={self.setcode}"
            f"&format=image&version={version}",
            f"https://api.scryfall.com/cards/named?exact={n}"
            f"&format=image&version={version}",
        ]

    def fetch(self, card: CardInfo) -> Optional[Path]:
        """Blocking download. Returns None for anything without real art."""
        if not self.enabled or is_generated(card):
            return None
        if card.name in self._missing:
            return None
        hit = self.cached(card)
        if hit:
            return hit
        with self._lock:                      # Scryfall asks for ~10 req/sec
            wait = 0.12 - (time.time() - self._last_fetch)
            if wait > 0:
                time.sleep(wait)
            self._last_fetch = time.time()
        for url in self._urls(card):
            try:
                req = urllib.request.Request(url, headers=UA)
                with urllib.request.urlopen(req, timeout=15) as r:
                    data = r.read()
                if len(data) < 1000:
                    continue
                p = self.path_for(card)
                p.write_bytes(data)
                return p
            except Exception:                 # noqa: BLE001 - art is optional
                continue
        self._missing.add(card.name)
        return None

    def prefetch(self, cards: list[CardInfo],
                 done: Optional[Callable[[CardInfo, Optional[Path]], None]] = None) -> None:
        """Warm the cache in the background."""
        if not self.enabled:
            return

        def work():
            for c in cards:
                p = self.fetch(c)
                if done:
                    try:
                        done(c, p)
                    except Exception:         # noqa: BLE001
                        pass
        threading.Thread(target=work, daemon=True).start()

    def stats(self) -> dict:
        return {"cached": len(list(self.dir.glob("*"))),
                "missing": len(self._missing), "pillow": HAVE_PIL}
