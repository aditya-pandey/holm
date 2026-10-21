"""MODE film v2 — 'From sketch to sachet'. Writes film/v2/film.html, a 1920×1080 stage driven by render(t).
Bars 1–10: the mark derived on paper (pencil, compass, ink). Bars 11–16: the product, in 3D (film/frames/*)."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "src"))
import mark      # noqa: E402

TL = json.load(open(os.path.join(HERE, "timeline.json")))
FR = os.path.join(HERE, "..", "frames")
TL["nframes"] = {s: len([n for n in os.listdir(os.path.join(FR, s)) if n[0].isdigit()]) if os.path.isdir(os.path.join(FR, s)) else 0
                 for s, *_ in TL["shots"]}


def stack_svg(fill, width, extra=""):
    g, box = mark.stack()
    vb = f"{mark.f(box[0])} {mark.f(box[1])} {mark.f(box[2] - box[0])} {mark.f(box[3] - box[1])}"
    return f'<svg viewBox="{vb}" width="{width}" style="display:block;overflow:visible" {extra}>{mark.paths(g, fill)}</svg>'


labels = "".join(f'<text id="l{i}" class="lab" x="{l["x"]}" y="{l["y"]}" font-size="{l["size"]}" text-anchor="{l["anchor"]}">{l["text"]}</text>'
                 for i, l in enumerate(TL["labels"]))

PAGE = r"""<!doctype html><html><head><meta charset="utf-8"><title>MODE film</title><style>
@font-face{font-family:'Instrument Sans';font-weight:400;src:url('../../fonts/InstrumentSans-Regular.ttf')}
@font-face{font-family:'Instrument Sans';font-weight:600;src:url('../../fonts/InstrumentSans-SemiBold.ttf')}
@font-face{font-family:'IBM Plex Mono';font-weight:400;src:url('../../fonts/PlexMono-Regular.ttf')}
@font-face{font-family:'IBM Plex Mono';font-weight:500;src:url('../../fonts/PlexMono-Medium.ttf')}
html,body{margin:0;width:1920px;height:1080px;overflow:hidden;background:#0e0e0e}
#stage{position:relative;width:1920px;height:1080px;overflow:hidden;font-family:'Instrument Sans',sans-serif;background:#F1EEE7}
.L{position:absolute;inset:0}
.mono{font-family:'IBM Plex Mono',monospace;text-transform:uppercase;letter-spacing:.2em}
.pencil{fill:none;stroke:#2a2a2a;stroke-opacity:.62;stroke-width:1.5px;vector-effect:non-scaling-stroke;stroke-linecap:round}
.pencil.second{stroke-opacity:.26;stroke-width:1px}
.guide{fill:none;stroke:#2a2a2a;stroke-opacity:.22;stroke-width:1px;vector-effect:non-scaling-stroke}
.guide.second{display:none}
.pen{fill:none;stroke:#151515;stroke-linecap:round}
.lab{font-family:'IBM Plex Mono',monospace;fill:#3a3a3a;letter-spacing:.04em}
.mask{overflow:hidden}.mask>span{display:block}
</style></head><body><div id="stage">
<div id="sheet" class="L"><svg width="1920" height="1080" viewBox="0 0 1920 1080" style="display:block">
  <defs>{INKCLIPS}</defs>
  <g id="cam">
    <image href="paper.jpg" x="-500" y="-420" width="1300" height="1000" preserveAspectRatio="none"/>
    <g id="construct">{STROKES_PENCIL}{LABELS}</g>
    <g id="inked">{INKS}{STROKES_PEN}</g>
    <line id="arm" x1="0" y1="0" x2="0" y2="0" stroke="#2a2a2a" stroke-opacity=".35" stroke-width="1" vector-effect="non-scaling-stroke"/>
    <circle id="tip" r="1" fill="#1d1d1d"/>
  </g>
</svg></div>
<img id="shot" class="L" style="width:1920px;height:1080px;display:none">
<div id="cw" class="L" style="display:none;align-items:center;justify-content:center"><div id="cwlogo" style="width:560px"></div></div>
<div id="card" class="L" style="display:none;background:#151515;color:#F4F2ED;align-items:center;justify-content:center">
  <div id="cardtxt" style="font-weight:600;font-size:176px;letter-spacing:-.035em"></div></div>
<div id="words" class="L" style="display:none"><div style="position:absolute;left:1020px;top:330px;font-weight:600;font-size:118px;line-height:1.0;letter-spacing:-.035em;color:#151515">
  {WORDS}</div></div>
<div id="modetag" class="mono" style="position:absolute;left:96px;bottom:92px;font-size:30px;color:#151515;display:none"></div>
<div id="rtxt" style="position:absolute;left:96px;top:84px;font-weight:600;font-size:84px;line-height:1.02;letter-spacing:-.03em;color:#151515;display:none">
  <div class="mask"><span id="r1">Five modes.</span></div><div class="mask"><span id="r2">One sachet each.</span></div></div>
<div id="end" style="position:absolute;left:150px;top:250px;width:520px;display:none">
  <div id="endlogo" style="width:330px">{ENDLOGO}</div>
  <div id="endsub" class="mono" style="margin-top:56px;font-size:22px;color:#151515">Coffee concentrate · in five modes</div>
  <div id="endtag" style="margin-top:18px;font-family:'IBM Plex Mono',monospace;font-weight:500;font-size:34px;color:#151515">#SwitchYourMode</div>
  <div id="endbar" style="margin-top:14px;width:330px;height:6px;display:flex">{ENDBAR}</div></div>
<div id="vig" class="L" style="background:radial-gradient(ellipse at 50% 46%,rgba(0,0,0,0) 55%,rgba(0,0,0,.22) 100%);pointer-events:none"></div>
<img id="grain" class="L" style="width:1920px;height:1080px;mix-blend-mode:overlay;opacity:.55">
<div id="barT" style="position:absolute;left:0;right:0;top:0;height:138px;background:#0e0e0e"></div>
<div id="barB" style="position:absolute;left:0;right:0;bottom:0;height:138px;background:#0e0e0e">
  <div id="fig" class="mono" style="position:absolute;left:96px;top:54px;font-size:20px;color:#F4F2ED;opacity:.75"></div>
  <div class="mono" style="position:absolute;right:96px;top:54px;font-size:20px;color:#F4F2ED;opacity:.45">MODE · a study in four letters</div></div>
</div>
<script>
const T = {TL};
const $ = (id) => document.getElementById(id);
const clamp = (v, a = 0, b = 1) => Math.min(b, Math.max(a, v));
const seg = (t, a, b) => clamp((t - a) / (b - a));
const eOut = (x) => 1 - Math.pow(1 - x, 3), eIn = (x) => x * x * x;
const eIO = (x) => x < .5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2;
const eQ = (x) => 1 - Math.pow(1 - x, 2);
const lerp = (a, b, x) => a + (b - a) * x;
const BEAT = T.beat, BAR = T.bar, b = (bar, beat = 0) => (bar - 1) * BAR + beat * BEAT;
$('cwlogo').innerHTML = {CWLOGO};
const SP = T.strokes.map((s, i) => ({ s, el: $('s' + i), el2: $('s' + i + 'b') }));
SP.forEach((o) => { o.len = o.el.getTotalLength(); });

// segments start at a cut and drift to their end key with a gentle ease-out
function camAt(t) {
  const K = T.cam;
  for (let i = 0; i < K.length - 1; i++) {
    const a = K[i], c = K[i + 1];
    if (t >= a[0] && t < c[0]) {
      const isCut = T.cuts.some((x) => Math.abs(x - a[0]) < 1e-6) || i === 0;
      const nextIsCut = T.cuts.some((x) => Math.abs(x - c[0]) < 1e-6);
      if (nextIsCut && !isCut) return a;
      const u = isCut ? eQ(seg(t, a[0], c[0])) : eIO(seg(t, a[0], c[0]));
      return [lerp(a[1], c[1], u), lerp(a[2], c[2], u), lerp(a[3], c[3], u), lerp(a[4], c[4], u)];
    }
  }
  const z = K[K.length - 1]; return [z[1], z[2], z[3], z[4]];
}
const camTf = (c) => `translate(960 540) rotate(${c[3]}) scale(${c[2]}) translate(${-c[0]} ${-c[1]})`;

let lastShot = '';
async function render(t, frame = 0) {
  const st = $('stage');
  // ------------------------------------------------ the sheet
  const c = camAt(t);
  $('cam').setAttribute('transform', camTf(c));
  const p = camAt(Math.max(0, t - 1 / 30));
  const crossCut = T.cuts.some((x) => x > t - 1 / 30 && x <= t);
  const dv = crossCut ? 0 : Math.hypot((c[0] - p[0]) * c[2], (c[1] - p[1]) * c[2]) + Math.abs(c[2] - p[2]) * 60;
  $('sheet').style.filter = dv > 6 ? `blur(${Math.min(7, dv / 22).toFixed(2)}px)` : 'none';
  let tip = null;
  SP.forEach((o) => {
    const s = o.s, q = s.kind === 'guide' ? eQ(seg(t, s.t0, s.t0 + s.dur)) : eIO(seg(t, s.t0, s.t0 + s.dur));
    const on = q > 0.001;
    o.el.style.display = on ? '' : 'none'; if (o.el2) o.el2.style.display = on ? '' : 'none';
    o.el.setAttribute('stroke-dasharray', `${q} 1`); if (o.el2) o.el2.setAttribute('stroke-dasharray', `${q} 1`);
    if (on && q < 0.999 && s.kind !== 'guide') tip = { o, q };
  });
  if (tip) {
    const pt = tip.o.el.getPointAtLength(tip.q * tip.o.len);
    $('tip').style.display = ''; $('tip').setAttribute('cx', pt.x); $('tip').setAttribute('cy', pt.y); $('tip').setAttribute('r', 2.6 / c[2]);
    if (tip.o.s.cx !== undefined) {
      $('arm').style.display = ''; $('arm').setAttribute('x1', tip.o.s.cx); $('arm').setAttribute('y1', tip.o.s.cy);
      $('arm').setAttribute('x2', pt.x); $('arm').setAttribute('y2', pt.y);
    } else $('arm').style.display = 'none';
  } else { $('tip').style.display = 'none'; $('arm').style.display = 'none'; }
  T.inks.forEach((k, i) => { $('icc' + i).setAttribute('r', eOut(seg(t, k.t0, k.t0 + k.dur)) * 150); });
  T.labels.forEach((l, i) => { const o = seg(t, l.t0, l.t0 + .25); $('l' + i).style.opacity = o; });
  const er = seg(t, T.erase[0], T.erase[1]);
  $('construct').style.opacity = 1 - eIO(er);

  // ------------------------------------------------ flash cards
  const card = T.cards.find(([a, z]) => t >= a && t < z);
  $('card').style.display = card ? 'flex' : 'none';
  if (card) { $('cardtxt').textContent = card[2]; const u = seg(t, card[0], card[1]); $('cardtxt').style.transform = `scale(${lerp(1.08, 1.0, eOut(u))})`; }
  // ------------------------------------------------ words (bar 9)
  const wOn = t >= b(9) && t < b(10, 0.5);
  $('words').style.display = wOn ? '' : 'none';
  T.words.forEach(([a], i) => { const u = eOut(seg(t, a, a + .3)); $('w' + i).style.transform = `translateY(${(1 - u) * 110}%)`; });
  if (wOn) $('words').style.opacity = 1 - eIn(seg(t, b(10, 0.0), b(10, 0.45)));
  // ------------------------------------------------ colour-way cuts (bar 10)
  const k = Math.floor((t - T.cw_t0) / (BEAT / 2));
  const cwOn = t >= T.cw_t0 && t < b(11) && k < T.colourways.length;
  $('cw').style.display = cwOn ? 'flex' : 'none';
  if (cwOn) { $('cw').style.background = T.colourways[k][0]; $('cwlogo').style.color = T.colourways[k][1];
    $('cwlogo').style.transform = `scale(${lerp(1.06, 1, eOut(seg(t, T.cw_t0 + k * BEAT / 2, T.cw_t0 + (k + .8) * BEAT / 2)))})`; }
  // ------------------------------------------------ 3D shots
  const sh = T.shots.find(([s, a, z]) => t >= a && t < z + 1e-6);
  const img = $('shot');
  if (sh) {
    const n = T.nframes[sh[0]] || 1;
    const idx = Math.min(n - 1, Math.round(seg(t, sh[1], sh[2]) * (n - 1)));
    const src = `../frames/${sh[0]}/${String(idx).padStart(4, '0')}.jpg`;
    img.style.display = '';
    if (src !== lastShot) { img.src = src; lastShot = src; try { await img.decode(); } catch (e) {} }
    // a white flash on each cut into a shot
    img.style.filter = `brightness(${1 + .5 * (1 - eOut(seg(t, sh[1], sh[1] + .18)))})`;
  } else img.style.display = 'none';
  // mode tags over the fan
  const mt = T.mode_tags.filter(([a]) => t >= a && t < b(13)).pop();
  $('modetag').style.display = mt ? '' : 'none';
  if (mt) { $('modetag').textContent = mt[1]; $('modetag').style.opacity = eOut(seg(t, mt[0], mt[0] + .15)); }
  const rOn = t >= b(13, .3) && t < b(15);
  $('rtxt').style.display = rOn ? '' : 'none';
  ['r1', 'r2'].forEach((id, i) => { const u = eOut(seg(t, b(13, .3 + i * .4), b(13, .9 + i * .4))); $(id).style.transform = `translateY(${(1 - u) * 110}%)`; });
  const eOn = t >= b(15, .6);
  $('end').style.display = eOn ? '' : 'none';
  if (eOn) {
    $('endlogo').style.opacity = eOut(seg(t, b(15, .6), b(15, 1.4))); $('endlogo').style.transform = `translateY(${(1 - eOut(seg(t, b(15, .6), b(15, 1.4)))) * 30}px)`;
    $('endsub').style.opacity = seg(t, b(15, 1.6), b(15, 2.2)) * .85; $('endtag').style.opacity = seg(t, b(15, 2.2), b(15, 2.8));
    [...$('endbar').children].forEach((el, i) => { el.style.transform = `scaleX(${eOut(seg(t, b(15, 2.6 + i * .25), b(15, 3.2 + i * .25)))})`; });
  }
  // ------------------------------------------------ letterbox, grain, captions
  const open = eIO(seg(t, b(11), b(11, .9)));
  $('barT').style.height = $('barB').style.height = `${138 * (1 - open)}px`;
  const fig = T.figs.find(([a, z]) => t >= a && t < z);
  $('fig').textContent = fig ? fig[2] : ''; $('fig').style.opacity = fig ? .75 * seg(t, fig[0], fig[0] + .2) : 0;
  $('grain').src = `grain${frame % 8}.png`;
  $('vig').style.opacity = sh ? .6 : 1;
  return true;
}
window.render = render;
window.__ready = document.fonts.ready.then(() => true);
</script></body></html>"""


def build():
    # split strokes into construction (pencil/guide) and pen (ink lines, which stay)
    pen_html, con_html = "", ""
    for i, s in enumerate(TL["strokes"]):
        if s["kind"] == "pen":
            pen_html += f'<path id="s{i}" class="pen" d="{s["d"]}" pathLength="1" stroke-width="{s.get("w", mark.W)}"/>'
        else:
            cls = "guide" if s["kind"] == "guide" else "pencil"
            con_html += (f'<path id="s{i}" class="{cls}" d="{s["d"]}" pathLength="1"/>'
                         f'<path id="s{i}b" class="{cls} second" d="{s["d"]}" pathLength="1" transform="translate(.35 .3)"/>')
    clips = "".join(f'<clipPath id="ic{i}" clipPathUnits="userSpaceOnUse"><circle id="icc{i}" cx="{k["ox"]}" cy="{k["oy"]}" r="0"/></clipPath>'
                    for i, k in enumerate(TL["inks"]))
    ink_paths = "".join(f'<path id="i{i}" d="{k["d"]}" fill="#151515" clip-path="url(#ic{i})"/>' for i, k in enumerate(TL["inks"]))
    words = "".join(f'<div class="mask"><span id="w{i}">{w}</span></div>' for i, (_, w) in enumerate(TL["words"]))
    tints = ["#2771BE", "#0B8457", "#4F758B", "#557F22", "#8C6A4E"]
    endbar = "".join(f'<i style="flex:1;background:{c};transform-origin:left;transform:scaleX(0)"></i>' for c in tints)
    g, box = mark.stack()
    vb = f"{mark.f(box[0])} {mark.f(box[1])} {mark.f(box[2] - box[0])} {mark.f(box[3] - box[1])}"
    cwlogo = json.dumps(f'<svg viewBox="{vb}" width="560" style="display:block">{mark.paths(g, "currentColor")}</svg>')
    page = (PAGE.replace("{INKCLIPS}", clips).replace("{STROKES_PENCIL}", con_html).replace("{LABELS}", labels)
            .replace("{INKS}", ink_paths).replace("{STROKES_PEN}", pen_html).replace("{WORDS}", words)
            .replace("{ENDLOGO}", stack_svg("#151515", 330)).replace("{ENDBAR}", endbar).replace("{CWLOGO}", cwlogo)
            .replace("{TL}", json.dumps(TL)))
    out = os.path.join(HERE, "film.html")
    open(out, "w").write(page)
    return out


if __name__ == "__main__":
    print(build())
