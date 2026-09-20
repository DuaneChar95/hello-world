# MTGA Coach — Reality Fracture

A read-only draft/sealed overlay and trainer for MTG Arena, built around the
[Reality Fracture guide](../reality-fracture/DRAFT-GUIDE.md).

It does three things:

0. **Practice** — a full 8-person draft pod, or a sealed pool, played in the
   terminal with no Arena needed. Bots commit to lanes and cut colours, so
   signal reading is real.
1. **Overlay** — an always-on-top window that reads the pack Arena is showing you
   and ranks it, with a one-line reason per card and a live read on which lane
   your pool is actually in.
2. **Review** — after the draft, it regrades every pick you made and tells you
   what your *patterns* are, not just your mistakes.
3. **Playstyle** — profiles how you draft, marks picks as in-style or stretch,
   and separates your preferences from the habits that actually cost you.
4. **Trainer** — concept drills on this format's mechanics, plus a pack quiz that
   replays the real packs you faced and makes you pick again.

```
python run_overlay.py --practice      # draft a pod against bots, no Arena needed
python run_overlay.py --practice-sealed
python run_overlay.py                 # the overlay (needs Arena)
python run_overlay.py --playstyle     # how you draft, and what would stretch you
python run_overlay.py --review        # grade your saved drafts (includes playstyle)
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

## Getting the Windows app

### Download a prebuilt one (no Python needed)

Every push builds it on a Windows runner. Go to the repository's
**Actions → Build Windows app → the latest run → Artifacts →
`MTGA-Coach-Windows`**, download the zip, and extract it anywhere.

You need to be signed in to GitHub to download a workflow artifact, and they
expire after 90 days. If the latest one has expired, open the workflow and press
**Run workflow** to build a fresh one.

### Or build it yourself

Double-click **`build.bat`**. It regenerates the icon, installs PyInstaller if
you don't have it, and builds into `dist\`:

```
dist\MTGA Coach.exe              <- double-click this
dist\MTGA Coach (console).exe    <- used by the terminal modes
```

**Keep both files in the same folder.** A windowed Windows executable has no
stdout, so the terminal modes (drills, review, playstyle, the text draft) run in
the console build, which the launcher starts for you.

`MTGA Coach.exe` opens a menu — practice draft, sealed, trainer, quiz, review,
playstyle, the live Arena overlay, and buttons to import a card list or 17Lands
CSV. No command line needed.

The icon is generated from source by `assets/make_icon.py` with no image library
— raw PNG bytes packed into a six-size `.ico`. Edit the colours at the top of
that file and re-run `build.bat` if you want a different mark.

**Where your data goes:** anything you import is written to
`%USERPROFILE%\.mtga-coach\` and takes precedence over the copy inside the
executable. That matters because a one-file build unpacks to a temporary folder
that is wiped on exit — your imports would not survive there. Drafts, your
playstyle profile and quiz progress live in the same folder.

macOS and Linux: the same spec works with `pyinstaller mtga-coach.spec`, though
the console binary is only needed on Windows.

---

## Practice

**Windows: build a double-clickable app** — see [Building the executable](#building-the-executable).

```
python run_overlay.py --practice --gui      # card images, hover for detail
python run_overlay.py --practice            # same draft, in the terminal
python run_overlay.py --practice-sealed     # 6 packs, build 40
python run_overlay.py --practice --coach    # training wheels: advice BEFORE you pick
python run_overlay.py --practice --silent   # no feedback until the end
python run_overlay.py --practice --seed 42  # a reproducible draft
```

You pick by number. `p` shows your pool and current lane read, `?` reprints the
rubric, `q` quits.

```
  PACK 1  PICK 1   (14 cards)
   1. Untamed Rootspeaker°         G  3  u    8. Reckless Agitator°      RG 3  R
   2. Grim Repriser                BR 3  c    9. Hollow Failing Grade°   B  3  c
   ...
  pick > 3

  - Invasive Rootspeaker° (2.55).  Model: Failing Grade° (3.92), -1.37
    why: Rated 3.5; in a strong colour
    style: in style, costly - typical of you, but it cost 1.4
