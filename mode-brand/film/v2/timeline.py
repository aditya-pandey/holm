"""The art section of the film, as data: every pencil stroke, compass arc, ink flood, label and camera key.
128 BPM: beat 0.46875 s, bar 1.875 s, 16 bars = 30 s. Sheet units = the mark's units (stack 224 × 212).
Writes film/v2/timeline.json, read by the film page and by the music (for synced pencil sounds)."""
import json
import math
import os
import sys
import random

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "src"))
import mark                     # noqa: E402
from mark import R, G, W, f     # noqa: E402

BEAT = 60 / 128
BAR = 4 * BEAT
b = lambda bar, beat=0.0: (bar - 1) * BAR + beat * BEAT      # time of a bar (1-based) + beats
rnd = random.Random(11)

strokes, inks, labels = [], [], []


def ruler(p0, p1, t0, dur=0.16, ext=6.0, kind="pencil"):
    """A ruled pencil line, overshooting both ends, with a hair of bow."""
    (x0, y0), (x1, y1) = p0, p1
    L = math.hypot(x1 - x0, y1 - y0)
    ux, uy = (x1 - x0) / L, (y1 - y0) / L
    a = (x0 - ux * ext, y0 - uy * ext)
    z = (x1 + ux * ext, y1 + uy * ext)
    bow = rnd.uniform(-0.6, 0.6)
    m = ((a[0] + z[0]) / 2 - uy * bow, (a[1] + z[1]) / 2 + ux * bow)
    strokes.append(dict(d=f"M{f(a[0])} {f(a[1])}Q{f(m[0])} {f(m[1])} {f(z[0])} {f(z[1])}", t0=t0, dur=dur, kind=kind))


def compass(cx, cy, r, t0, dur=0.42, a0=None, sweep=372.0, kind="compass"):
    """A compass arc: starts anywhere, runs a little past a full turn."""
    a0 = rnd.uniform(-160, 20) if a0 is None else a0
    x, y = mark.pt(cx, cy, r, a0)
    strokes.append(dict(d=f"M{f(x)} {f(y)}" + mark.arc_to(cx, cy, r, a0, a0 + sweep), t0=t0, dur=dur, kind=kind, cx=cx, cy=cy))


def cross(cx, cy, t0, s=3.5):
    strokes.append(dict(d=f"M{f(cx - s)} {f(cy)}H{f(cx + s)}M{f(cx)} {f(cy - s)}V{f(cy + s)}", t0=t0, dur=0.06, kind="pencil"))


def pen(d, t0, dur, width=W):
    strokes.append(dict(d=d, t0=t0, dur=dur, kind="pen", w=width))


def ink(d, ox, oy, t0, dur=0.34):
    inks.append(dict(d=d, ox=ox, oy=oy, t0=t0, dur=dur))


def label(x, y, text, t0, size=4.6, anchor="start"):
    labels.append(dict(x=x, y=y, text=text, t0=t0, size=size, anchor=anchor))


# ------------------------------------------------------------------ bar 1: the square
for i, (p0, p1) in enumerate((((0, 0), (100, 0)), ((100, 0), (100, 100)), ((100, 100), (0, 100)), ((0, 100), (0, 0)))):
    ruler(p0, p1, b(1, 0.15 + i * 0.85), 0.24)
label(50, -8, "100", b(1, 3.5), anchor="middle")
# ------------------------------------------------------------------ bar 2: one radius
cross(162, 50, b(2, 0.0))
compass(162, 50, 50, b(2, 0.25), 0.62, a0=-90)
label(170, 40, "R 50", b(2, 1.6))
ruler((162, 50), (197.4, 14.6), b(2, 1.35), 0.12, ext=0)
# ------------------------------------------------------------------ bar 3: the grid and the cut
grid_t = b(3, 0.0)
for i, x in enumerate((0, 100, 112, 215)):
    ruler((x, -40), (x, 252), grid_t + i * 0.07, 0.2, ext=0, kind="guide")
for i, y in enumerate((0, 50, 100, 112, 162, 212)):
    ruler((-40, y), (255, y), grid_t + 0.12 + i * 0.06, 0.2, ext=0, kind="guide")
