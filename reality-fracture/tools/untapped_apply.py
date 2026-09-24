#!/usr/bin/env python3
"""Install or refresh Untapped data in the Hexhaven page and the coach ratings file.

Usage: python3 untapped_apply.py <untapped-fra.json> [--page hexhaven.html] [--ratings fra_ratings.json]

Page: inserts/replaces the marked blocks (data, CSS, tab, panel, UI, card-sheet row).
Ratings: adds per-card `untapped` stats, keeps the pre-release grade as `grade_prerelease`,
and blends `grade` toward the data as the sample grows.
"""
import json, re, sys, os, statistics as st
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
args = sys.argv[1:]
src = args[0]
page = args[args.index('--page') + 1] if '--page' in args else None
ratings = args[args.index('--ratings') + 1] if '--ratings' in args else None
d = json.load(open(src, encoding='utf-8'))

xs = [c['stats']['gih_wr'] for c in d['cards'].values() if c['stats'].get('available_games', 0) >= 30 and c['stats'].get('gih_wr') is not None]
mean, sd = st.mean(xs), st.pstdev(xs)
captured = max(int(d.get('card_stats_last_modified') or 0), int(d.get('draft_last_modified') or 0)) / 1000
captured_s = datetime.fromtimestamp(captured, tz=timezone.utc).strftime('%Y-%m-%d %H:%M UTC') if captured else 'unknown'
games = d.get('games_by_rank') or {}
ev = [e for e in d.get('events', []) if 'PremierDraft' in e['name']]
matches = sum(sum(e['matches_by_rank'].values()) for e in ev)

def grade10(wr):
    return max(1.0, min(10.0, 5.5 + (wr - mean) / sd * 1.6))

cards = {}
for name, c in d['cards'].items():
    s, dr = c.get('stats', {}), c.get('draft', {})
    cards[name] = [s.get('available_games', 0), s.get('gih_wr'), s.get('in_opening_hands', 0), s.get('oh_wr'), s.get('games', 0),
                   dr.get('ata'), dr.get('alsa'), dr.get('offered', 0)]
pairs = {k: [v['matches'], v['wins'], v['wr'], v['popularity'], v['events']] for k, v in d['color_pairs'].items()}
decks = [{'p': x['player'], 'w': x['wins'], 'l': x['losses'], 'rk': x['rank'], 'c': x['colors'], 'd': x['date'], 'lands': x['lands'],
          'guild': x.get('guild'), 'rares': x.get('rares'), 'key': x['key_cards'], 'cards': [[c['name'], c['qty']] for c in x['cards']]}
         for x in d['trophy_decks']]
spg = [[n, cards[n][0], cards[n][1], cards[n][5]] for n, c in d['cards'].items() if c.get('set') != 'FRA' or c.get('collector') == '0']
meta = {'captured': captured_s, 'event': ', '.join(e['name'] for e in ev) or 'PREMIER_DRAFT', 'games': games, 'matches': matches,
        'decksTotal': d.get('trophy_decks_total'), 'mean': round(mean, 4), 'sd': round(sd, 4), 'cardsWithData': sum(1 for v in cards.values() if v[0])}
blob = json.dumps({'meta': meta, 'cards': cards, 'pairs': pairs, 'decks': decks, 'spg': spg}, separators=(',', ':'), ensure_ascii=False)

DATA = ('/*UNTAPPED-DATA*/var UNTAPPED=' + blob + ';\n'
        'function untappedGrade(wr){ return Math.max(1,Math.min(10,5.5+(wr-UNTAPPED.meta.mean)/UNTAPPED.meta.sd*1.6)); }\n'
        '(function(){ CARDS.forEach(function(r){ if(r[11]==null) r[11]=r[7]; var u=UNTAPPED.cards[r[0]]; if(!u||!u[0]||u[1]==null){ r[7]=r[11]; return; } '
        'var n=u[0], w=n/(n+60); r[7]=Math.round((w*untappedGrade(u[1])+(1-w)*r[11])*10)/10; }); })();\n/*END-UNTAPPED-DATA*/\n')

