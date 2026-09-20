# Reality Fracture (FRA) — Limited Deep Dive

**Draft & Sealed guide for MTG Arena.**
Set releases **October 2, 2026** · Paper prerelease **Sept 25 – Oct 1** · **Arena digital queues open Sept 29, 2026**.
Written 2026-09-20, during spoiler season.

**Interactive companion:** <https://claude.ai/artifact/CjBgGyDCeXzeGRLpyRGzwf> — the same analysis as a
working page, with a live signal tracker for the seat you're in.
**In-session coach:** run `/fra-draft` (skill at `.claude/skills/fra-draft/SKILL.md`).

---

## 0. How to read this guide (sourcing & confidence)

This set is **not out yet**. There is no 17Lands data, because nobody has played a game.
Anyone publishing a "definitive" pick order right now is guessing with confidence. This guide
separates the two things:

| Tag | Meaning |
|---|---|
| **[CONFIRMED]** | Stated by Wizards (mechanics articles, prerelease guide, release notes) or reported consistently across preview coverage. |
| **[EVAL]** | My own Limited evaluation, reasoned from set structure. Treat as a strong prior, not fact. |
| **[WATCH]** | Explicitly uncertain. Verify at prerelease / first 200 games. |

**Two of your links could not be opened from this machine.** The network egress policy on this
session blocks `media.wizards.com` (your archetype image), `docs.google.com` (your spreadsheet),
and every card database (Scryfall, mythicspoiler, Draftsim, MTGAZone). I rebuilt the archetype
chart from Wizards' own prerelease-guide text and preview coverage instead, so the ten archetype
names and themes below should match your image exactly. If your spreadsheet has card-by-card
ratings, paste them into the companion tool and they will override my priors.

**The single most valuable thing in this guide is not the card list — it's Sections 2 and 3.**
Card lists rot in a week. The mechanical math of `empower Jace` and `prepared` will still be
correct in six months, and it is what actually decides games.

---

## 1. The set in one page

| | |
|---|---|
| **Set** | Reality Fracture (**FRA**) |
| **Plane** | Echoverse Arcavios — a mirrored reality where Strixhaven is **Hexhaven** |
| **Size** | 290 cards: **71 commons, 109 uncommons, 64 rares, 26 mythics**, 10 basics [CONFIRMED] |
| **New mechanics** | **Empower Jace**, **Heartwood** tokens |
| **Returning** | **Prepared** (from Secrets of Strixhaven), **threshold**, flashback, surveil, scry, landfall |
| **Structure** | 5 allied pairs = Hexhaven **colleges**; 5 enemy pairs = the **Lorwyn Five** planeswalkers |
| **Booster quirk** | The **Echoed Pair** slot — 2 of 3 cards in that slot share a rarity and depict a mirrored pair |

### The structural fact most people will miss

**109 uncommons against 71 commons.** That ratio is lopsided, and the **Echoed Pair slot** pushes
even more uncommons into your packs than a normal Play Booster. [CONFIRMED]

Consequences [EVAL]:

1. **Power lives at uncommon, not rare.** Your deck's quality is decided by how many of the ~66
   Echoed Pair uncommons you convert, not by whether you opened a mythic.
2. **Commons are shallower than they look.** With only 71 commons across five colors, each color
   has roughly 14. You will wheel fewer playables than in a 101-common set — **do not plan to
   fill your 23 out of the back half of packs.**
3. **Signals are noisier.** A pack whose uncommons are all off-color tells you much less than it
   would in a commons-driven format. Read signals off **commons**, and specifically off the
   college prepared creatures (Section 3).

---

## 2. Empower Jace — the format's central math

> **Empower Jace N**: if you control a Jace planeswalker token, put N loyalty counters on it.
> If you don't, create a blue **Jace** planeswalker token with **0 loyalty**, then put N counters on it.
> The token's abilities: **−1: Surveil 1.** and **−3: Draw a card.** [CONFIRMED]

Read those two abilities again. **There is no plus ability.** This is the whole ballgame.

### 2.1 What a unit of loyalty is actually worth

Loyalty here is a **consumable resource**, not a growing engine. It is only refilled by drawing
more empower cards. So:

- **1 loyalty = surveil 1** (bin-or-keep the top card)
- **3 loyalty = draw a card**

Which means **surveil is the efficient rate and drawing is the luxury rate.** Three surveils cost
the same as one card. Unless you are flooding out or desperately need gas, **you should almost
always be spending −1 three times rather than −3 once.** [EVAL]

### 2.2 Converting "empower Jace N" into a card-evaluation number

Use this when a card has empower stapled on: [EVAL]

| Text on card | Rough value | How to price it |
|---|---|---|
| Empower Jace 1 | **≈ 0.15 cards** | A scry-ish effect on a stick. Nice, not a reason to pick. |
| Empower Jace 2 | **≈ 0.3 cards** | Real, still a tiebreaker. |
| Empower Jace 3 | **≈ 0.5–0.7 cards** | Meaningful. A full card if you'll live to spend it. |
| Empower Jace 3+ on a body that also affects board | **premium common** | This is what you're hunting. |

