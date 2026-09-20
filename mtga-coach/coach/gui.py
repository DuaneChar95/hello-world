"""Visual practice draft: real card images, hover for archetype and splash.

Real spoiled cards show their actual Scryfall art. Generated practice cards
have no art anywhere, so they are drawn as a plain card face with a PLACEHOLDER
stripe -- they are never dressed up to look like a real card.

Hovering any card fills the side panel with what it pairs with and whether you
can splash it. Clicking picks it.
"""
from __future__ import annotations

import textwrap
from pathlib import Path
from typing import Optional

try:
    import tkinter as tk
    from tkinter import font as tkfont
    HAVE_TK = True
except ImportError:                                    # pragma: no cover
    HAVE_TK = False

from .analysis import archetype_affinity, splash_advice
from .arenadb import CardInfo
from .art import ArtCache, HAVE_PIL, is_generated, placeholder_spec
from .model import Ratings, pool_summary
from .sim import DraftEngine, build_deck, grade_deck

BG = "#12161d"
BG2 = "#1b212b"
BG3 = "#242c38"
FG = "#e7ebf1"
MUTED = "#98a3b2"
ACCENT = "#4fb2bf"
GOOD = "#7fd3a8"
WARN = "#d5a25a"
STRETCH = "#c79bd8"
EASE = {"free": GOOD, "easy": GOOD, "hard": WARN, "unknown": MUTED}

CARD_W, CARD_H = 146, 204
COLS = 5


