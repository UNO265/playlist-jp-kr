// Render an SVG to a 1920x1080 PNG: node scripts/render_svg.js in.svg out.png
const { chromium } = require('playwright');
const fs = require('fs');
(async () => {
  const [src, out] = process.argv.slice(2);
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
  await page.setContent(`<html><body style="margin:0">${fs.readFileSync(src, 'utf8')}</body></html>`);
  await page.locator('svg').screenshot({ path: out });
  await browser.close();
})();