Multiply by **1.3 in UB Theorix and WU Fatehold**, where each surveil also feeds a payoff — you
get the selection *and* a trigger. Multiply by **0.7 in RW Ajani's Army and BR Stingerquill**,
where a deferred half-card is worse than a body that attacks now.

### 2.3 The Jace token is a permanent your opponent can attack

This is the least-discussed and most game-deciding detail. Your Jace is a **0-loyalty-ish
planeswalker sitting in front of your face**. That cuts both ways:

- **When you're the beatdown:** your opponent's Jace soaks nothing for them, but *your* Jace gives
  their team a target that isn't you. Attacking a Jace instead of a player is usually wrong for
  you — take the life total. [EVAL]
- **When you're defending:** your Jace is a **damage sponge**. Two loyalty you were going to spend
  on surveil can instead eat a 2-power attack. Sometimes correct, usually not — see below.
- **The real rule: use loyalty the turn you get it if you are under pressure.** Banked loyalty on
  a Jace that dies to an attack is loyalty you set on fire. Bank only when your board is stable.

### 2.4 Only one Jace, and that's good

Empower Jace **cannot create a second token** while you control one; extra empower cards stack
counters on the one you have. The tokens are **not legendary**. [CONFIRMED]

So **empower cards never anti-synergize with each other.** Redundancy is free. Draft them as
though they were all the same card and stack the loyalty. This makes a "count the empower cards"
heuristic reliable: **4+ empower cards in your 40 is a genuine card-advantage engine; 1–2 is
incidental upside.** [EVAL]

---

## 3. Prepared — why this format is grindy

> A **prepared** card has a creature face and a spell face. When the creature becomes prepared,
> a **copy of its spell is created in exile**, and you may cast that copy. Casting it **unprepares**
> the creature. The copy **vanishes if the creature leaves the battlefield or becomes unprepared**.
> A creature that is already prepared can't become prepared again. [CONFIRMED]

Different creatures become prepared differently: **some enter the battlefield prepared; some
become prepared at the beginning of your upkeep if they aren't already**; some have a condition
(one reported example becomes prepared at end step if three or more creatures died that turn).
[CONFIRMED]

### 3.1 The upkeep-repreparing creatures are engines

If a creature **re-prepares every upkeep**, then every copy you fail to cast before your next
upkeep is a copy you **wasted** — the re-prepare does nothing while it's already prepared.

> **Rule: with an upkeep-repreparer, spend the copy every turn cycle, even at break-even rates.**
> An unspent copy is not "saved for later," it is deleted. [EVAL]

This is the single most common play mistake this format will produce, and it is worth several
percent of win rate on its own.

### 3.2 The removal timing rule

Because the copy dies with the creature, **killing a prepared creature before it casts the copy
is a clean 2-for-1 in your favour.**

- **As the removal player:** hold instant-speed removal for **their upkeep** — after the
  re-prepare trigger they're tapped out of options, and you deny the spell. Against an
  enters-prepared creature, kill it **in response to nothing** — just kill it before they untap.
- **As the prepared player:** **cast the copy at the first reasonable window.** Do not hoard it
  to find a perfect line. Greed here loses you a card to a removal spell you could see coming.
- **Corollary:** sorcery-speed removal is worse than usual in FRA, and instant-speed removal is
  better than usual. Bump instants up roughly half a grade. [EVAL]

### 3.3 The five college spells (the signal-reading key)

At **common and uncommon**, every prepared creature in a college shares **the same prepared
spell**. This does not carry up to rares. [CONFIRMED]

| College | Colors | Shared prepared spell | Why it matters |
|---|---|---|---|
| **Fatehold** | W/U | **Create a 2/2 token and surveil** | Best spell half in the set — a body *and* a trigger |
| **Theorix** | U/B | **Self-mill** | No board impact; pure enabler for threshold |
| **Stingerquill** | B/R | **Damage to the opponent** | Reach, and turns on "damage dealt" payoffs |
| **Konstrari** | R/G | **Create a Heartwood token** | Ramp + artifact count |
| **Vigorbloom** | G/W | **Lifegain + +1/+1 counters** | Grows the board while stabilising |

**Use this to read the draft.** A late Fatehold prepared common means W/U is open. Because these
creatures are the backbone commons of five of the ten archetypes, they are the **most reliable
signal in the format** — far more reliable than a late gold uncommon. [EVAL]

### 3.4 Evaluating a prepared creature

`Value = body + (spell × how much your deck wants that spell)`

- **Floor:** the body alone. A prepared creature is never a dead card.
- **Baseline:** rate it **half a grade above** a vanilla creature of the same stats.
- **In-college:** rate it a **full grade above** — you get the spell *and* it feeds your payoffs.
- **Out-of-college:** the spell is often near-blank (self-mill in an aggro deck, lifegain in a
  burn deck). Rate the body only.

