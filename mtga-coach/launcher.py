#!/usr/bin/env python3
"""The window you get when you double-click MTGA Coach.

An executable that demands command-line arguments is a bad executable, so this
is the entry point: a menu of what the app does, with the terminal-only modes
opening their own console window.
"""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

try:
    import tkinter as tk
    from tkinter import filedialog, font as tkfont, messagebox
except ImportError:                                        # pragma: no cover
    sys.exit("tkinter is required.\n"
             "  Windows/macOS python.org installers include it.\n"
             "  Homebrew: brew install python-tk   Debian: apt install python3-tk")

BG, BG2, BG3 = "#12161d", "#1b212b", "#242c38"
FG, MUTED, ACCENT, GOOD = "#e7ebf1", "#98a3b2", "#4fb2bf", "#7fd3a8"

MODES = [
    ("Practice draft", "cards", ["--practice", "--gui"],
     "An 8-person pod with card images. Hover for archetype and splash advice."),
    ("Practice draft (terminal)", "text", ["--practice"],
     "The same pod, faster to read. 'i 3' inspects a card."),
    ("Practice sealed", "text", ["--practice-sealed"],
     "Six packs. Pick your colours before the model shows its build."),
    ("Trainer drills", "text", ["--drills"],
     "Fifteen questions on the decisions this format actually asks."),
    ("Quiz my own packs", "text", ["--quiz", "--hard"],
     "Replays the picks you got wrong and makes you choose again."),
    ("Review my drafts", "text", ["--review"],
     "Grades every pick and reports your patterns."),
    ("My playstyle", "text", ["--playstyle"],
     "How you draft, what it costs you, and what would stretch you."),
    ("Live Arena overlay", "gui", ["--overlay"],
     "Reads Arena's log during a real draft. Needs Detailed Logs enabled."),
]


