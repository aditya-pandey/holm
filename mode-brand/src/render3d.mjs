// Render the packaging scenes: node src/render3d.mjs [scene ...]. Serves the kit over a tiny local HTTP server
// (WebGL will not read textures from file://), then screenshots each scene to packaging/renders/<scene>.png.
import http from 'http';
import fs from 'fs';
import path from 'path';
import { createRequire } from 'module';
const require = createRequire(import.meta.url);
const { chromium } = require(path.join(process.env.NODE_PATH || '/opt/node22/lib/node_modules', 'playwright'));

const ROOT = path.resolve(path.dirname(new URL(import.meta.url).pathname), '..');
const TYPES = { '.html': 'text/html', '.js': 'text/javascript', '.png': 'image/png', '.json': 'application/json' };
const server = http.createServer((req, res) => {
  const p = path.join(ROOT, decodeURIComponent(req.url.split('?')[0].split('#')[0]));
  if (!p.startsWith(ROOT) || !fs.existsSync(p)) { res.writeHead(404); return res.end(); }
  res.writeHead(200, { 'Content-Type': TYPES[path.extname(p)] || 'application/octet-stream' });
  fs.createReadStream(p).pipe(res);
});
await new Promise((r) => server.listen(0, '127.0.0.1', r));
const port = server.address().port;
fs.writeFileSync(path.join(ROOT, 'src', 'scene.html'),
  '<!doctype html><html><head><meta charset="utf-8"><style>html,body{margin:0;overflow:hidden;background:#000}</style></head>' +
  '<body><script type="module" src="scene.js"></script></body></html>');

const all = ['sachets', 'frontback', 'carton', 'range', 'mailer-open', 'mailer-closed', 'tumbler'];
const names = process.argv.slice(2).length ? process.argv.slice(2) : all;
const [w, h] = [1800, 1200];
const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome',
  args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
fs.mkdirSync(path.join(ROOT, 'packaging', 'renders'), { recursive: true });
for (const n of names) {
  const page = await browser.newPage({ viewport: { width: w, height: h } });
  page.on('console', (m) => { if (m.type() === 'error') console.log(n, 'console:', m.text()); });
  page.on('pageerror', (e) => console.log(n, 'pageerror:', e.message));
  const t0 = Date.now();
  await page.goto(`http://127.0.0.1:${port}/src/scene.html?tm=${process.env.TM || 'linear'}#${n}`);
  await page.waitForFunction(() => window.__done || window.__error, null, { timeout: 300000 });
  const err = await page.evaluate(() => window.__error);
  if (err) { console.log(n, 'ERROR', err); await page.close(); continue; }
  await page.screenshot({ path: path.join(ROOT, 'packaging', 'renders', `mode-${n}.png`) });
  console.log(n, ((Date.now() - t0) / 1000).toFixed(1) + 's');
  await page.close();
}
await browser.close();
server.close();