---

## 4. Heartwood and threshold — the two narrow mechanics

**Heartwood token** [CONFIRMED]: a **red and green artifact** token with `{T}: Add {R} or {G}`.
First predefined coloured artifact token.

[EVAL] A mana rock as a token is **card disadvantage that buys a turn**. In Limited that is only
worth it if you have something worth ramping *into*. Heartwood is doing three jobs at once:
ramp, artifact count (for Konstrari payoffs like **Aerid Konstrari**), and fixing for a splash.
The third job is quietly the best one — **Heartwood makes greedy splashes in R/G real.**

**Threshold** (seven or more cards in your graveyard) [CONFIRMED]: reachable around **turn 5–6
with Theorix self-mill**, around **turn 9+ without it**. That gap is enormous.

> **Rule: threshold cards are U/B cards, full stop.** Outside Theorix they are late-game-only
> and you should treat the threshold text as absent. The upside: everyone else cuts them, so
> they come around late for the deck that actually wants them. [EVAL]

---

## 5. Format speed and shape

**Call: medium-slow midrange. Games decided on turns 8–12.** [EVAL]

Evidence for grindy:
- Prepared generates 2-for-1s on ordinary creatures across five archetypes.
- Empower Jace is a card-advantage trickle available at **common**, in every game.
- A dedicated lifegain archetype (GW Vigorbloom) exists and is well-supported.
- A self-mill/graveyard value deck (UB Theorix) exists.
- 109 uncommons means higher average card quality — fewer free wins from curve alone.

Evidence for fast:
- Two explicitly aggressive pairs: **RW Ajani's Army** (counters aggro) and **BR Stingerquill**
  (face burn), plus **WU Fatehold** is described by coverage as *surveil aggro*.
- Wizards' own guidance notes aggressive pairs want more 1s and 2s.

**Resolution:** the aggro decks are real but they are the **minority position**, and they are
preying on a format whose default is value. That makes them **good when underdrafted and bad when
everyone tries them** — classic high-variance. The stable, always-fine decks are the grindy ones.

### What this means for your 40

| | Draft | Sealed |
|---|---|---|
| Creatures | 15–17 | 15–17 |
| Removal/interaction | **4+ (prioritise instants)** | 3+ (take what you have) |
| Lands | 17 | 17 (18 with Heartwood ramp + a 6-drop top end) |
| Curve peak | 3 | 3–4 (sealed is slower) |
| 2-drops | 5–6 (7+ if RW/BR) | 4–5 |
| Empower cards | 3–4 is an engine | any number, it's free value |

---

## 6. Colour strength

Scores are 0–10, **pre-release prior** [EVAL]. Every colour appears in exactly four archetypes, so
this is about raw card quality and how well the colour matches a grindy format — not archetype count.

| Rank | Colour | Score | The case |
|---|---|---|---|
| 1 | **Blue (U)** | **8.5** | The format's mechanics are blue. Empower Jace is a blue token; surveil, self-mill, and card selection are blue's. In a format decided on turn 10, the card-advantage colour is the best colour. Blue is in both of my top-two archetypes. |
| 2 | **Black (B)** | **8.0** | Black's common removal is the premium currency in a format where killing a prepared creature is a 2-for-1. Add graveyard payoffs (Theorix) and recursion (Liliana's Attrition) and black is grindy-format royalty. |
| 3 | **White (W)** | **7.5** | Token generation via the Fatehold prepared spell plus the counters-aggro shell. White's ceiling is high but its cards are more synergy-dependent — a pile of white commons with no direction is the worst pile in the set. |
| 4 | **Green (G)** | **7.0** | Big bodies are genuinely good when games go long, and Heartwood fixes splashes. Held back by green's usual weakness: its removal is combat-based, and fight effects are bad against a deck that gets value from creatures dying or being prepared. |
| 5 | **Red (R)** | **6.5** | The trap colour. Red's headline plan — point damage at the opponent's face — is the worst plan in a midrange format containing a lifegain archetype. Red's *creature removal* is fine; red's *reach* will be overdrafted. Expect red to be the most available colour by pack 3. |

> **The practical takeaway:** if you have no signal, **start blue-black and move out of it**, and
> **be the drafter who is happy to end up in red when it's flowing** — not the one who starts there.

---

## 7. The ten archetypes

Format: **Tier · Score · Plan · First-picks · Signal · Trap**.

Wizards' own one-line descriptions are quoted where confirmed; the analysis is mine.

### S-Tier

#### 1. U/B — Theorix, School of Esoteric Mathematics · "Graveyard Math" · **8.6**
> *"Mill yourself to reach threshold and have the graveyard as a source of strength you can count on."* [CONFIRMED]

**Plan.** Self-mill to threshold (7 cards) by turn 5–6, then deploy cards that are simply bigger
than what anyone else is casting.

