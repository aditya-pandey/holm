"""The MODE brand film (30 s, 1920×1080, 30 fps): writes film/film.html, a stage driven by render(t).
Letters use the master geometry from src/mark.py, split into the pieces each animation needs."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "src"))
import mark      # noqa: E402
import brand     # noqa: E402
from mark import R, G, W, arc_to, f   # noqa: E402

rc = R - W / 2

# ------------------------------------------------------------------ letter pieces, each in its own 0..100 box
m_full = mark.m()[0]["solid"]
o_solid = f"M{f(R + G)} 0" + arc_to(R + G, R, R, -90, 90) + "Z"
o_hair = f"M{f(R)} {f(R + rc)}A{f(rc)} {f(rc)} 0 0 1 {f(R)} {f(R - rc)}"                  # bottom → left → top
cup = mark.CUP
bw, top, base, rb, hro, ht = cup["bw"], cup["top"], cup["base"], cup["rb"], cup["hro"], cup["ht"]
D_body = f"M0 {f(top)}H{f(bw)}V{f(base - rb)}" + arc_to(bw - rb, base - rb, rb, 0, 90) + "H0Z"
hx, hy = bw + G - 2, top + hro + 4
D_handle = f"M{f(hx)} {f(hy - hro)}" + arc_to(hx, hy, hro, -90, 90) + f"V{f(hy + hro - ht)}" + arc_to(hx, hy, hro - ht, 90, -90) + "Z"
sy = 100 - W / 2 - 2
D_saucer = f"M-8 {f(sy)}H{f(bw + 14)}"
e_left = f"M{f(R)} 0" + arc_to(R, R, R, -90, -270) + "Z"
e_quarter = f"M{f(R + G)} {f(R)}V0" + arc_to(R + G, R, R, -90, 0) + "Z"
x0, y0 = mark.pt(R + G, R, rc, 58)
x1, y1 = mark.pt(R + G, R, rc, 90)
e_tail = f"M{f(x0)} {f(y0)}A{f(rc)} {f(rc)} 0 0 1 {f(x1)} {f(y1)}"

full = {k: (mark.paths(v[0], "currentColor")) for k, v in
        (("m", mark.m()), ("o", mark.o()), ("D", mark.D()), ("e", mark.e()))}

MODES = [dict(key=m["key"], name=m["name"], line=m["line"].rstrip(".").upper(), tint=m["tint"]) for m in brand.MODES]
DATA = dict(modes=MODES, W=W)

# picto strokes (from the pack), in an 10×10 box
PICTO_FOLD = ('<rect x="1.2" y="1.0" width="5.6" height="8" rx="0.8"/>', '<path d="M1.2 5H6.8" stroke-dasharray="0.6 0.5"/>')
PAGE = r"""<!doctype html><html><head><meta charset="utf-8"><title>MODE film</title><style>
@font-face{font-family:'Instrument Sans';font-weight:400;src:url('../fonts/InstrumentSans-Regular.ttf')}
@font-face{font-family:'Instrument Sans';font-weight:500;src:url('../fonts/InstrumentSans-Medium.ttf')}
@font-face{font-family:'Instrument Sans';font-weight:600;src:url('../fonts/InstrumentSans-SemiBold.ttf')}
@font-face{font-family:'IBM Plex Mono';font-weight:400;src:url('../fonts/PlexMono-Regular.ttf')}
@font-face{font-family:'IBM Plex Mono';font-weight:500;src:url('../fonts/PlexMono-Medium.ttf')}
html,body{margin:0;width:1920px;height:1080px;overflow:hidden;background:#151515}
#stage{position:relative;width:1920px;height:1080px;overflow:hidden;font-family:'Instrument Sans',sans-serif}
.abs{position:absolute}
.mono{font-family:'IBM Plex Mono',monospace;text-transform:uppercase;letter-spacing:.18em}
.mask{overflow:hidden}
.mask>span{display:block}
svg{position:absolute;left:0;top:0}
img{display:block}
</style></head><body><div id="stage">
<div id="bg" class="abs" style="inset:0"></div>

<!-- range render, behind the modes text layer -->
<img id="range" class="abs" src="../packaging/renders/mode-range.png" style="left:0;top:0;width:1920px;height:1080px;object-fit:cover;object-position:50% 0%;opacity:0">

<svg id="sv" width="1920" height="1080" viewBox="0 0 1920 1080">
  <defs>
    <clipPath id="cm" clipPathUnits="userSpaceOnUse"><rect id="cmr"/></clipPath>
    <clipPath id="co" clipPathUnits="userSpaceOnUse"><rect id="cor"/></clipPath>
    <clipPath id="cDb" clipPathUnits="userSpaceOnUse"><rect id="cDbr"/></clipPath>
    <clipPath id="cDs" clipPathUnits="userSpaceOnUse"><rect id="cDsr"/></clipPath>
  </defs>
  <!-- the mode scenes' big tone-on-tone cup -->
  <g id="ghost" style="opacity:0">{GHOST}</g>
  <!-- single-letter scenes -->
  <g id="Lm"><circle id="drop" r="6"/><path id="m_full" d="{m_full}" clip-path="url(#cm)"/></g>
  <g id="Lo"><path id="o_hair" d="{o_hair}" fill="none" stroke-width="{W}" stroke-linecap="round"/><path id="o_solid" d="{o_solid}" clip-path="url(#co)"/></g>
  <g id="LD"><path id="D_saucer" d="{D_saucer}" fill="none" stroke-width="{W}" stroke-linecap="round" clip-path="url(#cDs)"/>
     <path id="D_body" d="{D_body}" clip-path="url(#cDb)"/><g id="D_hg"><path id="D_handle" d="{D_handle}"/></g></g>
  <g id="Le"><g id="e_lg"><path d="{e_left}"/></g><g id="e_qg"><path d="{e_quarter}"/></g>
     <path id="e_tail" d="{e_tail}" fill="none" stroke-width="{W}" stroke-linecap="round"/></g>
  <!-- the stack: four whole letters -->
  <g id="S">
    <g id="Sm">{F_m}</g><g id="So">{F_o}</g><g id="SD">{F_D}</g><g id="Se">{F_e}</g>
  </g>
</svg>

<!-- text + images -->
<div id="cap" class="abs mono" style="left:0;right:0;top:880px;text-align:center;font-size:26px"></div>
<div id="head" class="abs" style="left:980px;top:380px;width:860px;font-weight:600;font-size:92px;line-height:1.02;letter-spacing:-.025em">
  <div class="mask"><span id="h1">Every letter</span></div><div class="mask"><span id="h2">of MODE</span></div><div class="mask"><span id="h3">is a coffee.</span></div></div>
<img id="sach" class="abs" style="width:470px;border-radius:16px;filter:drop-shadow(0 30px 40px rgba(0,0,0,.28)) drop-shadow(0 6px 10px rgba(0,0,0,.18))">
<div id="mtop" class="abs" style="left:96px;top:72px;width:110px">{SMALL_LOGO}</div>
<div id="mnum" class="abs mono" style="right:96px;top:84px;font-size:22px"></div>
<div id="mname" class="abs mask" style="left:110px;top:370px;font-weight:600;font-size:250px;line-height:1;letter-spacing:-.04em;padding-bottom:30px"><span id="mname_s"></span></div>
<div id="mline" class="abs mono" style="left:124px;top:680px;font-size:30px"></div>
<div id="wipe" class="abs" style="left:0;right:0;bottom:0;height:0"></div>
<div id="rit" class="abs" style="left:0;right:0;top:0;bottom:0;display:none">{RITUAL}</div>
<div id="rtxt" class="abs" style="left:110px;top:80px;font-weight:600;font-size:80px;line-height:1.02;letter-spacing:-.025em;color:#151515">
  <div class="mask"><span id="r1">Five modes.</span></div><div class="mask"><span id="r2">One sachet each.</span></div></div>
<div id="endsub" class="abs mono" style="left:0;right:0;top:800px;text-align:center;font-size:24px;color:#151515"></div>
<div id="endtag" class="abs" style="left:0;right:0;top:860px;text-align:center;font-family:'IBM Plex Mono',monospace;font-weight:500;font-size:34px;color:#151515"></div>
<div id="endbar" class="abs" style="top:916px;height:6px;display:flex"></div>
</div>
<script>
const D = {DATA};
const PAPER = '#F4F2ED', CARBON = '#151515', OAT = '#E6DCCB', ROAST = '#4B3D2F';
const $ = (id) => document.getElementById(id);
const clamp = (v, a = 0, b = 1) => Math.min(b, Math.max(a, v));
const seg = (t, a, b) => clamp((t - a) / (b - a));
const eOut = (x) => 1 - Math.pow(1 - x, 3);
const eIn = (x) => x * x * x;
const eIO = (x) => x < .5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2;
const eBack = (x) => { const c = 1.6; return 1 + (c + 1) * Math.pow(x - 1, 3) + c * Math.pow(x - 1, 2); };
const lerp = (a, b, x) => a + (b - a) * x;
const show = (id, on) => { $(id).style.display = on ? '' : 'none'; };
const tf = (id, s) => $(id).setAttribute('transform', s);
const rect = (id, x, y, w, h) => { const r = $(id); r.setAttribute('x', x); r.setAttribute('y', y); r.setAttribute('width', Math.max(0, w)); r.setAttribute('height', Math.max(0, h)); };

// small logo for the top-left of the mode scenes
const PRELOAD = D.modes.map((m) => { const i = new Image(); i.src = `../build/tex/sachet-${m.key}-front.png`; return i; });

// letter scene placement: one letter, centred, 4.4× (letter ≈ 440 px tall)
const K1 = 4.4;
const centre = (wUnits, hUnits = 100, dy = -40) => `translate(${960 - wUnits * K1 / 2} ${540 - hUnits * K1 / 2 + dy}) scale(${K1})`;

function render(t) {
  // reset
  for (const id of ['Lm', 'Lo', 'LD', 'Le', 'S', 'ghost', 'drop']) show(id, false);
  for (const id of ['cap', 'head', 'sach', 'mtop', 'mnum', 'mname', 'mline', 'wipe', 'rit', 'rtxt', 'endsub', 'endtag', 'endbar']) $(id).style.opacity = 0;
  $('range').style.opacity = 0;
  $('rit').style.display = 'none';
  let bg = CARBON;

  const caption = (txt, a, b, col) => {
    const c = $('cap'); c.textContent = txt; c.style.color = col;
    const o = Math.min(seg(t, a, a + .35), 1 - seg(t, b - .25, b));
    c.style.opacity = o; c.style.transform = `translateY(${(1 - eOut(seg(t, a, a + .35))) * 24}px)`;
  };

  if (t < 2) {                                          // ---------- m
    bg = CARBON; show('Lm', true);
    const g = $('Lm'); g.style.color = PAPER; g.setAttribute('fill', PAPER); tf('Lm', centre(100));
    const d = $('drop'); d.setAttribute('fill', PAPER);
    if (t < .5) { show('drop', true); d.setAttribute('cx', 50); d.setAttribute('cy', lerp(-140, 25, eIn(seg(t, 0, .5)))); }
    const sq = eBack(seg(t, .5, .85));                    // the top block blooms from the impact point
    const leg = eOut(seg(t, .9, 1.45));                   // the legs pour down into drips
    const w = 100 * sq, h = 50 * sq + 50 * leg;
    rect('cmr', 50 - w / 2, 25 - 25 * sq, w, h + (sq >= .999 ? 0 : 0));
    caption('m · a square of coffee that drips', .95, 2, PAPER);
  } else if (t < 4) {                                   // ---------- o
    bg = PAPER; show('Lo', true); tf('Lo', centre(103));
    $('Lo').setAttribute('fill', CARBON); $('o_hair').setAttribute('stroke', CARBON);
    const L = Math.PI * 48.9, p = eIO(seg(t, 2.0, 2.5));
    $('o_hair').setAttribute('stroke-dasharray', `${L * p} ${L}`); $('o_hair').style.opacity = p > .01 ? 1 : 0;
    const fill = eOut(seg(t, 2.5, 3.05));                 // poured from the bottom up
    rect('cor', 50, 100 - 100 * fill, 60, 100 * fill + .5);
    caption('o · half poured, from the side', 2.95, 4, CARBON);
  } else if (t < 6) {                                   // ---------- D
    bg = OAT; show('LD', true); tf('LD', centre(103, 84, -40 - 16 * K1));
    $('LD').setAttribute('fill', CARBON); $('D_saucer').setAttribute('stroke', CARBON);
    const s = eOut(seg(t, 4.0, 4.35));
    rect('cDsr', 41 - 52 * s, 90, 104 * s, 20);
    const b = eOut(seg(t, 4.3, 4.85));                    // the cup fills from the bottom
    rect('cDbr', -2, 90 - 76 * b, 80, 76 * b + .5);
    const hpop = eBack(seg(t, 4.85, 5.2));
    tf('D_hg', `translate(${77} ${37}) scale(${hpop}) translate(${-77} ${-37})`);
    caption('D · a cup on its saucer', 4.95, 6, CARBON);
  } else if (t < 8) {                                   // ---------- e
    bg = ROAST; show('Le', true); tf('Le', centre(103));
    $('Le').setAttribute('fill', PAPER); $('e_tail').setAttribute('stroke', PAPER);
    const r = eOut(seg(t, 6.0, 6.5));                     // the half-disc swings in about its centre
    tf('e_lg', `rotate(${(1 - r) * 180} 50 50)`); $('e_lg').style.opacity = seg(t, 6.0, 6.1);
    const q = eBack(seg(t, 6.45, 6.8));
    tf('e_qg', `translate(${(1 - q) * 70} ${-(1 - q) * 70})`); $('e_qg').style.opacity = seg(t, 6.45, 6.55);
    const L = 48.9 * 32 * Math.PI / 180, p = eOut(seg(t, 6.85, 7.1));
    $('e_tail').setAttribute('stroke-dasharray', `${L * p} ${L}`); $('e_tail').style.opacity = p > .01 ? 1 : 0;
    caption('e · left open', 6.95, 8, PAPER);
  } else if (t < 10) {                                  // ---------- assembly
    bg = PAPER; show('S', true);
    const K = 2.5, ox = 250, oy = 540 - 106 * K;
    $('S').style.color = CARBON; tf('S', `translate(${ox + 9.1 * K} ${oy}) scale(${K})`);
    const from = { Sm: [-520, -420], So: [700, -480], SD: [-560, 520], Se: [760, 520] };
    const to = { Sm: [0, 0], So: [112, 0], SD: [0, 112], Se: [112, 112] };
    Object.keys(from).forEach((k, i) => {
      const p = eOut(seg(t, 8.0 + i * .07, 8.6 + i * .07));
      tf(k, `translate(${lerp(from[k][0], to[k][0], p)} ${lerp(from[k][1], to[k][1], p)}) rotate(${(1 - p) * (i % 2 ? 24 : -24)} 50 50)`);
    });
    const hd = $('head'); hd.style.opacity = 1; hd.style.color = CARBON;
    ['h1', 'h2', 'h3'].forEach((id, i) => { const p = eOut(seg(t, 8.7 + i * .12, 9.15 + i * .12)); $(id).style.transform = `translateY(${(1 - p) * 110}%)`; });
    // the first mode's tint rises like a fill level
    const w = eIO(seg(t, 9.55, 10.0)); const wp = $('wipe'); wp.style.opacity = 1; wp.style.background = D.modes[0].tint; wp.style.height = `${w * 1080}px`;
  } else if (t < 20) {                                  // ---------- the modes
    const i = Math.floor((t - 10) / 2), t0 = 10 + 2 * i, m = D.modes[i];
    bg = m.tint;
    show('ghost', true); $('ghost').style.opacity = .13; $('ghost').setAttribute('fill', PAPER); $('ghost').setAttribute('stroke', PAPER);
    const spin = (t - 10) * 3;
    tf('ghost', `translate(1010 220) scale(9.2) rotate(${-8 + spin} 45 60)`);
    const tl = $('mtop'); tl.style.opacity = 1;
    const nm = $('mnum'); nm.style.opacity = .85; nm.style.color = PAPER; nm.textContent = `${String(i + 1).padStart(2, '0')} / 05 · ${m.name} mode`;
    const n = $('mname'); n.style.opacity = 1; n.style.color = PAPER; $('mname_s').textContent = m.name;
    const pin = eOut(seg(t, t0, t0 + .42)), pout = eIn(seg(t, t0 + 1.6, t0 + 1.95));
    $('mname_s').style.transform = `translateY(${(1 - pin) * 105 - pout * 105}%)`;
    const ln = $('mline'); ln.textContent = m.line; ln.style.color = PAPER;
    ln.style.opacity = Math.min(seg(t, t0 + .25, t0 + .55), 1 - seg(t, t0 + 1.5, t0 + 1.7));
    ln.style.transform = `translateY(${(1 - eOut(seg(t, t0 + .25, t0 + .6))) * 26}px)`;
    const s = $('sach'); s.src = `../build/tex/sachet-${m.key}-front.png`; s.style.opacity = 1;
    const sin = eBack(seg(t, t0 + .05, t0 + .6)), sout = eIn(seg(t, t0 + 1.55, t0 + 1.95));
    const float = Math.sin((t - t0) * 2.2) * 6;
    s.style.left = '1240px'; s.style.top = `${190 + (1 - sin) * 900 - sout * 1000 + float}px`;
    s.style.transform = `rotate(${lerp(-16, -5, sin) + sout * 8}deg)`;
    const nxt = i < 4 ? D.modes[i + 1].tint : PAPER;
    const w = eIO(seg(t, t0 + 1.55, t0 + 2.0)); const wp = $('wipe'); wp.style.opacity = 1; wp.style.background = nxt; wp.style.height = `${w * 1080}px`;
  } else if (t < 24) {                                  // ---------- fold · squeeze · pour
    bg = PAPER; const r = $('rit'); r.style.display = ''; r.style.opacity = 1;
    [20.0, 21.333, 22.667].forEach((b, i) => {
      const p = eOut(seg(t, b, b + .4));
      const cell = $(`rc${i}`); cell.style.opacity = p; cell.style.transform = `translateY(${(1 - p) * 60}px)`;
      const a = seg(t, b + .15, b + .75);
      if (i === 0) $('fold_top').setAttribute('transform', `translate(0 5) scale(1 ${lerp(1, -0.62, eIO(a))}) translate(0 -5)`);
      if (i === 1) $('sq_drop').setAttribute('transform', `translate(0 ${eIn(a) * 1.6})`), $('sq_drop').style.opacity = 1 - seg(t, b + .7, b + .9);
      if (i === 2) $('po_drop').setAttribute('transform', `translate(0 ${eIn(a) * 2.6})`), $('po_drop').style.opacity = 1 - seg(t, b + .62, b + .75);
    });
    const w = eIO(seg(t, 23.6, 24.0)); const wp = $('wipe'); wp.style.opacity = 1; wp.style.background = '#DCD5C9'; wp.style.height = `${w * 1080}px`;
  } else if (t < 27) {                                  // ---------- the range
    bg = '#DCD5C9'; const im = $('range'); im.style.opacity = 1;
    const z = 1.0 + .07 * eIO(seg(t, 24, 27));
    im.style.transformOrigin = '50% 70%'; im.style.transform = `translateY(70px) scale(${z})`;
    $('rtxt').style.opacity = 1;
    ['r1', 'r2'].forEach((id, i) => { const p = eOut(seg(t, 24.2 + i * .15, 24.65 + i * .15)); $(id).style.transform = `translateY(${(1 - p) * 110}%)`; });
    const w = eIO(seg(t, 26.55, 27.0)); const wp = $('wipe'); wp.style.opacity = 1; wp.style.background = PAPER; wp.style.height = `${w * 1080}px`;
  } else {                                              // ---------- the classic mark
    bg = PAPER; show('S', true);
    const K = 2.0, ox = 960 - 224.1 * K / 2 + 9.1 * K, oy = 250;
    $('S').style.color = CARBON; tf('S', `translate(${ox} ${oy}) scale(${K})`);
    const to = { Sm: [0, 0], So: [112, 0], SD: [0, 112], Se: [112, 112] };
    Object.keys(to).forEach((k, i) => {
      const p = eBack(seg(t, 27.0 + i * .08, 27.4 + i * .08));
      tf(k, `translate(${to[k][0]} ${to[k][1]}) translate(50 50) scale(${lerp(.82, 1, p)}) translate(-50 -50)`);
      $(k).style.opacity = seg(t, 27.0 + i * .08, 27.15 + i * .08);
    });
    const sub = $('endsub'); sub.textContent = 'Coffee concentrate · in five modes'; sub.style.opacity = seg(t, 27.6, 27.9) * .8;
    const tag = $('endtag'); tag.textContent = '#SwitchYourMode'; tag.style.opacity = seg(t, 27.85, 28.15);
    const bar = $('endbar'); bar.style.opacity = 1; bar.style.left = '760px'; bar.style.width = '400px';
    bar.innerHTML = D.modes.map((m, i) => `<i style="flex:1;background:${m.tint};transform-origin:left;transform:scaleX(${eOut(seg(t, 28.0 + i * .09, 28.35 + i * .09))})"></i>`).join('');
  }
  $('bg').style.background = bg;
  return true;
}
window.render = render;
window.__ready = document.fonts.ready.then(() => Promise.all(PRELOAD.map((i) => i.decode().catch(() => 0)))).then(() => true);
</script></body></html>"""


def ritual():
    """Three cells: the pack's pictograms, big, with their words."""
    st = 'fill="none" stroke="#151515" stroke-width="0.32" stroke-linecap="round" stroke-linejoin="round"'
    cup_g, _ = mark.D()
    cells = []
    fold = (f'<g {st}><g id="fold_top"><path d="M1.2 5V1.8a0.8 0.8 0 0 1 0.8-0.8h4a0.8 0.8 0 0 1 0.8 0.8V5"/></g>'
            f'<path d="M1.2 5V8.2a0.8 0.8 0 0 0 0.8 0.8h4a0.8 0.8 0 0 0 0.8-0.8V5"/><path d="M0.6 5H7.4" stroke-dasharray="0.5 0.4"/></g>')
    squeeze = (f'<g {st}><path d="M1.4 1.4L4.5 6.4L7.6 1.4"/><path d="M2.8 1.4L4.5 4.4L6.2 1.4"/></g>'
               f'<path id="sq_drop" d="M4.5 6.9c-0.5 0.7-0.75 1.1-0.75 1.45a0.75 0.75 0 0 0 1.5 0c0-0.35-0.25-0.75-0.75-1.45z" fill="#151515"/>')
    pour = (f'<g transform="translate(0.9 3.4) scale(0.07)" fill="#151515">{mark.paths(cup_g, "#151515")}</g>'
            f'<path id="po_drop" d="M3.6 0.0c-0.5 0.7-0.75 1.1-0.75 1.45a0.75 0.75 0 0 0 1.5 0c0-0.35-0.25-0.75-0.75-1.45z" fill="#151515"/>')
    for i, (art, word) in enumerate(((fold, "Fold."), (squeeze, "Squeeze."), (pour, "Pour."))):
        cells.append(f'<div id="rc{i}" style="position:absolute;left:{170 + i * 560}px;top:250px;width:460px">'
                     f'<svg viewBox="-0.5 -0.5 9.5 10" width="300" height="316" style="position:static;overflow:visible">{art}</svg>'
                     f'<div style="margin-top:40px;font-weight:600;font-size:110px;letter-spacing:-.03em;color:#151515">{word}</div>'
                     f'<div class="mono" style="margin-top:10px;font-size:24px;color:#4A4C4F">{("Snap it at the line", "Into water or milk", "Hot or cold. Done.")[i]}</div></div>')
    return "".join(cells)


def small_logo():
    g, box = mark.stack(4.0)
    vb = f"{f(box[0])} {f(box[1])} {f(box[2] - box[0])} {f(box[3] - box[1])}"
    return f'<svg viewBox="{vb}" width="110" style="position:static;display:block">{mark.paths(g, "#F4F2ED")}</svg>'


def build():
    ghost = mark.paths(mark.D()[0], "currentColor").replace('fill="currentColor"', "")
    page = (PAGE.replace("{m_full}", m_full).replace("{o_hair}", o_hair).replace("{o_solid}", o_solid)
            .replace("{D_saucer}", D_saucer).replace("{D_body}", D_body).replace("{D_handle}", D_handle)
            .replace("{e_left}", e_left).replace("{e_quarter}", e_quarter).replace("{e_tail}", e_tail)
            .replace("{W}", f(W)).replace("{GHOST}", ghost).replace("{RITUAL}", ritual())
            .replace("{F_m}", full["m"]).replace("{F_o}", full["o"]).replace("{F_D}", full["D"]).replace("{F_e}", full["e"])
            .replace("{DATA}", json.dumps(DATA)).replace("{SMALL_LOGO}", small_logo()))
    out = os.path.join(HERE, "film.html")
    open(out, "w").write(page)
    return out


if __name__ == "__main__":
    print(build())