CSS = ('/*UNTAPPED-CSS*/.dgrid .cname b{color:var(--accent);font-size:9.5px;letter-spacing:0}\n'
       '#data-views button{white-space:nowrap}\n/*END-UNTAPPED-CSS*/\n')

TAB = '      <button class="tab" role="tab" id="t-data" aria-controls="p-data" aria-selected="false">Untapped Data</button>\n'

PANEL = '''<!--UNTAPPED-PANEL--><div class="panel" id="p-data" role="tabpanel" aria-labelledby="t-data" hidden>
  <section>
    <h2>Untapped.gg — early-access data</h2>
    <div class="frule"></div>
    <p class="lede">Real games at last. This is Untapped.gg's free-tier data for the <strong>Premier Draft early-access event</strong>
      (23–24 September), captured <span id="data-captured"></span>: <span id="data-summary"></span>.
      <strong>It is one day of games at Bronze–Platinum, so single-card numbers swing by ten points on a bad afternoon.</strong>
      The colour-pair table is the most trustworthy thing here; the tier list is next; a card with under 30 games in hand is a rumour.
      The grades on every card in this page are now a blend of the pre-release read and this data, weighted by sample size.</p>
    <div class="seg" id="data-views" role="group" aria-label="View" style="margin-bottom:6px">
      <button type="button" data-view="tier" aria-pressed="true">Tier list</button>
      <button type="button" data-view="pick" aria-pressed="false">Pick order</button>
      <button type="button" data-view="pairs" aria-pressed="false">Colour pairs</button>
      <button type="button" data-view="decks" aria-pressed="false">Trophy decks</button>
      <button type="button" data-view="mine" aria-pressed="false">Where I was wrong</button>
    </div>
    <div id="data-body"></div>
    <details style="margin-top:22px"><summary class="gmeta" style="cursor:pointer">How to refresh this data</summary>
      <p style="font-size:13px;color:var(--ink-2)">Untapped blocks robots, so the pages have to be saved from your own browser. In PowerShell, from the repo:</p>
      <pre style="font-size:12px;overflow:auto">powershell -ExecutionPolicy Bypass -File reality-fracture\\tools\\grab-untapped.ps1 -Out untapped-dump
python reality-fracture\\tools\\untapped_parse.py untapped-dump reality-fracture\\untapped\\untapped-fra.json
python reality-fracture\\tools\\untapped_apply.py reality-fracture\\untapped\\untapped-fra.json --page reality-fracture\\companion\\hexhaven.html --ratings mtga-coach\\data\\fra_ratings.json</pre>
      <p style="font-size:13px;color:var(--ink-2)">Then republish the page. The data block, this tab and the blended grades are all replaced in place.</p>
    </details>
  </section>
</div>
<!--END-UNTAPPED-PANEL-->
'''

UI = '/*UNTAPPED-UI*/\n' + open(os.path.join(HERE, 'untapped_ui.js'), encoding='utf-8').read() + '\n/*END-UNTAPPED-UI*/\n'
UI = UI.replace("document.getElementById('data-captured')", "x")  # (no-op guard, kept simple)
UI += ("(function(){ var c=document.getElementById('data-captured'), s=document.getElementById('data-summary'); if(c) c.textContent=UNTAPPED.meta.captured; "
       "if(s){ var g=UNTAPPED.meta.games||{}; var tot=Object.keys(g).reduce(function(a,k){return a+g[k];},0); s.textContent=UNTAPPED.meta.cardsWithData+' cards with stats from '+tot+' logged games ('+Object.keys(g).map(function(k){return k+' '+g[k];}).join(', ')+'), '+UNTAPPED.meta.matches+' matches in the colour-pair table, '+UNTAPPED.decks.length+' trophy decks'; } })();\n")


def between(s, a, b, new):
    i, j = s.find(a), s.find(b)
    if i >= 0 and j > i:
        return s[:i] + new + s[j + len(b):]
    return None


