"""MODE in the grammar of Hollenstein's L'Echoppe mark: square, half-disc, quarter-disc, split by a hairline cut,
with hairline arcs of the same radius finishing what the solids leave out. SVG coordinates (y down).
R = 50: the x-height (or cap height) of 100 is one circle."""
from shapely.geometry import box, LineString
from shapely.ops import unary_union
from geo import disc, half, arc_line

R = 50.0
G = 3.0       # the cut between solids
W = 2.2       # hairline (raise it for the small-size cut)
A = 6.0       # gap between a hairline and the solid it continues


def quarter(cx, cy, r, corner):
    """Quarter-disc whose square corner sits at (cx, cy); corner names the quadrant it fills: 'ne', 'nw', 'se', 'sw'."""
    x0, x1 = (cx, cx + r + 1) if corner[1] == "e" else (cx - r - 1, cx)
    y0, y1 = (cy - r - 1, cy) if corner[0] == "n" else (cy, cy + r + 1)
    return disc(cx, cy, r).intersection(box(x0, y0, x1, y1))


def hair(cx, cy, a0, a1, r=R):
    """A hairline on a circle of radius r, outer edge on the outline."""
    return arc_line(cx, cy, r - W / 2, a0, a1, W)


def line(p0, p1):
    return LineString([p0, p1]).buffer(W / 2, cap_style="round")


def word(letters, track):
    x, out = 0.0, []
    for f in letters:
        g, w = f(x)
        out.append(g)
        x += w + track
    return out, x - track


def flat(parts):
    """{'solid': g, 'hair': g} per letter → {'solid': union, 'hair': union}."""
    return {k: unary_union([p[k] for p in parts if p.get(k) is not None]) for k in ("solid", "hair")}


# ------------------------------------------------------------------ 1 · QUARTERS (lowercase, x-height 0..100)
def m_(x):
    """Two quarter shoulders over two squares, cut at the centre line like the e."""
    s = unary_union([quarter(x, R, R, "ne"), quarter(x + R + G, R, R, "ne"),
                     box(x, R + G, x + R, 2 * R), box(x + R + G, R + G, x + 2 * R + G, 2 * R)])
    return {"solid": s, "hair": None}, 2 * R + G


def o_(x):
    """The o as a cup: the lower half poured solid, the upper half a hairline."""
    cx = x + R
    return {"solid": half(cx, R + G / 2, R, "down"), "hair": hair(cx, R - G / 2, 180, 360)}, 2 * R


def d_(x):
    """Bowl and a square stem; the ascender is a hairline rising off the stem and curling over: steam."""
    cx = x + R
    stem = box(cx + G, 0, cx + G + R, 2 * R)
    return {"solid": unary_union([half(cx, R, R, "left"), stem]), "hair": hair(cx + G + R, -A, 180, 270)}, 2 * R + G


def e_(x):
    """Hollenstein's e, kept as drawn: left half-disc, top-right quarter, a hairline closing the bowl."""
    cx = x + R
    return {"solid": unary_union([half(cx, R, R, "left"), quarter(cx + G, R, R, "ne")]),
            "hair": hair(cx + G, R, 16, 90)}, 2 * R + G


def quarters():
    parts, w = word([m_, o_, d_, e_], track=12.0)
    return flat(parts)


# ------------------------------------------------------------------ 2 · HOLD & FINISH (capitals, cap height 0..100)
def M_(x):
    """Both shoulders solid (they make the notch); the legs are hairlines."""
    s = unary_union([quarter(x, R, R, "ne"), quarter(x + 2 * R + G, R, R, "nw")])
    h = unary_union([line((x + W / 2, R + A), (x + W / 2, 2 * R - W / 2)),
                     line((x + 2 * R + G - W / 2, R + A), (x + 2 * R + G - W / 2, 2 * R - W / 2))])
    return {"solid": s, "hair": h}, 2 * R + G


def O_(x):
    cx = x + R
    return {"solid": half(cx, R, R, "left"), "hair": hair(cx + G, R, -90, 90)}, 2 * R + G


def D_(x):
    return {"solid": box(x, 0, x + R, 2 * R), "hair": hair(x + R + G, R, -90, 90)}, 2 * R + G


def E_(x):
    h = unary_union([line((x + R + G + W / 2, y), (x + 2 * R - 6, y)) for y in (W / 2, R, 2 * R - W / 2)])
    return {"solid": box(x, 0, x + R, 2 * R), "hair": h}, 2 * R


def hold():
    parts, w = word([M_, O_, D_, E_], track=16.0)
    return flat(parts)


# ------------------------------------------------------------------ 3 · POUR (the reference's composition as a still life)
def pour():
    """Square sachet top-left; its hairline pours over into a half-disc cup; steam rises off the right.
    Same cast as L'Echoppe, on the same grid: square of side R, cup of radius R, every hairline radius R."""
    cx, top = R + G + R, R + G
    hr = 16.0
    return {"solid": unary_union([box(0, 0, R, R), half(cx, top, R, "down")]),
            "hair": unary_union([arc_line(R + G, R, R - W / 2, -90, -4, W),                 # the pour
                                 arc_line(cx + 14 + R, top - A, R, 180, 232, W),            # steam
                                 arc_line(cx + R - 4, top + hr + 3, hr, -80, 80, W)])}      # handle


MARKS = {"1": quarters, "2": hold, "3": pour}


def mark(k, w=None):
    """A mark's parts, optionally at a heavier hairline (the small-size cut)."""
    global W
    keep = W
    if w:
        W = w
    try:
        return MARKS[k]()
    finally:
        W = keep
