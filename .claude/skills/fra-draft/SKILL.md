---
name: fra-draft
description: Limited coach for Magic's Reality Fracture (FRA) on MTG Arena. Use when the user is drafting or playing sealed FRA — evaluating a pick between cards, deciding which archetype to move into, reading whether a color is open, cutting a 40-card deck down, choosing land counts, or asking how empower Jace / prepared / Heartwood / threshold work in play. Triggers on "P1P1", "which pick", "what do I take", "is blue open", "build my sealed pool", "Hexhaven", "Fatehold", "Theorix", "Stingerquill", "Konstrari", "Vigorbloom", "empower Jace", "prepared", "Heartwood", or any Reality Fracture draft/sealed question.
---

# Reality Fracture (FRA) Limited Coach

Full reasoning lives in `reality-fracture/DRAFT-GUIDE.md`. This file is the fast path —
answer from it directly; read the guide only when the user asks *why* or wants depth.

**Answer in the shape the user needs under a pick timer: a pick, one line of reasoning,
and the signal it implies. Not an essay.**

## Set facts (confirmed)

- 290 cards: 71 commons, **109 uncommons**, 64 rares, 26 mythics. Power lives at uncommon.
- **Empower Jace N** — put N loyalty on your Jace token, or create one with 0 loyalty first.
  Abilities: **−1 surveil 1**, **−3 draw a card**. **No plus ability.** One token max via empower;
  extras stack loyalty. Tokens aren't legendary.
- **Prepared** — creature face + spell face. On becoming prepared, a copy of the spell goes to
  exile; casting it unprepares the creature. **Copy dies if the creature leaves the battlefield.**
  Can't re-prepare while already prepared.
- **Heartwood token** — red-and-green artifact, `{T}: Add {R} or {G}`. **Fixes an R or G splash
  only — it does nothing for a W, U or B splash.** (An earlier version of this file overstated
  this; correct the user if they repeat it.)
- **Annex lands** (common): Fatehold W/U, Theorix U/B, Stingerquill B/R, Konstrari R/G,
  Vigorbloom G/W. Tap for their two allied colours; **enter tapped unless you already control a
  planeswalker** — a Jace token counts, but one entering the same turn does not.
- **Threshold** — 7+ cards in your graveyard.
- Allied pairs = Hexhaven colleges. Enemy pairs = the Lorwyn Five.

## The ten archetypes

| Pair | Name | Theme | Draft tier | Sealed shift |
|---|---|---|---|---|
| U/B | **Theorix** — Esoteric Mathematics | Self-mill → threshold | **S** (8.6) | ▼ needs enabler density |
| W/U | **Fatehold** — Future History | Scry/surveil, 2/2 tokens | **S** (8.4) | ▬ |
| W/B | **Liliana's Attrition** | Sacrifice + recursion | **A** (7.8) | ▼ |
| B/G | **Garruk's Bestiary** | Value creatures, deathtouch+trample | **A** (7.5) | ▲ |
| G/W | **Vigorbloom** — Invasive Healing | Lifegain + +1/+1 counters | **A** (7.2) | ▲ |
| R/W | **Ajani's Army** | Counters aggro, equipment | **B** (6.9) | ▼▼▼ can't get the curve |
| U/R | **Chandra's Prowess** | Noncreature spells, Thopters | **B** (6.7) | ▼ |
| G/U | **Jace's Mastery** | Empower value, walker abilities | **B** (6.5) | ▬ |
| B/R | **Stingerquill** — Painful Words | Face burn | **C** (6.2) | ▼▼ |
| R/G | **Konstrari** — Constructive Arts | Heartwood ramp | **C** (6.0) | **▲▲▲▲ → 7.3, top-3 in sealed** |

**College prepared spells (C/U, shared within a college):**
Fatehold = 2/2 token + surveil · Theorix = self-mill · Stingerquill = damage to opponent ·
Konstrari = Heartwood token · Vigorbloom = lifegain + counters.

## Color order (prior)

**U 8.5 > B 8.0 > W 7.5 > G 7.0 > R 6.5.** Blue and black are the grindy-format colors.
Red is the trap — its face-damage plan is bad in a midrange format with a lifegain archetype.
Expect red to be the most open color by pack 3.

## Pick rubric — use this when the card is unknown

1. Bombs (the five **Elder Sphinxes**: Denzilore Fatehold, Uldaros Theorix, Ingris Stingerquill,
   Aerid Konstrari, Kwia Vigorbloom) and unanswered planeswalkers
2. **Instant-speed unconditional removal ≤3 mana** — kills a prepared creature before it casts = 2-for-1
3. **In-college prepared creature** with a real body
4. Any other removal
5. **Empower Jace 3** on a relevant body (≈ half a card)
6. Evasive 2–4 drops (this format stalls)
7. Out-of-college prepared creature — **rate the body only**
8. Empower Jace 1–2 (tiebreaker)
9. Threshold cards outside U/B — **treat the threshold text as absent**
10. Face-damage payoffs outside a genuinely fast B/R — the format's biggest trap

