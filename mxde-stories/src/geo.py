"""MODE from a tiny kit of shapes: half-discs, squares, quarter-discs and thin arcs.
SVG coordinates (y down). Cap height 100, baseline at y = 100."""
import math
from shapely.geometry import Point, box, Polygon, LineString
from shapely.ops import unary_union
from shapely import affinity

H = 100.0
R = 50.0
G = 7.0          # the standard gap


def disc(cx, cy, r, res=128):
    return Point(cx, cy).buffer(r, resolution=res)


def half(cx, cy, r, facing):
    """Half-disc whose round side faces 'left', 'right', 'up' or 'down'; flat side through (cx, cy)."""
    d = disc(cx, cy, r)
    clip = {"right": box(cx, cy - r - 1, cx + r + 1, cy + r + 1), "left": box(cx - r - 1, cy - r - 1, cx, cy + r + 1),
            "up": box(cx - r - 1, cy - r - 1, cx + r + 1, cy), "down": box(cx - r - 1, cy, cx + r + 1, cy + r + 1)}[facing]
    return d.intersection(clip)


def arc_line(cx, cy, r, a0, a1, w, n=96):
    pts = [(cx + r * math.cos(math.radians(a0 + (a1 - a0) * i / n)), cy + r * math.sin(math.radians(a0 + (a1 - a0) * i / n))) for i in range(n + 1)]
    return LineString(pts).buffer(w / 2, cap_style="round", resolution=12)


def place(g, dx, dy=0):
    return affinity.translate(g, dx, dy)


# ------------------------------------------------------------------ A · ONE HALF
def one_half(gap=G, m_style="arches"):
    """Every letter is the same half-disc, turned: M = two turned up, O = two facing out, D = one facing right,
    E = one facing left with two cuts."""
    parts = {}
    x = 0
    if m_style == "arches":       # two half-discs facing up, standing on the baseline: the humps of an m
        r = 26.0
        m = unary_union([half(r, H, r * 1.0, "up"), half(3 * r + gap, H, r, "up")])
        m = unary_union([affinity.scale(half(r, H, r, "up"), 1, 100 / r, origin=(r, H)),
                         affinity.scale(half(3 * r + gap, H, r, "up"), 1, 100 / r, origin=(3 * r + gap, H))])
        mw = 4 * r + gap
    else:                          # two half-discs facing up at full width, half height
        m = unary_union([half(R, H, R, "up"), half(3 * R + gap, H, R, "up")])
        mw = 4 * R + gap
    parts["M"] = m
    x = mw + gap * 3
    o = unary_union([half(x + R, H / 2, R, "left"), half(x + R + gap, H / 2, R, "right")])
    parts["O"] = o
    x += 2 * R + gap + gap * 3
    parts["D"] = half(x, H / 2, R, "right")
    x += R + gap * 3
    e = half(x + R, H / 2, R, "left")
    cut = 9.0
    for yc in (H / 3, 2 * H / 3):
        e = e.difference(box(x + R * 0.42, yc - cut / 2, x + R + 1, yc + cut / 2))
    parts["E"] = e
    width = x + R
    return parts, width


# ------------------------------------------------------------------ B · THE TURN
def the_turn(open_deg=28.0, gap=G):
    """Square-and-circle MODE. The O's top half has swung open about its left end, like a switch being thrown;
    two thin arcs trace the movement."""
    parts = {}
    # M: a solid square with two arches cut from the base
    m = box(0, 0, 100, 100)
    for cx in (27, 73):
        arch = unary_union([box(cx - 14, 52, cx + 14, 101), disc(cx, 52, 14)])
        m = m.difference(arch)
    m = m.difference(box(48, 30, 52, 101))
    parts["M"] = m
    x = 100 + gap * 2.6
    cx, cy = x + R, H / 2
    bottom = half(cx, cy + gap / 2, R, "down")
    top = half(cx, cy - gap / 2, R, "up")
    top = affinity.rotate(top, -open_deg, origin=(cx - R, cy - gap / 2))
    parts["O"] = unary_union([bottom, top])
    parts["O_arcs"] = unary_union([arc_line(cx - R, cy - gap / 2, 2 * R + 14, -open_deg - 4, -1, 2.6),
                                   arc_line(cx - R, cy - gap / 2, 2 * R + 26, -open_deg - 2, -8, 2.6)])
    x += 2 * R + gap * 2.6
    d = unary_union([box(x, 0, x + 50, 100), half(x + 50, H / 2, R, "right")])
    parts["D"] = d
    x += 100 + gap * 2.6
    e = box(x, 0, x + 78, 100)
    for yc in (H / 3, 2 * H / 3):
        e = e.difference(box(x + 26, yc - 6, x + 79, yc + 6))
    parts["E"] = e
    return parts, x + 78