class DraftWindow:
    def __init__(self, engine: DraftEngine, art: ArtCache, scale: float = 1.0):
        if not HAVE_TK:
            raise RuntimeError(
                "tkinter is not available in this Python.\n"
                "  Windows/macOS python.org installers include it.\n"
                "  Homebrew:  brew install python-tk\n"
                "  Debian/Ubuntu:  sudo apt install python3-tk")
        self.eng = engine
        self.ratings = engine.ratings
        self.art = art
        self.cw = int(CARD_W * scale)
        self.ch = int(CARD_H * scale)
        self._images: dict[int, object] = {}      # grpid -> PhotoImage (kept alive)
        self._cells: list = []
        self._last_feedback: str = ""

        self.root = tk.Tk()
        self.root.title("MTGA Coach - Practice Draft")
        self.root.configure(bg=BG)
        self.f_h = tkfont.Font(family="Segoe UI", size=13, weight="bold")
        self.f_t = tkfont.Font(family="Segoe UI", size=10, weight="bold")
        self.f_b = tkfont.Font(family="Segoe UI", size=9)
        self.f_s = tkfont.Font(family="Segoe UI", size=8)
        self.f_c = tkfont.Font(family="Segoe UI", size=8, weight="bold")
        self._build()
        self.root.bind("<Escape>", lambda e: self._quit())
        self.refresh()

    # ---------------------------------------------------------------- chrome
    def _build(self) -> None:
        head = tk.Frame(self.root, bg=BG2)
        head.pack(fill="x")
        self.lbl_head = tk.Label(head, text="", bg=BG2, fg=ACCENT, font=self.f_h,
                                 anchor="w", padx=12, pady=8)
        self.lbl_head.pack(side="left")
        self.lbl_sub = tk.Label(head, text="", bg=BG2, fg=MUTED, font=self.f_s,
                                anchor="e", padx=12)
        self.lbl_sub.pack(side="right")

        body = tk.Frame(self.root, bg=BG)
        body.pack(fill="both", expand=True)

        self.grid_f = tk.Frame(body, bg=BG, padx=10, pady=10)
        self.grid_f.pack(side="left", fill="both", expand=True)

        side = tk.Frame(body, bg=BG2, width=340)
        side.pack(side="right", fill="y")
        side.pack_propagate(False)
        self.lbl_name = tk.Label(side, text="Hover a card", bg=BG2, fg=FG,
                                 font=self.f_h, anchor="w", justify="left",
                                 wraplength=312, padx=14, pady=12)
        self.lbl_name.pack(fill="x")
        self.lbl_meta = tk.Label(side, text="", bg=BG2, fg=MUTED, font=self.f_s,
                                 anchor="w", justify="left", wraplength=312, padx=14)
        self.lbl_meta.pack(fill="x")
        self.detail = tk.Frame(side, bg=BG2)
        self.detail.pack(fill="both", expand=True, padx=14, pady=10)

        foot = tk.Frame(self.root, bg=BG2)
        foot.pack(fill="x", side="bottom")
        self.lbl_pool = tk.Label(foot, text="", bg=BG2, fg=FG, font=self.f_s,
                                 anchor="w", justify="left", padx=12, pady=6,
                                 wraplength=1000)
        self.lbl_pool.pack(fill="x")
        self.lbl_fb = tk.Label(foot, text="", bg=BG2, fg=MUTED, font=self.f_s,
                               anchor="w", justify="left", padx=12,
                               wraplength=1000)
        self.lbl_fb.pack(fill="x", pady=(0, 8))

    # ------------------------------------------------------------ card faces
    def _photo(self, card: CardInfo):
        """A PhotoImage for a real card, or None to draw a placeholder."""
        if card.grpid in self._images:
            return self._images[card.grpid]
        path = self.art.cached(card)
        if not path:
            return None
        try:
            if HAVE_PIL:
                from PIL import Image, ImageTk
                im = Image.open(path).convert("RGB").resize(
                    (self.cw, self.ch), Image.LANCZOS)
                photo = ImageTk.PhotoImage(im)
            else:
                photo = tk.PhotoImage(file=str(path))
                factor = max(1, round(photo.width() / self.cw))
                if factor > 1:
                    photo = photo.subsample(factor, factor)
            self._images[card.grpid] = photo
            return photo
        except Exception:                              # noqa: BLE001
            return None

    def _draw_card(self, parent, card: CardInfo, index: int):
        cv = tk.Canvas(parent, width=self.cw, height=self.ch, bg=BG,
                       highlightthickness=1, highlightbackground=BG3, bd=0)
        photo = self._photo(card)
        if photo is not None:
            cv.create_image(self.cw // 2, self.ch // 2, image=photo)
        else:
            self._draw_face(cv, card)
        cv.create_text(6, 6, text=str(index + 1), anchor="nw", fill=ACCENT,
                       font=self.f_c)
        cv.bind("<Enter>", lambda e, c=card: self.show_detail(c))
        cv.bind("<Button-1>", lambda e, c=card: self.pick(c))
        return cv

    def _draw_face(self, cv, card: CardInfo) -> None:
        sp = placeholder_spec(card, self.ratings)
        w, h = self.cw, self.ch
        cv.create_rectangle(0, 0, w, h, fill=sp["bg"], outline="")
        cv.create_rectangle(6, 6, w - 6, 34, fill="", outline=sp["fg"])
        name = sp["name"]
        if len(name) > 20:
            name = name[:19] + "…"
        cv.create_text(11, 20, text=name, anchor="w", fill=sp["fg"], font=self.f_t)
        cv.create_text(w - 11, 20, text=sp["cost"], anchor="e", fill=sp["fg"],
                       font=self.f_s)
        cv.create_rectangle(6, 40, w - 6, h - 58, fill="", outline=sp["fg"])
        cv.create_text(w // 2, (40 + h - 58) // 2,
                       text=sp["colors"], fill=sp["fg"], font=("Segoe UI", 26, "bold"))
        cv.create_text(11, h - 50, text=sp["types"][:22], anchor="w", fill=sp["fg"],
                       font=self.f_s)
        if sp["tags"]:
            cv.create_text(11, h - 36, text=sp["tags"][:26], anchor="w",
                           fill=sp["fg"], font=self.f_s)
        if sp["generated"]:
            cv.create_rectangle(0, h - 22, w, h, fill=sp["fg"], outline="")
            cv.create_text(w // 2, h - 11, text="PLACEHOLDER · NOT A REAL CARD",
                           fill=sp["bg"], font=self.f_s)

    # ------------------------------------------------------------ side panel
    def show_detail(self, card: CardInfo) -> None:
        for w in self.detail.winfo_children():
            w.destroy()
        r = self.ratings
        cols = "".join(sorted(r.card_colors(card), key="WUBRG".index)) or "C"
        self.lbl_name.config(text=card.name.replace("°", ""))
        meta = f"{cols} · {card.cmc or '?'} mana · {(card.rarity or '?').title()}"
        if card.types:
            meta += f" · {card.types}"
        if is_generated(card):
            meta += "  ·  placeholder"
        self.lbl_meta.config(text=meta)

        sc = next((s for s in self.eng.scored if s.card.grpid == card.grpid), None)
        if sc is not None:
            self._section("IN YOUR POOL", f"Score {sc.score:.2f}",
                          [f"· {x}" for x in sc.reasons[:3]], ACCENT)
        note = r.note(card)
        if note:
            self._section("", "", [note], MUTED)

        aff = archetype_affinity(card, r)
        if aff:
            rows = []
            for a in aff[:3]:
                rows.append(f"{a['pair']}  {a['name']} — tier {a['tier']}")
                if a["why"]:
                    rows.append("     " + "; ".join(a["why"][:2]))
            self._section("PAIRS BEST WITH", "", rows, GOOD)

        sp = splash_advice(card, r)
        body = [sp["headline"], sp["detail"]] + list(sp.get("extra", []))
        if not sp.get("certain", True):
            body.append("(Pip count is a guess until the real card list is "
                        "imported.)")
        self._section("SPLASH", "", body, EASE.get(sp["ease"], MUTED))

    def _section(self, title: str, lead: str, rows: list[str], color: str) -> None:
        f = tk.Frame(self.detail, bg=BG2)
        f.pack(fill="x", pady=(0, 10), anchor="w")
        if title:
            tk.Label(f, text=title, bg=BG2, fg=color, font=self.f_c,
                     anchor="w").pack(fill="x")
        if lead:
            tk.Label(f, text=lead, bg=BG2, fg=FG, font=self.f_t,
                     anchor="w").pack(fill="x")
        for row in rows:
            tk.Label(f, text=row, bg=BG2, fg=MUTED, font=self.f_b, anchor="w",
                     justify="left", wraplength=300).pack(fill="x")

    # ---------------------------------------------------------------- render
    def refresh(self) -> None:
        for c in self._cells:
            c.destroy()
        self._cells = []
        if self.eng.done:
            return self._finish()

        pack = self.eng.current_pack()
        self.lbl_head.config(text=f"Pack {self.eng.pack_no}   Pick {self.eng.pick_no}")
        st = self.art.stats()
        self.lbl_sub.config(
            text=f"{len(pack)} cards · art {st['cached']} cached"
                 + ("" if HAVE_PIL else " · install Pillow for sharper art"))
        for i, card in enumerate(pack):
            cell = self._draw_card(self.grid_f, card, i)
            cell.grid(row=i // COLS, column=i % COLS, padx=4, pady=4)
            self._cells.append(cell)

        self.art.prefetch(pack, done=lambda c, p: self.root.after(0, self._art_ready))
        sm = pool_summary(self.eng.session.pool, self.ratings)
        colors = "  ".join(f"{k}{v}" for k, v in sm["colors"].items()) or "-"
        self.lbl_pool.config(
            text=f"{sm['picks']} picks   {colors}   ·   "
                 f"{sm['top_name']} ({sm['top_pair']}) tier {sm['tier']}   ·   "
                 f"interaction {sm['interaction']} (want 4+)   ·   {sm['verdict']}")
        self.lbl_fb.config(text=self._last_feedback)

    def _art_ready(self) -> None:
        """Art arrived from the network - redraw only if the pack is still up."""
        if not self.eng.done and self._cells:
            self.refresh()

    def pick(self, card: CardInfo) -> None:
        fb = self.eng.feedback(card.grpid)
        if fb:
            best, taken, loss = fb["best"], fb["taken"], fb["loss"]
            if loss <= 0.05:
                self._last_feedback = f"✓ {taken.card.name} — agrees with the model."
            else:
                self._last_feedback = (
                    f"{taken.card.name} ({taken.score:.2f}).  Model: "
                    f"{best.card.name} ({best.score:.2f}), −{loss}.  "
                    + "; ".join(best.reasons[:2]))
            if fb.get("style") and fb["style"] not in ("unknown", ""):
                self._last_feedback += f"   [{fb['style']}]"
        self.eng.pick(card.grpid)
        self._images.clear()
        self.refresh()

    def _finish(self) -> None:
        self.lbl_head.config(text="Draft complete")
        self.lbl_sub.config(text="")
        d = build_deck(self.eng.session.pool, self.ratings)
        lines = grade_deck(d, self.ratings)
        box = tk.Frame(self.grid_f, bg=BG)
        box.grid(row=0, column=0, sticky="nw")
        self._cells.append(box)
        for line in lines:
            tk.Label(box, text=textwrap.fill(line, 90), bg=BG, fg=FG,
                     font=self.f_b, anchor="w", justify="left").pack(fill="x", pady=1)
        deck = ", ".join(sorted(c.name.replace("°", "") for c in d["deck"]))
        tk.Label(box, text=textwrap.fill("Deck: " + deck, 90), bg=BG, fg=MUTED,
                 font=self.f_s, anchor="w", justify="left").pack(fill="x", pady=(10, 0))
        path = self.eng.finish()
        if path:
            tk.Label(box, text=f"saved to {path}\n"
                               "run  python run_overlay.py --review  to grade it",
                     bg=BG, fg=ACCENT, font=self.f_b, anchor="w",
                     justify="left").pack(fill="x", pady=(10, 0))

    def _quit(self) -> None:
        self.root.destroy()

    def run(self) -> None:
        self.root.mainloop()


def run_gui(base_ratings: Ratings, seed: Optional[int] = None, seats: int = 8,
            profile=None, art_enabled: bool = True, scale: float = 1.0) -> None:
    eng = DraftEngine(base_ratings, seed, seats, profile)
    art = ArtCache(setcode=base_ratings.raw.get("set", "fra").lower(),
                   enabled=art_enabled)
    DraftWindow(eng, art, scale=scale).run()
