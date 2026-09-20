#!/usr/bin/env python3
"""MTGA Coach launcher.  No install, no dependencies: python run_overlay.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

if sys.version_info < (3, 9):
    sys.exit("Python 3.9+ required (you have %d.%d)." % sys.version_info[:2])

from coach.cli import main  # noqa: E402

if __name__ == "__main__":
    raise SystemExit(main())
