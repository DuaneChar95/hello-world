#!/usr/bin/env python3
"""Install or refresh the My Decks tab in the companion page.  Usage: mydecks_apply.py <page.html>"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
page = sys.argv[1]
s = open(page, encoding='utf-8').read()
TAB = '      <button class="tab" role="tab" id="t-mydecks" aria-controls="p-mydecks" aria-selected="false">My Decks</button>\n'
PANEL = '''<!--MYDECKS-PANEL--><div class="panel" id="p-mydecks" role="tabpanel" aria-labelledby="t-mydecks" hidden>
  <section>
    <h2>My decks</h2>
    <div class="frule"></div>
    <p class="lede">Decks you've actually played. Save one from a screenshot, a pasted Arena export, the Rate-a-Deck list or a
      practice run; then ask Claude how it wins, which cards combo, how to sequence it, what beats it and what to cut.
      Add your own points from the games you played — Claude reads them and answers each one — and keep the record.
      Everything is stored in this browser.</p>
    <div id="md-body"></div>
  </section>
</div>
<!--END-MYDECKS-PANEL-->
'''
UI = '/*MYDECKS-UI*/\n' + open(os.path.join(HERE, 'mydecks_ui.js'), encoding='utf-8').read() + '\n/*END-MYDECKS-UI*/\n'
def between(s, a, b, new):
    i, j = s.find(a), s.find(b)
    return s[:i] + new + s[j + len(b):] if i >= 0 and j > i else None
if 'id="t-mydecks"' not in s:
    k = s.index('id="t-rate"'); k = s.index('\n', k) + 1; s = s[:k] + TAB + s[k:]
r = between(s, '<!--MYDECKS-PANEL-->', '<!--END-MYDECKS-PANEL-->\n', PANEL)
if r is None:
    k = s.index('<div class="panel" id="p-profile"'); r = s[:k] + PANEL + s[k:]
s = r
r = between(s, '/*MYDECKS-UI*/', '/*END-MYDECKS-UI*/\n', UI)
if r is None:
    k = s.rindex('</script>'); r = s[:k] + UI + s[k:]
s = r
open(page, 'w', encoding='utf-8').write(s)
print('page updated', page, len(s))