**Why it's the best deck [EVAL]:** the two mechanics *stack*. The Theorix prepared spell is
self-mill, and empower Jace's efficient ability is **surveil**, which also mills. So every
empower card in your deck is simultaneously card selection **and** a threshold enabler. No other
archetype gets two mechanics pulling the same direction for free. On top of that, threshold cards
are near-unplayable for the other nine archetypes, so **your payoffs are cheap** — you can take
the enablers early and let the payoffs wheel.

**Named cards [CONFIRMED as FRA cards; rarity unverified]:** **Uldaros Theorix** (mythic Elder
Sphinx — exile up to one nonland card of each type from your graveyard, copy them, cast any
number with total mana value 6 or less), **Paradox Shaper** (signpost), **Theorix Metamage**,
**Void Extrapolator**, **Null Summoner**, **Cruel Calculations**, **Winter, Tormented Loner**,
**Gallia, Tragic Host**, **Theorist's Proxy** (empower Jace 3).

**Signal:** late Theorix prepared commons, and late threshold cards (these will *always* be late).
**Trap:** drafting payoffs without enablers. **Count your self-mill sources: you want 5+.** A
threshold deck that reaches threshold on turn 9 is just a bad Dimir deck.

---

#### 2. W/U — Fatehold, School of Future History · "Surveil Aggro" · **8.4**
> *"Use surveil and foresee the future of your library to build up threats and pressure your opponents."* [CONFIRMED]

**Plan.** Curve out with prepared creatures that each make a **2/2 token and surveil**, then
convert the scry/surveil triggers into a board that's ahead.

**Why it's this high [EVAL]:** Fatehold has **the best prepared spell in the set by a distance** —
it is the only one that adds a body *and* triggers the archetype's own payoffs. Most synergy decks
have enablers that do nothing and payoffs that need enablers; Fatehold's enablers **are** the
payoffs. That means the deck has almost no failure mode: even the "bad" draw is creatures and
tokens. Empower Jace's surveil also triggers your payoffs, so the format's free mechanic is a
bonus for you specifically.

**Named cards [CONFIRMED as FRA cards; rarity unverified]:** **Denzilore Fatehold** (mythic Elder
Sphinx — 4 mana 3/4 flash flying, *whenever you scry or surveil, put a +1/+1 counter on each
creature you control*), **Proctor of Potential**, **Surveillance Phantasm**, **Prudent Fateseer**,
**Semester Foreseer**, **Fatehold Chronologist**, **Fatehold Charm**, **Campus Crier**.

**Signal:** late Fatehold prepared creatures. **Trap:** the "aggro" label. This deck's tokens and
selection make it a **tempo-value** deck, not a burn-them-out deck. Don't cut your 4-drops to
chase a turn-6 kill that isn't there.

---

### A-Tier

#### 3. W/B — Liliana's Attrition · **7.8**
> *"Look to the graveyard for effects that allow you to continue deploying small creatures to the battlefield until you bury your enemies."* [CONFIRMED]

**Plan.** Cheap bodies, sacrifice outlets, recursion. Win by having the last card.

[EVAL] Two best colours, and the grindiest game plan in a grindy format = very strong floor.
Attrition decks are also the **best home for the format's removal**, since you're happy to trade
one-for-one all day when your cards come back. **Needs a sacrifice outlet or two** to convert
recursion into an actual engine — without one it's a pile of small creatures.
**Echoed Pair legends:** *Liliana the Repentant* / *Liliana the Faultless*. [CONFIRMED]

#### 4. B/G — Garruk's Bestiary · **7.5**
> *"Bring out fearsome creatures to hunt down your foes, combining deathtouch and trample to smash through any defenses!"* [CONFIRMED]

**Plan.** Value creatures, each with a benefit attached. Deathtouch + trample to break board stalls.

[EVAL] **The highest-floor deck in the format and the correct default when you open nothing.**
It asks for almost no synergy — good creatures are good creatures. Deathtouch is unusually well
positioned here: it profitably blocks the big Konstrari ramp payoffs and trades with prepared
creatures before they get value. Ceiling is capped because it has no engine; it just plays fair
Magic slightly better than you do. **Echoed Pair legends:** *Garruk, Curse Breaker* /
*Garruk, Veiled Butcher*. [CONFIRMED]

#### 5. G/W — Vigorbloom, School of Invasive Healing · "Life Gain" · **7.2**
> *"Grow your creatures in a variety of ways while boosting life to overwhelm the battlefield with harsh medicine."* [CONFIRMED]

**Plan.** +1/+1 counters and lifegain on the same cards; go bigger than the aggro decks and
outlast them.

[EVAL] The Vigorbloom prepared spell gives **lifegain *and* counters**, which is the second-best
spell half in the set. This deck is **the direct predator of BR Stingerquill and RW Ajani's Army**
— if those two are popular at your table, Vigorbloom's stock rises sharply. Its weakness is the
mirror against UB/WB: lifegain does nothing against a deck that wins with card advantage, and
Vigorbloom has no way to close a long game quickly.