# ------------------------------------------------------------------ C · BLOCK
def block(gap=8.0):
    """MO over DE: four tiles of one square, each a letter from the kit. Compact for a sachet or an icon."""
    s = 100.0
    parts = {}
    m = box(0, 0, s, s)
    for cx in (27, 73):
        m = m.difference(unary_union([box(cx - 14, 54, cx + 14, s + 1), disc(cx, 54, 14)]))
    parts["M"] = m
    parts["O"] = disc(s + gap + s / 2, s / 2, s / 2)
    y = s + gap
    parts["D"] = unary_union([box(0, y, s / 2, y + s), half(s / 2, y + s / 2, s / 2, "right")])
    e = box(s + gap, y, 2 * s + gap, y + s)
    for yc in (y + s / 3, y + 2 * s / 3):
        e = e.difference(box(s + gap + 30, yc - 6.5, 2 * s + gap + 1, yc + 6.5))
    parts["E"] = e
    return parts, 2 * s + gap


# ------------------------------------------------------------------ the mode kit: one half-disc, turned
MODES = ["wake", "active", "zen", "vital", "calm"]
MODE_TURN = {"wake": "up", "active": "right", "zen": "whole", "vital": "diag", "calm": "down"}


def mode_shape(m, cx, cy, r):
    """Wake rises (facing up), Active moves forward (right), Zen is whole, Vital grows (turned 45°, up and forward),
    Calm rests (facing down). Each is centred on (cx, cy) by its bounding box."""
    t = MODE_TURN[m]
    if t == "whole":
        return disc(cx, cy, r * 0.82)
    g = affinity.rotate(half(0, 0, r, "up"), -45, origin=(0, 0)) if t == "diag" else half(0, 0, r, t)
    b = g.bounds
    return place(g, cx - (b[0] + b[2]) / 2, cy - (b[1] + b[3]) / 2)


def one_half_final(gap=G):
    """A, tuned: the same half-disc (r 50) six times. Letter spacing set optically."""
    parts = {}
    parts["M"] = unary_union([half(R, H, R, "up"), half(3 * R + gap, H, R, "up")])
    x = 4 * R + gap + 22
    parts["O"] = unary_union([half(x + R, H / 2, R, "left"), half(x + R + gap, H / 2, R, "right")])
    x += 2 * R + gap + 20
    parts["D"] = half(x, H / 2, R, "right")
    x += R + 13
    e = half(x + R, H / 2, R, "left")
    for yc in (H / 3, 2 * H / 3):
        e = e.difference(box(x + R * 0.42, yc - 4.5, x + R + 1, yc + 4.5))
    parts["E"] = e
    return parts, x + R


def slot_o(gap=G, ring_w=5.0, mode=None):
    """B: solid M, D, E from squares and half-discs; the O is two thin arcs, an open slot each mode fills."""
    parts = {}
    m = box(0, 0, 92, 100)
    m = m.difference(Polygon([(26, -1), (66, -1), (46, 58)]))
    parts["M"] = m
    x = 92 + 22
    cx, cy = x + R, H / 2
    parts["O"] = unary_union([arc_line(cx, cy, R - ring_w / 2, 112, 248, ring_w), arc_line(cx, cy, R - ring_w / 2, -68, 68, ring_w)])
    if mode:
        parts["fill"] = mode_shape(mode, cx, cy, R * 0.56)
    x += 2 * R + 22
    parts["D"] = unary_union([box(x, 0, x + 40, 100), half(x + 40, H / 2, R, "right")])
    x += 90 + 20
    e = box(x, 0, x + 70, 100)
    for yc in (H / 3, 2 * H / 3):
        e = e.difference(box(x + 24, yc - 6, x + 71, yc + 6))
    parts["E"] = e
    return parts, x + 70, (cx, cy)


def block_final(gap=8.0, mode=None):
    """C: MO over DE. In a mode, the O tile shows that mode's turn of the half-disc."""
    parts, w = block(gap)
    if mode:
        s = 100.0
        parts["O"] = mode_shape(mode, s + gap + s / 2, s / 2, s / 2)
        parts["O_ring"] = disc(s + gap + s / 2, s / 2, s / 2).difference(disc(s + gap + s / 2, s / 2, s / 2 - 3.5))
    return parts, w
