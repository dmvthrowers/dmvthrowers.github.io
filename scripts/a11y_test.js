#!/usr/bin/env node
// Run the axe accessibility checker on every page of the built showcase, at phone and desktop width.
//
//   python3 scripts/build_showcase.py && node scripts/a11y_test.js
//
// For each site in _site (the showcase page and every example under _site/examples/), it follows every internal
// link and runs axe-core on each page. The run fails on any violation axe rates "serious" or "critical"
// (low-contrast text, a button with no name, a missing form label...); "moderate" and "minor" ones are listed
// but don't fail. Nothing leaves your machine: outside requests are blocked. Needs Node, Playwright with Chromium
// and axe-core (set CHROMIUM_PATH to use a browser you already have). Used only by the original template repository.
const http = require('http');
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');
const axeSource = fs.readFileSync(require.resolve('axe-core/axe.min.js'), 'utf8');

const root = path.resolve(process.argv[2] || path.join(__dirname, '..', '_site'));
const TYPES = { '.html': 'text/html', '.css': 'text/css', '.js': 'text/javascript', '.json': 'application/json',
  '.svg': 'image/svg+xml', '.png': 'image/png', '.jpg': 'image/jpeg', '.webp': 'image/webp', '.xml': 'text/xml',
  '.txt': 'text/plain', '.webmanifest': 'application/manifest+json', '.ico': 'image/x-icon', '.ics': 'text/calendar' };

const server = http.createServer((req, res) => {
  let p = decodeURIComponent(new URL(req.url, 'http://x').pathname);
  let file = path.join(root, p);
  if (!file.startsWith(root)) { res.writeHead(403).end(); return; }
  if (fs.existsSync(file) && fs.statSync(file).isDirectory()) file = path.join(file, 'index.html');
  if (!fs.existsSync(file)) { res.writeHead(404, { 'Content-Type': 'text/html' }).end('<h1>not found</h1>'); return; }
  res.writeHead(200, { 'Content-Type': TYPES[path.extname(file)] || 'application/octet-stream' });
  fs.createReadStream(file).pipe(res);
});

function sites() {
  const out = [];
  if (fs.existsSync(path.join(root, 'index.html'))) out.push('/');
  const ex = path.join(root, 'examples');
  if (fs.existsSync(ex)) for (const d of fs.readdirSync(ex).sort()) {
    if (fs.existsSync(path.join(ex, d, 'index.html'))) out.push(`/examples/${d}/`);
  }
  return out;
}

(async () => {
  await new Promise(r => server.listen(0, '127.0.0.1', r));
  const origin = `http://127.0.0.1:${server.address().port}`;
  const browser = await chromium.launch(process.env.CHROMIUM_PATH ? { executablePath: process.env.CHROMIUM_PATH } : {});
  const problems = [], notes = [];
  let pages = 0;
  for (const base of sites()) {
    const queue = [base], seen = new Set();
    while (queue.length) {
      const url = queue.shift();
      if (seen.has(url)) continue;
      seen.add(url);
      const links = [];
      for (const width of [360, 1100]) {
        const ctx = await browser.newContext({ viewport: { width, height: 780 } });
        const page = await ctx.newPage();
        await page.route('**/*', route => route.request().url().startsWith(origin) ? route.continue() : route.abort());
        await page.goto(origin + url, { waitUntil: 'load' });
        await page.evaluate(axeSource);
        const result = await page.evaluate(() => axe.run(document, { resultTypes: ['violations'] }));
        for (const v of result.violations) {
          const line = `${url} (${width}px): ${v.id}: ${v.help} [${v.impact}] x${v.nodes.length}, e.g. ${v.nodes[0].target.join(' ')}`;
          (['serious', 'critical'].includes(v.impact) ? problems : notes).push(line);
        }
        if (width === 360) {
          pages++;
          links.push(...await page.$$eval('a[href]', as => as.map(a => a.getAttribute('href'))));
        }
        await ctx.close();
      }
      for (const href of links) {
        if (!href || href.startsWith('#') || /^(mailto:|tel:|https?:|webcal:|javascript:)/.test(href)) continue;
        const next = new URL(href, origin + url);
        if (next.origin !== origin || !next.pathname.startsWith(base) || !/(\/|\.html)$/.test(next.pathname)) continue;
        queue.push(next.pathname);
      }
    }
  }
  await browser.close();
  server.close();
  if (notes.length) console.log('Minor and moderate (not failing):\n' + [...new Set(notes)].map(p => '  - ' + p).join('\n') + '\n');
  if (problems.length) {
    console.log('Serious and critical:\n' + [...new Set(problems)].map(p => '  - ' + p).join('\n'));
    console.log(`\nFAILED: ${new Set(problems).size} problem(s) across ${pages} pages.`);
    process.exit(1);
  }
  console.log(`OK: ${pages} pages checked with axe, no serious or critical problems.`);
})().catch(e => { console.error(e); process.exit(2); });
