"""Parametric letter builders (shapely, y-up, baseline 0, cap height H=100) and SVG helpers."""
import math
from shapely.geometry import LineString, Polygon, Point, box
from shapely.ops import unary_union
from shapely import affinity

H = 100.0


def bar(p0, p1, w0, w1=None, ext=0.0):
    """A straight bar from p0 to p1 whose perpendicular width runs from w0 to w1 (tapered if they differ)."""
    w1 = w0 if w1 is None else w1
    (x0, y0), (x1, y1) = p0, p1
    dx, dy = x1 - x0, y1 - y0
    L = math.hypot(dx, dy)
    ux, uy = dx / L, dy / L
    nx, ny = -uy, ux
    # exact taper between p0 and p1; beyond them (for clipping to level terminals) the width stays constant
    a0 = (x0 - ux * ext, y0 - uy * ext)
    a1 = (x1 + ux * ext, y1 + uy * ext)
    return Polygon([(a0[0] + nx * w0 / 2, a0[1] + ny * w0 / 2), (x0 + nx * w0 / 2, y0 + ny * w0 / 2),
                    (x1 + nx * w1 / 2, y1 + ny * w1 / 2), (a1[0] + nx * w1 / 2, a1[1] + ny * w1 / 2),
                    (a1[0] - nx * w1 / 2, a1[1] - ny * w1 / 2), (x1 - nx * w1 / 2, y1 - ny * w1 / 2),
                    (x0 - nx * w0 / 2, y0 - ny * w0 / 2), (a0[0] - nx * w0 / 2, a0[1] - ny * w0 / 2)]).buffer(0)


def M(s, W=92.0, vertex=0.30, diag=0.92, foot=0.55):
    """Vertical stems; the V meets at `vertex`·H with a small flat foot so it never fills in."""
    vb = H * vertex
    f = foot * s
    run = W / 2 - f / 2
    theta = math.atan2(H - vb, run)
    t = diag * s / math.sin(theta)
    slope = (H - vb) / run
    vi = H - (W / 2 - t) * slope
    v = Polygon([(0, H), (t, H), (W / 2, vi), (W - t, H), (W, H), (W / 2 + f / 2, vb), (W / 2 - f / 2, vb)])
    return unary_union([box(0, 0, s, H), box(W - s, 0, W, H), v]), W


def D(s, W=84.0, hthin=0.9):
    """Geometric D: straight stem, semicircular bowl."""
    R = H / 2
    c = W - R  # centre of the bowl
    right = box(c, -1, W + 1, H + 1)
    outer = unary_union([box(0, 0, c, H), Point(c, R).buffer(R, resolution=128).intersection(right)])
    sh = s * hthin
    inner_round = affinity.translate(affinity.scale(Point(0, 0).buffer(1, resolution=128), R - s, R - sh), c, R)
    inner = unary_union([box(s, sh, c, H - sh), inner_round.intersection(right)])
    return outer.difference(inner), W


def E(s, W=62.0, mid=0.92, hthin=0.9):
    sh = s * hthin
    return unary_union([box(0, 0, s, H), box(0, H - sh, W, H), box(0, 0, W, sh),
                        box(0, H / 2 - sh / 2, W * mid, H / 2 + sh / 2)]), W


def X(s, W=88.0, diag=1.0):
    a = bar((0, H), (W, 0), s * diag, ext=40).intersection(box(0, 0, W, H))
    b = bar((0, 0), (W, H), s * diag, ext=40).intersection(box(0, 0, W, H))
    return unary_union([a, b]), W


def place(g, x, y=0.0):
    return affinity.translate(g, xoff=x, yoff=y)


def to_d(geom, ox=0.0, oy=0.0, s=1.0, ndp=2):
    """SVG path data; flips y (y-up geometry → y-down SVG) with the baseline at oy."""
    geom = geom.buffer(0)
    polys = [geom] if geom.geom_type == "Polygon" else [g for g in geom.geoms if g.geom_type == "Polygon"]
    out = []
    for p in polys:
        p = p.simplify(0.01)
        for ring in [p.exterior] + list(p.interiors):
            pts = list(ring.coords)[:-1]
            out.append("M" + "L".join(f"{round(ox + x * s, ndp):g} {round(oy - y * s, ndp):g}" for x, y in pts) + "Z")
    return "".join(out)


def svg(vb, body, title=""):
    x, y, w, h = vb
    t = f"<title>{title}</title>" if title else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x:g} {y:g} {w:g} {h:g}" role="img" aria-label="{title}">'
            f"{t}{body}</svg>\n")


def P(d, fill, extra=""):
    return f'<path fill="{fill}" d="{d}"{extra}/>'
