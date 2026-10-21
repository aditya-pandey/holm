// Render film/film.html frame by frame and encode with the music.
//   node film/render.mjs                 → film/out/MODE-brand-film-1080p.mp4
//   node film/render.mjs --stills 0.4,3,9.6   → film/out/stills/t-<sec>.png (for review)
import { spawn } from 'child_process';
import path from 'path';
import fs from 'fs';
import { pathToFileURL } from 'url';
import { createRequire } from 'module';
const require = createRequire(import.meta.url);
const { chromium } = require(path.join(process.env.NODE_PATH || '/opt/node22/lib/node_modules', 'playwright'));

const HERE = path.dirname(new URL(import.meta.url).pathname);
const FPS = 30, DUR = 30, W = 1920, H = 1080;
const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
const page = await browser.newPage({ viewport: { width: W, height: H } });
page.on('pageerror', (e) => console.log('pageerror', e.message));
await page.goto(pathToFileURL(path.join(HERE, 'film.html')).href);
await page.evaluate(() => window.__ready);

const i = process.argv.indexOf('--stills');
if (i > 0) {
  const ts = process.argv[i + 1].split(',').map(Number);
  fs.mkdirSync(path.join(HERE, '..', 'out', 'stills'), { recursive: true });
  for (const t of ts) {
    await page.evaluate(async (t) => await window.render(t, Math.round(t * 30)), t);
    await page.screenshot({ path: path.join(HERE, '..', 'out', 'stills', `t-${t.toFixed(2)}.png`) });
  }
  console.log('stills', ts.length);
} else {
  const out = path.join(HERE, '..', 'out', 'MODE-brand-film-v2-1080p.mp4');
  const ff = spawn('ffmpeg', ['-hide_banner', '-loglevel', 'error', '-y', '-f', 'image2pipe', '-framerate', String(FPS), '-c:v', 'png', '-i', '-',
    '-i', path.join(HERE, '..', 'out', 'mode-music-v2.wav'),
    '-c:v', 'libx264', '-preset', 'slow', '-crf', '16', '-pix_fmt', 'yuv420p', '-profile:v', 'high', '-r', String(FPS),
    '-c:a', 'aac', '-b:a', '256k', '-shortest', '-movflags', '+faststart', out], { stdio: ['pipe', 'inherit', 'inherit'] });
  const t0 = Date.now();
  for (let f = 0; f < FPS * DUR; f++) {
    await page.evaluate(async (f) => await window.render(f / 30, f), f);
    const buf = await page.screenshot({ type: 'png' });
    if (!ff.stdin.write(buf)) await new Promise((r) => ff.stdin.once('drain', r));
    if (f % 150 === 0) console.log('frame', f, ((Date.now() - t0) / 1000).toFixed(0) + 's');
  }
  ff.stdin.end();
  await new Promise((r) => ff.on('close', r));
  console.log('done', out, ((Date.now() - t0) / 1000).toFixed(0) + 's');
}
await browser.close();