```

**Advice is hidden while you pick.** A practice tool that shows the answer first
is a reading exercise, not a draft. You get the verdict *after* committing, plus
the style read once you have a profile. `--coach` turns that off if you want
training wheels; `--silent` defers everything to the end.

### Card images and hover  (`--gui`)

```
python run_overlay.py --practice --gui
python run_overlay.py --practice --gui --card-scale 1.3   # bigger cards
python run_overlay.py --practice --gui --no-art           # skip downloads
```

Opens a window with the pack laid out as cards. **Hover any card** and the side
panel tells you what it pairs with and whether you can splash it:

```
  PAIRS BEST WITH
    WU  Fatehold — tier S
         exactly WU; wants flying, surveil
    UB  Theorix — tier A
         half on-colour; wants surveil

  SPLASH
    Gold (WU) - not a splash card.
    Needs both colours on curve. Only playable in a deck already in one
    of them, and even then the second colour has to be real.
```

Splash analysis uses **pip counts, not colour identity** — `{1}{R}` and `{R}{R}`
are the same colour and completely different propositions. When a real mana cost
is available the count is exact; when it isn't, the panel says so rather than
inventing precision. It also knows the format-specific bit: **R/G Konstrari
splashes best here, because Heartwood tokens tap for R or G and fix a third
colour for free.**

The same analysis is in the terminal draft — type `i 3` to inspect card 3.

#### About the images

- **Real spoiled cards** pull their actual art from Scryfall, downloaded once
  and cached in `~/.mtga-coach/art/`. Needs internet the first time.
- **Generated practice cards** have no art anywhere, so they are drawn as a
  plain card face with a `PLACEHOLDER · NOT A REAL CARD` stripe. They are never
  dressed up to look real.
- `pip install Pillow` gives smoother scaling and smaller downloads. Without it
  the app fetches PNGs and scales by integer steps, which works but is chunkier.
- The web version of this guide **cannot** show card images — published artifacts
  block external images at the CSP level. Images are desktop-only.

### The bots actually cut colours

Seven bots keep colour counts and commit to lanes, and packs pass left, right,
left. What gets taken upstream genuinely dries up downstream:

```
  colour share of cards reaching your seat, early picks vs late picks
    W: early 23.3%  late 11.6%   DRIED UP
    U: early 17.6%  late  7.2%   DRIED UP
    R: early 22.2%  late 33.3%   FLOWING
    G: early 17.0%  late 31.9%   FLOWING
```

That is the whole point: signal reading is a skill you can only practise against
opponents who are really competing for cards. The bots are tuned slightly below
optimal so lanes open up the way they do at a real table.

At the end it builds your best deck, grades the curve, interaction and creature
counts, and saves the draft — so `--review`, `--playstyle` and `--quiz` all work
on your practice drafts exactly as they do on real ones.

Sealed asks for your two colours *first*, then shows what the model would have
built and why:

```
  YOUR BUILD: UB
  Best build: Theorix (UB) - 23 playables from 28 on-colour cards
  Interaction: 3. Every FRA deck wants 4+...

  The model would build Fatehold (WU) instead:
  Best build: Fatehold (WU) - 23 playables from 44 on-colour cards
