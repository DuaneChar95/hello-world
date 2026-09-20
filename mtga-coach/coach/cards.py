"""A playable card pool for practice, shaped like Reality Fracture.

The set is not out yet, so a faithful practice pool cannot be built from real
cards -- only ~46 are known. This module does the honest thing instead:

  * every REAL card from data/fra_ratings.json is seeded in, at its real rarity
  * the rest of the pool is generated from the format's actual mechanical
    vocabulary (college prepared creatures, empower Jace, Heartwood, threshold,
    removal, evasion) at the set's real rarity distribution

Generated cards are marked with a degree sign and are clearly labelled in the
UI. They are placeholders, not predictions -- no claim is made that any of them
will exist.

This still trains the things that actually decide drafts: reading signals,
committing at the right time, curve, interaction counts, archetype fit, and
applying the pick rubric. None of those are card knowledge. When the real card
list lands, swap this generator for it and everything downstream is unchanged.
"""
from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Optional

from .arenadb import CardInfo
from .model import Ratings

SYNTH = "°"          # marks a generated placeholder

# Set composition, matched to the real thing: 71 / 109 / 64 / 26.
TARGET = {"common": 71, "uncommon": 109, "rare": 64, "mythic": 26}

COLLEGE = {"WU": "Fatehold", "UB": "Theorix", "BR": "Stingerquill",
           "RG": "Konstrari", "GW": "Vigorbloom"}
COLLEGE_TAG = {"WU": "prepared_fatehold", "UB": "prepared_theorix",
               "BR": "prepared_stingerquill", "RG": "prepared_konstrari",
               "GW": "prepared_vigorbloom"}

# Flavour vocabulary, per colour, used to name generated cards.
NOUNS = {
    "W": ["Proctor", "Bursar", "Archivist", "Sentinel", "Chorister", "Warden",
          "Acolyte", "Invigilator", "Beadle", "Herald"],
    "U": ["Fateseer", "Theorist", "Cartographer", "Extrapolator", "Scryer",
          "Lecturer", "Auditor", "Diviner", "Annotator", "Sophist"],
    "B": ["Reclaimer", "Grudgekeeper", "Mortician", "Ledgerman", "Whisperer",
          "Exhumer", "Debtor", "Nihilist", "Gravewright", "Censor"],
    "R": ["Heckler", "Firebrand", "Wordsmith", "Provocateur", "Kindler",
          "Ranter", "Sparkwright", "Agitator", "Barker", "Combustor"],
    "G": ["Herbalist", "Grafter", "Rootspeaker", "Cultivator", "Beastwarden",
          "Propagator", "Surgeon", "Bloomwright", "Thornkeeper", "Verdurist"],
}
ADJ = {
    "W": ["Dutiful", "Tenured", "Lawbound", "Radiant", "Steadfast", "Prudent"],
    "U": ["Recursive", "Theoretical", "Paradox", "Liminal", "Indexed", "Tacit"],
    "B": ["Sunken", "Indebted", "Hollow", "Vengeful", "Unmarked", "Cadaverous"],
    "R": ["Reckless", "Blistering", "Caustic", "Unhinged", "Searing", "Brazen"],
    "G": ["Overgrown", "Invasive", "Sprouting", "Rooted", "Untamed", "Grafted"],
}
SPELL = {
    "W": ["Censure", "Binding Writ", "Dismissal Notice", "Final Exam", "Reprimand"],
    "U": ["Thesis Revision", "Retraction", "Marginalia", "Errata", "Footnote"],
    "B": ["Expulsion", "Blood Ledger", "Failing Grade", "Severance", "Culling"],
    "R": ["Detention Blast", "Heated Rebuttal", "Combustion", "Outburst", "Flare"],
    "G": ["Grafting", "Overgrowth", "Field Study", "Regimen", "Wild Draft"],
}


@dataclass
class PoolCard:
    info: CardInfo
    grade: float
    tags: list[str]
    real: bool = False

    @property
    def name(self) -> str:
        return self.info.name


