// Render the film's 3D shots frame by frame: node film/shots3d.mjs [shot ...] [--frames N] [--test u1,u2]
// Writes film/frames/<shot>/0000.jpg … (1920×1080). Shots use the scene definitions in src/scene.js (film-*).
import http from 'http';
import fs from 'fs';
import path from 'path';
import { createRequire } from 'module';
const require = createRequire(import.meta.url);
const { chromium } = require(path.join(process.env.NODE_PATH || '/opt/node22/lib/node_modules', 'playwright'));

const ROOT = path.resolve(path.dirname(new URL(import.meta.url).pathname), '..');
const TYPES = { '.html': 'text/html', '.js': 'text/javascript', '.png': 'image/png' };
const server = http.createServer((req, res) => {
  const p = path.join(ROOT, decodeURIComponent(req.url.split('?')[0].split('#')[0]));
  if (!p.startsWith(ROOT) || !fs.existsSync(p)) { res.writeHead(404); return res.end(); }
  res.writeHead(200, { 'Content-Type': TYPES[path.extname(p)] || 'application/octet-stream' });
  fs.createReadStream(p).pipe(res);
});
await new Promise((r) => server.listen(0, '127.0.0.1', r));
fs.writeFileSync(path.join(ROOT, 'src', 'scene.html'),
  '<!doctype html><html><head><meta charset="utf-8"><style>html,body{margin:0;overflow:hidden;background:#000}</style>' +
  '<script type="importmap">{"imports":{"three":"./three.module.js"}}</script></head><body><script type="module" src="scene.js"></script></body></html>');
const args = process.argv.slice(2);
const fi = args.indexOf('--frames'); const N = fi >= 0 ? Number(args[fi + 1]) : 113;
const ti = args.indexOf('--test'); const test = ti >= 0 ? args[ti + 1].split(',').map(Number) : null;
const shots = args.filter((a, i) => !a.startsWith('--') && !(i > 0 && args[i - 1].startsWith('--')));
const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome',
  args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
for (const s of (shots.length ? shots : ['fan', 'range', 'hero'])) {
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
  page.on('pageerror', (e) => console.log(s, 'pageerror', e.message));
  await page.goto(`http://127.0.0.1:${server.address().port}/src/scene.html?tm=linear#film-${s}`);
  await page.waitForFunction(() => window.__done || window.__error, null, { timeout: 300000 });
  const err = await page.evaluate(() => window.__error); if (err) { console.log(s, err); continue; }
  const dir = path.join(ROOT, 'film', 'frames', s); fs.mkdirSync(dir, { recursive: true });
  const us = test || Array.from({ length: N }, (_, i) => i / (N - 1));
  const t0 = Date.now();
  for (let i = 0; i < us.length; i++) {
    await page.evaluate((u) => window.frameAt(u), us[i]);
    await page.screenshot({ path: path.join(dir, test ? `test-${us[i]}.jpg` : `${String(i).padStart(4, '0')}.jpg`), type: 'jpeg', quality: 93 });
  }
  console.log(s, us.length, 'frames', ((Date.now() - t0) / 1000).toFixed(0) + 's');
  await page.close();
}
await browser.close(); server.close();