```

### About the cards — and how to make them real

**One command switches the whole app to the real card list:**

```
python fetch_cards.py
```

It pulls every Reality Fracture card from Scryfall (following pagination,
rate-limited politely), saves the JSON, and rebuilds the ratings file. From then
on **practice packs are drawn from the real 333 cards**, the overlay recognises
them, and hover shows real mana costs — which makes splash advice exact instead
of approximate.

**No Python where the internet is?** Open this one URL in a browser and save the
file — Scryfall's CSV export returns the whole set in a single response, with no
pagination to deal with:

```
https://api.scryfall.com/cards/search?q=set%3Afra&format=csv
python run_overlay.py --import-cards fra.csv
```

If you save the JSON instead, it pages at 175 cards, so you will get two files.
That is fine — pass both and they are merged and de-duplicated:

```
python run_overlay.py --import-cards page1.json page2.json
```

`--import-cards` also accepts an **MTGJSON** set file or a **CSV** with a name
column. It derives tags from oracle text — prepared and which college's spell it
carries, empower Jace, threshold, Heartwood, removal (splitting instant-speed
cheap removal from the rest), board wipes, evasion, lands and fixing — so the
scorer understands real cards the same way it understands the hand-written ones.

It also **tells you which hand-written cards are not in the real list.** Those
are names guessed wrong during research; `--prune` drops them.

**Until you import**, the pool is: every card known at the time of writing
(~51) seeded at its real rarity, plus generated placeholders marked `°` filling
out the set's true composition (71/109/64/26). Placeholders are not predictions —
no claim is made that any of them will exist.

Either way the practice trains what decides drafts: reading signals, committing
at the right time, curve, interaction counts, archetype fit, and the rubric.
None of that is card knowledge.

**Grades stay heuristic even after importing** — rarity and type with adjustments
for removal, evasion and rate. The confidence flag reads `carddata`, not `data`.
Run `--import-17lands` once win rates exist and it becomes real.

Practice drafts are tagged `simulated` in the saved file. `--real-only` excludes
them from `--review` and `--playstyle` once you have real Arena drafts.

---

## Playstyle

```
python run_overlay.py --playstyle
```

Profiles you from your own saved drafts across six axes — curve, power vs
synergy, commitment timing, interaction appetite, creature balance, and late
discipline — plus colour bias measured properly: **how often you take a colour
against how often you actually see it**, so a blue bias means you reach for
blue, not that you opened blue cards.

```
  PLAYSTYLE: OPEN MIDRANGE DRAFTER
  5 drafts, 195 graded picks - confidence: emerging

  Curve            slow / top-heavy ------O---|---------- fast / cheap
               your picks average 2.70 mana against 2.37 for the cards you see

  COLOURS - how often you take a colour vs how often you see it
    U   1.20x   favoured
    G   0.91x   neutral
    -> you reach for U/B
```

### Style is not a leak

The report keeps those two apart on purpose. A tendency is only called a leak
when the numbers say so — the average pick loss on picks that express it,
against picks that don't:

```
  TENDENCIES - measured cost, not opinion
    COSTS  taking a rare over a better-scoring common or uncommon
           1.09 vs 0.56 (+0.53 per pick over 57 picks)
    EARNS  taking the synergy card over the strongest card
           0.0 vs 0.78 (-0.78 per pick over 15 picks) - keep doing this
```

Some of your habits will be *earning* you points. Those get left alone rather
than sanded into a generic drafter.

### In-style and stretch picks, live

Once you have ~20 graded picks, the overlay starts flagging two things:

- **`STRETCH`** — a card nearly as good as your default pick, but the kind you
  normally pass. Offered as a choice, never a correction; taking it is how your
  range grows, and skipping it isn't a mistake.
- **`NOT YOUR USUAL PICK`** on the top recommendation — the best card in the
  pack is itself one your bias would make you pass. This is the more valuable
  warning of the two.

Fit is judged **against the rest of that pack**, not an absolute scale, so a
pack that doesn't split along your preferences produces no stretch pick at all
rather than a manufactured one. `--review` labels every past pick *in style* /
*in style, costly* / *stretch* / *off profile*.

The report ends with concrete experiments drawn from your most lopsided axes —
a colour you avoid that the format rates well, a tier-A lane you have never
ended in, a commitment habit worth testing once.

**Sample size is stated, not hidden.** Under 3 drafts it says `provisional` and
tells you to treat it as a sketch; 3–9 is `emerging`; 10+ is `established`.

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