**Empower math:** empower 1 ≈ 0.15 cards, 2 ≈ 0.3, 3 ≈ 0.5–0.7. ×1.3 in U/B and W/U
(surveil also feeds payoffs); ×0.7 in R/W and B/R (deferred value is bad when you're the beatdown).

## Signal reading

- The **college prepared commons are the most reliable signal in the format** — they're the backbone
  commons of five archetypes. Two late Fatehold creatures = W/U is open.
- Late gold uncommons mean less than usual: the Echoed Pair slot floods packs with uncommons.
- Only ~14 commons per color. **You cannot fill a deck from the back half of packs** — take
  playables over speculation earlier than in a normal set.
- Default lane when lost: **B/G Garruk's Bestiary** (highest floor, least synergy needed).
  Lane to avoid unless screaming: **B/R Stingerquill**.

## Deckbuilding targets

|  | Draft | Sealed |
|---|---|---|
| Creatures | 15–17 | 15–17 |
| Interaction | **4+, prefer instants** | 3+ |
| Lands | 17 | 17 (**18** with Heartwood ramp + 6-drop top end) |
| 2-drops | 5–6 (7+ for R/W, B/R) | 4–5 |
| Curve peak | 3 | 3–4 |

**Sealed build order:** find bombs → build the deck your bombs are in (not the best synergy) →
count removal across all five colors and let that drive color choice → treat Heartwood as **fixing
for a splash**, not just ramp → be slower than feels right.

**Theorix check:** 5+ self-mill sources or the threshold payoffs are dead.
**Empower check:** 4+ empower cards = a real engine; 1–2 = incidental.

## Play patterns (say these when relevant)

- **Spend the prepared copy every turn cycle** on an upkeep-repreparer. An unspent copy is deleted,
  not saved — the creature can't re-prepare while already prepared.
- **Hold instant removal for their upkeep** to deny a prepared spell; kill prepared creatures
  *before* the copy is cast.
- **Spend Jace loyalty immediately when under pressure**; bank only when stable — a Jace that dies
  with counters on it wasted them.
- **−1 surveil three times before −3 draw.** Surveil is the efficient rate.
- **Don't attack their Jace** unless it's winning them the game; take the life total.
- **Your removal can point at planeswalkers** — FRA has more than any set since War of the Spark.

## Three colours

**There is no enemy-colour dual in this set at any rarity.** Both dual cycles (common Annexes,
rare Portal slowlands) are allied only. That drives everything:

- A dual sharing one colour with your pair is a **free splash land** — never a dead draw.
- So the supported three-colour decks are the **five shards** (contiguous arcs of the wheel).
  **Wedges are not supported** — one Annex, and it doesn't bridge.
- Each college pair reaches two third colours: WU→+B/+G, UB→+W/+R, BR→+U/+G, RG→+B/+W, GW→+R/+U.
- **Enemy pairs improve their mana by adding the bridge colour**, because it turns two half-dead
  Annexes into perfect duals: WB+U=Esper, UR+B=Grixis, BG+R=Jund, RW+G=Naya, GU+W=Bant.
- **Price of entry is two Annexes.** One is a maybe; none means play two colours.
- Annexes are taplands turns 1–3 and duals from turn 4, so three colours is a midrange plan.
  R/W Ajani's Army should almost never splash.
- Splash bombs, premium removal and expensive cards. Never a two-drop. Single pip = 2–3 sources;
  double pip is a main colour, not a splash.

## Practice

The user can draft without Arena: `python run_overlay.py --practice` (8-person
pod with bots that cut colours) or `--practice-sealed`. Cards marked with a
degree sign are generated placeholders shaped like FRA cards, not real spoilers
- never present them as real cards. Practice drafts feed the same review and
playstyle pipeline.

## Playstyle

The desktop app (`mtga-coach/`) profiles the user from their saved drafts:
`python run_overlay.py --playstyle`. If they ask about their tendencies, habits,
or which picks are in-character, point them there rather than guessing — it
measures colour bias against what they actually saw, and separates preferences
from habits that cost measurable pick loss. Never characterise their playstyle
from memory or from a single draft.

## Honesty rules for this skill

- These numbers are a **pre-release prior**, not data. The set releases 2026-10-02; Arena queues
  open 2026-09-29. **The moment 17Lands GIH WR exists, it overrides everything here** — say so.
- Rarities for most named cards are **unverified**. If the user states a card's real text or
  rarity, trust the user over this file and say what changes.
- If asked about a card not listed here, **say you don't know it** and score it with the rubric
  above from the text the user gives you. Never invent card text or ratings.
