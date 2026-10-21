// Batch renderer: NODE_PATH=$(npm root -g) node render.mjs jobs.json
// jobs: [{in: "file.svg|file.html", out: "file.png|file.pdf", w: 1200, h: 800, scale: 1, bg: "#fff", full: false}]
import { createRequire } from 'module';
import fs from 'fs';
import path from 'path';
import { pathToFileURL } from 'url';
const require = createRequire(import.meta.url);
const { chromium } = require(path.join(process.env.NODE_PATH || '/opt/node22/lib/node_modules', 'playwright'));

const jobs = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
for (const j of jobs) {
  const ctx = await browser.newContext({ viewport: { width: j.w, height: j.h || j.w }, deviceScaleFactor: j.scale || 1 });
  const page = await ctx.newPage();
  const abs = path.resolve(j.in);
  if (abs.endsWith('.svg')) {
    const svg = fs.readFileSync(abs, 'utf8').replace('<svg ', '<svg style="width:100%;height:100%" ');
    const bg = j.bg ? `background:${j.bg};` : 'background:transparent;';
    await page.setContent(`<html><body style="margin:0;${bg}"><div style="width:${j.w}px;height:${j.h || j.w}px;box-sizing:border-box;padding:${j.pad || 0}px">${svg}</div></body></html>`);
  } else {
    await page.goto(pathToFileURL(abs).href, { waitUntil: 'networkidle' });
  }
  await page.evaluate(() => document.fonts.ready);
  fs.mkdirSync(path.dirname(path.resolve(j.out)), { recursive: true });
  if (j.out.endsWith('.pdf')) {
    await page.pdf({ path: j.out, printBackground: true, preferCSSPageSize: true, ...(j.pdf || {}) });
  } else {
    await page.screenshot({ path: j.out, omitBackground: !j.bg, fullPage: !!j.full });
  }
  await ctx.close();
}
await browser.close();
console.log(`rendered ${jobs.length}`);