class Launcher:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("MTGA Coach")
        self.root.configure(bg=BG)
        self.root.geometry("470x600")
        self.root.minsize(420, 520)
        ico = HERE / "assets" / "mtga-coach.ico"
        if ico.exists():
            try:
                self.root.iconbitmap(default=str(ico))
            except tk.TclError:
                pass
        self.f_h = tkfont.Font(family="Segoe UI", size=15, weight="bold")
        self.f_t = tkfont.Font(family="Segoe UI", size=10, weight="bold")
        self.f_b = tkfont.Font(family="Segoe UI", size=9)
        self._build()

    def _build(self) -> None:
        head = tk.Frame(self.root, bg=BG2)
        head.pack(fill="x")
        tk.Label(head, text="MTGA Coach", bg=BG2, fg=ACCENT, font=self.f_h,
                 anchor="w", padx=16).pack(fill="x", pady=(12, 0))
        tk.Label(head, text="Reality Fracture  ·  draft and sealed", bg=BG2,
                 fg=MUTED, font=self.f_b, anchor="w",
                 padx=16).pack(fill="x", pady=(0, 12))

        body = tk.Frame(self.root, bg=BG, padx=12, pady=10)
        body.pack(fill="both", expand=True)
        for label, kind, argv, blurb in MODES:
            self._button(body, label, blurb, kind, argv)

        foot = tk.Frame(self.root, bg=BG2)
        foot.pack(fill="x", side="bottom")
        self.status = tk.Label(foot, text=self._card_status(), bg=BG2, fg=MUTED,
                               font=self.f_b, anchor="w", justify="left",
                               wraplength=430, padx=16, pady=8)
        self.status.pack(fill="x")
        row = tk.Frame(foot, bg=BG2)
        row.pack(fill="x", padx=12, pady=(0, 12))
        tk.Button(row, text="Import card list…", command=self.import_cards,
                  bg=BG3, fg=FG, font=self.f_b, bd=0, padx=10, pady=5,
                  activebackground=ACCENT, cursor="hand2").pack(side="left")
        tk.Button(row, text="Import 17Lands CSV…", command=self.import_17lands,
                  bg=BG3, fg=FG, font=self.f_b, bd=0, padx=10, pady=5,
                  activebackground=ACCENT, cursor="hand2").pack(side="left", padx=6)

    def _button(self, parent, label, blurb, kind, argv) -> None:
        f = tk.Frame(parent, bg=BG3, cursor="hand2")
        f.pack(fill="x", pady=3)
        t = tk.Label(f, text=label, bg=BG3, fg=FG, font=self.f_t, anchor="w",
                     padx=12)
        t.pack(fill="x", pady=(7, 0))
        b = tk.Label(f, text=blurb, bg=BG3, fg=MUTED, font=self.f_b, anchor="w",
                     justify="left", wraplength=400, padx=12)
        b.pack(fill="x", pady=(0, 7))
        for w in (f, t, b):
            w.bind("<Button-1>", lambda e, k=kind, a=argv: self.run(k, a))
            w.bind("<Enter>", lambda e, ww=(f, t, b): [x.config(bg="#2c3644") for x in ww])
            w.bind("<Leave>", lambda e, ww=(f, t, b): [x.config(bg=BG3) for x in ww])

    # ---------------------------------------------------------------- data
    def _card_status(self) -> str:
        try:
            from coach.model import Ratings
            r = Ratings.load()
            n = len(r.cards)
            real = r.raw.get("card_data") == "real"
            conf = r.confidence
            if real:
                return (f"{n} real cards loaded · grades are "
                        + ("17Lands data" if conf == "data" else "heuristic"))
            return (f"{n} cards, practice placeholders in use. "
                    "Import the real list below.")
        except Exception as e:                             # noqa: BLE001
            return f"could not read ratings: {e}"

    # ---------------------------------------------------------------- run
    def run(self, kind: str, argv: list) -> None:
        """Every mode runs in its own process.

        tkinter is not thread-safe and a second Tk root cannot share images
        with the first: running a draft window on a background thread produced
        `image "pyimageN" doesn't exist` the moment it drew a card. A separate
        process gives each window its own interpreter on its own main thread,
        which is the only arrangement tkinter actually supports.
        """
        self._spawn(argv, console=(kind == "text"))

    def _target(self, console: bool):
        """(command prefix, working directory) for a child process."""
        if getattr(sys, "frozen", False):
            exe = Path(sys.executable)
            if not console:
                return [str(exe)], exe.parent
            for name in ("MTGA Coach (console).exe", "MTGA Coach (console)"):
                cand = exe.with_name(name)
                if cand.exists():
                    return [str(cand)], exe.parent
            return None, exe.parent
        return [sys.executable, str(HERE / "run_overlay.py")], HERE

    def _spawn(self, argv: list, console: bool) -> None:
        cmd, cwd = self._target(console)
        if cmd is None:
            messagebox.showerror(
                "MTGA Coach",
                "The console build is missing.\n\n"
                "Keep 'MTGA Coach.exe' and 'MTGA Coach (console).exe' together "
                "in the same folder - the text modes run in the console build.")
            return
        kwargs = {}
        if os.name == "nt" and console:
            kwargs["creationflags"] = subprocess.CREATE_NEW_CONSOLE
        try:
            subprocess.Popen(cmd + argv, cwd=str(cwd), **kwargs)
        except Exception as e:                             # noqa: BLE001
            messagebox.showerror("MTGA Coach", f"could not start: {e}")

    # -------------------------------------------------------------- import
    def import_cards(self) -> None:
        paths = filedialog.askopenfilenames(
            title="Card list from Scryfall (JSON or CSV) or MTGJSON",
            filetypes=[("Card data", "*.json *.csv"), ("All files", "*.*")])
        if not paths:
            return
        self._import(["--import-cards", *paths])

    def import_17lands(self) -> None:
        p = filedialog.askopenfilename(title="17Lands card ratings CSV",
                                       filetypes=[("CSV", "*.csv")])
        if p:
            self._import(["--import-17lands", p])

    def _import(self, argv: list) -> None:
        try:
            from coach.cli import main
            main(argv)
            messagebox.showinfo("MTGA Coach", "Imported. " + self._card_status())
        except Exception as e:                             # noqa: BLE001
            messagebox.showerror("Import failed", str(e))
        self.status.config(text=self._card_status())

    def go(self) -> None:
        self.root.mainloop()


def main() -> int:
    """With arguments, this executable is the CLI; without, it is the menu."""
    if len(sys.argv) > 1:
        from coach.cli import main as cli_main
        return cli_main(sys.argv[1:])
    Launcher().go()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
