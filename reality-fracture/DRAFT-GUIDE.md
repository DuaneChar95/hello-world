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

## 0.5 Corrections from the real card list  [CONFIRMED 2026-09-20]

The full set data is now in hand (285 cards: 5 basics, 81 commons, 109 uncommons,
64 rares, 26 mythics — the "71 commons" figure quoted below counts common *spells*,
with 10 more at common being lands). **49 of the 51 card names I researched were
real.** Here is everything the real data corrected, because several of these change
the advice:

| Card | I said | Actually | Why it matters |
|---|---|---|---|
| **Titanbones, Towering Heart** | two separate cards | **one card**, `{3}{G}` uncommon | I split one name in half. There is no card called "Towering Heart". |
| **Master of Barbs** | B/R uncommon | **mono-R rare** | I called this "the payoff that makes Stingerquill work". At rare you usually won't have it — this makes **B/R worse, not better**, and reinforces the C-tier call. |
| **Stingcaster Mage** | uncommon | **mythic** | Not a build-around you can plan on. It's a bomb you occasionally open. |
| **Overwrite the Multiverse** | "if it's a rare…" | **mythic** | I flagged its rarity as a key unknown. Answered — and being mythic, it reshapes sealed far less than I speculated. |
| **Proctor of Potential** | W common | **W/U rare** | W/U's scry/surveil payoff is rarer than implied. |
| **Null Summoner** | B common | **U/B rare** | Same for Theorix's threshold payoff. |
| **Cruel Calculations** | B common | **mono-U rare** | |
| **Void Extrapolator** | uncommon | **common**, and it's a *prepared* Theorix card (`Void Extrapolator // Omit Variables`) | Good news for U/B: the enabler is at common. |
| **Prudent Fateseer** | common | **uncommon** | |
| **The Echoed Pair planeswalkers** | gold rares in the enemy pair | **two mono-coloured cards, one in each colour** — and not all of them planeswalkers. *Ajani Resolute* (W) / *Ajani Unrelenting* (R), *Chandra, Chill of Compliance* (U) / *Chandra, Torch of Defiance* (R) and *Garruk, Veiled Butcher* (B) / *Garruk, Curse Breaker* (G) are mythic planeswalkers. *Liliana the Faultless* (W) / *Liliana the Repentant* (B) are **rare legendary creatures** — Liliana is the one who lost her spark. **Jace has no green half at all**: his echo is the Jace *token*, and G/U is built around it. | I had this structurally wrong twice: first as gold cards, then as "five pairs of mythics." §7 now names each pair and what it does. |

### What the real data confirmed

- **Every college shares one prepared spell, by name.** `Semester Foreseer // Peer
  Review` and `Prudent Fateseer // Peer Review` (Fatehold); `Theorix Metamage //
  Omit Variables` and `Void Extrapolator // Omit Variables` (Theorix);
  `Stingerquill Voxmancer // Vicious Verse` and `Whiplash Wordsmith // Vicious
  Verse` (Stingerquill); `Woodwork Prodigy // Soul Tether` (Konstrari);
  `Vigorbloom Vanguard // Seed Suture` (Vigorbloom).
- **The Annexes are commons.** *Fatehold Annex*, *Theorix Annex*, *Stingerquill
  Annex*, *Konstrari Annex*, *Vigorbloom Annex* — all common lands. **But they are only half
  the cycle** — there are five more common duals covering the enemy pairs, which I missed on
  the first pass and which broke Section 4.5. See §0.8 and the corrected §4.5.
- **Rarity distribution** matches exactly: 109 uncommons against 71 common spells.

### One thing that changes Section 4.5

**Many of the college cards are hybrid**, not gold: `Theorix Metamage {2}{U/B}`,
`Stingerquill Voxmancer {B/R}`, `Vigorbloom Vanguard {1}{G/W}`, `Woodwork Prodigy
{2}{R/G}`. A hybrid card is castable with **either** colour, so it behaves like a
mono-coloured card for mana purposes and slides into a splash far more easily than a
true gold card. Two consequences [EVAL]:

1. **Hybrid college cards are not a splash problem at all** — if you're in one of
   the two colours, you can cast it.
2. **They are a weaker signal than I claimed.** A late Fatehold hybrid card doesn't
   prove W/U is open; a mono-W or mono-U drafter could also want it. Weight the
   *mono-coloured* college cards more heavily when reading signals.

---

## 0.6 Deck shells, and two rankings the card data changed  [CONFIRMED card data, EVAL analysis]

With all 285 cards in hand I counted what each colour actually offers. Two of my
earlier calls were wrong, and both were wrong for the same reason: I reasoned
from archetype design instead of from how many playable cards exist.

