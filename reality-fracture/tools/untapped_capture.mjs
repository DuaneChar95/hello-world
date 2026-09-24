// Capture Untapped.gg's Reality Fracture Limited data with a real browser.
//
// The session that maintains the guide cannot reach untapped.gg, but a CI
// runner can. This opens each page, records every JSON response the page
// fetches (that is where the tier list, pick order and trophy decks come
// from), scrolls to force lazy tables to load, and saves the rendered text
// plus a screenshot so the shape of the data can be inspected afterwards.
import { chromium } from 'playwright';
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';

const OUT = process.argv[2] || 'reality-fracture/untapped';
const BASE = 'https://mtga.untapped.gg/limited/draft/reality-fracture/';
const PAGES = [
  ['tier-list', BASE],
  ['pick-order', BASE + 'pick-order'],
  ['trophy-decks', BASE + 'trophy-decks'],
  ['cards', BASE + 'cards'],
  ['archetypes', BASE + 'archetypes'],
  ['sealed', 'https://mtga.untapped.gg/limited/sealed/reality-fracture/'],
];
fs.mkdirSync(path.join(OUT, 'raw'), { recursive: true });
fs.mkdirSync(path.join(OUT, 'text'), { recursive: true });
fs.mkdirSync(path.join(OUT, 'shots'), { recursive: true });

const browser = await chromium.launch();
const ctx = await browser.newContext({
  viewport: { width: 1400, height: 1000 },
  userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0 Safari/537.36',
  locale: 'en-US',
});
const index = [];
ctx.on('response', async (res) => {
  try {
    const ct = (res.headers()['content-type'] || '').toLowerCase();
    const url = res.url();
    if (!(ct.includes('json') || /\/api\/|\.json(\?|$)/.test(url))) return;
    if (res.status() !== 200) return;
    const body = await res.text();
    if (body.length < 20) return;
    const id = crypto.createHash('md5').update(url).digest('hex').slice(0, 12);
    fs.writeFileSync(path.join(OUT, 'raw', id + '.json'), body);
    index.push({ id, url, bytes: body.length, page: currentPage });
  } catch (e) { /* streamed or gone */ }
});
let currentPage = '';
for (const [slug, url] of PAGES) {
  currentPage = slug;
  const page = await ctx.newPage();
  const rec = { slug, url, status: null, title: null, error: null };
  try {
    const resp = await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 60000 });
    rec.status = resp && resp.status();
    await page.waitForLoadState('networkidle', { timeout: 30000 }).catch(() => {});
    for (let i = 0; i < 12; i++) { await page.mouse.wheel(0, 1500); await page.waitForTimeout(600); }
    await page.waitForTimeout(1500);
    rec.title = await page.title();
    const text = await page.evaluate(() => document.body.innerText);
    fs.writeFileSync(path.join(OUT, 'text', slug + '.txt'), text);
    await page.screenshot({ path: path.join(OUT, 'shots', slug + '.png'), fullPage: true });
    console.log(`${slug}: ${rec.status} "${rec.title}" text ${text.length} chars`);
  } catch (e) { rec.error = String(e.message).slice(0, 200); console.log(`${slug}: ERROR ${rec.error}`); }
  index.push({ page: slug, nav: rec });
  await page.close();
}
await browser.close();
fs.writeFileSync(path.join(OUT, 'index.json'), JSON.stringify(index, null, 1));
console.log('captured', index.filter(x => x.id).length, 'JSON responses');
