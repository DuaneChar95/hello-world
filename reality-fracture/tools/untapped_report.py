#!/usr/bin/env python3
"""Render the Untapped JSON as the Markdown section used in DRAFT-GUIDE.md.
Usage: python3 untapped_report.py reality-fracture/untapped/untapped-fra.json [fra_ratings.json]"""
import json, sys, statistics as st
from datetime import datetime, timezone

d = json.load(open(sys.argv[1], encoding='utf-8'))
R = json.load(open(sys.argv[2], encoding='utf-8'))['cards'] if len(sys.argv) > 2 else {}
cards = d['cards']
xs = [c['stats']['gih_wr'] for c in cards.values() if c['stats'].get('available_games', 0) >= 30]
mean, sd = st.mean(xs), st.pstdev(xs)
ts = max(int(d.get('card_stats_last_modified') or 0), int(d.get('draft_last_modified') or 0)) / 1000
cap = datetime.fromtimestamp(ts, tz=timezone.utc).strftime('%Y-%m-%d %H:%M UTC')
g = d['games_by_rank']; tot = sum(g.values())
ARCH = {'WU': 'Fatehold', 'UB': 'Theorix', 'BR': 'Stingerquill', 'RG': 'Konstrari', 'GW': 'Vigorbloom', 'WB': 'Liliana', 'UR': 'Chandra', 'BG': 'Garruk', 'RW': 'Ajani', 'GU': 'Tam / Kiora'}
def key(k): return ''.join(sorted(k))
def arch(k):
    for a, n in ARCH.items():
        if key(a) == key(k): return n
    return ''
def pct(x): return '—' if x is None else f'{x*100:.1f}%'
def tier(wr): return 'S' if wr >= .62 else 'A' if wr >= .58 else 'B' if wr >= .54 else 'C' if wr >= .50 else 'D' if wr >= .45 else 'F'
out = []
w = out.append
w(f'## 14. Untapped early-access data  [MEASURED — small sample]\n')
w(f'Untapped.gg free-tier numbers for the **Premier Draft early-access event** (23–24 Sep), captured {cap}. '
  f'Card stats come from **{tot} logged games** (bronze {g.get("bronze",0)}, silver {g.get("silver",0)}, gold {g.get("gold",0)}, platinum {g.get("platinum",0)}); '
  f'the colour-pair table pools every rank. Raw JSON: `reality-fracture/untapped/untapped-fra.json`; refresh steps in `reality-fracture/untapped/README.md`.\n')
w('**Read it with the sample size in view.** One day of games. A common with 150 games in hand has a win rate that can move five points by the weekend; '
  'anything under 30 games is noise. The colour-pair table is the most reliable thing here, the tier list next, single-card pick orders last. '
  'The companion page and `fra_ratings.json` now blend these numbers into every grade with weight `n/(n+60)`, so the data dominates as it grows.\n')
w('### 14.1 Colour pairs — match win rate, all ranks\n')
w('| Pair | Archetype | Match WR | Matches | Popularity | Pre-release call |')
w('|---|---|---:|---:|---:|---|')
prior = {'UB': 'S 8.6', 'BR': 'S', 'WB': 'A', 'WU': 'A', 'RG': 'B', 'UR': 'B', 'BG': 'B', 'GW': 'C', 'RW': 'C', 'GU': 'C'}
pairs = sorted(d['color_pairs'].items(), key=lambda kv: -(kv[1]['wr'] or 0))
for k, v in pairs:
    if len(k) != 2: continue
    pr = next((p for a, p in prior.items() if key(a) == key(k)), '')
    w(f'| {k} | {arch(k)} | **{pct(v["wr"])}** | {v["matches"]} | {v["popularity"]:.1f}% | {pr} |')
w('')
three = [(k, v) for k, v in pairs if len(k) == 3]
if three:
    w('Three-colour decks: ' + ', '.join(f'{k} {pct(v["wr"])} ({v["matches"]})' for k, v in three) + '.\n')
w('### 14.2 Tier list by games-in-hand win rate (30+ games)\n')
ok = sorted([c for c in cards.values() if c['stats'].get('available_games', 0) >= 30], key=lambda c: -c['stats']['gih_wr'])
for t in 'SABCDF':
    grp = [c for c in ok if tier(c['stats']['gih_wr']) == t]
    if not grp: continue
    lo = {'S': '62%+', 'A': '58–62%', 'B': '54–58%', 'C': '50–54%', 'D': '45–50%', 'F': 'under 45%'}[t]
    w(f'**{t} ({lo})** — ' + ', '.join(f'{c["name"]} {pct(c["stats"]["gih_wr"])} ({c["stats"]["available_games"]})' for c in grp) + '\n')
w('### 14.3 Pick order — average taken at (ATA), 20+ offers\n')
po = sorted([c for c in cards.values() if c.get('draft', {}).get('offered', 0) >= 20 and c['draft'].get('ata')], key=lambda c: c['draft']['ata'])
w('| # | Card | ATA | Last seen | GIH WR | Games |')
w('|---:|---|---:|---:|---:|---:|')
for i, c in enumerate(po[:40], 1):
    w(f'| {i} | {c["name"]} | {c["draft"]["ata"]:.1f} | {c["draft"]["alsa"]:.1f} | {pct(c["stats"].get("gih_wr"))} | {c["stats"].get("available_games", 0)} |')
w('')
w('### 14.4 Where the pre-release reads were wrong\n')
if R:
    diffs = []
    for n, c in cards.items():
        r = R.get(n)
        if not r or c['stats'].get('available_games', 0) < 40: continue
        dg = (5.5 + (c['stats']['gih_wr'] - mean) / sd * 1.6) / 2
        diffs.append((dg - r.get('grade_prerelease', r['grade']), n, r.get('grade_prerelease', r['grade']), dg, c['stats']['gih_wr'], c['stats']['available_games']))
    diffs.sort()
    w('Underrated (read → data, 0–5 scale): ' + '; '.join(f'{n} {a:.1f}→{b:.1f} ({pct(wr)}, {ng})' for _, n, a, b, wr, ng in diffs[::-1][:12]) + '.\n')
    w('Overrated: ' + '; '.join(f'{n} {a:.1f}→{b:.1f} ({pct(wr)}, {ng})' for _, n, a, b, wr, ng in diffs[:12]) + '.\n')
w('### 14.5 Trophy decks (7 wins)\n')
for dk in d['trophy_decks']:
    spells = sum(c['qty'] for c in dk['cards'])
    lst = ', '.join((f'{c["qty"]}× ' if c['qty'] > 1 else '') + c['name'] for c in sorted(dk['cards'], key=lambda c: c['name']))
    w(f'- **{dk["colors"]} {dk.get("guild") or ""}** — {dk["wins"]}–{dk["losses"]}, {dk.get("rank_name") or ""}, {dk["player"]}, {dk["date"][:10]}. {spells} spells + {dk["lands"]} lands. {lst}.')
w(f'\n{d.get("trophy_decks_total")} trophy decks exist on Untapped; the free page lists these {len(d["trophy_decks"])}.\n')
spg = [c for c in cards.values() if c.get('collector') == '0']
if spg:
    w('Special Guests seen in the data: ' + ', '.join(f'{c["name"]} ({pct(c["stats"].get("gih_wr"))}, {c["stats"].get("available_games",0)})' for c in spg) + '.\n')
print('\n'.join(out))
