#!/usr/bin/env python3
"""Catch tuple padx/pady passed as a widget option.

Tk accepts (a, b) for padding in pack()/grid(), but a widget's own padx/pady
must be a single value - a tuple stringifies to "12 0" and Tk raises
TclError: bad screen distance. The stubbed-Tk smoke test cannot catch this
because a stub accepts anything, so it is checked statically instead.
"""
from __future__ import annotations

import ast
import sys
from pathlib import Path

# Never read or write .pyc here: a cached module from an earlier edit can
# make this report a failure that no longer exists in the source.
sys.dont_write_bytecode = True

GEOMETRY = {"pack", "grid", "place", "pack_configure", "grid_configure"}


def offenders(path: Path) -> list[tuple[int, str]]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    out = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        # A geometry call is fine; anything else taking padx/pady is a widget.
        if isinstance(node.func, ast.Attribute) and node.func.attr in GEOMETRY:
            continue
        for kw in node.keywords:
            if kw.arg in ("padx", "pady") and isinstance(kw.value, ast.Tuple):
                vals = ", ".join(ast.unparse(e) for e in kw.value.elts)
                out.append((kw.value.lineno, f"{kw.arg}=({vals})"))
    return out


def main(paths: list[str]) -> int:
    bad = 0
    for p in paths:
        path = Path(p)
        for line, what in offenders(path):
            print(f"  {path}:{line}  {what}  <- widget option, must be a single value")
            bad += 1
    print(f"tk padding check: {'FAIL' if bad else 'ok'} ({bad} offender(s))")
    return 1 if bad else 0


if __name__ == "__main__":
    files = sys.argv[1:] or ["launcher.py", "coach/gui.py", "coach/overlay.py"]
    raise SystemExit(main(files))
