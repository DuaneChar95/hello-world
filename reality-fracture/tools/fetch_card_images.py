"""Download every Reality Fracture card image and pack them into sprite sheets.

Runs in GitHub Actions (see .github/workflows/fetch-card-images.yml), because
the machine that writes the draft guide cannot reach any image host. The
output is committed back to the repo:

    reality-fracture/card-images/thumb-<n>.webp   240px-wide cards, 28 per sheet
    reality-fracture/card-images/full-<n>.webp    480px-wide cards, 28 per sheet
    reality-fracture/card-images/sprites.json     card name -> sheet, column, row

Sprite sheets rather than one file per card because the published page may
carry at most 255 supporting files, and there are 280 cards.

Scryfall asks for a descriptive User-Agent and 50-100 ms between requests;
both are honoured. Image URLs come from mtga-coach/data/fra_ratings.json,
which was built from the user's own Scryfall export.
"""
from __future__ import annotations

import io
import json
import sys
import time
from pathlib import Path

import requests
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
RATINGS = ROOT / "mtga-coach" / "data" / "fra_ratings.json"
OUT = ROOT / "reality-fracture" / "card-images"

COLS, ROWS = 7, 4                      # 28 cards per sheet -> 10 sheets
SIZES = {"thumb": 240, "full": 480}    # card width in px; height follows 488:680
RATIO = 680 / 488
UA = "hexhaven-draft-table/1.0 (card-image fetch for a personal draft guide)"
DELAY = 0.1


def card_size(width: int) -> tuple[int, int]:
    return width, round(width * RATIO)


def fetch(url: str, session: requests.Session) -> Image.Image | None:
    for attempt in range(3):
        try:
            r = session.get(url, timeout=30, headers={"User-Agent": UA, "Accept": "image/*"})
            if r.status_code == 200:
                return Image.open(io.BytesIO(r.content)).convert("RGB")
            if r.status_code == 404:
                return None
            print(f"  {r.status_code} on attempt {attempt + 1}: {url}")
        except requests.RequestException as e:  # noqa: PERF203
            print(f"  error on attempt {attempt + 1}: {e}")
        time.sleep(1.5 * (attempt + 1))
    return None


def main() -> int:
    cards = json.loads(RATINGS.read_text(encoding="utf-8"))["cards"]
    basics_path = OUT / "basics.json"
    if basics_path.exists():
        for name, url in json.loads(basics_path.read_text(encoding="utf-8")).items():
            cards[name] = {"image": url}
    names = sorted(cards)
    print(f"{len(names)} cards to fetch")
    OUT.mkdir(parents=True, exist_ok=True)

    session = requests.Session()
    images: dict[str, Image.Image] = {}
    missing: list[str] = []
    for i, name in enumerate(names):
        url = cards[name]["image"].replace("/large/", "/normal/")
        img = fetch(url, session)
        if img is None:
            missing.append(name)
            print(f"MISSING {name}")
        else:
            images[name] = img
        if (i + 1) % 25 == 0:
            print(f"  {i + 1}/{len(names)}")
        time.sleep(DELAY)

    print(f"fetched {len(images)}, missing {len(missing)}")
    if len(images) < len(names) * 0.9:
        print("fewer than 90% of images fetched - refusing to commit a broken set")
        return 1

    manifest: dict = {"cols": COLS, "rows": ROWS, "sizes": {}, "cards": {}, "missing": missing}
    per_sheet = COLS * ROWS
    ordered = [n for n in names if n in images]
    for label, width in SIZES.items():
        cw, ch = card_size(width)
        manifest["sizes"][label] = {"w": cw, "h": ch, "sheets": 0}
        for s in range(0, len(ordered), per_sheet):
            sheet_idx = s // per_sheet
            chunk = ordered[s:s + per_sheet]
            rows_used = (len(chunk) + COLS - 1) // COLS
            sheet = Image.new("RGB", (COLS * cw, rows_used * ch), (24, 24, 28))
            for k, name in enumerate(chunk):
                col, row = k % COLS, k // COLS
                sheet.paste(images[name].resize((cw, ch), Image.LANCZOS), (col * cw, row * ch))
                if label == "thumb":
                    manifest["cards"][name] = {"sheet": sheet_idx, "col": col, "row": row}
            path = OUT / f"{label}-{sheet_idx}.webp"
            sheet.save(path, "WEBP", quality=82, method=6)
            manifest["sizes"][label]["sheets"] = sheet_idx + 1
            print(f"wrote {path.name}  {sheet.size[0]}x{sheet.size[1]}  {path.stat().st_size // 1024} KB")

    (OUT / "sprites.json").write_text(json.dumps(manifest, indent=1, ensure_ascii=False), encoding="utf-8")
    total = sum(p.stat().st_size for p in OUT.glob("*.webp"))
    print(f"total {total / 1e6:.1f} MB across {len(list(OUT.glob('*.webp')))} sheets")
    return 0


if __name__ == "__main__":
    sys.exit(main())