ruler((162, -6), (162, 106), b(3, 1.6), 0.14, ext=0)
ruler((165, -6), (165, 106), b(3, 1.85), 0.14, ext=0)
label(163.5, -10, "cut 3", b(3, 2.2), anchor="middle")
label(106, -14, "12", b(3, 1.2), anchor="middle")
label(-14, 52, "½", b(3, 1.4), anchor="end", size=6)
label(-14, 108, "12", b(3, 1.5), anchor="end")
# ------------------------------------------------------------------ bar 4: one hairline (the o's left half, in ink)
rc = R - W / 2
pen(f"M162 {f(50 + rc)}A{f(rc)} {f(rc)} 0 0 1 162 {f(50 - rc)}", b(4, 0.2), 0.75)
label(108, 30, "hairline 2.2", b(4, 1.6), anchor="end")
# ------------------------------------------------------------------ bar 5: m
t = b(5)
ruler((-6, 50), (106, 50), t + 0.02, 0.14, ext=0)
for cx in (30, 70):
    compass(cx, 50, 10, t + 0.16 + (cx - 30) / 40 * 0.16, 0.22)
for i, x in enumerate((20, 40, 60, 80)):
    ruler((x, 50), (x, 90), t + 0.5 + i * 0.04, 0.12, ext=3)
for i, cx in enumerate((10, 50, 90)):
    compass(cx, 90, 10, t + 0.72 + i * 0.07, 0.18)
ink(mark.m()[0]["solid"], 50, -10, b(5, 2.0), 0.42)
label(50, 120, "the arches stop halfway", b(5, 2.9), anchor="middle", size=4.0)
# ------------------------------------------------------------------ bar 6: o
t = b(6)
ruler((165, 50), (222, 50), t + 0.05, 0.14, ext=0)
o_solid = f"M{f(R + G + 112)} 0" + mark.arc_to(R + G + 112, R, R, -90, 90) + "Z"
ink(o_solid, 190, 104, b(6, 1.0), 0.45)
label(220, 106, "poured from the side", b(6, 2.6), anchor="end", size=4.0)
# ------------------------------------------------------------------ bar 7: D (at 0, 112)
t = b(7)
cup = mark.CUP
oy = 112
ruler((-10, oy + cup["top"]), (86, oy + cup["top"]), t + 0.02, 0.13)
ruler((0, oy + 6), (0, oy + 98), t + 0.12, 0.13)
cross(cup["bw"] - cup["rb"], oy + cup["base"] - cup["rb"], t + 0.24)
compass(cup["bw"] - cup["rb"], oy + cup["base"] - cup["rb"], cup["rb"], t + 0.3, 0.4, a0=-40, sweep=150)
hx, hy = cup["bw"] + G - 2, oy + cup["top"] + cup["hro"] + 4
compass(hx, hy, cup["hro"], t + 0.62, 0.2)
compass(hx, hy, cup["hro"] - cup["ht"], t + 0.74, 0.16)
ruler((-16, oy + 100 - W / 2 - 2), (100, oy + 100 - W / 2 - 2), t + 0.86, 0.13, ext=0)
Dg = mark.D(0, oy)[0]
ink(Dg["solid"], 30, oy + 96, b(7, 2.0), 0.42)
sy = oy + 100 - W / 2 - 2
pen(f"M-8 {f(sy)}H{f(cup['bw'] + 14)}", b(7, 3.0), 0.22)
label(108, oy + 22, "R 60 · R 17", b(7, 1.2), size=4.0)
# ------------------------------------------------------------------ bar 8: e (at 112, 112)
t = b(8)
cross(162, 162, t)
compass(162, 162, 50, t + 0.06, 0.42)
ruler((110, 162), (222, 162), t + 0.5, 0.13, ext=0)
ruler((162, 106), (162, 218), t + 0.6, 0.13, ext=0)
ruler((165, 106), (165, 165), t + 0.68, 0.11, ext=0)
eg = mark.e(112, 112)[0]
left = f"M162 112" + mark.arc_to(162, 162, R, -90, -270) + "Z"
quarter = f"M165 162V112" + mark.arc_to(165, 162, R, -90, 0) + "Z"
ink(left, 108, 162, b(8, 2.0), 0.34)
ink(quarter, 218, 108, b(8, 2.55), 0.26)
x0, y0 = mark.pt(165, 162, rc, 58)
x1, y1 = mark.pt(165, 162, rc, 90)
pen(f"M{f(x0)} {f(y0)}A{f(rc)} {f(rc)} 0 0 1 {f(x1)} {f(y1)}", b(8, 3.0), 0.2)
label(220, 228, "Hollenstein's e, left open", b(8, 3.1), anchor="end", size=4.0)

