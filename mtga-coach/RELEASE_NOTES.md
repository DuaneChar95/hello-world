Windows build of **MTGA Coach** — a draft and sealed companion for Magic's *Reality Fracture*.

## Install

1. Download **`MTGA-Coach-Windows.zip`** below and extract it anywhere.
2. Run **`MTGA Coach.exe`**.

Keep **`MTGA Coach.exe`** and **`MTGA Coach (console).exe`** in the same folder — a windowed
Windows program has no console, so the text modes (drills, review, playstyle) run in the console
build, which the launcher starts for you.

Windows SmartScreen will say the publisher is unknown, because the executable is unsigned.
Choose **More info → Run anyway** if you're happy to.

## What's in it

- **Practice draft** — an 8-person pod with card images. Bots commit to lanes and cut colours, so
  reading signals is a real skill. Hover any card for what it pairs with and whether you can splash it.
- **Practice sealed** — six packs; you pick your colours before the model shows its build.
- **Trainer** — drills on empower Jace, prepared timing, threshold and the archetype tiers, plus a
  quiz that replays the packs you got wrong.
- **Review & playstyle** — grades every pick and separates your preferences from the habits that
  measurably cost you.
- **Live Arena overlay** — reads Arena's log during a real draft. Needs *Options → Account →
  Detailed Logs (Plugin Support)* switched on, and Arena in Windowed or Borderless mode.

Ships with all 285 Reality Fracture cards. Grades are a heuristic starting point, not win-rate
data — import a 17Lands CSV from the launcher once the set has been played.

Your imports, drafts and profile are stored in `%USERPROFILE%\.mtga-coach\`.
