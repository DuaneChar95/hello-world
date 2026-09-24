# Untapped.gg data for Reality Fracture

`untapped-fra.json` is the parsed free-tier data from <https://mtga.untapped.gg/limited/draft/reality-fracture/>:
per-card games-in-hand and opening-hand win rates, average pick taken / last seen, colour-pair match
win rates, event totals and the trophy decks the free page lists. The `captured` timestamps inside the
file say when Untapped last updated each table.

Untapped serves its pages through a bot check, so a CI runner cannot fetch them. Refresh from your own
browser on Windows:

```powershell
powershell -ExecutionPolicy Bypass -File reality-fracture\tools\grab-untapped.ps1 -Out untapped-dump
python reality-fracture\tools\untapped_parse.py untapped-dump reality-fracture\untapped\untapped-fra.json
python reality-fracture\tools\untapped_apply.py reality-fracture\untapped\untapped-fra.json --page reality-fracture\companion\hexhaven.html --ratings mtga-coach\data\fra_ratings.json
python reality-fracture\tools\untapped_report.py reality-fracture\untapped\untapped-fra.json mtga-coach\data\fra_ratings.json
```

* `untapped_parse.py` reads the `__NEXT_DATA__` payload in `pick-order.html` (card stats, draft picks, colour
  pairs, the Arena card table that maps title ids to names) and the rendered decklists in `trophy-decks.html`.
* `reality-fracture/companion/hexhaven.html` is the source of the published companion page (card art comes from `../card-images`, published as `cards/`).
* `untapped_apply.py` rewrites the marked blocks in the companion page (data, tab, UI, card-sheet row) and
  blends the grades in `fra_ratings.json`: `grade = w * data + (1 - w) * grade_prerelease`, `w = games / (games + 60)`.
* `mydecks_apply.py` installs the My Decks tab (decks you played, Claude's analysis of win conditions and combos, your points, W–L record) from `mydecks_ui.js` the same way.
* `untapped_report.py` prints the Markdown for guide section 14.

Only `pick-order.html` and `trophy-decks.html` carry data in a saved page; the tier-list and sealed pages
load their tables after the page renders and save empty. The tier list here is derived from the same card
stats (games-in-hand win rate bands), which is what Untapped's own tier list is built from.
