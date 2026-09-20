#!/usr/bin/env python3
"""Download a full set's card list from Scryfall, then import it.

    python fetch_cards.py                # Reality Fracture
    python fetch_cards.py --set dsk      # any set code
    python fetch_cards.py --no-import    # just save the JSON

Scryfall pages its search results; this follows next_page until done and
rate-limits politely. Run it on a machine with internet access.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
UA = {"User-Agent": "mtga-coach/1.0", "Accept": "application/json"}


def fetch(setcode: str) -> list[dict]:
    q = urllib.parse.quote(f"set:{setcode} -is:extra")
    url = f"https://api.scryfall.com/cards/search?q={q}&unique=prints&order=set"
    cards: list[dict] = []
    page = 1
    while url:
        req = urllib.request.Request(url, headers=UA)
        with urllib.request.urlopen(req, timeout=30) as r:
            data = json.load(r)
        got = data.get("data", [])
        cards += got
        total = data.get("total_cards", "?")
        print(f"  page {page}: +{len(got)}  ({len(cards)}/{total})")
        url = data.get("next_page") if data.get("has_more") else None
        page += 1
        if url:
            time.sleep(0.12)          # Scryfall asks for ~10 req/sec
    return cards


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--set", default="fra", help="set code (default: fra)")
    ap.add_argument("--out", help="where to write the JSON")
    ap.add_argument("--no-import", action="store_true",
                    help="save the file but do not rebuild the ratings")
    a = ap.parse_args()

    out = Path(a.out) if a.out else HERE / "data" / f"{a.set.lower()}_cards.json"
    out.parent.mkdir(parents=True, exist_ok=True)

    print(f"fetching {a.set.upper()} from Scryfall...")
    try:
        cards = fetch(a.set)
    except Exception as e:                                   # noqa: BLE001
        print(f"\nfailed: {e}\n")
        print("If this machine cannot reach Scryfall, open this in a browser and")
        print("save the JSON, then run:  python run_overlay.py --import-cards <file>")
        print(f"  https://api.scryfall.com/cards/search?q=set%3A{a.set.lower()}")
        return 2
    if not cards:
        print("no cards returned - is the set code right?")
        return 2
    out.write_text(json.dumps(cards), encoding="utf-8")
    print(f"\nsaved {len(cards)} cards -> {out}")

    if a.no_import:
        print(f"run:  python run_overlay.py --import-cards {out}")
        return 0
    sys.path.insert(0, str(HERE))
    from coach.cli import main as cli_main
    return cli_main(["--import-cards", str(out)])


if __name__ == "__main__":
    raise SystemExit(main())
