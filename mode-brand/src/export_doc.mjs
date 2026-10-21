// Guidelines → PDF (16:9 pages) + a PNG preview of every page, and a screen screenshot for review.
import fs from 'fs';
import path from 'path';
import { pathToFileURL } from 'url';
import { createRequire } from 'module';
const require = createRequire(import.meta.url);
const { chromium } = require(path.join(process.env.NODE_PATH || '/opt/node22/lib/node_modules', 'playwright'));

const ROOT = path.resolve(path.dirname(new URL(import.meta.url).pathname), '..');
const src = path.join(ROOT, 'guidelines', 'mode-brand-guidelines.html');
// the published page is wrapped in a skeleton; locally, wrap it the same way
const wrapped = path.join(ROOT, 'guidelines', '.print.html');
fs.writeFileSync(wrapped, '<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"></head><body>'
  + fs.readFileSync(src, 'utf8') + '</body></html>');
const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
const page = await browser.newPage({ viewport: { width: 1600, height: 900 } });
await page.goto(pathToFileURL(wrapped).href, { waitUntil: 'networkidle' });
await page.evaluate(() => document.fonts.ready);
await page.pdf({ path: path.join(ROOT, 'guidelines', 'MODE-Brand-Guidelines.pdf'), printBackground: true, preferCSSPageSize: true });
const prev = path.join(ROOT, 'build', 'pages');
fs.mkdirSync(prev, { recursive: true });
await page.emulateMedia({ media: 'print' });
const n = await page.locator('section.pg').count();
for (let i = 0; i < n; i++) {
  await page.locator('section.pg').nth(i).screenshot({ path: path.join(prev, `p${String(i + 1).padStart(2, '0')}.png`) });
}
await page.emulateMedia({ media: 'screen' });
for (const [w, name] of [[1280, 'screen-desktop'], [390, 'screen-mobile']]) {
  await page.setViewportSize({ width: w, height: 900 });
  await page.screenshot({ path: path.join(ROOT, 'build', `${name}.png`), fullPage: true });
}
console.log('pages', n);
await browser.close();
fs.unlinkSync(wrapped);