**Named cards:** **Kwia Vigorbloom** (mythic Elder Sphinx — makes **Lotus** tokens: colourless
artifacts that tap-and-sacrifice for three mana of one colour), **Vigorbloom Vanguard**
(signpost), **Graft Surgeon** (keeps counters around after creatures die), **Bloombrute** (draws
on lifegain), **Greenhouse Propagator**, **Surgical Precision**, **Titanbones**, **Towering Heart**.

---

### B-Tier

#### 6. R/W — Ajani's Army · **6.9**
> *"Strengthen your creatures with +1/+1 counters to go aggro with reckless abandon!"* [CONFIRMED]

**Plan.** Curve 1–4 with counters on everything, token creatures for two-bodies-per-card, and
equipment. Speed is the win condition.

[EVAL] Real, but **the highest-variance deck in the set**. It preys on stumbling ramp draws and
loses badly to Vigorbloom lifegain and to any deck that 2-for-1s it with prepared creatures. The
deck needs a **near-perfect curve and 7+ two-drops** — a Vigorbloom deck can afford a clunky card,
this one cannot. Only take this lane when it is clearly open early.
**Echoed Pair legends:** *Ajani Resolute* / *Ajani Unrelenting*. [CONFIRMED]

#### 7. U/R — Chandra's Prowess · **6.7**
> *"Cast noncreature spells to trigger abilities and keep up the heat on your opponents."* [CONFIRMED]

**Plan.** Prowess bodies + a high noncreature count, with Thopters as a token sub-theme.
**Key card:** *Saheeli, Jewel of Avishkar*. **Echoed Pair legends:** Chandra goes from red
*Chandra, Torch of Defiance* to mono-blue *Chandra, Chill of Compliance*. [CONFIRMED]

[EVAL] Prowess wants ~10 noncreature spells; a grindy format wants creature quality. That tension
caps the deck. It's excellent when the spells you find are **removal** (so your spell count and
your interaction count are the same cards) and mediocre when they're cantrips. **Also note:**
`Stingcaster Mage` — a reported two-mana red haste creature that **gives an instant or sorcery
flashback as it enters** — is effectively a red Snapcaster and is a genuine build-around for this
lane. [WATCH — rarity unverified]

#### 8. G/U — Jace's Mastery · **6.5**
> *"Keep empowering Jace to provide a steady flow of cards or pick your path to victory with cards that grant your planeswalkers abilities!"* [CONFIRMED]

**Plan.** Feed the Jace token, then convert loyalty into wins with cards that grant your
planeswalkers extra abilities. **Key card:** *Kiora of Salt and Sand*. [CONFIRMED]

[EVAL] **The set's most seductive trap, and I want to be blunt about why.** The base Jace token
has **no plus ability**. A value engine that only ticks *down* is not an engine — it's a battery.
Building your deck around it means building around a permanent that (a) shrinks every time you
use it and (b) can be attacked by a 2/2. The archetype is only good if the
"grant your planeswalkers abilities" cards are **genuinely powerful and you get two or more** —
they're what turn the battery into an engine. Without them you have a green-blue goodstuff deck
paying a tax. **[WATCH]** — this is the archetype most likely to move a full tier once real data
exists, in either direction.

---

### C-Tier

#### 9. B/R — Stingerquill, School of Painful Words · "Face Burn" · **6.2**
> *"Add insult to injury by using cards that deal damage directly to your opponent, which in turn lets you strengthen your cards and press the attack."* [CONFIRMED]

**Plan.** Cheap attackers and pingers that enable each other; damage to the face turns on payoffs.

**Named cards:** **Ingris Stingerquill** (mythic Elder Sphinx — *whenever your creatures attack,
each of them deals 1 damage to each opponent*), **Stingerquill Voxmancer** (signpost),
**Hallway Heckler**, **Whiplash Wordsmith**, **Grim Repriser**, **Master of Barbs**. [CONFIRMED as FRA cards]

[EVAL] **I have this as the most likely archetype to underperform its hype.** The core tension:
every burn spell you point at a face is a burn spell you did not point at a creature, in a format
where **killing a prepared creature is a 2-for-1**. You are paying a real cost for your payoffs.
It also runs directly into GW Vigorbloom, whose whole deck is lifegain. Stingerquill is good only
when you are **genuinely the fastest deck at the table** and have **Ingris or Master of Barbs** to
convert chip damage into a real clock. Coverage itself notes the archetype is light on explicit
payoffs beyond Master of Barbs — that's a warning sign, not a nitpick.

#### 10. R/G — Konstrari, School of Constructive Arts · "Mana Ramp" · **6.0** *(draft)* / **7.3** *(sealed)*
> *"Create Heartwood tokens to get tons of mana and show your opponent the art of building big!"* [CONFIRMED]

**Plan.** Heartwood tokens ramp you; artifact count and big spells pay you off.

**Named cards:** **Aerid Konstrari** (mythic Elder Sphinx — `{1}{R}{G}{G}` 5/4 flying, makes a
Heartwood on ETB *and* on death; `{6}`: make a Heartwood and get +X/+0 where X is your artifact
count), **Woodwork Prodigy** (signpost). [CONFIRMED]

