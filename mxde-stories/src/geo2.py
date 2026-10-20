"""MODE alone: three geometric logos, each with a different logic. SVG coordinates (y down), cap height 100."""
import math
from shapely.geometry import Point, box, Polygon, LineString
from shapely.ops import unary_union
from shapely import affinity
from geo import disc, half, place, arc_line

H = 100.0


# ------------------------------------------------------------------ 1 · TWO SHAPES
def comb(s=24.0, w=100.0, h=100.0, mid=1.0):
    """The E: a stem and three arms, filling a square."""
    arms = [box(0, 0, w, s), box(0, h / 2 - s / 2, w * mid, h / 2 + s / 2), box(0, h - s, w, h)]
    return unary_union([box(0, 0, s, h)] + arms)


def two_shapes(s=24.0, gap=15.0):
    """M is the E turned a quarter; D is the O cut in half. Two shapes, each used twice."""
    e = comb(s)
    m = affinity.rotate(e, 90, origin=(50, 50))            # stem on top, three legs down: the m
    parts = {"M": m}
    x = 100 + gap
    parts["O"] = disc(x + 50, 50, 50)
    x += 100 + gap
    parts["D"] = half(x, 50, 50, "right")
    x += 50 + gap
    parts["E"] = place(e, x)
    return parts, x + 100


# ------------------------------------------------------------------ 2 · LINES
def skeleton_letters(s=26.0):
    """Solid geometric MODE used as the outer contour for the line version."""
    W = 100.0
    vb = 30.0
    m = unary_union([box(0, 0, s, H), box(W - s, 0, W, H),
                     Polygon([(0, 0), (s * 1.15, 0), (W / 2, H - vb - s * 1.2), (W - s * 1.15, 0), (W, 0), (W / 2 + s * 0.45, H - vb), (W / 2 - s * 0.45, H - vb)])])
    o = disc(W + 22 + 52, 50, 52)
    dx = W + 22 + 104 + 22
    d = unary_union([box(dx, 0, dx + 40, H), half(dx + 40, 50, 50, "right")])
    ex = dx + 90 + 22
    e = unary_union([box(ex, 0, ex + s, H), box(ex, 0, ex + 74, s), box(ex, 50 - s / 2, ex + 66, 50 + s / 2), box(ex, H - s, ex + 74, H)])
    return {"M": m, "O": o, "D": d, "E": e}, ex + 74


def lines(n=3, pitch=8.6, w=3.6, s=26.0):
    """Each letter drawn as n parallel contour lines, like the lines of Mexico 68: no solids, only rhythm."""
    solids, width = skeleton_letters(s)
    out = {}
    for k, g in solids.items():
        rings = []
        for i in range(n):
            shape = g.buffer(-i * pitch, join_style="mitre", mitre_limit=3.0) if i else g
            if shape.is_empty:
                continue
            band = shape.difference(shape.buffer(-w, join_style="mitre", mitre_limit=3.0))
            rings.append(band)
        out[k] = unary_union(rings)
    return out, width


# ------------------------------------------------------------------ 3 · ECLIPSE
def eclipse(overlap=0.5, gap=16.0, arcs=True):
    """The D slides across the O. Where they overlap, the shape is cut away: the O becomes a crescent,
    the D a lens-bitten half. Thin arcs trace the orbit, as in Hollenstein's L'Echoppe."""
    parts = {}
    # M from two quarter-discs and a square: the arches of an m standing on a block
    q = 50.0
    left = disc(q, q, q).intersection(box(0, 0, q, q))           # quarter, round at top-left
    right = disc(q, q, q).intersection(box(q, 0, 2 * q, q))      # quarter, round at top-right
    m = unary_union([left, right, box(0, q, q * 0.46, H), box(2 * q - q * 0.46, q, 2 * q, H), box(q - q * 0.23, q * 0.55, q + q * 0.23, H)])
    m = m.difference(box(q - 1.6, 0, q + 1.6, q * 0.55))
    parts["M"] = m
    x = 100 + gap
    ocx = x + 50
    o = disc(ocx, 50, 50)
    dcx = ocx + 100 * (1 - overlap)                               # flat side of the D
    d = half(dcx, 50, 50, "right").union(box(dcx - 14, 0, dcx, H))
    both = o.intersection(d)
    parts["O"] = o.difference(d)
    parts["D"] = d.difference(o)
    parts["lens"] = both.difference(both.buffer(-3.2))
    if arcs:
        parts["arcs"] = unary_union([arc_line(ocx, 50, 64, 200, 250, 2.4), arc_line(dcx, 50, 64, -70, -20, 2.4)])
    x = dcx + 50 + gap
    e = unary_union([box(x, 0, x + 22, H), box(x, 0, x + 72, 20), box(x, 40, x + 64, 60), box(x, 80, x + 72, H)])
    parts["E"] = e
    return parts, x + 72


