"""Five MXDE identities — logo geometry. Cap height = 100 user units throughout.

Each concept exposes build(state=None) -> dict of named path layers + viewBox, so the same
geometry feeds the SVG masters, the concept sheet, the 3D label painters and the films.
"""
import json
import math
import os
from type import glyphs, text

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
CAP = 100.0
MODES = ["wake", "active", "zen", "vital", "calm"]


def rect(x, y, w, h):
    return f"M{x:.2f} {y:.2f}h{w:.2f}v{h:.2f}h{-w:.2f}Z"


def poly(pts):
    return "M" + "L".join(f"{x:.2f} {y:.2f}" for x, y in pts) + "Z"


# ------------------------------------------------------------------ 1 · SAY IT MODE — the macron
def say(state=None):
    """MXDE with a macron over the X. In phonetics a macron marks a long vowel: X̄ = ō. It tells you how to say it."""
    gl = glyphs("MXDE", "SchibstedGrotesk-ExtraBold.ttf", 0, CAP, CAP, tracking=0.035)
    x0, _, x1, _ = gl[1][2]
    w = (x1 - x0) * 0.66
    bar_h = 12.5
    bar_y = -12.5 - bar_h
    macron = rect((x0 + x1) / 2 - w / 2, bar_y, w, bar_h)
    letters = "".join(g[1] for g in gl)
    right = gl[-1][2][2]
    return {"layers": {"letters": letters, "macron": macron}, "box": (0, bar_y, right, CAP - bar_y),
            "x_center": (x0 + x1) / 2}


def say_lockup():
    base = say()
    d, ink = text("/mōd/", "PlexMono-Medium.ttf", 2, CAP + 74, 34, tracking=0.0)
    L = dict(base["layers"])
    L["phonetic"] = d
    b = base["box"]
    return {"layers": L, "box": (0, b[1], b[2], CAP + 74 + 10 - b[1])}


def say_symbol():
    gl = glyphs("X", "SchibstedGrotesk-ExtraBold.ttf", 0, 0, 100)
    x0, y0, x1, y1 = gl[0][2]
    S = 200
    k = 1.0
    ox = S / 2 - (x0 + x1) / 2
    oy = S / 2 + 50 + 14          # X cap from -100..0 → shift down; leave room for macron
    w = (x1 - x0) * 0.66
    letters = f'<g transform="translate({ox:.2f} {oy:.2f})">'
    d = gl[0][1]
    macron = rect(S / 2 - w / 2, oy - 100 - 12.5 - 12.5, w, 12.5)
    return {"layers": {"x": (d, (ox, oy)), "macron": macron}, "box": (0, 0, S, S)}


# ------------------------------------------------------------------ 2 · SET YOUR STATE — the dial
DIAL_ANGLE = {"logo": 90.0, "wake": -60.0, "active": -30.0, "zen": 0.0, "vital": 30.0, "calm": 60.0}


def knob(cx, cy, r, angle=90.0, knurl=True):
    """Top view of a knurled control knob with a pointer slot. angle: 0 = 12 o'clock, clockwise."""
    from shapely.geometry import Point, Polygon, box
    from shapely import affinity
    from shapely.ops import unary_union
    disc = Point(cx, cy).buffer(r, resolution=64)
    cuts = []
    if knurl:
        n = 60
        for i in range(n):
            a = 2 * math.pi * i / n
            t = box(-r * 0.026, -r - 1, r * 0.026, -r + r * 0.07)
            cuts.append(affinity.translate(affinity.rotate(t, math.degrees(a), origin=(0, 0)), cx, cy))
    ptr = box(-r * 0.075, -r * 0.86, r * 0.075, -r * 0.22)
    cuts.append(affinity.translate(affinity.rotate(ptr, angle, origin=(0, 0)), cx, cy))
    shape = disc.difference(unary_union(cuts))
    return geom_to_d(shape)


def geom_to_d(g):
    g = g.buffer(0)
    polys = [g] if g.geom_type == "Polygon" else list(g.geoms)
    out = []
    for p in polys:
        for ring in [p.exterior] + list(p.interiors):
            pts = list(ring.coords)[:-1]
            out.append("M" + "L".join(f"{x:.2f} {y:.2f}" for x, y in pts) + "Z")
    return "".join(out)


def dial(state="logo"):
    r = 66
    k = knob(r, CAP / 2, r, DIAL_ANGLE.get(state, 90.0))
    tx = 2 * r + 42
    capw = 64
    d, ink = text("MXDE", "BarlowSemiCond-SemiBold.ttf", tx, CAP / 2 + capw / 2, capw, tracking=0.20)
    return {"layers": {"knob": k, "letters": d}, "box": (0, CAP / 2 - r, ink[2], 2 * r)}