class CardPool:
    """The full set, addressable by rarity, for pack generation."""

    def __init__(self, ratings: Ratings, seed: int = 20261002):
        self.ratings = ratings
        self.rng = random.Random(seed)
        self.by_rarity: dict[str, list[PoolCard]] = {k: [] for k in TARGET}
        self.all: list[PoolCard] = []
        self._next_id = 900000
        self._seed_real()
        self._generate()

    # -- construction ---------------------------------------------------
    def _add(self, name, colors, rarity, cmc, types, grade, tags, real=False) -> PoolCard:
        self._next_id += 1
        c = PoolCard(CardInfo(self._next_id, name, colors, rarity, "FRA", cmc, types),
                     round(grade, 2), list(tags), real)
        self.by_rarity.setdefault(rarity, []).append(c)
        self.all.append(c)
        return c

    def _seed_real(self) -> None:
        for name, e in self.ratings.cards.items():
            rarity = (e.get("rarity") or "uncommon").lower()
            if rarity not in TARGET:
                rarity = "uncommon"
            tags = list(e.get("tags", []))
            if "land" in tags:
                self._add(name, "", rarity, 0, "Land",
                          float(e.get("grade", 2.2)), tags, real=True)
                continue
            cmc = self._infer_cmc(tags, rarity)
            types = "Creature" if self._is_creature(tags, name) else "Instant"
            self._add(name, e.get("colors", ""), rarity, cmc, types,
                      float(e.get("grade", 3.0)), tags, real=True)

    def _infer_cmc(self, tags, rarity) -> int:
        if "bomb" in tags:
            return self.rng.choice([4, 4, 5])
        if any(t.startswith("removal") for t in tags):
            return self.rng.choice([2, 2, 3])
        if "aggro" in tags or "haste" in tags:
            return self.rng.choice([1, 2, 2])
        if "bigcreature" in tags:
            return self.rng.choice([5, 6])
        return self.rng.choice([2, 3, 3, 4])

    @staticmethod
    def _is_creature(tags, name) -> bool:
        if any(t in tags for t in ("prepared", "bigcreature", "flying", "deathtouch",
                                   "haste", "aggro", "bomb")):
            return True
        return not any(t in tags for t in ("removal", "removal_instant_cheap",
                                           "boardwipe", "empower", "empower3"))

    def _name(self, color: str, kind: str) -> str:
        r = self.rng
        if kind == "spell":
            base = r.choice(SPELL[color])
            if r.random() < 0.4:
                base = f"{r.choice(ADJ[color])} {base}"
        else:
            base = f"{r.choice(ADJ[color])} {r.choice(NOUNS[color])}"
        return base + SYNTH

    def _unique(self, color, kind, taken: set) -> str:
        for _ in range(60):
            n = self._name(color, kind)
            if n not in taken:
                taken.add(n)
                return n
        n = f"{self._name(color, kind)} {len(taken)}"
        taken.add(n)
        return n

    def _generate(self) -> None:
        taken = {c.name for c in self.all}
        r = self.rng
        colors = "WUBRG"

        # ---- commons -------------------------------------------------
        need = TARGET["common"] - len(self.by_rarity["common"])
        per_color = max(0, need) // 5
        for col in colors:
            plan = self._common_plan(col)
            for cmc, types, grade, tags, kind in plan[:per_color]:
                self._add(self._unique(col, kind, taken), col, "common", cmc, types,
                          grade + r.uniform(-0.15, 0.15), tags)
        while len(self.by_rarity["common"]) < TARGET["common"]:
            self._add(f"Heartwood Sapling{SYNTH} {len(self.by_rarity['common'])}", "",
                      "common", 2, "Artifact", 1.9, ["heartwood"])

        # ---- uncommons: mono, then two gold per archetype ------------
        for pair, meta in self.ratings.archetypes.items():
            wants = meta.get("wants", [])
            for i in range(2):
                tags = ["prepared", COLLEGE_TAG[pair]] if pair in COLLEGE and i == 0 \
                    else list(wants[:2])
                self._add(f"{COLLEGE.get(pair, meta['name'].split()[0])} "
                          f"{r.choice(NOUNS[pair[i % 2]])}{SYNTH}",
                          pair, "uncommon", r.choice([3, 3, 4]), "Creature",
                          3.3 + r.uniform(-0.2, 0.3), tags)
        need = TARGET["uncommon"] - len(self.by_rarity["uncommon"])
        per_color = max(0, need) // 5
        for col in colors:
            for _ in range(per_color):
                cmc, types, grade, tags, kind = r.choice(self._uncommon_plan(col))
                self._add(self._unique(col, kind, taken), col, "uncommon", cmc, types,
                          grade + r.uniform(-0.2, 0.2), tags)
        while len(self.by_rarity["uncommon"]) < TARGET["uncommon"]:
            self._add(f"Echo Relic{SYNTH} {len(self.by_rarity['uncommon'])}", "",
                      "uncommon", 3, "Artifact", 2.7, ["artifact"])

        # ---- rares and mythics ---------------------------------------
        for rarity, lo, hi in (("rare", 3.0, 4.3), ("mythic", 3.8, 4.8)):
            while len(self.by_rarity[rarity]) < TARGET[rarity]:
                col = r.choice(colors) if r.random() < 0.8 else \
                    "".join(r.sample(colors, 2))
                is_removal = r.random() < 0.25
                tags = ["removal"] if is_removal else \
                    (["bomb"] if r.random() < 0.35 else ["value"])
                if r.random() < 0.12:
                    tags = ["boardwipe"]
                self._add(self._unique(col[0], "spell" if is_removal else "creature", taken),
                          col, rarity, r.choice([3, 4, 4, 5]),
                          "Instant" if is_removal else "Creature",
                          r.uniform(lo, hi), tags)

    def _common_plan(self, col: str):
        """(cmc, types, grade, tags, name-kind) - the shape of a colour's commons."""
        removal_depth = {"B": 3, "R": 3, "W": 2, "G": 1, "U": 1}[col]
        plan = []
        for i in range(removal_depth):
            instant = i == 0
            plan.append((2 if instant else 3, "Instant",
                         3.3 if instant else 2.9,
                         ["removal_instant_cheap"] if instant else ["removal"], "spell"))
        plan += [
            (1, "Creature", 2.4, ["aggro"], "creature"),
            (2, "Creature", 2.8, ["aggro"], "creature"),
            (2, "Creature", 2.9, ["empower"], "creature"),
            (3, "Creature", 3.0, ["flying"] if col in "WU" else ["value"], "creature"),
            (3, "Creature", 3.1, ["prepared", self._college_tag_for(col)], "creature"),
            (4, "Creature", 2.9, ["value"], "creature"),
            (4, "Creature", 2.8, ["flying"] if col in "WU" else ["deathtouch"], "creature"),
            (5, "Creature", 2.7, ["bigcreature"], "creature"),
            (2, "Instant", 2.6, ["empower3"], "spell"),
            (3, "Instant", 2.5, ["threshold"] if col in "UB" else ["counters"], "spell"),
            (2, "Creature", 2.5, ["selfmill"] if col in "UB" else ["lifegain"], "creature"),
            (3, "Creature", 2.7, ["heartwood"] if col in "RG" else ["counters"], "creature"),
        ]
        self.rng.shuffle(plan)
        return plan

    @staticmethod
    def _college_tag_for(col: str) -> str:
        for pair, tag in COLLEGE_TAG.items():
            if col in pair:
                return tag
        return "prepared"

    def _uncommon_plan(self, col: str):
        return [
            (2, "Instant", 3.5, ["removal_instant_cheap"], "spell"),
            (3, "Instant", 3.2, ["removal"], "spell"),
            (3, "Creature", 3.3, ["flying"] if col in "WU" else ["deathtouch"], "creature"),
            (2, "Creature", 3.1, ["aggro", "counters"], "creature"),
            (4, "Creature", 3.2, ["value"], "creature"),
            (5, "Creature", 3.0, ["bigcreature"], "creature"),
            (3, "Creature", 3.1, ["prepared", self._college_tag_for(col)], "creature"),
            (2, "Instant", 2.9, ["empower3"], "spell"),
        ]

    # -- packs -----------------------------------------------------------
    def make_pack(self, rng: random.Random) -> list[PoolCard]:
        """14 playable cards, weighted toward uncommons the way FRA is."""
        pack: list[PoolCard] = []
        pack.append(rng.choice(self.by_rarity["mythic" if rng.random() < 0.125
                                              else "rare"]))
        pack += rng.sample(self.by_rarity["uncommon"], 4)
        pack += rng.sample(self.by_rarity["common"], 9)
        rng.shuffle(pack)
        return pack

    def index(self) -> dict[int, PoolCard]:
        return {c.info.grpid: c for c in self.all}

    def ratings_overlay(self) -> dict:
        """Grades/tags for generated cards, so the scorer knows them."""
        return {c.name: {"grade": c.grade, "colors": c.info.colors,
                         "rarity": c.info.rarity, "tags": c.tags,
                         "note": "" if c.real else "generated practice card"}
                for c in self.all}