# ------------------------------------------------------------------ 2b · LINES, the Mexico 68 way
def _strokes(line, offsets, w):
    out = []
    for o in offsets:
        c = line if o == 0 else line.offset_curve(o, join_style="mitre", mitre_limit=4.0)
        if not c.is_empty:
            out.append(c.buffer(w / 2, cap_style="flat", join_style="mitre", mitre_limit=4.0))
    return unary_union(out)


def lines_open(pitch=9.0, w=3.8, n=3):
    """Each letter is drawn as n parallel strokes following its skeleton, open at the ends:
    the M a triple zigzag, the O and D nested rings, the E a triple bracket and a triple bar."""
    offs = [(i - (n - 1) / 2) * pitch for i in range(n)]
    half_w = (n - 1) / 2 * pitch + w / 2
    parts = {}
    # M: up, down to the vertex, up, down
    m = LineString([(half_w, H), (half_w, half_w), (50, 64), (100 - half_w, half_w), (100 - half_w, H)])
    parts["M"] = _strokes(m, offs, w).intersection(box(-1, 0, 101, H))
    # O: concentric rings
    x = 100 + 24
    cx = x + 50
    rings = []
    for o in offs:
        r = 50 - half_w + w / 2 + (o + (n - 1) / 2 * pitch)
        rings.append(disc(cx, 50, r + w / 2).difference(disc(cx, 50, r - w / 2)))
    parts["O"] = unary_union(rings)
    # D: nested D rings (stem + bowl as one closed skeleton)
    x += 100 + 24
    pts = [(x + half_w, half_w), (x + 40, half_w)]
    for i in range(1, 48):
        t = -90 + 180 * i / 48
        pts.append((x + 40 + (50 - half_w) * math.cos(math.radians(t)), 50 + (50 - half_w) * math.sin(math.radians(t))))
    pts += [(x + 40, H - half_w), (x + half_w, H - half_w), (x + half_w, half_w)]
    dring = Polygon(pts)
    rings = []
    for o in offs:
        g = dring.buffer(-o, join_style="mitre", mitre_limit=4.0)
        rings.append(g.difference(g.buffer(-w, join_style="mitre", mitre_limit=4.0)))
    parts["D"] = unary_union(rings)
    # E: a bracket and a middle bar, each tripled
    x += 90 + 24
    br = LineString([(x + 76, half_w), (x + half_w, half_w), (x + half_w, H - half_w), (x + 76, H - half_w)])
    bar_ = LineString([(x + half_w + pitch - w / 2, 50), (x + 66, 50)])   # the bar joins the innermost line only
    parts["E"] = unary_union([_strokes(br, offs, w), _strokes(bar_, offs, w)])
    return parts, x + 76


# ------------------------------------------------------------------ 3b · COUNTERS
def counters(h=H, pad=22.0):
    """One solid bar. Only the counters are cut out: a V for M, a circle for O, a half-circle for D,
    two slots for E. You read the name from what's missing."""
    W = 4 * 100 + 3 * pad + 2 * pad
    bar_ = box(0, 0, W, h)
    x = pad
    holes = [Polygon([(x + 18, -1), (x + 82, -1), (x + 50, 62)])]                       # M: the V between the peaks
    x += 100 + pad
    holes.append(disc(x + 50, 50, 30))                                                 # O
    x += 100 + pad
    holes.append(half(x + 30, 50, 30, "right").union(box(x + 22, 20, x + 30, 80)))     # D: a D-shaped counter
    x += 100 + pad
    for yc in (33, 67):
        holes.append(box(x + 30, yc - 8, W + 1, yc + 8))                               # E: two slots open to the right
    return {"bar": bar_.difference(unary_union(holes))}, W