[EVAL] **This is the archetype with the biggest format-to-format split, and it's the most useful
single insight in this guide for you specifically, because you're playing both draft and sealed.**

- **In draft it's the worst deck.** Ramp is card disadvantage. You spend picks on Heartwood
  enablers, and then the top end you needed to justify them isn't in your pool, because eight
  other drafters took the bombs. You lose to RW and BR before you untap with six mana.
- **In sealed it's a top-three deck.** Sealed pools contain **more expensive bombs than you can
  normally cast**, and sealed games are slower, so the aggro punish barely exists. Heartwood turns
  your uncastable 6- and 7-drops into your win conditions and fixes a third-colour splash for the
  best rare in your pool. **In sealed, go up to 18 lands and jam the top end.**

---

## 8. Archetype strength chart

**Draft** (0–10, pre-release prior [EVAL]):

```
UB Theorix        8.6  ████████████████████████████████████▏  S
WU Fatehold       8.4  ███████████████████████████████████▏   S
WB Liliana        7.8  ████████████████████████████████▌      A
BG Garruk         7.5  ███████████████████████████████▏       A
GW Vigorbloom     7.2  ██████████████████████████████         A
RW Ajani          6.9  ████████████████████████████▋          B
UR Chandra        6.7  ███████████████████████████▉           B
GU Jace           6.5  ███████████████████████████            B
BR Stingerquill   6.2  █████████████████████████▊             C
RG Konstrari      6.0  █████████████████████████              C
```

**Sealed** — the order changes meaningfully. Sealed is slower, pools are deeper in expensive
cards, and consistency matters less than raw power:

```
RG Konstrari      7.3  ███████████████████████████████    ▲▲▲▲  (+4 places)
BG Garruk         7.6  ███████████████████████████████▋   ▲▲
UB Theorix        7.9  █████████████████████████████████  ▼ (fewer enablers per pool)
GW Vigorbloom     7.6  ███████████████████████████████▋   ▲
WU Fatehold       7.8  ████████████████████████████████▋  ▬
WB Liliana        7.4  ██████████████████████████████▊    ▼
UR Chandra        6.4  ██████████████████████████▋        ▼
GU Jace           6.3  ██████████████████████████▎        ▬
RW Ajani          5.9  ████████████████████████▋          ▼▼▼ (can't assemble the curve)
BR Stingerquill   5.7  ███████████████████████▊           ▼▼
```

**Why the shuffle:** sealed punishes decks that need **density** (RW's curve, Theorix's 5+ self-mill
enablers) and rewards decks that need **one good card plus mana** (Konstrari, Garruk). In sealed,
build the deck your **bombs** are in, then use Heartwood/lands to make it castable.

---

## 9. Card priority

### 9.1 The FRA pick-order rubric [EVAL]

When you don't know a card, score it. This rubric is built from the mechanics above and will hold
up better than a memorised list.

| Tier | What it is | Take it over |
|---|---|---|
| **1. Bombs** | Wins the game alone, uninteractive. The five **Elder Sphinxes** are all here. | Everything |
| **2. Premium removal, instant-speed, ≤3 mana, unconditional** | Answers a prepared creature **before the copy is cast** — a 2-for-1 in your favour | Any creature |
| **3. In-college prepared creature with a good body** | Two cards on one card, feeding your own payoffs | Good vanilla creatures |
| **4. Removal, sorcery-speed or conditional** | Still essential. 4+ interaction in every deck. | Filler creatures |
| **5. Empower Jace 3 on a relevant body** | ~half a card of pure profit | Vanilla creatures |
| **6. Evasive 2–4 drops** | Grindy format = board stalls = flyers win | Ground creatures of same size |
| **7. Out-of-college prepared creature** | Rate the body only; the spell half is near-blank | Vanilla of the same stats |
| **8. Empower Jace 1–2, incidental value** | Tiebreaker only | Nothing — this *is* the tiebreaker |
| **9. Threshold cards (outside UB)** | Treat the threshold text as absent | Nothing |
| **10. Face-damage payoffs (outside a truly fast BR)** | The format's biggest trap | Nothing |

### 9.2 Top rares & mythics [CONFIRMED as FRA cards, EVAL on Limited value]

The five **Elder Sphinxes** are the set's mythic legendary cycle, one per college, and every one
of them is a Limited bomb that also **tells you what its college wants**:

| Card | Colors | What it does | Limited take |
|---|---|---|---|
| **Denzilore Fatehold** | W/U | 4 mana **3/4 flash flying**; whenever you scry or surveil, **+1/+1 counter on each creature you control** | **The best of the five for Limited.** A 4-mana flash flyer is already a fine card; the trigger is repeatable and fires off the free Jace surveils. First-pick. |
| **Aerid Konstrari** | R/G | `{1}{R}{G}{G}` **5/4 flying**; Heartwood on ETB **and** on death; `{6}`: Heartwood + `+X/+0` for artifacts | A 4-mana 5/4 flier that replaces itself twice. Enormous rate, plus a mana sink. |
| **Ingris Stingerquill** | B/R | Whenever your creatures attack, **each deals 1 damage to each opponent** | Converts a wide board into a hard clock. The card that makes Stingerquill playable. |
| **Uldaros Theorix** | U/B | Exile up to one nonland card of **each type** from your graveyard, copy them, cast any number with total MV ≤ 6 | Game-ending in a deck with a full graveyard. Needs threshold-level setup to be a bomb rather than good. |
| **Kwia Vigorbloom** | G/W | Creates **Lotus** tokens (tap & sac for three mana of one colour) | The weakest of the five in Limited — ritual mana is worst in the slowest deck. Still a mythic body. |

**Other high-profile cards flagged in coverage** [WATCH — mostly Constructed/Commander framing,
verify Limited relevance]: **Overwrite the Multiverse** (a board wipe that cantrips when it clears
multiple threats — if this is a rare, it is a top-5 Limited card and a **sealed sleeper**),
**Hexing Squelcher**, **Karn, Argent Defender**, **Samut**, **Vivi Ornitier**, **Marwyn, the
Preserver**, **Hall of Echoes**, **Loyal Tutor**, **Saheeli, Jewel of Avishkar** (UR signpost),
**Kiora of Salt and Sand** (GU signpost), and the **Echoed Pair planeswalkers** — *Ajani Resolute /
Ajani Unrelenting*, *Liliana the Repentant / Liliana the Faultless*, *Garruk, Curse Breaker /
Garruk, Veiled Butcher*, *Chandra, Torch of Defiance / Chandra, Chill of Compliance*.

> **Planeswalker note:** FRA has **more planeswalkers than any premier set since War of the Spark**
> [CONFIRMED]. In Limited that means two things: an unanswered walker ends games, and **your
> removal should be able to point at a planeswalker.** Value burn spells and evasive creatures
> slightly higher than usual for this reason. [EVAL]

### 9.3 Top commons — honest status

**I could not retrieve a verified common-by-common rating list.** Every card database and review
site is blocked from this machine, and no public 17Lands data exists for an unreleased set. Rather
than invent a ranked list of commons with fake ratings — which would actively mislead you in a
draft — here is what is solid:

**Commons confirmed to exist in FRA** (rarity mostly unverified; grouped by lane):

- **Fatehold / W-U:** Prudent Fateseer, Semester Foreseer, Fatehold Chronologist, Fatehold Charm,
  Campus Crier, Proctor of Potential, Surveillance Phantasm
- **Theorix / U-B:** Paradox Shaper, Theorix Metamage, Theorist's Proxy, Void Extrapolator,
  Null Summoner, Cruel Calculations
- **Stingerquill / B-R:** Stingerquill Voxmancer, Hallway Heckler, Whiplash Wordsmith,
  Grim Repriser, Master of Barbs, Stingcaster Mage
- **Konstrari / R-G:** Woodwork Prodigy
- **Vigorbloom / G-W:** Vigorbloom Vanguard, Graft Surgeon, Bloombrute, Greenhouse Propagator,
  Surgical Precision, Titanbones, Towering Heart
- **Other:** Way of the Healer (empower Jace)

**The best commons in the set will almost certainly be, in this order** [EVAL]:

1. **Unconditional instant-speed removal at ≤3 mana** — in any colour, but expect black and red.
2. **The Fatehold prepared commons** (Prudent Fateseer, Semester Foreseer, Fatehold Chronologist).
   A body + a 2/2 + a surveil at common is a broken rate, and there are at least three of them.
