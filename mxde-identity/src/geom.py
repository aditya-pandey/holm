"""MXDE letterform geometry.

Every letter is built from straight strokes on a cap-height grid (H = 100 units),
unioned with shapely and written out as clean SVG paths. No fonts, no curves.
"""
from shapely.geometry import LineString, Polygon, box
from shapely.ops import unary_union
from shapely import affinity

H = 100.0  # cap height


def stroke(p1, p2, width, ext=0.0):
    """A straight bar of constant perpendicular `width` from p1 to p2, extended by `ext` at both ends."""
    (x1, y1), (x2, y2) = p1, p2
    ls = LineString([(x1, y1), (x2, y2)])
    if ext:
        dx, dy = x2 - x1, y2 - y1
        n = (dx * dx + dy * dy) ** 0.5
        ux, uy = dx / n, dy / n
        ls = LineString([(x1 - ux * ext, y1 - uy * ext), (x2 + ux * ext, y2 + uy * ext)])
    return ls.buffer(width / 2, cap_style="flat", join_style="mitre")


def halfplane_inset(outer_pts, insets):
    """Inset a convex polygon edge-by-edge (counter-clockwise points, one inset per edge)."""
    big = box(-1e4, -1e4, 1e4, 1e4)
    poly = big
    n = len(outer_pts)
    for i in range(n):
        (ax, ay), (bx, by) = outer_pts[i], outer_pts[(i + 1) % n]
        ex, ey = bx - ax, by - ay
        L = (ex * ex + ey * ey) ** 0.5
        nx, ny = -ey / L, ex / L  # inward normal for CCW polygon
        d = insets[i]
        ox, oy = ax + nx * d, ay + ny * d
        # half-plane as a huge polygon on the inner side of the offset edge
        tx, ty = ex / L * 1e4, ey / L * 1e4
        hp = Polygon([(ox - tx, oy - ty), (ox + tx, oy + ty),
                      (ox + tx + nx * 2e4, oy + ty + ny * 2e4), (ox - tx + nx * 2e4, oy - ty + ny * 2e4)])
        poly = poly.intersection(hp)
    return poly


# ---------------------------------------------------------------- letters
# Coordinates: y up, baseline 0, cap height H. Each returns (shape, advance width).

def letter_M(w, width=None, angle=60.0, diag=0.90, flat=0.80):
    """Straight-stem M; the V's diagonals run at exactly `angle`° and end in a flat foot `flat`·w wide
    (no sharp point to fill in when embossed). The vertex depth follows from the angle."""
    import math
    W = width or 1.02 * H
    f = flat * w
    run = W / 2 - f / 2
    vb = H - run * math.tan(math.radians(angle))
    theta = math.atan2(H - vb, run)
    t = diag * w / math.sin(theta)  # horizontal thickness that gives `diag`·w perpendicular weight
    slope = (H - vb) / run
    vi = H - (W / 2 - t) * slope     # inner crotch height
    v = Polygon([(0, H), (t, H), (W / 2, vi), (W - t, H), (W, H), (W / 2 + f / 2, vb), (W / 2 - f / 2, vb)])
    stems = unary_union([box(0, 0, w, H), box(W - w, 0, W, H)])
    return unary_union([stems, v]), W


def letter_D(w, width=None, chamfer=0.30, hthin=0.90):
    W = width or 0.84 * H
    c = chamfer * H
    outer = [(0, 0), (W - c, 0), (W, c), (W, H - c), (W - c, H), (0, H)]
    wh = w * hthin
    inner = halfplane_inset(outer, [wh, w * 0.96, w, w * 0.96, wh, w])
    return Polygon(outer).difference(inner), W


def letter_E(w, width=None, mid=0.88, hthin=0.90):
    W = width or 0.66 * H
    wh = w * hthin
    parts = [box(0, 0, w, H), box(0, H - wh, W, H), box(0, 0, W, wh),
             box(0, (H - wh) / 2, W * mid, (H + wh) / 2)]
    return unary_union(parts), W


def x_strokes(w, W, diag=1.0):
    d = w * diag
    a = stroke((0 + d * 0.0, 0), (W, H), d, ext=60).intersection(box(0, 0, W, H))
    b = stroke((0, H), (W, 0), d, ext=60).intersection(box(0, 0, W, H))
    return a, b


def letter_X_plain(w, width=None):
    W = width or 0.92 * H
    a, b = x_strokes(w, W)
    return unary_union([a, b]), W


def letter_X_crossover(w, width=None, gap=0.42):
    """Route A: one bar passes over the other; the under-bar is cut either side of the crossing."""
    W = width or 0.92 * H
    a, b = x_strokes(w, W)
    cut = stroke((0, 0), (W, H), w + 2 * gap * w, ext=60)
    return unary_union([a, b.difference(cut)]), W


