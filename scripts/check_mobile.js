#!/usr/bin/env node
// Fail if any page scrolls sideways on a 360px-wide phone. Runs before every deploy.
//
//   node scripts/check_mobile.js            # from the repo root; needs Playwright with Chromium
//
// Serves the repo root locally (pages use <base href="/">), opens every top-level *.html at 360px, and compares the
// page's scroll width to the viewport. Outside requests are blocked, so embeds and fonts from other hosts can't
// change the result. Redirect stubs (meta refresh) are skipped. Lists the widest elements to make fixes easy.
const http = require('http');
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

const WIDTH = 360;
const root = path.resolve(process.argv[2] || path.join(__dirname, '..'));
const TYPES = { '.html': 'text/html', '.css': 'text/css', '.js': 'text/javascript', '.json': 'application/json',
  '.svg': 'image/svg+xml', '.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.webp': 'image/webp',
  '.gif': 'image/gif', '.woff2': 'font/woff2', '.woff': 'font/woff', '.ico': 'image/x-icon', '.xml': 'text/xml',
  '.webmanifest': 'application/manifest+json', '.ics': 'text/calendar' };

const server = http.createServer((req, res) => {
  const file = path.join(root, decodeURIComponent(new URL(req.url, 'http://x').pathname));
  if (!file.startsWith(root) || !fs.existsSync(file) || fs.statSync(file).isDirectory()) { res.writeHead(404).end(); return; }
  res.writeHead(200, { 'Content-Type': TYPES[path.extname(file).toLowerCase()] || 'application/octet-stream' });
  fs.createReadStream(file).pipe(res);
});

const pages = fs.readdirSync(root).filter(f => f.endsWith('.html')).sort()
  .filter(f => !/<meta[^>]+http-equiv=["']refresh/i.test(fs.readFileSync(path.join(root, f), 'utf8')));

(async () => {
  await new Promise(r => server.listen(0, '127.0.0.1', r));
  const origin = `http://127.0.0.1:${server.address().port}`;
  const browser = await chromium.launch(process.env.CHROMIUM_PATH ? { executablePath: process.env.CHROMIUM_PATH } : {});
  const ctx = await browser.newContext({ viewport: { width: WIDTH, height: 780 }, deviceScaleFactor: 2, isMobile: true, hasTouch: true });
  await ctx.route('**/*', route => route.request().url().startsWith(origin) ? route.continue() : route.abort());
  const failures = [];
  for (const name of pages) {
    const page = await ctx.newPage();
    await page.goto(`${origin}/${name}`, { waitUntil: 'load' });
    const r = await page.evaluate((w) => {
      const sw = Math.max(document.documentElement.scrollWidth, document.body.scrollWidth);
      const wide = [];
      if (sw > w + 1) {
        for (const el of document.body.querySelectorAll('*')) {
          const b = el.getBoundingClientRect();
          if (b.right > w + 1 && b.width > 0 && getComputedStyle(el).position !== 'fixed') {
            const id = el.id ? `#${el.id}` : '';
            const cls = typeof el.className === 'string' && el.className.trim() ? '.' + el.className.trim().split(/\s+/).join('.') : '';
            wide.push(`${el.tagName.toLowerCase()}${id}${cls} (right edge ${Math.round(b.right)}px)`);
          }
        }
      }
      return { sw, wide: wide.slice(0, 5) };
    }, WIDTH);
    if (r.sw > WIDTH + 1) failures.push(`${name}: scrolls sideways at ${WIDTH}px (page is ${r.sw}px wide)\n    ${r.wide.join('\n    ')}`);
    await page.close();
  }
  await browser.close();
  server.close();
  if (failures.length) {
    console.log(failures.join('\n'));
    console.log(`\nFAILED: ${failures.length} of ${pages.length} pages scroll sideways at ${WIDTH}px.`);
    process.exit(1);
  }
  console.log(`OK: ${pages.length} pages fit a ${WIDTH}px screen with no sideways scroll.`);
})().catch(e => { console.error(e); process.exit(1); });
