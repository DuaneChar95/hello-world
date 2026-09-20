# MTGA Coach — Reality Fracture

A read-only draft/sealed overlay and trainer for MTG Arena, built around the
[Reality Fracture guide](../reality-fracture/DRAFT-GUIDE.md).

It does three things:

1. **Overlay** — an always-on-top window that reads the pack Arena is showing you
   and ranks it, with a one-line reason per card and a live read on which lane
   your pool is actually in.
2. **Review** — after the draft, it regrades every pick you made and tells you
   what your *patterns* are, not just your mistakes.
3. **Trainer** — concept drills on this format's mechanics, plus a pack quiz that
   replays the real packs you faced and makes you pick again.

```
python run_overlay.py                 # the overlay
python run_overlay.py --review        # grade your saved drafts
python run_overlay.py --drills        # concept drills (works before the set is out)
python run_overlay.py --quiz --hard   # re-pick the packs you got wrong
```

---

## What it is and isn't

**It reads a log file. That's all it does.** Arena writes `Player.log` when you
turn on *Detailed Logs (Plugin Support)* — a setting Wizards added specifically
so tools like this can exist. This app tails that file. It does not inject code,
modify the client, touch game memory, automate any action, or show you anything
you can't already see on your own screen. That's the same mechanism 17Lands and
Untapped use.

**Desktop only.** Windows and macOS. There is no log file on iOS/Android, so
there is no way to do this on mobile — by anyone, not just by this tool.

**Arena must be in Windowed or Borderless mode.** An exclusive-fullscreen game
paints over every other window. That's an OS-level rule, not a bug here.

---

## Setup

**1. Turn on detailed logs in Arena**

> Options → Account → **Detailed Logs (Plugin Support)** → on → **restart Arena**

Nothing works without this, and it's the number one reason a tracker shows blank.

**2. Check your Python**

Python 3.9 or newer, with `tkinter` (the python.org installers for Windows and
macOS include it). No pip install, no dependencies.

```
python3 -c "import tkinter; print('ok')"
```

If that fails: `brew install python-tk` (macOS/Homebrew) or
`sudo apt install python3-tk` (Linux).

**3. Run it**

```
cd mtga-coach
python run_overlay.py
```

Then start a draft. Drag the window by its title bar; `Esc` closes it.
Your draft is saved to `~/.mtga-coach/drafts/` when you close the overlay.

For sealed: `python run_overlay.py --mode sealed`

---

## Reading the overlay

```
PACK 1  PICK 5
 1. Denzilore Fatehold            4.95     <- top pick, highlighted
    Rated 4.5; on-colour for WU; feeds Fatehold
 2. Prudent Fateseer              3.80
    Rated 3.5; in-college prepared - body plus a spell you want
 3. Theorist's Proxy              3.05
    empower surveil also fires your payoffs here
then: Hallway Heckler 1.9 · Titanbones 2.1 · ...

12 picks   W7 U6 B2
Fatehold (WU) tier S
Clearly in Fatehold. Commit and take playables.
interaction 2 (want 4+)   creatures 8
```

The score is the card's grade adjusted for your pool: colour fit (weighted by
how late it is), archetype fit, curve holes, interaction count, and the
format-specific rules from the guide — threshold outside U/B, face damage
outside a fast B/R, empower in a deck that can use the surveils.

**The reasons matter more than the number.** If you disagree with the reason,
you're probably right and the model is probably missing something about your pool.

---

## Review

```
python run_overlay.py --review
```

Per pick it shows what you took, what the model wanted, and the gap. Then the
part that's actually useful — the aggregate:

```
  * Average pick loss 0.60 across 39 picks (reasonable).
  * You and the model agreed on 12/39 picks (30%).
  * Your early picks cost more than your late ones - you are over-thinking
    pack 1. Early, just take the most powerful card.
  * You ended in Stingerquill (BR, tier C, 6.2 draft score).
  * Stingerquill is a C-tier lane. Ask whether it was open, or whether you forced it.
  * Biggest three leaks: P2p11 took Theorist's Proxy over Overwrite the
    Multiverse (-2.83); ...
```

Across several drafts it also reports the cards you most often pass that the
model wants — which is usually where a real leak lives.

---

## Trainer

**Concept drills** — 15 questions on this format's mechanics: empower Jace
pricing, prepared timing, threshold, the archetype tiers, signal reading. These
work right now, before the set is playable.

```
python run_overlay.py --drills -n 10
```

**Pack quiz** — replays real packs from your own drafts, with your real pool as
context, and grades your pick. `--hard` restricts it to the picks you got wrong,
which is the version worth doing.

```
python run_overlay.py --quiz --hard -n 15
```

Progress and your recurring misses are tracked in `~/.mtga-coach/profile.json`.

---

## Replacing my ratings with real data

The bundled ratings are a **pre-release prior** — my evaluation, written before
anyone had played the set. The overlay says `eval` until you fix that.

Once you have 17Lands data (from ~Oct 2026), export their card-ratings CSV and:

```
python run_overlay.py --import-17lands 17lands-fra.csv
```

It maps GIH WR onto the 0–5 limited scale (50% → 3.0, 60% → 4.5), merges it over
the priors, and flips the confidence flag to `data`. **Do this as soon as you
can** — a few thousand real games beat my reasoning every time.

---

## Troubleshooting

| Symptom | Fix |
|---|---|
| Overlay says "waiting for a pack" forever | Detailed Logs off, or Arena not restarted after enabling it. |
| Card names show as `Unknown #91234` | Arena's card database wasn't found. Try `--card-db <path to Raw_CardDatabase_*.mtga>`, or `--refresh-cards`, or let it use Scryfall (drop `--offline`). |
| Overlay hidden behind Arena | Set Arena to Windowed or Borderless. |
| Log found but nothing parses | Run with `--dump-unknown unknown.json`, play a draft, and send me that file — Arena's log format drifts and the parser is keyed to shapes, not exact strings. |
| Want to test without drafting | `python run_overlay.py --replay <a saved Player.log>` prints what the overlay would have shown. |
| Want to check the logic | `python run_overlay.py --selftest` |

`--card-map cards.json` accepts a plain `{"91234": "Card Name"}` map if you ever
need to bypass card resolution entirely.

---

## Layout

```
run_overlay.py        launcher
coach/logwatch.py     finds and tails Player.log; tolerant JSON event parser
coach/arenadb.py      grpId -> name/colors/rarity (Arena's SQLite, or Scryfall)
coach/model.py        pick scoring and pool/lane reading - the guide, as code
coach/session.py      draft state and persistence
coach/review.py       regrading and the lesson generator
coach/quiz.py         drills and pack quiz
coach/overlay.py      the tkinter HUD (thin - it only draws)
data/fra_ratings.json card grades, archetypes, tags   <- edit this freely
data/drills.json      the concept questions
```

`data/fra_ratings.json` is meant to be edited. Add cards as they're spoiled, fix
grades you disagree with — the overlay picks up changes on restart.

## Limits worth knowing

- Card grades for FRA are incomplete: the set wasn't fully spoiled when this was
  written, so unrated cards fall back to a rarity placeholder and say so.
- Interaction counts under-read until real removal cards are in the ratings file.
- The model reads *your* pool, not what's being passed. Signal reading is still
  yours to do — the guide's section on college prepared commons is the method.