def letter_X_box(w, width=None, gap=0.46):
    """Route B: the O's square footprint with the X knocked out as negative space (four wedges)."""
    W = width or H
    sq = box(0, 0, W, H)
    k = gap * w
    cuts = unary_union([stroke((0, 0), (W, H), k, ext=60), stroke((0, H), (W, 0), k, ext=60)])
    return sq.difference(cuts), W


def letter_X_shift(w, width=None, shift=0.5):
    """Route C: the X split at its waist, the upper half thrown one half-stem to the right — a switch flipped."""
    W = width or 0.92 * H
    X, _ = letter_X_plain(w, W)
    s = shift * w
    lower = X.intersection(box(-1, -1, W + 1, H / 2))
    upper = affinity.translate(X.intersection(box(-1, H / 2, W + 1, H + 1)), xoff=s)
    return unary_union([lower, upper]), W + s


# ---------------------------------------------------------------- mode glyphs (two bars, re-arranged)

def glyph(name, w, S=H):
    """Each mode glyph is the X's two bars re-arranged into a new state. S = square size."""
    d = w
    if name == "x":
        g = unary_union(x_strokes(w, S))
    elif name == "wake":      # Λ  rising peak — the lower half of the X, stood up
        g = unary_union([stroke((0, 0), (S / 2, S), d, ext=40), stroke((S / 2, S), (S, 0), d, ext=40)])
        g = g.intersection(box(0, 0, S, S))
    elif name == "active":    # >  forward chevron
        g = unary_union([stroke((S * 0.18, S), (S * 0.86, S / 2), d, ext=40),
                         stroke((S * 0.86, S / 2), (S * 0.18, 0), d, ext=40)])
        g = g.intersection(box(S * 0.18, 0, S * 0.86 + d * 0.62, S))
        g = g.intersection(box(0, 0, S, S))
    elif name == "zen":       # ||  two uprights — an aligned, focused mind
        g = unary_union([box(S * 0.30 - d / 2, 0, S * 0.30 + d / 2, S), box(S * 0.70 - d / 2, 0, S * 0.70 + d / 2, S)])
    elif name == "vital":     # +  the X turned upright — replenish, add
        g = unary_union([box(S / 2 - d / 2, 0, S / 2 + d / 2, S), box(0, S / 2 - d / 2, S, S / 2 + d / 2)])
    elif name == "calm":      # =  two bars laid down — a body at rest
        g = unary_union([box(0, S * 0.30 - d / 2, S, S * 0.30 + d / 2), box(0, S * 0.70 - d / 2, S, S * 0.70 + d / 2)])
    else:
        raise ValueError(name)
    return g


def mode_tile(name, k, S=H):
    """The X slot, cut differently per mode. Same square, same cut width `k` — the cut is the mode."""
    sq = box(0, 0, S, S)
    if name == "x":
        cut = [stroke((0, 0), (S, S), k, ext=60), stroke((0, S), (S, 0), k, ext=60)]
    elif name == "wake":    # ▲ rises out of the square
        cut = [stroke((0, 0), (S / 2, S), k, ext=60), stroke((S / 2, S), (S, 0), k, ext=60)]
    elif name == "active":  # ▶ points forward
        cut = [stroke((0, S), (S, S / 2), k, ext=60), stroke((S, S / 2), (0, 0), k, ext=60)]
    elif name == "zen":     # ||| upright
        cut = [box(S / 3 - k / 2, -1, S / 3 + k / 2, S + 1), box(2 * S / 3 - k / 2, -1, 2 * S / 3 + k / 2, S + 1)]
    elif name == "vital":   # + the X turned upright
        cut = [box(S / 2 - k / 2, -1, S / 2 + k / 2, S + 1), box(-1, S / 2 - k / 2, S + 1, S / 2 + k / 2)]
    elif name == "calm":    # ≡ laid down
        cut = [box(-1, S / 3 - k / 2, S + 1, S / 3 + k / 2), box(-1, 2 * S / 3 - k / 2, S + 1, 2 * S / 3 + k / 2)]
    else:
        raise ValueError(name)
    return sq.difference(unary_union(cut))


# ---------------------------------------------------------------- SVG output

def _ring(coords, ox, oy, s, ndp=2):
    pts = list(coords)[:-1]
    out = []
    for i, (x, y) in enumerate(pts):
        X = round(ox + x * s, ndp)
        Y = round(oy - y * s, ndp)  # flip y
        out.append(("M" if i == 0 else "L") + f"{X:g} {Y:g}")
    return "".join(out) + "Z"


def to_path(geom, ox=0.0, oy=0.0, s=1.0):
    geom = geom.buffer(0)
    polys = [geom] if geom.geom_type == "Polygon" else list(geom.geoms)
    d = []
    for p in polys:
        p = p.simplify(0.001)
        d.append(_ring(p.exterior.coords, ox, oy, s))
        for r in p.interiors:
            d.append(_ring(r.coords, ox, oy, s))
    return "".join(d)


def place(geom, x):
    return affinity.translate(geom, xoff=x)
