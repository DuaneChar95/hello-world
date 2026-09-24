#!/usr/bin/env python3
"""Turn saved Untapped.gg Limited pages (from grab-untapped.ps1) into one JSON file.

Usage:  python3 untapped_parse.py <dir-with-html-dumps> <out.json>

Reads the __NEXT_DATA__ payload embedded in pick-order.html (card stats, draft
pick data, colour-pair results, event totals, the Arena card table) and the
rendered trophy-decks.html (full decklists).  Works on the free tier: ranks
bronze..platinum for cards, all ranks for colour pairs.
"""
import base64, json, re, sys, glob, os
from collections import defaultdict

RANKS = {'b': 'bronze', 's': 'silver', 'g': 'gold', 'p': 'platinum'}
COLOR_IDX = {1: 'W', 2: 'U', 3: 'B', 4: 'R', 5: 'G'}
RARITY = {2: 'C', 3: 'U', 4: 'R', 5: 'M'}
MASK = {1: 'W', 2: 'U', 4: 'B', 8: 'R', 16: 'G'}


def next_data(path):
    s = open(path, encoding='utf-8').read()
    m = re.search(r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>', s, re.S)
    if not m:
        return None, s
    return json.loads(m.group(1))['props']['pageProps'].get('ssrProps'), s


def mask_name(mask):
    if mask < 0:
        return 'other'
    return ''.join(c for b, c in MASK.items() if mask & b) or 'colorless'


def parse(dirpath):
    files = {os.path.basename(p).split('-', 1)[-1]: p for p in glob.glob(os.path.join(dirpath, '*.html'))}
    out = {'source': 'mtga.untapped.gg (free tier)', 'set': 'FRA', 'event': 'PREMIER_DRAFT'}

    po = files.get('pick-order.html')
    ss, _ = next_data(po) if po else (None, '')
    if not ss:
        raise SystemExit('pick-order.html has no ssrProps payload')

    mj = ss['minifiedMtgaJsonData']
    loc = {a: b for a, b in mj['localeData']}
    cards = {}
    by_tid = {}
    for c in mj['cardData']:
        grpid, tid = c[0], c[1]
        name = loc.get(tid)
        if not name:
            continue
        colors = [COLOR_IDX[i] for i in (c[14] or []) if i in COLOR_IDX]
        rec = {'name': name, 'title_id': tid, 'grpid': grpid, 'set': c[6], 'collector': c[3],
               'cost': c[7], 'cmc': c[8], 'rarity': RARITY.get(c[9], str(c[9])), 'colors': colors,
               'back_face': bool(c[5])}
        by_tid.setdefault(tid, rec)
        if not c[5]:
            cards[name] = rec

    # ---- card stats (games in deck / games-in-hand / opening hand) ----
    cs = ss['limitedCardStatsResp']['data']
    fields = cs['metadata']['fields']
    for tid, v in cs['data'].items():
        rec = by_tid.get(int(tid))
        if not rec:
            continue
        per = {}
        tot = defaultdict(int)
        for r, arr in v['ALL'].items():
            row = {}
            for grp, vals in zip(fields, arr):
                if vals is None:
                    continue
                for f, x in zip(grp, vals):
                    row[f] = x
                    tot[f] += x
            per[RANKS.get(r, r)] = row
        rec['stats_by_rank'] = per
        st = dict(tot)
        st['gih_wr'] = round(st.get('available_wins',0) / st['available_games'], 4) if st.get('available_games') else None
        st['oh_wr'] = round(st.get('in_opening_hand_wins',0) / st['in_opening_hands'], 4) if st.get('in_opening_hands') else None
        rec['stats'] = st
    out['card_stats_last_modified'] = ss['limitedCardStatsResp'].get('lastModified')
    out['games_by_rank'] = cs['metadata']['games'].get('ALL')

    # ---- draft pick data ----
    for row in ss['limitedDraftInfo']['data']:
        rec = by_tid.get(row['title_id'])
        if not rec:
            continue
        off = row['offered_qty']; ata = row['avg_pick_chosen']; alsa = row['avg_last_pick_offered']
        n = sum(off.values())
        wa = sum(off[r] * ata[r] for r in off if ata.get(r)) / max(1, sum(off[r] for r in off if ata.get(r)))
        wl = sum(off[r] * alsa[r] for r in off if alsa.get(r)) / max(1, sum(off[r] for r in off if alsa.get(r)))
        rec['draft'] = {'offered': n, 'ata': round(wa, 2), 'alsa': round(wl, 2), 'by_rank': {r: {'offered': off[r], 'ata': ata.get(r), 'alsa': alsa.get(r)} for r in off}}
    out['draft_last_modified'] = ss['limitedDraftInfo'].get('lastModified')

    # ---- colour pairs ----
    si = ss['limitedSetInfo']['data']
    pairs = {}
    for mask, v in si['color_combinations_data'].items():
        m = int(mask)
        matches = sum(v['matches_all_by_rank'].values())
        won = sum(v['matches_won_by_rank'].values())
        pairs[mask_name(m)] = {
            'mask': m, 'matches': matches, 'wins': won,
            'wr': round(won / matches, 4) if matches else None,
            'events': sum(v['events_all_by_rank'].values()),
            'popularity': round(sum(v['popularity_by_rank'].values()), 2),
            'tier_val_by_rank': v['tier_val_by_rank'],
            'matches_by_rank': v['matches_all_by_rank'], 'wins_by_rank': v['matches_won_by_rank'],
            'avg_turns_won': v.get('avg_turns_won_by_rank'),
        }
    out['color_pairs'] = pairs
    out['color_pairs_last_modified'] = si.get('color_combinations_last_modified')

    ev = [e for e in ss['mtgaEvents']['data'] if e.get('limited_set') == 'FRA']
    out['events'] = [{'name': e['event_name'], 'start': e['start_ts'], 'last_seen': e['last_observed_ts'],
                      'matches_by_rank': e['total_matches_by_rank']} for e in ev]

    out['cards'] = cards

    # ---- trophy decks ----
    tp = files.get('trophy-decks.html')
    decks = []
    if tp:
        tss, html = next_data(tp)
        meta = tss['trophyDecksByEvent']['data'] if tss else {'data': [], 'all_decks': 0}
        out['trophy_decks_total'] = meta.get('all_decks')
        blocks = [m.start() for m in re.finditer(r'aria-label="land"></i></div><span>(\d+)</span>', html)]
        lands = [int(m.group(1)) for m in re.finditer(r'aria-label="land"></i></div><span>(\d+)</span>', html)]
        rows = []
        for m in re.finditer(r'<a class="sc-3a3a5fb6-11 [^"]*" href="/meta/cards/(\d+)/[^"]*"[^>]*>(.*?)</a>', html, re.S):
            body = m.group(2)
            name = re.search(r'<img alt="([^"]+)"', body).group(1)
            q = re.search(r'<span>x(\d+)</span>', body)
            rows.append((m.start(), int(m.group(1)), name, int(q.group(1)) if q else 1))
        text = re.sub(r'\|+', '|', re.sub(r'<[^>]+>', '|', html))
        heads = {}
        for m in re.finditer(r'\|([^|]+)\|([^|]+)\|RECORD\|([^|]+)\|RARE\+\|(\d+)\|PLAYER\|([^|]+)\|RANK\|([^|]+)\|', text):
            heads.setdefault(m.group(5).strip(), []).append({'label': m.group(1).strip(), 'guild': m.group(2).strip(),
                                                              'record': m.group(3).strip(), 'rares': int(m.group(4)), 'rank_name': m.group(6).strip()})
        for i, dk in enumerate(meta['data']):
            hl = heads.get(dk['pn'], [])
            hd = hl.pop(0) if hl else {}
            lo = blocks[i] if i < len(blocks) else 0
            hi = blocks[i + 1] if i + 1 < len(blocks) else len(html)
            lst = [{'name': n, 'qty': q, 'title_id': t} for p, t, n, q in rows if lo <= p < hi]
            decks.append({'player': dk['pn'], 'wins': dk['wi'], 'losses': dk['lo'], 'rank': dk['rk'],
                          'colors': mask_name(dk['dc']), 'date': dk['dt'], 'lands': lands[i] if i < len(lands) else None,
                          'guild': hd.get('guild'), 'rares': hd.get('rares'), 'rank_name': hd.get('rank_name'),
                          'key_cards': [c for c in (by_tid.get(t, {}).get('name') for t in dk.get('kc', [])) if c],
                          'cards': lst})
        # key cards were grpids, remap
        gmap = {r['grpid']: r['name'] for r in by_tid.values()}
        for d, dk in zip(decks, meta['data']):
            d['key_cards'] = [gmap[g] for g in dk.get('kc', []) if g in gmap]
    out['trophy_decks'] = decks
    return out


if __name__ == '__main__':
    src, dst = sys.argv[1], sys.argv[2]
    data = parse(src)
    json.dump(data, open(dst, 'w'), indent=0, ensure_ascii=False)
    n = sum(1 for c in data['cards'].values() if c.get('stats'))
    print(f"cards {len(data['cards'])}, with stats {n}, colour pairs {len(data['color_pairs'])}, trophy decks {len(data['trophy_decks'])}/{data.get('trophy_decks_total')}")