def dial_scale(cx, cy, r, active=None):
    """The mode scale: five ticks on the upper arc, the active one long."""
    out = []
    for m in MODES:
        a = math.radians(DIAL_ANGLE[m])
        L = 0.22 * r if m == active else 0.12 * r
        w = 0.05 * r
        r0 = r * 1.14
        # tick as a rotated rect
        pts = []
        for (px, py) in ((-w / 2, -r0 - L), (w / 2, -r0 - L), (w / 2, -r0), (-w / 2, -r0)):
            pts.append((cx + px * math.cos(a) - py * math.sin(a), cy + px * math.sin(a) + py * math.cos(a)))
        out.append(poly(pts))
    return "".join(out)


def dial_symbol(state="logo"):
    S = 200
    return {"layers": {"knob": knob(S / 2, S / 2, 78, DIAL_ANGLE.get(state, 90.0))}, "box": (0, 0, S, S)}


# ------------------------------------------------------------------ 3 · LIGHT HOURS — the horizon
LIGHT_H = {"logo": 0.42, "wake": 0.18, "active": 0.62, "zen": 0.50, "vital": 0.80, "calm": 0.10}
KELVIN = {"wake": 6500, "active": 5600, "zen": 4000, "vital": 5000, "calm": 2700}


def light(state="logo", gap=6.5):
    """MXDE cut by a horizon. The cut sits where the sun sits at that hour: low at dawn and dusk, high at noon."""
    d, ink = text("MXDE", "InstrumentSans-SemiBold.ttf", 0, CAP, CAP, tracking=0.05)
    h = LIGHT_H.get(state, 0.42)
    y = CAP - h * CAP
    W = ink[2]
    return {"layers": {"letters": d}, "box": (0, 0, W, CAP), "horizon": (y - gap / 2, y + gap / 2), "width": W}


# ------------------------------------------------------------------ 4 · TEAR. POUR. SWITCH. — the slash
SLASH_ANGLE = 64.0  # degrees from horizontal; the same angle as the sachet's tear notch


def tear(word=None):
    gl = glyphs("MXDE", "Archivo-Condensed-ExtraBold.ttf", 0, CAP, CAP, tracking=0.03)
    letters = "".join(g[1] for g in gl)
    right = gl[-1][2][2]
    stem = 21.0
    run = (CAP + 16) / math.tan(math.radians(SLASH_ANGLE))
    sx = right + 9
    top, bot = -8, CAP + 8
    slash = poly([(sx + run, top), (sx + run + stem, top), (sx + stem, bot), (sx, bot)])
    end = sx + run + stem
    L = {"letters": letters, "slash": slash}
    if word:
        d, ink = text(word, "Archivo-Condensed-ExtraBold.ttf", end + 9, CAP, CAP, tracking=0.03)
        L["word"] = d
        end = ink[2]
    return {"layers": L, "box": (0, top, end, bot - top)}


def tear_symbol():
    S = 200
    stem = 30
    run = 150 / math.tan(math.radians(SLASH_ANGLE))
    cx = S / 2
    slash = poly([(cx - run / 2 - stem / 2 + run, 25), (cx - run / 2 + stem / 2 + run, 25),
                  (cx - run / 2 + stem / 2, 175), (cx - run / 2 - stem / 2, 175)])
    return {"layers": {"slash": slash}, "box": (0, 0, S, S)}


# ------------------------------------------------------------------ 5 · FIVE STATES — the variable word
SHIFT_STATE = {   # Roboto Flex coordinates per mode: (wght, wdth, slnt)
    "logo": (640, 100, 0),
    "wake": (300, 32, 0),      # condensed, light, tall: crisp
    "active": (1000, 112, -10),  # black, leaning forward: momentum
    "zen": (500, 100, 0),      # even, balanced: the default
    "vital": (720, 151, 0),    # wide, open: breathing room
    "calm": (150, 151, 0),     # thin and wide: low and slow
}


def shift(state="logo", progressive=False):
    """MXDE set from one variable design space. The master logo is a frozen transition: each letter one step wider."""
    if progressive:
        steps = [(640, 50, 0), (640, 82, 0), (640, 114, 0), (640, 151, 0)]
    else:
        steps = [SHIFT_STATE[state]] * 4
    x = 0
    ds, inks = [], []
    for ch, (wg, wd, sl) in zip("MXDE", steps):
        axes = {"wght": wg, "wdth": wd, "slnt": sl, "opsz": 144}
        gl = glyphs(ch, "RobotoFlex-VF.ttf", x, CAP, CAP, axes=axes)
        ds.append(gl[0][1])
        inks.append(gl[0][2])
        x += gl[0][3] + 4
    return {"layers": {"letters": "".join(ds)}, "box": (min(i[0] for i in inks) - 2, 0, max(i[2] for i in inks) + 2, CAP)}


# ------------------------------------------------------------------ SVG writing

def svg(box, body, title):
    x, y, w, h = box
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x:.2f} {y:.2f} {w:.2f} {h:.2f}" role="img" aria-label="{title}">'
            f"<title>{title}</title>{body}</svg>\n")


def P(d, fill, extra=""):
    return f'<path fill="{fill}" d="{d}"{extra}/>'
