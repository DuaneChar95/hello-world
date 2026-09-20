"""Where data lives, whether running from source or from a frozen executable.

PyInstaller unpacks bundled files to a temporary directory that is wiped on
exit, so the shipped ratings file is read-only. Anything the user changes --
an imported card list, 17Lands grades -- is written to their home directory
instead and takes precedence on load.
"""
from __future__ import annotations

import sys
from pathlib import Path

USER_DIR = Path.home() / ".mtga-coach"


def frozen() -> bool:
    return bool(getattr(sys, "frozen", False))


def bundled_dir() -> Path:
    """The read-only data that ships with the app."""
    if frozen():
        return Path(getattr(sys, "_MEIPASS", Path(sys.executable).parent)) / "data"
    return Path(__file__).resolve().parent.parent / "data"


def user_dir() -> Path:
    USER_DIR.mkdir(parents=True, exist_ok=True)
    return USER_DIR


def ratings_path() -> Path:
    """User's own ratings if they have imported any, else the shipped file."""
    mine = USER_DIR / "fra_ratings.json"
    if mine.exists():
        return mine
    return bundled_dir() / "fra_ratings.json"


def writable_ratings_path() -> Path:
    """Where an import should write - never into the bundle."""
    return user_dir() / "fra_ratings.json"


def data_file(name: str) -> Path:
    mine = USER_DIR / name
    return mine if mine.exists() else bundled_dir() / name