3. **The Vigorbloom prepared commons** (Vigorbloom Vanguard and friends) — counters + life on a body.
4. **Any common with empower Jace 3** (Theorist's Proxy is the confirmed example).
5. **Common flyers in the 2–4 slot** — this format stalls.

Verify against the real list at prerelease and overwrite these in the companion tool.

---

## 10. Draft plan (Arena)

**P1P1–P1P3.** Take the most powerful card, near-colour-blind. Sphinxes and premium removal only.
Do not commit.

**P1P4–P1P8.** Start counting **college prepared commons**. They're the backbone commons of five
archetypes, so lateness is a clean signal. Two late Fatehold creatures = W/U is open.

**P1P9–P2P5.** Commit to a pair. Remember: **only ~14 commons per colour** — you cannot fill a
deck from the back half of packs. Take playables over speculation earlier than you're used to.

**P2P6–P3.** Fill the curve and hit **4+ interaction**. Prefer instants. Count your empower cards
(4+ = engine) and, if you're Theorix, your self-mill sources (5+ = functional).

**The default lane when lost:** **B/G Garruk's Bestiary.** It needs the least synergy and has the
highest floor. **The lane to avoid unless it's screaming:** **B/R Stingerquill.**

---

## 11. Sealed plan (Arena)

1. **Find your bombs first.** Sealed is won by the best card that resolves. Sphinxes, walkers,
   **Overwrite the Multiverse**.
2. **Build the deck your bombs are in**, not the deck with the best synergy. Sealed pools rarely
   have archetype density.
3. **Count removal across all five colours** before choosing. Removal is scarcer per-pool than
   creatures, so it should drive colour choice more than playable count.
4. **Consider Heartwood as fixing, not ramp.** If R/G is close, Heartwood lets you splash the best
   card in your pool. **Go to 18 lands** if you're ramping to a real top end.
5. **Be slower than you think.** Sealed games in FRA will go long. A 6-drop that wins the game is
   better than a 2-drop that doesn't. Cut the aggro plan unless the pool hands it to you.
6. **Bring instant-speed removal in from the sideboard** against decks showing prepared creatures.

---

## 12. Play-pattern checklist

Print this next to your monitor.

- [ ] **Spend the prepared copy this turn cycle** if the creature re-prepares at upkeep. An unspent copy is deleted.
- [ ] **Hold instant removal for their upkeep** to deny a prepared spell entirely.
- [ ] **Kill prepared creatures before they cast the copy** — that's the 2-for-1.
- [ ] **Spend Jace loyalty now if you're under pressure**; bank only when stable.
- [ ] **Use −1 surveil three times before −3 draw.** Surveil is the efficient rate.
- [ ] **Don't attack their Jace** unless it's actively winning them the game. Take the life total.
- [ ] **Count your graveyard before casting a threshold card.** Seven.
- [ ] **Heartwood is also fixing.** Check whether it enables a splash before you treat it as ramp.
- [ ] **Your removal can point at planeswalkers.** This set has a lot of them.

---

## 13. What to verify at prerelease

The three things most likely to move this guide [WATCH]:

1. **How good are the "grant your planeswalkers abilities" cards in G/U Jace's Mastery?** If
   there are two playable ones at common/uncommon, GU moves from B to A. If not, it drops to C.
2. **Is there a premium common that gains a lot of life in G/W?** If Vigorbloom can gain 6+ per
   card, B/R Stingerquill drops out of the format entirely.
3. **What rarity is Overwrite the Multiverse?** A cantripping wipe at rare reshapes sealed.

Once Arena queues open **Sept 29**, replace every [EVAL] number with 17Lands **GIH WR** — trust
data over this document the moment data exists.

---

## Sources

- [Reality Fracture Mechanics — Wizards of the Coast](https://magic.wizards.com/en/news/feature/reality-fracture-mechanics)
- [Reality Fracture Prerelease Guide — Wizards of the Coast](https://magic.wizards.com/en/news/feature/reality-fracture-prerelease-guide)
- [Reality Fracture Release Notes — Wizards of the Coast](https://magic.wizards.com/en/news/feature/reality-fracture-release-notes)
- [Enter the Echoverse with Reality Fracture Design — Wizards of the Coast](https://magic.wizards.com/en/news/feature/enter-the-echoverse-with-reality-fracture-design)
- [Exploring All 10 Reality Fracture Limited Archetypes — Draftsim](https://draftsim.com/mtg-fra-draft-archetypes/)
- [Reality Fracture Cards, Mechanics, and Set Information — Draftsim](https://draftsim.com/mtg-reality-fracture/)
- [Empower Jace in MTG: Rules, History, and Best Cards — Draftsim](https://draftsim.com/mtg-empower-jace/)
- [Fan Favorite Mechanic Sees Fundamental Change in Reality Fracture — Draftsim](https://draftsim.com/mtg-fra-prepared-change/)
- [Reality Fracture — MTG Wiki](https://mtg.wiki/page/Reality_Fracture)
- [Empower Jace — MTG Wiki](https://mtg.wiki/page/Empower_Jace)
- [Reality Fracture (FRA) Limited Set Review: White — MTG Arena Zone](https://mtgazone.com/reality-fracture-fra-limited-set-review-white/)
- [The Five Colleges of Hexhaven in MTG, Explained — TheGamer](https://www.thegamer.com/magic-the-gathering-the-five-hexhaven-colleges-explained/)
- [New MTG Reality Fracture mechanic means Jace shows up in basically every game — Wargamer](https://www.wargamer.com/magic-the-gathering/reality-fracture-empower-jace)
- [Reality Fracture Limited Archetypes — Reality Fracture Wiki](https://realityfracture.wiki/tier-list/limited-archetypes/)
- [Reality Fracture Play Booster Fact Sheet — MTG Scribe](https://mtgscribe.com/2026/09/08/reality-fracture-play-booster-fact-sheet/)
- [Reality Fracture Unveils Hexhaven Elder Sphinxes — GameDaily](https://gamedaily.com/games/mtg-reality-fracture-elder-sphinxes)
- [Every MTG Reality Fracture Echoed Pair — Thornberry Media](https://www.thornberrymedia.com/post/reality-fracture-echoed-pairs)