if page:
    s = open(page, encoding='utf-8').read()
    # data block
    r = between(s, '/*UNTAPPED-DATA*/', '/*END-UNTAPPED-DATA*/\n', DATA)
    if r is None:
        k = s.index('var BEST='); r = s[:k] + DATA + s[k:]
    s = r
    r = between(s, '/*UNTAPPED-CSS*/', '/*END-UNTAPPED-CSS*/\n', CSS)
    if r is None:
        k = s.rfind('</style>', 0, s.index('<div class="panel" id="p-format"')); r = s[:k] + CSS + s[k:]
    s = r
    if 'id="t-data"' not in s:
        k = s.index('id="t-str"'); k = s.index('\n', k) + 1; s = s[:k] + TAB + s[k:]
    r = between(s, '<!--UNTAPPED-PANEL-->', '<!--END-UNTAPPED-PANEL-->\n', PANEL)
    if r is None:
        k = s.index('<div class="panel" id="p-rate"'); r = s[:k] + PANEL + s[k:]
    s = r
    r = between(s, '/*UNTAPPED-UI*/', '/*END-UNTAPPED-UI*/\n', UI)
    if r is None:
        k = s.index('/* ---------------- archetype board ---------------- */'); r = s[:k] + UI + s[k:]
    s = r
    hook = "(r[10]?'<div><dt>What it does</dt><dd>'+esc(r[10])+'</dd></div>':'')+"
    if 'untappedRow(name)+' not in s and hook in s:
        s = s.replace(hook, hook + '\n        untappedRow(name)+', 1)
    if "data-goto=\"t-data\"" not in s:
        s = s.replace("take them in. Click any card for who wants it and whether you can splash it.</p>",
                      "take them in. Click any card for who wants it and whether you can splash it. <strong>Early-access games are now in:</strong> see the <a href=\"#\" data-goto=\"t-data\">Untapped Data</a> tab for the measured tier list, and note that every grade shown on a card is now blended with it.</p>", 1)
        s = s.replace("<strong>The moment Arena queues open on 29 September, trust GIH WR over this chart.</strong></p>",
                      "<strong>The moment Arena queues open on 29 September, trust GIH WR over this chart.</strong> The first day of early-access games is in the <a href=\"#\" data-goto=\"t-data\">Untapped Data</a> tab, colour pairs included.</p>", 1)
    open(page, 'w', encoding='utf-8').write(s)
    print('page updated', page, len(s))

if ratings:
    R = json.load(open(ratings, encoding='utf-8'))
    n = 0
    for name, rec in R['cards'].items():
        c = d['cards'].get(name)
        if 'grade_prerelease' not in rec:
            rec['grade_prerelease'] = rec['grade']
        if not c or not c['stats'].get('available_games'):
            rec['grade'] = rec['grade_prerelease']
            rec.pop('untapped', None)
            continue
        s_, dr = c['stats'], c.get('draft', {})
        rec['untapped'] = {'gih_games': s_.get('available_games', 0), 'gih_wr': s_.get('gih_wr'), 'oh_games': s_.get('in_opening_hands', 0), 'oh_wr': s_.get('oh_wr'),
                           'games': s_.get('games', 0), 'ata': dr.get('ata'), 'alsa': dr.get('alsa'), 'offered': dr.get('offered', 0)}
        ng = s_['available_games']; w = ng / (ng + 60)
        rec['grade'] = round(w * grade10(s_['gih_wr']) / 2 + (1 - w) * rec['grade_prerelease'], 2)
        n += 1
    R['untapped'] = {'captured': captured_s, 'event': meta['event'], 'games_by_rank': games, 'matches': matches, 'gih_mean': round(mean, 4), 'gih_sd': round(sd, 4),
                     'blend': 'grade = w*data + (1-w)*grade_prerelease, w = gih_games/(gih_games+60); data grade on 0-5 = (5.5 + z*1.6)/2',
                     'color_pairs': {k: {'matches': v['matches'], 'wins': v['wins'], 'wr': v['wr'], 'popularity': v['popularity']} for k, v in d['color_pairs'].items()},
                     'trophy_decks': d['trophy_decks']}
    R['updated'] = datetime.now(timezone.utc).strftime('%Y-%m-%d')
    R['source'] = (R.get('source', '') + ' | Untapped.gg early-access Premier Draft data blended in (' + captured_s + ')').strip(' |')
    json.dump(R, open(ratings, 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
    print('ratings updated', ratings, n, 'cards blended')
