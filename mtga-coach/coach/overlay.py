"""Always-on-top HUD.

Deliberately thin: all the thinking happens in model.py. This file only draws
what a DraftSession already decided, and pumps a queue that a background log
watcher fills.

Arena must be in Windowed or Borderless mode -- an exclusive-fullscreen game
will paint over any other window, which is a platform rule, not a bug here.
"""
from __future__ import annotations

import queue
import threading
from typing import Optional

try:
    import tkinter as tk
    from tkinter import font as tkfont
    HAVE_TK = True
except ImportError:                                   # pragma: no cover
    HAVE_TK = False

from .session import DraftSession

BG = "#12161d"
BG2 = "#1b212b"
FG = "#e7ebf1"
MUTED = "#98a3b2"
ACCENT = "#4fb2bf"
GOOD = "#7fd3a8"
WARN = "#d5a25a"
TIER = {"S": "#8ad6e0", "A": "#4fb2bf", "B": "#2e8b99", "C": "#1e6673"}
STRETCH = "#c79bd8"


class Overlay:
    def __init__(self, session: DraftSession, evq: "queue.Queue", title: str = "MTGA Coach - FRA",
                 alpha: float = 0.93, frameless: bool = False, topmost: bool = True):
        if not HAVE_TK:
            raise RuntimeError(
                "tkinter is not available in this Python.\n"
                "  Windows/macOS python.org installers include it.\n"
                "  Homebrew:  brew install python-tk\n"
                "  Debian/Ubuntu:  sudo apt install python3-tk")
        self.session = session
        self.q = evq
        self.root = tk.Tk()
        self.root.title(title)
        self.root.configure(bg=BG)
        self.root.geometry("380x560+40+40")
        self.root.minsize(300, 340)
        if topmost:
            self.root.attributes("-topmost", True)
        try:
            self.root.attributes("-alpha", alpha)
        except tk.TclError:
            pass
        if frameless:
            self.root.overrideredirect(True)
            self._enable_drag(self.root)

        self.f_h = tkfont.Font(family="Segoe UI", size=11, weight="bold")
        self.f_b = tkfont.Font(family="Segoe UI", size=9)
        self.f_s = tkfont.Font(family="Segoe UI", size=8)
        self.f_m = tkfont.Font(family="Consolas", size=9)

        self._build()
        self.root.bind("<Escape>", lambda e: self.root.destroy())
        self.root.after(200, self._pump)

    # -- chrome ---------------------------------------------------------
    def _enable_drag(self, w) -> None:
        def down(e):
            w._dx, w._dy = e.x, e.y
        def move(e):
            w.geometry(f"+{e.x_root - getattr(w, '_dx', 0)}+{e.y_root - getattr(w, '_dy', 0)}")
        w.bind("<Button-1>", down)
        w.bind("<B1-Motion>", move)

    def _build(self) -> None:
        top = tk.Frame(self.root, bg=BG2)
        top.pack(fill="x")
        self.lbl_head = tk.Label(top, text="waiting for a pack...", bg=BG2, fg=ACCENT,
                                 font=self.f_h, anchor="w", padx=10, pady=6)
        self.lbl_head.pack(side="left", fill="x", expand=True)
        tk.Button(top, text="x", command=self.root.destroy, bg=BG2, fg=MUTED,
                  bd=0, highlightthickness=0, font=self.f_s,
                  activebackground=BG2, activeforeground=FG).pack(side="right", padx=6)
        self._enable_drag(top)
        self._enable_drag(self.lbl_head)

        self.picks = tk.Frame(self.root, bg=BG)
        self.picks.pack(fill="both", expand=True, padx=8, pady=(8, 4))

        rest = tk.Frame(self.root, bg=BG)
        rest.pack(fill="x", padx=8)
        self.lbl_rest = tk.Label(rest, text="", bg=BG, fg=MUTED, font=self.f_s,
                                 anchor="w", justify="left", wraplength=350)
        self.lbl_rest.pack(fill="x")

        bot = tk.Frame(self.root, bg=BG2)
        bot.pack(fill="x", side="bottom")
        self.lbl_pool = tk.Label(bot, text="pool: empty", bg=BG2, fg=FG, font=self.f_s,
                                 anchor="w", justify="left", wraplength=360, padx=10, pady=6)
        self.lbl_pool.pack(fill="x")
        self.lbl_foot = tk.Label(bot, text="", bg=BG2, fg=MUTED, font=self.f_s,
                                 anchor="w", padx=10, pady=(0, 6))
        self.lbl_foot.pack(fill="x")

    # -- rendering ------------------------------------------------------
    def _render(self) -> None:
        s = self.session
        for w in self.picks.winfo_children():
            w.destroy()

        if s.current_scored:
            mode = "SEALED POOL" if s.pool.mode == "sealed" else f"PACK {s.pack_number}  PICK {s.pick_number}"
            self.lbl_head.config(text=mode)
            for i, sc in enumerate(s.current_scored[:3]):
                row = tk.Frame(self.picks, bg=BG2 if i == 0 else BG)
                row.pack(fill="x", pady=(0, 4))
                col = GOOD if i == 0 else FG
                head = tk.Frame(row, bg=row["bg"])
                head.pack(fill="x", padx=8, pady=(5, 0))
                tk.Label(head, text=f"{i + 1}.", bg=row["bg"], fg=MUTED,
                         font=self.f_m).pack(side="left")
                tk.Label(head, text=f" {sc.card.name}", bg=row["bg"], fg=col,
                         font=self.f_h if i == 0 else self.f_b,
                         anchor="w", justify="left", wraplength=250).pack(side="left", fill="x", expand=True)
                tk.Label(head, text=f"{sc.score:.2f}", bg=row["bg"], fg=ACCENT,
                         font=self.f_m).pack(side="right")
                why = "; ".join(sc.reasons[:2])
                if i == 0 and (s.annotation or {}).get("default_is_stretch"):
                    tk.Label(row, text="NOT YOUR USUAL PICK - best card here is one you "
                                       "normally pass", bg=row["bg"], fg=STRETCH,
                             font=self.f_s, anchor="w", justify="left",
                             wraplength=340).pack(fill="x", padx=8)
                tk.Label(row, text=why, bg=row["bg"], fg=MUTED, font=self.f_s,
                         anchor="w", justify="left", wraplength=340).pack(fill="x", padx=8, pady=(0, 5))
            st = (s.annotation or {}).get("stretch")
            if st is not None and st.card.grpid not in [x.card.grpid for x in s.current_scored[:3]]:
                row = tk.Frame(self.picks, bg=BG, highlightbackground=STRETCH,
                               highlightthickness=1)
                row.pack(fill="x", pady=(2, 4))
                head = tk.Frame(row, bg=BG)
                head.pack(fill="x", padx=8, pady=(5, 0))
                tk.Label(head, text="STRETCH", bg=BG, fg=STRETCH,
                         font=self.f_s).pack(side="left")
                tk.Label(head, text=f" {st.card.name}", bg=BG, fg=FG, font=self.f_b,
                         anchor="w", justify="left", wraplength=230).pack(side="left", fill="x", expand=True)
                tk.Label(head, text=f"{st.score:.2f}", bg=BG, fg=STRETCH,
                         font=self.f_m).pack(side="right")
                tk.Label(row, text="strong, but not the card you usually take",
                         bg=BG, fg=MUTED, font=self.f_s, anchor="w",
                         justify="left", wraplength=340).pack(fill="x", padx=8, pady=(0, 5))
                excl = {st.card.grpid}
            else:
                excl = set()
            rest = [x for x in s.current_scored[3:] if x.card.grpid not in excl]
            if rest:
                self.lbl_rest.config(text="then: " + " · ".join(
                    f"{r.card.name} {r.score:.1f}" for r in rest[:10]))
            else:
                self.lbl_rest.config(text="")
        else:
            self.lbl_head.config(text="waiting for a pack...")
            self.lbl_rest.config(text="")
            tk.Label(self.picks,
                     text="Open a draft or sealed event in Arena.\n\n"
                          "If nothing appears:\n"
                          "  Options > Account > Detailed Logs\n"
                          "  (Plugin Support) must be ON,\n"
                          "  then restart Arena.\n\n"
                          "Picks are graded against your own\n"
                          "playstyle once you have a few drafts:\n"
                          "  python run_overlay.py --playstyle",
                     bg=BG, fg=MUTED, font=self.f_b, justify="left",
                     anchor="w").pack(fill="x", padx=4, pady=6)

        sm = s.summary()
        if sm["picks"]:
            colors = " ".join(f"{k}{v}" for k, v in sm["colors"].items())
            tier = sm.get("tier", "")
            self.lbl_pool.config(
                text=f"{sm['picks']} picks   {colors}\n"
                     f"{sm['top_name']} ({sm['top_pair']}) {('tier ' + tier) if tier else ''}\n"
                     f"{sm['verdict']}",
                fg=TIER.get(tier, FG))
            foot = f"interaction {sm['interaction']} (want 4+)   creatures {sm['creatures']}"
            if self.session.profile is not None:
                foot += f"\n{self.session.profile.label()} · {self.session.profile.confidence}"
            self.lbl_foot.config(text=foot)
        else:
            self.lbl_pool.config(text="pool: empty", fg=FG)
            self.lbl_foot.config(text="")

    # -- event pump -----------------------------------------------------
    def _pump(self) -> None:
        dirty = False
        try:
            while True:
                fn = self.q.get_nowait()
                try:
                    if fn():
                        dirty = True
                except Exception:                      # noqa: BLE001 - never kill the UI
                    pass
        except queue.Empty:
            pass
        if dirty:
            self._render()
        self.root.after(250, self._pump)

    def run(self) -> None:
        self._render()
        self.root.mainloop()
