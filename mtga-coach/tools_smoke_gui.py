#!/usr/bin/env python3
"""Drive the Tk windows against a stub that enforces real Tk's rules.

The previous stub accepted every argument, so it happily passed a tuple as a
widget's pady - which real Tk rejects with "bad screen distance". A stub that
accepts anything proves nothing, so this one validates the options it knows
about and then exercises the launcher and a full draft through the window.
"""
from __future__ import annotations

import sys
import types
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

ERRORS: list[str] = []


class TclError(Exception):
    pass


def _check_options(where: str, kwargs: dict) -> None:
    for key in ("padx", "pady", "borderwidth", "bd", "highlightthickness",
                "wraplength", "width", "height"):
        if key in kwargs and isinstance(kwargs[key], (tuple, list)):
            vals = " ".join(str(v) for v in kwargs[key])
            ERRORS.append(f'{where}: {key}={kwargs[key]!r} -> Tk would raise '
                          f'TclError: bad screen distance "{vals}"')


class FakeWidget:
    def __init__(self, *a, **k):
        _check_options(f"{type(self).__name__}()", k)

    def __getattr__(self, name):
        def anything(*a, **k):
            return FakeWidget()
        return anything

    def config(self, *a, **k):
        _check_options("config()", k)

    configure = config

    def winfo_children(self):
        return []

    def width(self):
        return 480

    def subsample(self, a, b=None):
        return self

    # geometry managers legitimately accept tuples
    def pack(self, *a, **k): pass
    def grid(self, *a, **k): pass
    def place(self, *a, **k): pass
    def destroy(self): pass
    def bind(self, *a, **k): pass
    def title(self, *a, **k): pass
    def pack_propagate(self, *a, **k): pass


def install_stub() -> None:
    fake = types.ModuleType("tkinter")
    for n in ("Tk", "Frame", "Label", "Button", "Canvas", "PhotoImage",
              "StringVar", "Text", "Toplevel"):
        setattr(fake, n, FakeWidget)
    fake.TclError = TclError
    for sub in ("font", "filedialog", "messagebox"):
        m = types.ModuleType("tkinter." + sub)
        setattr(fake, sub, m)
        sys.modules["tkinter." + sub] = m
    fake.font.Font = FakeWidget
    fake.filedialog.askopenfilenames = lambda **k: ()
    fake.filedialog.askopenfilename = lambda **k: ""
    fake.messagebox.showerror = lambda *a, **k: None
    fake.messagebox.showinfo = lambda *a, **k: None
    sys.modules["tkinter"] = fake


def main() -> int:
    install_stub()
    from coach.model import Ratings
    from coach.art import ArtCache
    from coach.sim import DraftEngine
    from coach.gui import DraftWindow
    from launcher import Launcher, MODES

    Launcher()
    print(f"  launcher builds ............ {len(MODES)} modes")

    eng = DraftEngine(Ratings.load(), seed=3)
    win = DraftWindow(eng, ArtCache(enabled=False))
    for c in eng.current_pack()[:6]:
        win.show_detail(c)
    for c in eng.current_pack()[:4]:
        win._draw_card(win.grid_f, c, 0)
    n = 0
    while not eng.done and n < 45:
        win.pick(eng.current_pack()[0])
        n += 1
    win.refresh()
    print(f"  draft window ............... {n} picks, finish screen ok")

    if ERRORS:
        print(f"  widget options ............. FAIL ({len(ERRORS)})")
        for e in ERRORS:
            print("     " + e)
        return 1
    print("  widget options ............. ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