> **This section has since been superseded in one respect.** The removal counts below were made
> before I had oracle text for every card, and they undercount white and green — *Memory Trap*
> and *Compel Brutality* are both removal and both are commons. The counts and colour scores in
> **§0.8 and §6 are the current ones**; what follows is kept because the *reasoning* (count the
> cards, don't reason from archetype design) is the part worth keeping, and because it shows the
> direction the numbers moved.

### The counts that matter

**Removal, by colour** (every card that kills a creature, all rarities):

| Colour | Removal | At common | The commons |
|---|---|---|---|
| **Black** | **12** | **3** | Last Gasp `{1}{B}` instant · Silence the Echo `{1}{B}` · Extended Absence `{3}{B}` instant |
| **Red** | 8 | 2 | Wrath of the Bloodmane `{2}{R}` instant · Awaken the Inferno `{4}{R}` |
| White | 6 | 1 | Surgical Precision `{1}{W}` |
| Green | 4 | 1 | Sureshot Sower `{1}{G}` (a 2-mana flier with removal attached) |
| **Blue** | **3** | **1** | Icy Reception `{1}{U}` |

**Commons per colour: 11 mono, plus ~4 hybrid shared with a neighbour.** A
two-colour deck draws on roughly 24 distinct commons. That is thin, and it is
why taking playables early beats speculating.

**Empower Jace: 35 cards.** Blue 9, black 7, white 6, green 4, red 4, plus a
G/U pair. Common empower-3 exists in blue (Mindseeker Oculus, Protege's
Awakening) and G/U (Tam's Resistance).

### Correction 1 — black is the best colour, not blue

I had **U 8.5 > B 8.0**. That was wrong. **Black has twelve removal spells and
three at common; blue has three and one.** In a format whose central tension is
killing a prepared creature before it casts its copy, a colour that cannot
interact is not the best colour no matter how many cards it draws. Blue's
empower count is real, but a blue deck holding Icy Reception and hoping is
losing the 2-for-1 war it is trying to win.

### Correction 2 — red is better than I said, for the opposite reason to the one I gave

I had red last at 6.5, on the grounds that its plan points damage at faces.
That plan is still a trap — but red's actual **removal suite is second-best in
the set**, and `Wrath of the Bloodmane` at common is a premium card. Red is fine;
*Stingerquill* is the problem. Those are different claims and I conflated them.

**Revised colour ranking** [EVAL, from confirmed counts] — *superseded by §6; White is now 7.9
and Green 6.9 on the recounted removal:*

| | Colour | Was | Now | Why |
|---|---|---|---|---|
| 1 | **Black** | 8.0 | **8.6** | 12 removal, 3 at common, plus the graveyard payoffs |
| 2 | Blue | 8.5 | **8.2** | Most empower and selection — but 3 removal total |
| 3 | White | 7.5 | **7.5** | Unchanged: counters, flyers, lifegain, 6 removal |
| 4 | **Red** | 6.5 | **7.2** | Second-best removal. The face plan is the trap, not the colour |
| 5 | Green | 7.0 | **6.6** | 4 removal, fewest rares, and its removal is a creature |

### Correction 3 — G/U Jace's Mastery has its payoffs after all

I flagged this as the archetype most likely to move a tier, because I couldn't
tell whether the "grant your planeswalkers abilities" cards existed. **They do:
a ten-card uncommon cycle of legendary enchantments — `Way of the Mind Sculptor`,
`Way of the Paradox`, `Way of the Pyromancer`, `Way of the Warlord`,
`Way of the Wildspeaker`, and five more — two per colour.** Each one empowers Jace on entry
(2, 5 or 7) *and* permanently changes what your planeswalkers can do — `Way of the Deathbringer`
gives every planeswalker you control "−2: sacrifice a creature, create a 4/4 trample Beast";
`Way of the Warlord` gives them a −4 that deals damage. They are how a 0-loyalty Jace token
becomes a threat. That is real support. **G/U moves from B to A- (6.5 → 7.1)**, and §0.8
confirms it: both sealed builders independently ran two Ways in their G/U decks.

---

## 0.7 The shell for each deck

A shell is the 23 nonland slots broken into roles. Land counts are 17 unless noted.

Each one now carries a **Spine** — the cards **both** builders independently played in that pair,
from the 20 registered sealed decks in §0.8. That is the closest thing to evidence this guide
has: nobody's opinion, two people arriving at the same card from different pools. Where they
disagreed I've left the card out rather than pick a side.

Read the rest as: **Engine** (how many you need before the deck works) · **Interaction** (what the
pool actually gave, not a target) · **Curve** (revised down from §0.8 — these decks are cheaper
than I first wrote) · **Fails when**.

> **One standing caveat.** These are *sealed* builds. Sealed pools are shallower and slower than
> draft decks, so a low removal count may mean "the pool had none," not "the deck doesn't want
> any." Agreement between the two builders is evidence; a single low number is not.

### U/B Theorix — Graveyard Math · 23 spells, 17 land

- **Signposts:** `Uldaros Theorix` (M, {3}{U}{B}{B}) · `Paradox Shaper` (U, {1}{U/B}) · `Theorix Charm` (U, {U}{B}) — The college's Elder Sphinx, its uncommon prepared creature and its charm.
- **Enablers to look for:** `Theorix Metamage` (C, {2}{U/B}) · `Paradox Shaper` (U, {1}{U/B}) · `Void Extrapolator` (C, {1}{B}) · `Theorix Charm` (U, {U}{B}) · `Liliana the Repentant` (R, {1}{B}) · `Mindseeker Oculus` (C, {2}{U}) · `Protege's Awakening` (C, {3}{U}). Anything that puts your own cards in the graveyard: the Theorix prepared spell is self-mill, every Jace surveil is a mill, and Liliana the Repentant mills two per body. **Count these first — you want five or more.**
- **Payoffs to look for:** `Uldaros Theorix` (M, {3}{U}{B}{B}) · `Void Extrapolator` (C, {1}{B}) · `Null Summoner` (R, {2}{U}{B}) · `Loot, the Anomaly` (U, {2}{B}) · `Winter, Tormented Loner` (U, {2}{B}) · `Gallia, Tragic Host` (U, {1}{B}) · `Eye of Jace` (U, {1}) · `Tarmogoyf` (M, {1}{G}). Threshold cards and graveyard recursion. Nobody else can use them, so they wheel — **take enablers over payoffs until you have five**, then the payoffs will still be there.
- **Spine (both builders):** `Theorix Charm` (U) · `Paradox Shaper` (U) · `Last Gasp` (C) · `Void Extrapolator` (C) · `Theorix Metamage` (C) · `Arni, Humble Scribe` (U) · `Extended Absence` (C) · `Recursive Recruitment` (U) · `Undulating Witness` (C) · `Twinned Vision` (C)
- **Take over anything comparable:** `Theorix Metamage` — flier, self-mill, threshold *and* prepared, four cards in one. `Uldaros Theorix` (M) if you open it.
- **Engine:** **5+ self-mill sources.** The Theorix prepared spell (*Omit Variables*) is self-mill, so each prepared creature counts. Only 3 prepared cards exist in-college, so the Jace surveils make up the difference — **4+ empower cards**, easy in blue.
- **Threshold payoffs:** `Null Summoner` (R), `Loot, the Anomaly` (U), `Void Extrapolator`. These wheel; nobody else can use them.
- **Interaction:** the builders had **4 and 5** — the highest of the ten pairs, and the one case where my shell number (5) was right. Black delivers.
- **Curve:** 1:1 · 2:10 · 3:5 · 4:4 · 5:2 · 6:1
- **Fails when:** you have the threshold payoffs and not the mill. Count enablers before taking a third payoff.

### W/U Fatehold — Surveil Tempo · 23 spells, 17 land

- **Signposts:** `Denzilore Fatehold` (M, {1}{W}{U}{U}) · `Prudent Fateseer` (U, {1}{W/U}{W/U}) · `Fatehold Charm` (U, {W}{U}) — The college's Elder Sphinx, its uncommon prepared creature and its charm.
- **Enablers to look for:** `Fatehold Chronologist` (C, {1}{W/U}) · `Prudent Fateseer` (U, {1}{W/U}{W/U}) · `Semester Foreseer` (C, {3}{U}) · `Campus Crier` (C, {1}{W}) · `Mindseeker Oculus` (C, {2}{U}) · `Academic Ascent` (C, {1}{W}) · `Fatehold Charm` (U, {W}{U}). Scry and surveil sources. The Fatehold prepared spell makes a 2/2 *and* surveils, and every empower card is a surveil waiting to happen — so the enablers here are also bodies.
- **Payoffs to look for:** `Denzilore Fatehold` (M, {1}{W}{U}{U}) · `Surveillance Phantasm` (C, {1}{U}) · `Diviner of Victory` (R, {U}) · `Prudent Fateseer` (U, {1}{W/U}{W/U}) · `Enlightened Confidant` (M, {1}{W}) · `Proctor of Potential` (R, {W}{U}). Cards that trigger whenever you scry or surveil. Two or three is enough; the enablers are already strong on their own, which is why this deck is S-tier.
- **Spine (both builders, 14 of 23 — the strongest agreement in the sample):** `Prudent Fateseer` (U) · `Fatehold Chronologist` (C) · `Semester Foreseer` (C) · `Desperate Futurescribe` (U) · `Saheeli, Consul of Oversight` (U) · `Surveillance Phantasm` (C) · `Proft, Consulting Detective` (U) · `Surgical Precision` (C) · `Fatehold Charm` (U) · `Campus Crier` (C) · `Mindseeker Oculus` (C) · `Yuriko, Hope from the Shadows` (U) · `Memory Trap` (C) · `Hexhaven Battalion` (C)
- **Engine:** the prepared spell (*Peer Review*) makes a 2/2 **and** surveils, so your enablers are your payoffs. `Denzilore Fatehold` (M) is the best of the five sphinxes.
- **Interaction:** **corrected** — I said "W+U is 4 removal total, 2 at common." It is **10 total, 3 at common**: `Memory Trap`, `Surgical Precision`, `Infinite Coursework`. *Memory Trap is an Oblivion Ring at common* and both builders played it. W/U is not the removal-starved pair I described. It is still last-but-one; that's U's fault, not W's.
- **Curve:** 1:2 · 2:9 · 3:6 · 4:4 · 5:1 · 6:1
- **Fails when:** you treat it as aggro. It is a tempo-value deck — fliers, tokens, selection.

### W/B Liliana's Attrition — Sacrifice & Recursion · 23 spells, 17 land

- **Signposts — the Liliana pair:** `Liliana the Faultless` (W, `{W}` 1/1 rare) and `Liliana the Repentant` (B, `{1}{B}` 2/2 rare). **Both are legendary creatures, not planeswalkers** — Liliana is the one of the five who lost her spark, and her halves are a one-drop and a two-drop, which is exactly why this deck is cheap bodies plus recursion. *Repentant* is the engine: every other creature or planeswalker you play mills two (recursion targets, threshold fuel), and her exhaust ability reanimates one of them. *Faultless* gains a life per body and hands out hexproof. Take either over any common.
- **Enablers to look for:** `Blessed Ghoul` (C, {W/B}) · `Rank Rat` (C, {1}{B}) · `Theoretical Necromancer` (C, {2}{B}) · `Silence the Echo` (C, {1}{B}) · `Winter, Tormented Loner` (U, {2}{B}) · `Way of the Deathbringer` (U, {2}{B}) · `Liliana the Repentant` (R, {1}{B}). Cheap bodies that are happy to die, and **sacrifice outlets** — Silence the Echo and Way of the Deathbringer are the ones that also do something. Without an outlet, recursion is just small creatures.
- **Payoffs to look for:** `Liliana the Repentant` (R, {1}{B}) · `Gallia, Tragic Host` (U, {1}{B}) · `Edgar, Ancient Bloodlord` (U, {W}{B}) · `Darklight Phoenix` (M, {3}{B}) · `Bloodline Recollector` (M, {1}{B}) · `Massacre Girl, Most Wanted` (U, {4}{B}) · `Way of the Necromancer` (U, {1}{B}). Things that come back, or that get better when creatures die. Liliana the Repentant is both — she fills the graveyard and reanimates from it.
- **Spine (both builders):** `Winter, Tormented Loner` (U) · `Last Gasp` (C) · `Way of the Deathbringer` (U) · `Edgar, Ancient Bloodlord` (U) · `Silence the Echo` (C) · `Teyo, Lightshield Expert` (U) · `Mabel, Bitter Recluse` (U) · `Campus Crier` (C) · `Massacre Girl, Most Wanted` (U) · `Memory Trap` (C) · `Rank Rat` (C) · `Hexhaven Battalion` (C)
- **Engine:** a sacrifice outlet. `Silence the Echo` (C) doubles as removal *and* an outlet. `Way of the Deathbringer` is in both decks and is why: it hands your Jace token "−2: sac a creature, make a 4/4 trample Beast" — an outlet, a payoff and a mana-fixer clause in one card.
- **Interaction:** the pair contains **22 removal spells, 5 at common** — second-deepest in the set. The builders had **4 and 3**. Take every piece you see; do not expect six.
- **Curve:** 1:2 · 2:10 · 3:6 · 4:3 · 5:1 · 6:1
- **Mana:** **corrected** — I wrote "no dual exists." *Meticulous Commons* is a `W/B` common dual. See §4.5.
- **Fails when:** you draft it as cheap creatures with no outlet and no payoff.

### B/G Garruk's Bestiary — Value Creatures · 23 spells, 17 land

- **Signposts — the Garruk pair:** `Garruk, Veiled Butcher` (B, `{3}{B}{B}` mythic) and `Garruk, Curse Breaker` (G, `{3}{G}{G}` mythic). Two five-mana planeswalkers that **each make a 4/4 trample Beast** — the deck's deathtouch-and-trample theme on one card apiece. *Curse Breaker*'s static (draw whenever a power-4+ creature enters) is the card-advantage engine this deck otherwise lacks; *Veiled Butcher*'s +2 (−4/−1) is repeatable removal and its static exiles anything of theirs that dies. Either is a first-pick bomb; both is the best B/G deck in the room.
- **Enablers to look for:** `Rampart Hunter` (C, {3}{B}) · `Ferocity of the Hunt` (C, {1}{B/G}) · `Arcane Amphisbaena` (C, {1}{G}) · `Primal Witchstalker` (U, {1}{B}{G}) · `Carnivorous Cultivator` (R, {1}{G}) · `Last Gasp` (C, {1}{B}) · `Compel Brutality` (C, {1}{G}). Deathtouch bodies and removal. This deck has no engine on purpose — its enablers are good creatures that trade up, and its interaction keeps the board clear for the top end.
- **Payoffs to look for:** `Garruk, Curse Breaker` (M, {3}{G}{G}) · `Garruk, Veiled Butcher` (M, {3}{B}{B}) · `Vraska, the Cutting Glare` (R, {B}{B}{G}) · `Hapatra, the Desert Fang` (U, {2}{B}{B}{G}) · `Vinelasher Adept` (C, {4}{G}{G}) · `Apex Witchstalker` (C, {4}{B}{B}) · `Bestial Incursion` (C, {3}{G}). Big things with trample, and the two Garruks — Curse Breaker draws off every 4-power creature, so the more of these you have the more cards he gives you.
- **Spine (both builders):** `Gallia, Tragic Host` (U) · `Last Gasp` (C) · `Extended Absence` (C) · `Hapatra, the Desert Fang` (U) · `Primal Witchstalker` (U) · `Rewrite Regrets` (U) · `Arcane Amphisbaena` (C) · `Bestial Incursion` (C) · `Something Worth Saving` (C) · `Apex Witchstalker` (C) · `Vinelasher Adept` (C)
- **Engine:** none — and that is the point. The highest-floor deck, because good creatures are good creatures.
- **Interaction:** 18 in the pair, 5 at common. The builders had **3 and 4**, all black.
- **Curve:** the two heaviest decks in the sample (avg 3.70 and 3.09). **1:1 · 2:9 · 3:4 · 4:5 · 5:2 · 6:2** — this is the one shell where a high curve is correct.
- **Fails when:** never badly. Loses to the two S-tier decks by a little, beats everything else by a little.

### G/W Vigorbloom — Lifegain & Counters · 23 spells, 17 land

- **Signposts:** `Kwia Vigorbloom` (M, {3}{G}{W}{W}) · `Vigorbloom Vanguard` (U, {1}{G/W}) · `Vigorbloom Charm` (U, {G}{W}) — The college's Elder Sphinx, its uncommon prepared creature and its charm.
- **Enablers to look for:** `Emergency Phytomedic` (C, {G/W}) · `Vigorbloom Vanguard` (U, {1}{G/W}) · `Greenhouse Propagator` (C, {2}{G}) · `Unflinching Hortimancer` (C, {1}{W}) · `Predictive Preparations` (C, {1}{W}) · `Liliana the Faultless` (R, {W}) · `Vigorbloom Charm` (U, {G}{W}). Lifegain and +1/+1 counter sources. The Vigorbloom prepared spell does both, and Liliana the Faultless gains a life for every body you play.
- **Payoffs to look for:** `Bloombrute` (U, {2}{G}{W}) · `Graft Surgeon` (C, {2}{W}) · `Ajani Resolute` (M, {1}{W}) · `Lyra, Archangel of Dawn` (R, {2}{W}) · `Enlightened Confidant` (M, {1}{W}) · `Solarium Sentry` (R, {G}{W}) · `Germinate Recruits` (R, {2}{W}) · `Kwia Vigorbloom` (M, {3}{G}{W}{W}). Cards that draw, grow or make tokens when you gain life. Bloombrute and Graft Surgeon are the commons that matter; Ajani Resolute is the mythic that wants this deck more than his own.
- **Spine (both builders, 14 of 23):** `Vigorbloom Vanguard` (U) · `Bloombrute` (U) · `Blossom-Blessed Angel` (C) · `Edgar, Moonlit Sovereign` (U) · `Surgical Precision` (C) · `Titanbones, Towering Heart` (U) · `Vigorbloom Charm` (U) · `Yoshimaru, Scrappy Stray` (U) · `Greenhouse Propagator` (C) · `Emergency Phytomedic` (C) · `Compel Brutality` (C) · `Memory Trap` (C) · `Unflinching Hortimancer` (C) · `Blessed Ghoul` (C)
- **Engine:** `Graft Surgeon` (C) keeps counters after a creature dies; `Bloombrute` (U) draws on lifegain. Two payoffs is enough.
- **Interaction:** **corrected** — I called this "weakest in the format, 10 removal, 2 at common." It is **12 and 4** (`Compel Brutality`, `Sureshot Sower`, `Memory Trap`, `Surgical Precision`), and the weakest pair is **G/U**, not G/W.
- **Curve:** 1:3 · 2:10 · 3:5 · 4:3 · 5:1 · 6:1
- **Fails when:** it plays a long game against U/B or W/B. Lifegain does nothing to a deck winning on cards.

### R/W Ajani's Army — Counters Aggro · 23 spells, **16 land**

- **Signposts — the Ajani pair:** `Ajani Resolute` (W, `{1}{W}`, 2 loyalty, mythic) and `Ajani Unrelenting` (R, `{4}{R}{R}`, 5 loyalty, mythic). **The pair is split across the aggro/lifegain line**, and that matters: *Resolute* is a two-mana walker that ticks itself up whenever you gain life and makes a Pridemate — it wants G/W Vigorbloom as much as R/W. *Unrelenting* is the aggro one: a Cadet on every activation, +1 for team haste, and a −3 one-sided sweep that spares your tokens. Six mana in a 16-land deck is a real cost; it is still the best top-end this deck can have.
- **Enablers to look for:** `Predictive Preparations` (C, {1}{W}) · `Charge the Sanctum` (C, {2}{R/W}) · `Skilled Battlecarver` (C, {1}{R}) · `Marwyn, the Clearcutter` (U, {R}) · `Emergency Phytomedic` (C, {G/W}) · `Warrior's Blades` (U, {2}{R}{W}) · `Heartstring Puller` (C, {3}{R}). Cheap bodies and counter sources. The curve *is* the engine — nine two-drops and 16 lands — so the enablers are anything that costs two or less and attacks.
- **Payoffs to look for:** `Mabel, Valley Hero` (U, {1}{R}{W}) · `Ajani Unrelenting` (M, {4}{R}{R}) · `Ajani Resolute` (M, {1}{W}) · `Ajani's Anguish` (R, {X}{R}) · `Gallia, the Merrymaker` (U, {1}{R}) · `Winter, Team Player` (U, {4}{R}) · `Master of Barbs` (R, {1}{R}). Anthems, haste and reach to close. Ajani Unrelenting is the top end; Ajani's Anguish gives the whole team trample. Don't take payoffs over two-drops.
- **Spine (both builders):** `Wrath of the Bloodmane` (C) · `Awaken the Inferno` (C) · `Gallia, the Merrymaker` (U) · `Mabel, Valley Hero` (U) · `Winter, Team Player` (U) · `Marwyn, the Clearcutter` (U) · `Warrior's Blades` (U) · `Emergency Phytomedic` (C) · `Heartstring Puller` (C) · `Predictive Preparations` (C) · `Skilled Battlecarver` (C) · `Hexhaven Battalion` (C)
- **Note:** both builders ran `Emergency Phytomedic` `{G/W}` and Pete ran `Vigorbloom Vanguard` `{1}{G/W}` in a deck with no Forests. **Hybrids are on-colour if you have either half** — confirmed.
- **Engine:** the curve *is* the engine. **9 two-drops, 16 lands.**
- **Interaction:** 3 is right, and 3 is what both builders had (2 and 3). Don't trade; race.
- **Curve:** 1:3 · 2:9 · 3:5 · 4:3 · 5:2 · 6:1
- **Fails when:** anything. No late game, loses to Vigorbloom lifegain, gets 2-for-1'd by prepared creatures. **Only take this lane when it is screaming.**

### B/R Stingerquill — Face Burn · 23 spells, 17 land

- **Signposts:** `Ingris Stingerquill` (M, {B}{R}{R}) · `Stingerquill Voxmancer` (U, {B/R}) · `Stingerquill Charm` (U, {B}{R}) — The college's Elder Sphinx, its uncommon prepared creature and its charm.
- **Enablers to look for:** `Stingerquill Voxmancer` (U, {B/R}) · `Hallway Heckler` (C, {2}{R}) · `Whiplash Wordsmith` (C, {3}{B/R}) · `No Admittance` (C, {1}{R}) · `Stingerquill Charm` (U, {B}{R}) · `Screeching Soulbreaker` (C, {2}{B}) · `Cast Away Doubt` (C, {2}{B}). Noncombat damage to the opponent: the Stingerquill prepared spell, pingers and burn. These also happen to be the deck's bodies.
- **Payoffs to look for:** `Master of Barbs` (R, {1}{R}) · `Ingris Stingerquill` (M, {B}{R}{R}) · `Grim Repriser` (U, {B}{R}) · `Sanctum Lurker` (R, {2}{B}) · `Command the Stage` (U, {2}{R}). Cards that trigger when an opponent takes damage. **Master of Barbs is a rare**, so the payoff usually isn't there — which is why the right B/R deck is a removal deck that ignores this list.
- **Spine (both builders):** `Stingerquill Voxmancer` (U) · `Sanctum Lurker` (R) · `Command the Stage` (U) · `Grim Repriser` (U) · `Tomik, Izzet Sparkmage` (U) · `Stingerquill Charm` (U) · `Whiplash Wordsmith` (C) · `Blazing Crescendo` (C) · `Skilled Battlecarver` (C) · `No Admittance` (C)
- **`Sanctum Lurker` in both decks is the find here.** "Planeswalkers you control aren't put into their owners' graveyards for having 0 loyalty" — a Jace token enters at **0** and normally dies on the spot unless something empowers it. Lurker makes every empower card in your deck work, and keeps a spent Jace on the board to hold your duals untapped.
- **Interaction: I have to withdraw a number.** I wrote "run 7. Yes, seven." The pair genuinely has the deepest interaction in the set — **23 spells, 7 at common** — and both builders, from real pools, ended on **1 and 2**. Seven was never a sealed target. In draft, take every removal spell; in sealed, build what you opened.
- **Curve:** 1:3 · 2:10 · 3:7 · 4:2 · 5:1 · 6:0
- **Fails when:** you point burn at the face. `Master of Barbs` is a mono-R **rare**, so the face-damage payoff usually isn't there. **Re-rated 6.2 → 6.9 as a removal deck**, still C-tier as the deck it's designed to be.

### U/R Chandra's Prowess — Noncreature Spells · 23 spells, 17 land

- **Signposts — the Chandra pair:** `Chandra, Chill of Compliance` (U, `{1}{U}{U}` mythic) and `Chandra, Torch of Defiance` (R, `{2}{R}{R}` mythic). Both reward noncreature spells directly: *Chill*'s +1 surveils and picks up a noncreature card, her other +1 makes {U} for noncreature spells only, and −X stuns a blocker. *Torch* is the strongest reprint in the set for Limited — +1 card or 2 damage, +1 for {R}{R}, −3 kills a creature — removal and card advantage on one permanent. Either walker is a reason to be in this deck; the common prowess bodies are not.
- **Enablers to look for:** `Twinned Vision` (C, {1}{U/R}) · `Unsummon` (C, {U}) · `Blazing Crescendo` (C, {1}{R}) · `Icy Reception` (C, {1}{U}) · `Essence Burn` (U, {1}{R}) · `Wrath of the Bloodmane` (C, {2}{R}) · `Clash of Elements` (U, {1}{U}{R}) · `Artifist Acumen` (C, {R}). Cheap noncreature spells — and they should be **removal or tempo**, so your spell count and your interaction count are the same cards. A bad cantrip is still a bad card.
- **Payoffs to look for:** `Chandra's Emberling` (C, {2}{R}) · `Cryotheory Adept` (C, {1}{U}) · `Saheeli, Jewel of Avishkar` (U, {2}{U}{R}) · `Variable Chaser` (R, {2}{U}) · `Pyre Rhymer` (R, {1}{R}{R}) · `Stingcaster Mage` (M, {1}{R}) · `Chandra, Chill of Compliance` (M, {1}{U}{U}) · `Chandra, Torch of Defiance` (M, {2}{R}{R}) · `Tomik, Izzet Sparkmage` (U, {1}{R}). Prowess and spell-cast triggers. Saheeli makes a hasty Thopter per spell; both Chandras reward noncreature spells directly.
- **Spine (both builders):** `Pompous Battlemage` (R) · `Stingerquill Voxmancer` (U) · `Traxos, Academy Guardian` (U) · `Clash of Elements` (U) · `Plan for All Outcomes` (U) · `Tomik, Izzet Sparkmage` (U) · `Tam's Resistance` (C) · `Blazing Crescendo` (C) · `Chandra's Emberling` (C) · `Cryotheory Adept` (C) · `Unsummon` (C)
- **Engine:** ~9 noncreature spells, and they should be **removal**, so your spell count and your interaction count are the same cards. Red supplies what blue cannot.
- **The cheapest deck in the sample:** Dafore's U/R averaged **2.12** mana with **seven one-drops** and only 10 creatures. If a pair is going to run 13 two-or-fewer-drops, it's this one.
- **Curve:** 1:5 · 2:9 · 3:5 · 4:3 · 5:1 · 6:0
- **Fails when:** you play weak cantrips to hit a prowess count. A bad spell is still a bad card.

### G/U Jace's Mastery — Empower Value · 23 spells, 17 land  **(upgraded)**

- **Signposts — Jace, who did not split:** there is no green Jace. **Jace's echo is the Jace *token*** — the empower mechanic itself — and this deck is built around feeding it. The Jace cards are all blue: `The Theorist, Jace Beleren` (`{2}{U}{U}` mythic — you draw on each opponent's draw step; +1 Illusion, −2 bounce) and `Jace, Reality Sculptor` (`{3}{U}{U}` rare — +1 empowers by your Island count). The green half of the archetype is carried by the cards that give your walkers abilities: `Way of the Paradox`, `Way of the Wildspeaker`, `Kiora of Salt and Sand`, `Avatar of Burgeoning Echoes`. So unlike the other four enemy pairs, the signpost here is a mechanic, not a card pair.
- **Enablers to look for:** `Tam's Resistance` (C, {1}{G/U}) · `Arcane Amphisbaena` (C, {1}{G}) · `Mindseeker Oculus` (C, {2}{U}) · `Protege's Awakening` (C, {3}{U}) · `Inspired Tethermage` (C, {2}{G}) · `Plan for All Outcomes` (U, {3}{U}) · `Jace's Machinations` (R, {2}{U}) · `Jace, Reality Sculptor` (R, {3}{U}{U}). Empower cards — six or more. Blue has the big ones (Oculus 4, Awakening 6, Machinations 8); green's are cheaper bodies. The loyalty is the battery.
- **Payoffs to look for:** `Way of the Paradox` (U, {2}{G}) · `Way of the Wildspeaker` (U, {4}{G}) · `Way of the Mind Sculptor` (U, {4}{U}) · `Way of the Cryomancer` (U, {2}{U}) · `Kiora of Salt and Sand` (U, {1}{G}{U}) · `Avatar of Burgeoning Echoes` (M, {G}{U}) · `Mind Meanderer` (U, {3}{G}{U}{U}) · `Compel Brutality` (C, {1}{G}). Cards that give your walkers abilities, or that care about loyalty. **Two Ways is the line** — both real sealed builders had two. Compel Brutality turns five loyalty into a removal spell.
- **Spine (both builders):** `Way of the Wildspeaker` (U) · `Sureshot Sower` (C) · `Way of the Mind Sculptor` (U) · `Mind Meanderer` (U) · `Mindseeker Oculus` (C) · `Protege's Awakening` (C) · `Tam's Resistance` (C) · `Arcane Amphisbaena` (C) · `Compel Brutality` (C) · `Infinite Coursework` (C) · `Inspired Tethermage` (C)
- **Both builders independently ran two Ways.** That is the clearest confirmation in the whole sample of something this guide claimed on reasoning alone: the Ways are what turn a battery of empower cards into an engine.
- **Engine:** **6+ empower cards and 2+ Ways.** Without two Ways you have a green-blue goodstuff deck paying a tax.
- **Interaction:** **the genuine floor of the format — 8 spells, 3 at common.** But `Compel Brutality` is better here than anywhere: its second mode has *a planeswalker you control deal damage equal to its loyalty*, and this is the deck with a five-loyalty Jace. A 2-mana instant that kills almost anything, in the colour that isn't supposed to have removal.
- **Curve:** 1:1 · 2:8 · 3:6 · 4:4 · 5:3 · 6:1
- **Fails when:** you get the empower and not the Ways.

### R/G Konstrari — Heartwood Ramp · 23 spells, **18 land in sealed, 17 in draft**

- **Signposts:** `Aerid Konstrari` (M, {1}{R}{G}{G}) · `Woodwork Prodigy` (U, {2}{R/G}) · `Konstrari Charm` (U, {R}{G}) — The college's Elder Sphinx, its uncommon prepared creature and its charm.
- **Enablers to look for:** `Konstrari Improviser` (C, {1}{R/G}) · `Woodwork Prodigy` (U, {2}{R/G}) · `Heartwood Crafter` (U, {G}) · `Aerid Konstrari` (M, {1}{R}{G}{G}) · `Hungering Puppetbeast` (R, {3}{G}{G}) · `Konstrari Charm` (U, {R}{G}). Heartwood makers. Woodwork Prodigy re-prepares every upkeep, so it's a Heartwood a turn. Three or more, or the top end never gets cast.
- **Payoffs to look for:** `Aerid Konstrari` (M, {1}{R}{G}{G}) · `Craftwork Crusher` (U, {3}{R}{R}{G}{G}) · `Draconic Visitor` (R, {3}{R}{R}) · `Kiora of Fire and Ashes` (U, {4}{R}{R}) · `Wrecking Gecko` (C, {4}{G}) · `Vinelasher Adept` (C, {4}{G}{G}) · `Ghalta the Unstoppable` (U, {8}{G}) · `Puppet Crafting` (R, {1}{G}). Expensive things worth ramping into, and artifact-count cards. Draconic Visitor turns every Heartwood into a 5/5 Dragon. In sealed the pool hands you these; in draft take them *before* the enablers.
- **Spine (both builders):** `Woodwork Prodigy` (U) · `Wrath of the Bloodmane` (C) · `Craftwork Crusher` (U) · `Heartwood Crafter` (U) · `Yoshimaru, Scrappy Stray` (U) · `Kiora of Fire and Ashes` (U) · `Konstrari Improviser` (C) · `Arcane Amphisbaena` (C) · `Wrecking Gecko` (C) · `Compel Brutality` (C) · `Vinelasher Adept` (C)
- **Engine:** **3+ Heartwood makers AND 3+ cards worth ramping into.** Both halves, or neither works.
- **Interaction:** 14 in the pair, 5 at common — and the builders had **4 and 5, the highest counts in the sample.** Green's interaction is better than I credited it; see §0.8.
- **Curve:** 1:1 · 2:9 · 3:4 · 4:2 · 5:4 · 6:3 — deliberately top-heavy, and both builders confirmed it (avg 3.48 and 3.30, the second- and third-heaviest decks).
- **Fails when:** in draft, the top end went to the other eight drafters. **In sealed it is a top-three deck** and this shell is why: pools hand you expensive cards draft won't.

### The one-line version

> **Black first, blue second, and the best deck in any seat is the one holding
> the most removal.** Six of the ten shells are built around killing a prepared
> creature before it casts its copy. What twenty real sealed decks add: **you will
> not have as much of it as you want** — median two pieces — so the pick order
> matters more than the target.

---

## 0.8 What 20 real sealed builds changed  [CONFIRMED decklists, 2026-09-21]

Twenty registered sealed decks — two builders, **Pete** and **Dafore**, one deck per colour pair
each. Every card parsed against the real set list: **169 distinct cards, 0 unrecognised.** This is
the first section of this guide checked against decks somebody actually built.

### What it confirmed

- **23 spells is right.** 16 of 20 decks ran exactly 23; the others 22 or 24.
- **Hybrid college cards slot into single-colour decks.** Both "W/R" builds run *Emergency
  Phytomedic* `{G/W}` and Pete's runs *Vigorbloom Vanguard* `{1}{G/W}` — castable off Plains.
  If you are in either half of a hybrid, the card is on-colour. This was an [EVAL] note; it's
  now confirmed behaviour.
- **The Jace commons are the glue.** *Fatehold Chronologist* is the single most-played card in
  the sample (7/20), and 8 of the top 15 have empower or surveil text.

### What it contradicted — my interaction counts

This is the important one. My shells told you to run **6 removal in W/B** and **7 in B/R**. Here
is what the builders actually had:

| Pair | Removal, Pete | Removal, Dafore | My shell said |
|---|---|---|---|
| W/U | 1 | 2 | — |
| W/B | 4 | 3 | **6** |
| W/R | 2 | 3 | 3 |
| W/G | 3 | 2 | — |
| U/B | 4 | 5 | 5 |
| U/R | 2 | 1 | — |
| U/G | 2 | 1 | — |
| **B/R** | **1** | **2** | **7** |
| B/G | 3 | 4 | 5–6 |
| G/R | 4 | 5 | 4 |

**I was conflating two different numbers.** How much removal a colour pair *contains* is a fact
about the set; how much removal you *have* is a fact about your pool. B/R really is the deepest
interaction pair in Reality Fracture — 23 removal spells, 7 at common — and a single sealed pool
still handed each builder one or two. "Run seven" was never a target anyone could hit in sealed;
I stated an aspiration as a requirement.

> **The rule that replaces it:** set-wide removal depth tells you *what to take when you see it*.
> It does not tell you what you will have. In sealed, build the deck your pool gave you and take
> the interaction count as a tiebreaker between two otherwise-equal builds — not as a gate.

In **draft** the 4+ target still stands, because in draft you get to choose.

### What it contradicted — my curves

Every one of the 20 decks peaks at **two mana**, and they are lower than the curves I wrote:
**7–13 two-drops** (median 10) against my 5–8. Average mana value ran 2.12 (Dafore's U/R, with
seven one-drops) to 3.70 (Pete's B/G). Treat my per-shell curves in §0.7 as revised: **add two to
the two-drop row and take them off the four-and-above rows.**

### Three commons I never mentioned, in 6 decks each

| Card | | Why I missed it | Why it's good |
|---|---|---|---|
| ***Memory Trap*** | `{2}{W}` C | I had no oracle text for it and graded it 2.5 | **It's an Oblivion Ring.** Exiles *any* nonland permanent an opponent controls. This is premium white common removal and it changes white's evaluation — see below. |
| ***Compel Brutality*** | `{1}{G}` C | Same | Instant fight-lite — *and* its second mode has **a planeswalker you control deal damage equal to its loyalty.** A Jace token at 5 loyalty makes this a 2-mana instant that kills almost anything. |
| ***Hexhaven Battalion*** | `{4}{W}{W}` C | Graded 2.2 as an expensive sorcery | Three 2/2s **plus empower Jace 2**, and it **basic landcycles for {2}** when you don't want it. A six-drop with no floor problem. |

### The correction that follows: white and green both have more removal than I said

Recounted from oracle text — cards that kill, exile, or permanently neutralise a creature or
planeswalker:

| Colour | Total | At common | I previously said |
|---|---|---|---|
| **B** | 13 | 3 | 12 / 3 |
| **R** | 8 | 3 | 8 / 2 |
| **W** | **7** | **2** | 6 / 1 |
| **G** | **4** | **2** | 4 / 1 |
| **U** | 3 | 1 | 3 / 1 |

White gains *Memory Trap*; green gains *Compel Brutality*; red gains *Hallway Heckler // Vicious
Verse*. **Colour scores move: W 7.5 → 7.9, G 6.6 → 6.9.** Black and blue are unchanged and black
is still the best colour. The claim in §0.7 that "W+U is 4 removal total, 2 at common" is wrong —
it is **10 total, 3 at common**, and G/W is not the weakest interaction pair in the format,
**G/U is**.

By pair, counting mono removal in both colours plus gold and hybrid cards in that pair:

| | B/R | W/B | B/G | U/B | W/R | G/R | W/G | U/R | W/U | U/G |
|---|---|---|---|---|---|---|---|---|---|---|
| **Total** | 23 | 22 | 18 | 17 | 16 | 14 | 12 | 12 | 10 | 8 |
| **Common** | 7 | 5 | 5 | 4 | 5 | 5 | 4 | 4 | 3 | 3 |

### How to read the per-pair lists in §0.7

Each shell now carries a **spine** — the cards *both* builders independently played in that pair.
Two builders agreeing is evidence. Two builders disagreeing is not a 50/50 to be averaged; it is
an open question, and I've left those cards out of the spines rather than pick a side. Agreement
ran 10–15 cards out of 23, so roughly **half of a sealed deck is forced and half is yours.**

---

## 1. The set in one page

| | |
|---|---|
| **Set** | Reality Fracture (**FRA**) |
| **Plane** | Echoverse Arcavios — a mirrored reality where Strixhaven is **Hexhaven** |
| **Size** | 290 cards: **71 commons, 109 uncommons, 64 rares, 26 mythics**, 10 basics [CONFIRMED] |
| **New mechanics** | **Empower Jace**, **Heartwood** tokens |
| **Returning** | **Prepared** (from Secrets of Strixhaven), **threshold**, flashback, surveil, scry, landfall |
| **Structure** | 5 allied pairs = Hexhaven **colleges**, each signposted by an Elder Sphinx; 5 enemy pairs = the **Lorwyn Five** planeswalkers, each split into two mono-coloured cards (one per colour). Ajani → R/W, Chandra → U/R, Garruk → B/G, Liliana → W/B, Jace → G/U. Collector numbers 195–262 are the whole *Echoed Pair* run: every legend in the set has a mirror in another colour, and the five walkers are its mythic tier. |
| **Booster quirk** | The **Echoed Pair** slot: **three cards per play booster, two of which are one real mirrored pair** and the third any echo-slot card. **43 pairs, 86 cards: 66 uncommon, 14 rare, 6 mythic** [CONFIRMED — Wizards' collecting article]. Every pair is same-rarity across two colours. The five *Way* enchantments pair by planeswalker (Mentor/Warlord, Cryomancer/Pyromancer, Deathbringer/Wildspeaker, Healer/Necromancer, Mind Sculptor/Paradox). One rare pair — *Jace, Reality Sculptor* / *Tam, the Possibility* — is inferred from the count rather than confirmed by name. |

### The structural fact most people will miss

**109 uncommons against 81 commons.** That ratio is lopsided, and the **Echoed Pair slot** pushes
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
worth it if you have something worth ramping *into*. Heartwood does two jobs: ramp, and artifact
count (for Konstrari payoffs like **Aerid Konstrari**).

> **Correction to an earlier version of this guide.** I previously wrote that Heartwood "fixes a
> third colour for free." That was too broad and I was wrong to say it. Heartwood adds **{R} or
> {G} and nothing else** — it pays for an R or G splash specifically, and does nothing at all for
> a W, U or B splash. The set's actual fixing is the Annex land cycle; see Section 4.5.

**Threshold** (seven or more cards in your graveyard) [CONFIRMED]: reachable around **turn 5–6
with Theorix self-mill**, around **turn 9+ without it**. That gap is enormous.

> **Rule: threshold cards are U/B cards, full stop.** Outside Theorix they are late-game-only
> and you should treat the threshold text as absent. The upside: everyone else cuts them, so
> they come around late for the deck that actually wants them. [EVAL]

---

## 4.5 Three-colour decks: what actually works

> ### Correction — this section was built on a false premise
>
> Earlier versions of this guide said: *"there is no enemy-colour dual land in this set at any
> rarity,"* and built the whole section on it — shards supported, wedges not, and enemy pairs
> "repairing" their mana by going to three colours. **That is wrong.** I had found the five
> *Annex* lands and stopped looking. There is a second common dual cycle, the **Commons** cycle,
> and it covers exactly the five enemy pairs. Every pair in Reality Fracture has a common dual.
> The colour-wheel geometry I described does not exist. What follows is the corrected version.
> [CONFIRMED from oracle text]

### Every piece of fixing in the set

| Source | Rarity | What it does |
|---|---|---|
| **Annex cycle** — Fatehold `WU`, Theorix `UB`, Stingerquill `BR`, Konstrari `RG`, Vigorbloom `GW` | **common** | Taps for its two **allied** colours. Enters tapped **unless you control a planeswalker**. |
| **Commons cycle** — Meticulous `WB`, Innovative `UR`, Formidable `BG`, Dedicated `RW`, Transformative `GU` | **common** | Taps for its two **enemy** colours. *Identical text:* enters tapped unless you control a planeswalker. |
| Slowlands — Deserted Beach `WU`, Shipwreck Marsh `UB`, Haunted Ridge `BR`, Rockfall Vale `RG`, Overgrown Farmland `GW` | rare | Allied only. Enters tapped unless you control **two or more other lands** — so untapped from turn 3, no planeswalker needed. |
| **Room of Refuge** | **common** | Always enters tapped; choose a colour as it enters, taps for that colour. A universal splash land with no condition. |
| **Heartwood** token | common (6 makers) | `{T}: Add {R} or {G}` — **and nothing else.** |
| Theorist's Sanctum | rare | Blue land; untapped if you behold a Jace. `{2}{U}, {T}: Empower Jace 2`. |
| Lotus token (Kwia Vigorbloom) | mythic | Tap and sacrifice for three mana of one colour — one-shot. |

**Ten common duals, one per pair.** That single fact replaces everything the old section said.

### What actually follows from it

**1. Every three-colour combination has three common duals — one for each of its pairs.**
Esper `WUB` gets Fatehold + Theorix + Meticulous. Mardu `RWB` gets Dedicated + Meticulous +
Stingerquill. **Shards and wedges are equally supported.** There is no wheel arc to respect, and
"you're in a wedge, don't" was bad advice I should not have given.

**2. Every two-colour pair has its own dual, so no pair needs a third colour to fix itself.**
The old claim that W/B "opens the set with nothing" was wrong — it opens with *Meticulous
Commons*. Enemy pairs are not mana-disadvantaged at common. The only allied advantage left is at
**rare**, where the five slowlands exist and the enemy pairs get nothing.

**3. The slowlands are the better card, and they're the ones that are allied.** *Haunted Ridge*
is untapped from turn 3 unconditionally; *Stingerquill Annex* may still be tapped on turn 8. If
you open a slowland in sealed, that's a real nudge toward its pair.

### The real gate on three colours: the planeswalker clause

All ten common duals share one line — **enters tapped unless you control a planeswalker.** That
is the actual constraint in this format, and it is not a colour-wheel question, it is a deck
question. [CONFIRMED]

Two consequences that matter at the table:

1. **A planeswalker arriving the same turn does not count.** Playing the dual on the turn you
   make your first Jace does not untap it. The Jace has to already be there.
2. **Your duals are taplands on turns 1–3 and real duals from turn 4** — backwards for an aggro
   deck, fine for a midrange one. **Three colours in FRA is a midrange/control plan.** R/W
   Ajani's Army should almost never do it.

So a three-colour deck wants **3+ empower cards**, and not primarily for the card advantage:
*empower Jace is the set's mana-fixing mechanic.* It appears at common in every colour, which is
why it is in every colour. A deck with six empower cards has six duals that work; a deck with one
has six taplands.

> **The honest rule, restated:** two duals is the price of entry for a third colour, and a
> planeswalker you can land by turn 3 is the price of the duals. With two duals and the empower
> count, the third colour is genuinely open. With two duals and no empower, you have bought
> taplands.

### The rule that survives: a dual sharing one colour with you is a free splash land

If a land makes one of your main colours *and* your splash colour, it is never a dead draw. That
was true before and it is still true — it just now applies to every pair, not five of them.

### When to splash, concretely

- **Splash for:** bombs (an Elder Sphinx, a planeswalker), premium removal, and expensive cards
  you'll cast on turn 6 anyway — by then you've drawn your sources.
- **Never splash for:** two-drops, curve filler, or synergy pieces that must arrive on time. A
  card you can't cast on curve isn't doing its job.
- **Sources:** single coloured pip → 2–3 sources. **Double pip → that is a main colour, not a
  splash.** `{1}{R}` and `{R}{R}` are the same colour and completely different cards.
- **Count a dual as a source for both its colours**, but discount it on turns 1–3 unless your
  empower count is high.
- **Room of Refuge is the splash land that asks nothing.** It's always tapped, but it needs no
  planeswalker and it makes any colour. In a deck splashing one bomb it is often better than the
  "correct" dual.

A worked example — U/B Theorix splashing W for a bomb, 17 lands:

```
2 Meticulous Commons  (W/B - the bridge, and it was always available)
2 Theorix Annex       (U/B - your own pair)
1 Room of Refuge      (names W)
6 Island
6 Swamp
= 5 white sources, 8 blue, 10 black, and every land makes a main colour
```

### Draft vs sealed

- **Sealed:** much more likely. Deeper pools, slower games, more uncastable bombs. Count your
  duals *and your empower cards* before you settle on two colours.
- **Draft:** you have to take them. Ten common duals across three packs means fixing is genuinely
  available — but it also means the player two seats down is splashing too. If you're planning
  it, take the second dual around pick 6–8 rather than hoping it wheels.

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

| | Draft target | Sealed — *observed* across 20 real builds |
|---|---|---|
| Spells | 23 | **22–24** (23 in 16 of 20) |
| Creatures | 15–17 | **10–17**, median 15 |
| Removal/interaction | **4+ (prioritise instants)** | **1–5, median 2** — see §0.8 |
| Lands | 17 | 17 (18 with Heartwood ramp + a 6-drop top end) |
| Curve peak | 3 | **2** — every one of the 20 decks peaked at two |
| 2-drops | 5–6 (7+ if RW/BR) | **7–13**, median 10 |
| Average mana value | ~2.9 | **2.12–3.70**, median 2.8 |
| Empower cards | 3–4 is an engine | any number, it's free value |

The sealed column is not my estimate — it is what two experienced builders actually registered,
counted card by card. Where it disagrees with the draft column, trust it for sealed and read
§0.8 before you trust the draft column either.

---

## 6. Colour strength

Scores are 0–10 [EVAL]. **This table has been revised twice** — once against the real card list
(§0.6) and once against the recounted removal in §0.8. What follows is the current version; the
original pre-release guesses are kept in the right-hand column so you can see how far off they were.

Every colour appears in exactly four archetypes, so this is about raw card quality and fit with a
grindy format — not archetype count.

| Rank | Colour | Score | Removal (total / common) | The case | First guess |
|---|---|---|---|---|---|
| 1 | **Black (B)** | **8.6** | **13 / 3** | Black has more removal than any two other colours combined, and in a format where killing a prepared creature before it casts its copy is a 2-for-1, that is the premium currency. Add graveyard payoffs (Theorix) and recursion (Liliana's Attrition). Black is the best colour and it isn't close. | 8.0 |
| 2 | **Blue (U)** | **8.2** | 3 / 1 | The format's mechanics are blue — empower Jace makes a *blue* token, and surveil, self-mill and selection are blue's. Blue is in both top-two archetypes. It drops below black on one number: it cannot kill anything. `Infinite Coursework` is the only blue common that permanently stops a creature. | 8.5 |
| 3 | **White (W)** | **7.9** | **7 / 2** | **Revised up.** White's stated weakness was "no common removal" and that was my error: *Memory Trap* `{2}{W}` is an Oblivion Ring at common, and both sealed builders played it in every white deck they made. Add `Surgical Precision`, token generation off the Fatehold prepared spell and the counters shell, and white is a real colour, not a synergy-dependent one. | 7.5 |
| 4 | **Red (R)** | **7.2** | 8 / 3 | **Revised up, for the opposite reason to the one I gave.** Red's headline plan — damage at the face — is still the worst plan in a midrange format with a lifegain archetype. But red's *creature removal* is the second-best in the set at three commons, and I had marked the colour down for its archetype's bad idea. Be happy to end up in red; don't start there. | 6.5 |
| 5 | **Green (G)** | **6.9** | **4 / 2** | **Revised up slightly.** Big bodies are good when games go long. I said green had one removal common; it has two, and `Compel Brutality` is the more interesting one — its planeswalker mode deals damage equal to *your Jace's loyalty*, which turns green's empower commons into a removal engine. Still last: green's interaction is conditional and its top end is beatable by card advantage. | 7.0 |

> **The practical takeaway:** if you have no signal, **start black and move out of it.** Black is
> the deepest colour at common and the one whose cards are good in every deck. Blue is the best
> *partner*; it is a bad colour to be in alone. And be the drafter who is happy to end up in red
> when it's flowing — not the one who starts there.

### 6.1 The best cards in each colour  [EVAL]

Eight per colour at any rarity, then the commons you will actually be handed. Order inside a colour is
my read of the cards; the score is from the table above.

#### Black — 8.6

The best colour, and it isn't close. Thirteen removal spells, three at common — more than any two other colours combined — in a format where killing a prepared creature before it casts its copy is a two-for-one. The graveyard payoffs and the Liliana/Garruk halves are the bonus.

**Top eight:**

1. `Garruk, Veiled Butcher` (M, {3}{B}{B}) — +2 gives −4/−1 every turn — repeatable removal. −2 is an edict that leaves you a 4/4 trampler. Anything of theirs that dies is exiled.
2. `Overwrite the Multiverse` (M, {4}{B}{B}) — Six-mana exile-all that empowers Jace once per creature swept. A wipe that refills your hand. Sealed sleeper.
3. `Liliana the Repentant` (R, {1}{B}) — A two-drop that mills two whenever another creature or walker enters, and reanimates one of them once. The W/B and U/B engine.
4. `Vraska's Final Mercy` (R, {B}{B}) — {B}{B}: destroy a creature or planeswalker for 2 life — or empower Jace 6. The cheapest hard removal in the set, with a second mode.
5. `Rise of the Deathbringer` (R, {4}{B}) — Instant: draw cards equal to your biggest creature's power, or −3/−3 to everything. Both modes are premium.
6. `Darklight Phoenix` (M, {3}{B}) — Four-mana 3/2 flying haste that returns from the graveyard whenever two creatures died this turn. Never stays dead in a sacrifice deck.
7. `Sanctum Lurker` (R, {2}{B}) — Your planeswalkers don't die at 0 loyalty — so the Jace token survives its own entry — and each gets +2: ping and gain. Turns every empower card on.
8. `Winter, Tormented Loner` (U, {2}{B}) — Three-mana edict on entry that grows with the creatures and walkers in your graveyard. Removal that becomes a finisher.

**Commons you'll see:** `Last Gasp` (C, {1}{B}) · `Silence the Echo` (C, {1}{B}) · `Void Extrapolator` (C, {1}{B}) · `Extended Absence` (C, {3}{B}) · `Screeching Soulbreaker` (C, {2}{B}) · `Rampart Hunter` (C, {3}{B})

#### Blue — 8.2

The format's mechanics are blue — the Jace token is blue, surveil and self-mill are blue — and blue is in both S-tier decks. It drops below black on one number: it cannot kill anything. Infinite Coursework is the only blue common that permanently stops a creature. Blue is the best partner and a poor colour to be in alone.

**Top eight:**

1. `The Theorist, Jace Beleren` (M, {2}{U}{U}) — You draw on every opponent's draw step; the +1 makes chump-blockers to keep it alive. Wins a stalled game by itself.
2. `Chandra, Chill of Compliance` (M, {1}{U}{U}) — Three-mana walker: +1 surveils and picks up a noncreature card, the other +1 makes {U} for noncreature spells, −X stuns a blocker. Card advantage for the spells deck.
3. `Jace, Reality Sculptor` (R, {3}{U}{U}) — +1 empowers by your Island count, so it builds its own battery; −3 makes attacking into you pointless for a turn.
4. `Variable Chaser` (R, {2}{U}) — Three-mana 2/3 flying prowess that enters prepared. A body, a spell and evasion on one card.
5. `Seasoned Cryomancer` (M, {1}{U}{U}) — Three-mana 2/2 that loots two and stuns a creature per nonland discard. Tempo and selection; recurs from the graveyard.
6. `Sphinx of False Conclusions` (R, {2}{U}{U}) — Four-mana 4/2 flash flier that loots on attack and copies itself when it dies. Two bodies and card selection.
7. `Lyra, Tolarian Archangel` (R, {1}{U}{U}) — Three-mana 3/3 flier that makes a 3/3 flying Angel each end step you've drawn three. Pairs with The Theorist and the Jace draw.
8. `Jace's Machinations` (R, {2}{U}) — Instant empower Jace 8 that lets you activate Jace at instant speed this turn. Eight loyalty for three mana.

**Commons you'll see:** `Semester Foreseer` (C, {3}{U}) · `Icy Reception` (C, {1}{U}) · `Surveillance Phantasm` (C, {1}{U}) · `Infinite Coursework` (C, {2}{U}) · `Mindseeker Oculus` (C, {2}{U}) · `Protege's Awakening` (C, {3}{U})

#### White — 7.9

Revised up once I found Memory Trap — an Oblivion Ring at common, played in every white deck in the real sealed sample. With two good removal commons, three instant-speed removal uncommons, token generation and the counters shell, white is a real colour and not a synergy-dependent one.

**Top eight:**

1. `Ajani Resolute` (M, {1}{W}) — Two-mana walker that gains loyalty whenever you gain life and makes a Pridemate. Wants a lifegain deck more than an aggro one.
2. `Liliana the Faultless` (R, {W}) — A one-drop that gains a life per body and discards to grant hexproof. Protects the bomb you splashed for.
3. `Enlightened Confidant` (M, {1}{W}) — Two-mana 2/1 lifelink that surveils each end step you've gained life and picks up cheap cards. A lifegain engine on a two-drop.
4. `Prophesied End` (U, {1}{W}) — Two-mana instant: destroy a creature; they draw only if it wasn't attacking. Kill blockers on your turn, attackers on theirs.
5. `Your Fate Ends Here` (U, {2}{W}) — Three-mana instant: destroy a creature or walker with mana value 3+, and surveil. Hits everything that matters.
6. `Memory Trap` (C, {2}{W}) — Oblivion Ring at common: exile any nonland permanent. Hits walkers and enchantments. White's best common.
7. `Lyra, Archangel of Dawn` (R, {2}{W}) — Three-mana 3/3 flier; every lifegain grows all your Angels. Lifegain deck top-end that flies.
8. `Kindred Judgment` (R, {5}{W}{W}) — Seven-mana one-sided wipe: name a type, everything else dies. Slow, but sealed games get there.

**Commons you'll see:** `Memory Trap` (C, {2}{W}) · `Graft Surgeon` (C, {2}{W}) · `Hexhaven Battalion` (C, {4}{W}{W}) · `Blossom-Blessed Angel` (C, {3}{W}) · `Surgical Precision` (C, {1}{W}) · `Fatehold Chronologist` (C, {1}{W/U})

#### Red — 7.2

Better than its archetype. Red's creature removal is second-best in the set — three commons, with Wrath of the Bloodmane premium — and Fulminous Forte is the best uncommon removal in any colour. The face-damage plan is the trap, not the colour. Be happy to end up here; don't start here.

**Top eight:**

1. `Chandra, Torch of Defiance` (M, {2}{R}{R}) — +1 for a card or 2 damage, +1 for {R}{R}, −3 kills a creature. Removal and card advantage on one permanent.
2. `Ajani Unrelenting` (M, {4}{R}{R}) — A Cadet on every activation, +1 for team haste, −3 is a one-sided sweep that spares your tokens. Six mana in a 16-land deck is the cost.
3. `Fulminous Forte` (U, {2}{R}) — Instant: 5 damage to a creature or walker, or 1 damage to everything they control. Red's best removal at any rarity.
4. `Curse-Marred Demon` (R, {2}{R}{R}) — Four-mana 4/4 flying trample that tutors on entry (then discards at random). The rate alone is a first pick.
5. `Identity Echo` (R, {2}{R}) — Repeatable: exile your creature or walker, reveal until you hit another, put it in. In a token deck it digs for your bomb every turn.
6. `Draconic Visitor` (R, {3}{R}{R}) — Five-mana 5/5 flier; any artifact token you'd make becomes a 5/5 Dragon instead. Every Heartwood in R/G is a Dragon.
7. `Master of Barbs` (R, {1}{R}) — Menace two-drop that pumps your team whenever an opponent takes noncombat damage. The payoff that makes B/R's pings matter.
8. `Pyre Rhymer` (R, {1}{R}{R}) — Three-mana 3/3 prowess that enters prepared. A body plus a spell in the prowess deck.

**Commons you'll see:** `Wrath of the Bloodmane` (C, {2}{R}) · `Awaken the Inferno` (C, {4}{R}) · `Hallway Heckler` (C, {2}{R}) · `Heartstring Puller` (C, {3}{R}) · `Skilled Battlecarver` (C, {1}{R}) · `Stingerquill Voxmancer` (U, {B/R})

#### Green — 6.9

Last, but closer than I first had it. Two removal commons, and Compel Brutality is the more interesting: its second mode has your planeswalker deal damage equal to its loyalty, which turns green's empower commons into a removal engine. Big bodies matter in long games; the top end is still beatable by card advantage.

**Top eight:**

1. `Garruk, Curse Breaker` (M, {3}{G}{G}) — Draws a card whenever a power-4+ creature enters, and −3 makes one. The card-advantage engine B/G otherwise lacks.
2. `Carnivorous Cultivator` (R, {1}{G}) — Two-mana 2/3 deathtouch that enters prepared and returns lands from the graveyard on damage. The best green two-drop.
3. `Hexhaven Invigorator` (M, {G}{G}{G}{G}) — {G}{G}{G}{G} 6/6 vigilance that ramps you whenever it's damaged. Mono-green only, and then a monster.
4. `Tarmogoyf` (M, {1}{G}) — Two mana for a body that scales with card types in all graveyards — in a self-mill format that's a 4/5 by turn four.
5. `Hungering Puppetbeast` (R, {3}{G}{G}) — Five-mana 5/5 artifact that makes a Heartwood and eats artifacts for counters and keywords. The R/G payoff that's also an enabler.
6. `Simulacrum Shaper` (R, {1}{G}{G}) — Three-mana 2/2 that ramps a land on entry and draws when it dies. Never a bad draw.
7. `Compel Brutality` (C, {1}{G}) — Instant fight-lite — or your planeswalker deals damage equal to its loyalty. With a 5-loyalty Jace it kills almost anything for two.
8. `Way of the Wildspeaker` (U, {4}{G}) — Empower 7 on entry; every walker gets −4 for a 4/4 trample Beast. The biggest single empower in the set.

**Commons you'll see:** `Compel Brutality` (C, {1}{G}) · `Sureshot Sower` (C, {1}{G}) · `Greenhouse Propagator` (C, {2}{G}) · `Arcane Amphisbaena` (C, {1}{G}) · `Bestial Incursion` (C, {3}{G}) · `Wrecking Gecko` (C, {4}{G})

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
**Echoed Pair legends:** *Liliana the Repentant* (B, `{1}{B}` 2/2 rare — mill two whenever another creature or planeswalker enters; exhaust `{5}{B}`: reanimate one) / *Liliana the Faultless* (W, `{W}` 1/1 rare — gain 1 life per body; discard to give hexproof). **Legendary creatures, not planeswalkers** — the one member of the Lorwyn Five who lost her spark. [CONFIRMED]

#### 4. B/G — Garruk's Bestiary · **7.5**
> *"Bring out fearsome creatures to hunt down your foes, combining deathtouch and trample to smash through any defenses!"* [CONFIRMED]

**Plan.** Value creatures, each with a benefit attached. Deathtouch + trample to break board stalls.

[EVAL] **The highest-floor deck in the format and the correct default when you open nothing.**
It asks for almost no synergy — good creatures are good creatures. Deathtouch is unusually well
positioned here: it profitably blocks the big Konstrari ramp payoffs and trades with prepared
creatures before they get value. Ceiling is capped because it has no engine; it just plays fair
Magic slightly better than you do. **Echoed Pair legends:** *Garruk, Curse Breaker* (G, `{3}{G}{G}` — draw when a power-4+ creature enters; −3 makes a 4/4 trample Beast) /
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
**Echoed Pair legends:** *Ajani Resolute* (W, `{1}{W}` — loyalty on every lifegain, −4 Pridemate; it wants Vigorbloom's lifegain as much as this deck) / *Ajani Unrelenting* (R, `{4}{R}{R}` — a Cadet per activation, +1 team haste, −3 one-sided sweep). [CONFIRMED]

#### 7. U/R — Chandra's Prowess · **6.7**
> *"Cast noncreature spells to trigger abilities and keep up the heat on your opponents."* [CONFIRMED]

**Plan.** Prowess bodies + a high noncreature count, with Thopters as a token sub-theme.
**Key card:** *Saheeli, Jewel of Avishkar*. **Echoed Pair legends:** *Chandra, Chill of Compliance* (U, `{1}{U}{U}` — +1 surveil and pick up a noncreature; +1 {U} for noncreature spells; −X stun) / *Chandra, Torch of Defiance* (R, `{2}{R}{R}` — the classic; −3 kills a creature). Chandra goes from red
*Chandra, Torch of Defiance* to mono-blue *Chandra, Chill of Compliance*. [CONFIRMED]

[EVAL] Prowess wants ~10 noncreature spells; a grindy format wants creature quality. That tension
caps the deck. It's excellent when the spells you find are **removal** (so your spell count and
your interaction count are the same cards) and mediocre when they're cantrips. **Also note:**
`Stingcaster Mage` — a reported two-mana red haste creature that **gives an instant or sorcery
flashback as it enters** — is effectively a red Snapcaster and is a genuine build-around for this
lane. [WATCH — rarity unverified]

#### 8. G/U — Jace's Mastery · **6.5**
> *"Keep empowering Jace to provide a steady flow of cards or pick your path to victory with cards that grant your planeswalkers abilities!"* [CONFIRMED]

**Echoed Pair legends:** none — **Jace did not split.** His echo is the Jace *token*; the archetype feeds it. The Jace cards are blue only: *The Theorist, Jace Beleren* (`{2}{U}{U}` mythic) and *Jace, Reality Sculptor* (`{3}{U}{U}` rare, +1 empowers by Island count). Green's share is the Way cycle and *Kiora of Salt and Sand*. [CONFIRMED]

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
  your uncastable 6- and 7-drops into your win conditions. **In sealed, go up to 18 lands and jam
  the top end.** (Heartwood only makes R or G — for a splash outside those colours you need the
  common duals or *Room of Refuge*, Section 4.5.)

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

### 9.3 Best cards by rarity  [EVAL — a read, not a measurement]

An earlier version of this section refused to rank commons: "there is no verified common-by-common
rating list, and I won't invent one." That was right when the card list was unverified. With every
card's oracle text in hand, a reasoned order is worth more than no order — **as long as it is labelled
as inference, which this is.** When Arena queues open on 29 September, GIH WR replaces every list here.

#### Mythics (26 in the set)

1. `Denzilore Fatehold` (M, {1}{W}{U}{U}) — Four-mana 3/4 flash flier; every scry or surveil puts a counter on your whole team, and the free Jace surveils fire it. Best of the five Sphinxes.
2. `Aerid Konstrari` (M, {1}{R}{G}{G}) — Four-mana 5/4 flier that makes a Heartwood on entry *and* on death, with a mana sink. Replaces itself twice.
3. `The Theorist, Jace Beleren` (M, {2}{U}{U}) — You draw on every opponent's draw step; the +1 makes chump-blockers to keep it alive. Wins a stalled game by itself.
4. `The Echoverse Fulcrum` (M, {2}) — Two-mana loot on entry, then a five-mana one-shot board wipe. Colourless, so every deck plays it — the wipe is the sealed bomb.
5. `Chandra, Torch of Defiance` (M, {2}{R}{R}) — +1 for a card or 2 damage, +1 for {R}{R}, −3 kills a creature. Removal and card advantage on one permanent.
6. `Garruk, Veiled Butcher` (M, {3}{B}{B}) — +2 gives −4/−1 every turn — repeatable removal. −2 is an edict that leaves you a 4/4 trampler. Anything of theirs that dies is exiled.
7. `Garruk, Curse Breaker` (M, {3}{G}{G}) — Draws a card whenever a power-4+ creature enters, and −3 makes one. The card-advantage engine B/G otherwise lacks.
8. `Overwrite the Multiverse` (M, {4}{B}{B}) — Six-mana exile-all that empowers Jace once per creature swept. A wipe that refills your hand. Sealed sleeper.
9. `Ingris Stingerquill` (M, {B}{R}{R}) — Every attacker pings each opponent. Turns a wide board into a clock, and makes the B/R deck real.
10. `Uldaros Theorix` (M, {3}{U}{B}{B}) — Five-mana 5/5 flier that recasts a card of each type from your graveyard for free. A bomb at threshold, merely very good before it.
11. `Ajani Unrelenting` (M, {4}{R}{R}) — A Cadet on every activation, +1 for team haste, −3 is a one-sided sweep that spares your tokens. Six mana in a 16-land deck is the cost.
12. `Ajani Resolute` (M, {1}{W}) — Two-mana walker that gains loyalty whenever you gain life and makes a Pridemate. Wants a lifegain deck more than an aggro one.

#### Rares (64)

1. `Vindictive Triumph` (R, {W}{B}{B}) — Three-mana instant: exile any creature or planeswalker, and if it cost three or less you get it for a turn first. Premium removal with a bonus.
2. `Vraska's Final Mercy` (R, {B}{B}) — {B}{B}: destroy a creature or planeswalker for 2 life — or empower Jace 6. The cheapest hard removal in the set, with a second mode.
3. `Jace, Reality Sculptor` (R, {3}{U}{U}) — +1 empowers by your Island count, so it builds its own battery; −3 makes attacking into you pointless for a turn.
4. `Liliana the Repentant` (R, {1}{B}) — A two-drop that mills two whenever another creature or walker enters, and reanimates one of them once. The W/B and U/B engine.
5. `Rise of the Deathbringer` (R, {4}{B}) — Instant: draw cards equal to your biggest creature's power, or −3/−3 to everything. Both modes are premium.
6. `Vraska, the Cutting Glare` (R, {B}{B}{G}) — Three-mana 4/4 deathtouch; with six lands it destroys any permanent on entry. A sealed finisher.
7. `Sanctum Lurker` (R, {2}{B}) — Your planeswalkers don't die at 0 loyalty — so the Jace token survives its own entry — and each gets +2: ping and gain. Turns every empower card on.
8. `Variable Chaser` (R, {2}{U}) — Three-mana 2/3 flying prowess that enters prepared. A body, a spell and evasion on one card.
9. `Liliana the Faultless` (R, {W}) — A one-drop that gains a life per body and discards to grant hexproof. Protects the bomb you splashed for.
10. `Curse-Marred Demon` (R, {2}{R}{R}) — Four-mana 4/4 flying trample that tutors on entry (then discards at random). The rate alone is a first pick.
11. `Carnivorous Cultivator` (R, {1}{G}) — Two-mana 2/3 deathtouch that enters prepared and returns lands from the graveyard on damage. The best green two-drop.
12. `Identity Echo` (R, {2}{R}) — Repeatable: exile your creature or walker, reveal until you hit another, put it in. In a token deck it digs for your bomb every turn.
13. `Draconic Visitor` (R, {3}{R}{R}) — Five-mana 5/5 flier; any artifact token you'd make becomes a 5/5 Dragon instead. Every Heartwood in R/G is a Dragon.
14. `Codie, Ravenous Codex` (R, {3}) — Copies every prepared spell you cast. Colourless, so any prepared deck can run it.

#### Uncommons (109)

1. `Konstrari Charm` (U, {R}{G}) — {R}{G}: 6 damage to a flier, or two counters and trample, or {C}{C}{C}. Three good modes at two mana.
2. `Fulminous Forte` (U, {2}{R}) — Instant: 5 damage to a creature or walker, or 1 damage to everything they control. Red's best removal at any rarity.
3. `Prophesied End` (U, {1}{W}) — Two-mana instant: destroy a creature; they draw only if it wasn't attacking. Kill blockers on your turn, attackers on theirs.
4. `Your Fate Ends Here` (U, {2}{W}) — Three-mana instant: destroy a creature or walker with mana value 3+, and surveil. Hits everything that matters.
5. `Theorix Charm` (U, {U}{B}) — {U}{B}: soft counter, −2/−2, or mill three and draw. Never dead.
6. `Winter, Tormented Loner` (U, {2}{B}) — Three-mana edict on entry that grows with the creatures and walkers in your graveyard. Removal that becomes a finisher.
7. `Saheeli, Jewel of Avishkar` (U, {2}{U}{R}) — A hasty 1/1 flying Thopter for every noncreature spell. The U/R deck on one card.
8. `Terminal Criticism` (U, {1}{B}) — {1}{B} instant: destroy a blue or red creature or walker. A hoser you maindeck when half the table is blue.
9. `Vigorbloom Vanguard` (U, {1}{G/W}) — Two-mana 2/2 that enters prepared (life and counters) and gives countered creatures vigilance. Hybrid, so mono-G or mono-W casts it.
10. `Paradox Shaper` (U, {1}{U/B}) — Re-prepares every upkeep: a self-mill spell every turn for two mana. The Theorix engine.
11. `Prudent Fateseer` (U, {1}{W/U}{W/U}) — Three-mana 1/4 that enters prepared; the first scry or surveil each turn pumps the team. A wall that attacks.
12. `Kiora of Salt and Sand` (U, {1}{G}{U}) — Activate a loyalty ability, then your attacker untaps and can't be blocked. Gives walkers −8 for an 8/8 hexproof.
13. `Way of the Deathbringer` (U, {2}{B}) — Empower 5 on entry, and every planeswalker gets −2: sacrifice a creature, make a 4/4 trample Beast. Outlet, payoff and mana-fixer clause in one card.
14. `Stingerquill Voxmancer` (U, {B/R}) — Hybrid one-drop with a prepared burn spell. Castable off Swamp or Mountain alone.
15. `Woodwork Prodigy` (U, {2}{R/G}) — Three-mana 3/3 that re-prepares every upkeep — a Heartwood every turn.
16. `Gallia, Tragic Host` (U, {1}{B}) — Two-mana menace that recurs itself by exiling a creature card from your graveyard. Never stays dead.

#### Commons (81)

1. `Memory Trap` (C, {2}{W}) — Oblivion Ring at common: exile any nonland permanent. Hits walkers and enchantments. White's best common.
2. `Last Gasp` (C, {1}{B}) — {1}{B} instant −3/−3. Kills most of the format's two- and three-drops on their upkeep, before a prepared copy is cast.
3. `Wrath of the Bloodmane` (C, {2}{R}) — Instant 4 damage to a creature or walker, two mana with a legend out. The best red common.
4. `Compel Brutality` (C, {1}{G}) — Instant fight-lite — or your planeswalker deals damage equal to its loyalty. With a 5-loyalty Jace it kills almost anything for two.
5. `Fatehold Chronologist` (C, {1}{W/U}) — Two-mana flier that enters prepared: a 2/2 token and a surveil attached. Most-played card in the real sealed sample.
6. `Silence the Echo` (C, {1}{B}) — {1}{B}: destroy a creature or walker; sacrifice a creature or pay three. Removal and a sacrifice outlet.
7. `Semester Foreseer` (C, {3}{U}) — Four-mana Fatehold prepared body: the 2/2-and-surveil spell on a bigger creature.
8. `Void Extrapolator` (C, {1}{B}) — Two-mana 2/2 that enters prepared (self-mill) and is a 3/3 at threshold. Enabler and payoff.
9. `Icy Reception` (C, {1}{U}) — Instant: soft-counter a creature, or −5/−0. Blue's best trick — it wins a combat or a tempo turn.
10. `Surveillance Phantasm` (C, {1}{U}) — Two-mana 2/3 flying vigilance that attacks whenever you've scried or surveilled. A wall on defence, a flier on offence.
11. `Theorix Metamage` (C, {2}{U/B}) — Hybrid three-mana flier that self-mills, has threshold and enters prepared. Four cards in one.
12. `Hexhaven Battalion` (C, {4}{W}{W}) — Three 2/2s plus empower 2, or cycles for a basic when you'd rather have a land. No bad draw.
13. `Extended Absence` (C, {3}{B}) — Four-mana instant exile that drains one. Answers anything, including a walker.
14. `Infinite Coursework` (C, {2}{U}) — Pacifism that also taps the creature, unprepares it and stops it untapping. Blue's only hard answer at common.
15. `Graft Surgeon` (C, {2}{W}) — 2/2 with a counter that hands its counters to another creature when it dies. Counters that never go away.
16. `Sureshot Sower` (C, {1}{G}) — Two-mana 3/1 reach that discards itself to kill a flier. Green's anti-air, on a body.


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
4. **Count your duals before you plan a splash — and your empower cards.** There are ten
   common duals, one for every pair, so the fixing exists; but all ten enter tapped unless a
   planeswalker is already on the battlefield. See Section 4.5. Heartwood adds R or G only.
   *Room of Refuge* makes any colour with no condition. **Go to 18 lands** if you're ramping
   to a real top end.
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
- [ ] **Heartwood adds R or G only.** It pays for a red or green splash, not any splash.
- [ ] **A dual enters untapped only if a planeswalker is *already* there** — one arriving the same turn doesn't count. This applies to all ten commons, Annex and Commons alike.
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
