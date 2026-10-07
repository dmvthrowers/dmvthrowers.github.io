// Renders the two share cards from cards.html into assets/images/og/ (1200 x 630 PNG).
// Needs Node and Playwright with Chromium:  node scripts/share-cards/render.js
const { chromium } = require('playwright');
const path = require('path');
const root = path.resolve(__dirname, '../..');
(async () => {
  const browser = await chromium.launch(process.env.CHROMIUM_PATH ? { executablePath: process.env.CHROMIUM_PATH } : {});
  const page = await browser.newPage({ viewport: { width: 1200, height: 630 } });
  for (const [cls, out] of [['dmvt', 'dmvt-share.png'], ['vsyc', 'vsyc26-share.png']]) {
    await page.goto('file://' + path.join(__dirname, 'cards.html'));
    await page.evaluate((c) => { document.body.className = c; }, cls);
    await page.evaluate(() => document.fonts.ready);
    await page.waitForTimeout(300);
    await page.screenshot({ path: path.join(root, 'assets/images/og', out), clip: { x: 0, y: 0, width: 1200, height: 630 } });
    console.log('wrote assets/images/og/' + out);
  }
  await browser.close();
})();