# ------------------------------------------------------------------ camera: (time, cx, cy, zoom, rotation°); a repeated time is a cut
CAM = [
    (0.0, 50, 50, 5.6, -5), (b(1, 3.6), 50, 52, 5.0, -3),
    (b(2, 0.0), 150, 48, 5.6, 3), (b(2, 3.0), 158, 50, 4.8, 1.5),
    (b(3, 0.0), 120, 90, 3.6, 0), (b(3, 3.0), 108, 106, 2.9, 0),
    (b(4, 0.0), 118, 60, 12.0, -2), (b(4, 0.5), 113, 64, 11.5, -1), (b(4, 1.0), 122, 22, 11.0, 0), (b(4, 3.0), 132, 38, 8.5, 0),
    (b(5, 0.0), 50, 60, 4.4, -2), (b(5, 3.9), 50, 58, 4.0, 0),
    (b(6, 0.0), 164, 56, 4.5, 2), (b(6, 3.9), 162, 54, 4.1, 0),
    (b(7, 0.0), 40, 166, 4.4, -2), (b(7, 3.9), 40, 164, 4.0, 0),
    (b(8, 0.0), 164, 166, 4.5, 2), (b(8, 3.9), 162, 164, 4.1, 0),
    (b(9, 0.0), 212, 106, 2.95, 0), (b(9, 3.9), 224, 106, 3.1, 0),
    (b(10, 0.5), 106, 106, 3.3, 0), (b(11, 0.0), 106, 106, 3.3, 0),
]
CUTS = [b(2), b(3), b(4), b(5), b(6), b(7), b(8), b(9), b(10, 0.5)]          # hard cuts: no easing across these

# flash cards and colour-way cuts (screen space)
CARDS = [(b(2, 3), b(3), "One radius."), (b(3, 3), b(4), "One cut."), (b(4, 3), b(5), "One hairline.")]
FIGS = [(0.1, b(2), "Fig. 01 · the square"), (b(2), b(3), "Fig. 02 · one radius"), (b(3), b(4), "Fig. 03 · grid, gap 12, cut 3"),
        (b(4), b(5), "Fig. 04 · the hairline"), (b(5), b(6), "Fig. 05 · m, a square of coffee that drips"),
        (b(6), b(7), "Fig. 06 · o, half poured"), (b(7), b(8), "Fig. 07 · D, a cup on its saucer"),
        (b(8), b(9), "Fig. 08 · e, left open"), (b(9), b(10, 1), "Fig. 09 · MODE")]
WORDS = [(b(9, 0.0), "Every letter"), (b(9, 1.0), "of MODE"), (b(9, 2.0), "is a"), (b(9, 3.0), "coffee.")]
COLOURWAYS = [("#151515", "#F4F2ED"), ("#2771BE", "#F4F2ED"), ("#0B8457", "#F4F2ED"), ("#4F758B", "#F4F2ED"),
              ("#557F22", "#F4F2ED"), ("#8C6A4E", "#F4F2ED")]
CW_T0 = b(10, 1.0)
SHOTS = [("fan", b(11), b(13)), ("range", b(13), b(15)), ("hero", b(15), 30.0)]
MODE_TAGS = [(b(11, 0.3), "01 · Wake"), (b(11, 1.8), "02 · Active"), (b(11, 3.3), "03 · Zen"), (b(12, 0.8), "04 · Vital"), (b(12, 2.3), "05 · Calm")]

out = dict(beat=BEAT, bar=BAR, strokes=strokes, inks=inks, labels=labels, cam=CAM, cuts=CUTS, cards=CARDS, figs=FIGS,
           words=WORDS, colourways=COLOURWAYS, cw_t0=CW_T0, shots=SHOTS, mode_tags=MODE_TAGS,
           erase=[b(10, 0.5), b(10, 1.0)], stack=dict(solid=mark.stack()[0]["solid"], hair=mark.stack()[0]["hair"]))
json.dump(out, open(os.path.join(HERE, "timeline.json"), "w"))
print(len(strokes), "strokes", len(inks), "inks", len(labels), "labels")
