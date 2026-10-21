"""The MODE mark, drawn with exact arcs (no approximated curves) so the master SVG/PDF files are clean vectors.

Units: letter height 100. The kit is Hollenstein's: square, half-disc, quarter-disc, a thin cut between solids,
hairlines of the same radius. MO sits over DE.

    m  a square of coffee that drips: two arches bitten up to the halfway line, three legs ending in drops
    o  half poured from the side: solid right half, hairline left half
    D  a coffee cup on its saucer: straight back (stem), round belly (bowl), small high handle
    e  Hollenstein's e, left open: half-disc, quarter-disc and the start of a hairline
"""
import math

R = 50.0        # the one radius
G = 3.0         # the cut between solids
W = 2.2         # hairline weight (small-size cut: 6)
STACK = 12.0    # gap between the columns and between the rows
LEG = 20.0      # width of each of the m's legs (also the clear-space unit: clear space = 2 legs)
CUP = dict(bw=76.0, top=16.0, base=90.0, rb=60.0, hro=17.0, ht=7.5)


def f(v):
    s = f"{v:.3f}".rstrip("0").rstrip(".")
    return "0" if s in ("-0", "") else s


def pt(cx, cy, r, a):
    return cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a))


def arc_to(cx, cy, r, a0, a1):
    """SVG arc commands from angle a0 to a1 (degrees, y down, increasing = clockwise), split into <=90° pieces."""
    n = max(1, math.ceil(abs(a1 - a0) / 90 - 1e-9))
    out = []
    for i in range(1, n + 1):
        a = a0 + (a1 - a0) * i / n
        x, y = pt(cx, cy, r, a)
        out.append(f"A{f(r)} {f(r)} 0 0 {1 if a1 > a0 else 0} {f(x)} {f(y)}")
    return "".join(out)


def hairline_arc(cx, cy, a0, a1, w, r=R):
    """A hairline on a circle of radius r (outer edge on the outline), with round ends, as a filled outline."""
    rc, h = r - w / 2, w / 2
    x0, y0 = pt(cx, cy, rc + h, a0)
    xi1, yi1 = pt(cx, cy, rc - h, a1)
    xs, ys = pt(cx, cy, rc - h, a0)
    return (f"M{f(x0)} {f(y0)}" + arc_to(cx, cy, rc + h, a0, a1)
            + f"A{f(h)} {f(h)} 0 0 {1 if a1 > a0 else 0} {f(xi1)} {f(yi1)}"
            + arc_to(cx, cy, rc - h, a1, a0)
            + f"A{f(h)} {f(h)} 0 0 {1 if a1 > a0 else 0} {f(xs)} {f(ys)}Z")


def hairline_line(x0, x1, y, w):
    """A horizontal hairline with round ends, centred on y."""
    h = w / 2
    return f"M{f(x0)} {f(y - h)}H{f(x1)}A{f(h)} {f(h)} 0 0 1 {f(x1)} {f(y + h)}H{f(x0)}A{f(h)} {f(h)} 0 0 1 {f(x0)} {f(y - h)}Z"


# ------------------------------------------------------------------ the four letters (each at its own origin)
def m(ox=0.0, oy=0.0):
    c = (100 - 3 * LEG) / 2
    r, b = c / 2, LEG / 2
    xs = [0, LEG + c, 2 * LEG + 2 * c]
    X = lambda v: f(ox + v)
    Y = lambda v: f(oy + v)
    d = f"M{X(0)} {Y(0)}H{X(100)}V{Y(100 - b)}"
    d += f"A{f(b)} {f(b)} 0 0 1 {X(xs[2])} {Y(100 - b)}V{Y(R)}"
    d += f"A{f(r)} {f(r)} 0 0 0 {X(xs[1] + LEG)} {Y(R)}V{Y(100 - b)}"
    d += f"A{f(b)} {f(b)} 0 0 1 {X(xs[1])} {Y(100 - b)}V{Y(R)}"
    d += f"A{f(r)} {f(r)} 0 0 0 {X(LEG)} {Y(R)}V{Y(100 - b)}"
    d += f"A{f(b)} {f(b)} 0 0 1 {X(0)} {Y(100 - b)}Z"
    return {"solid": d, "hair": ""}, 100.0


def o(ox=0.0, oy=0.0, w=None):
    w = w or W
    cx = ox + R
    solid = f"M{f(cx + G)} {f(oy)}" + arc_to(cx + G, oy + R, R, -90, 90) + "Z"
    return {"solid": solid, "hair": hairline_arc(cx, oy + R, 90, 270, w)}, 2 * R + G


def D(ox=0.0, oy=0.0, w=None):
    w = w or W
    k = CUP
    bw, top, base, rb, hro, ht = k["bw"], k["top"], k["base"], k["rb"], k["hro"], k["ht"]
    body = (f"M{f(ox)} {f(oy + top)}H{f(ox + bw)}V{f(oy + base - rb)}"
            + arc_to(ox + bw - rb, oy + base - rb, rb, 0, 90) + f"H{f(ox)}Z")
    hx, hy = ox + bw + G - 2, oy + top + hro + 4
    handle = (f"M{f(hx)} {f(hy - hro)}" + arc_to(hx, hy, hro, -90, 90) + f"V{f(hy + hro - ht)}"
              + arc_to(hx, hy, hro - ht, 90, -90) + "Z")
    saucer = hairline_line(ox - 8, ox + bw + 14, oy + 100 - w / 2 - 2, w)
    return {"solid": body + handle, "hair": saucer}, bw + G + hro


def e(ox=0.0, oy=0.0, w=None):
    w = w or W
    cx = ox + R
    left = f"M{f(cx)} {f(oy)}" + arc_to(cx, oy + R, R, -90, -270) + "Z"
    quarter = f"M{f(cx + G)} {f(oy + R)}V{f(oy)}" + arc_to(cx + G, oy + R, R, -90, 0) + "Z"
    return {"solid": left + quarter, "hair": hairline_arc(cx + G, oy + R, 58, 90, w)}, 2 * R + G


def stack(w=None):
    """MO over DE. Returns {'solid': d, 'hair': d} and the bounding box (x0, y0, x1, y1)."""
    col = max(100.0, CUP["bw"] + G + CUP["hro"]) + STACK
    row = 100 + STACK
    parts = [m(0, 0)[0], o(col, 0, w)[0], D(0, row, w)[0], e(col, row, w)[0]]
    ww = w or W
    box = (-8 - ww / 2, 0.0, col + 2 * R + G, row + 100.0)
    return {"solid": "".join(p["solid"] for p in parts), "hair": "".join(p["hair"] for p in parts)}, box


def letters(w=None):
    """Each letter alone, with its own box, for the guidelines and the packaging heroes."""
    out = {}
    g, _ = m()
    out["m"] = (g, (0, 0, 100, 100))
    g, _ = o(w=w)
    out["o"] = (g, (0, 0, 103, 100))
    g, _ = D(w=w)
    out["D"] = (g, (-8 - (w or W) / 2, CUP["top"], CUP["bw"] + G + CUP["hro"] - 2 + 0.01, 100))
    g, _ = e(w=w)
    out["e"] = (g, (0, 0, 103, 100))
    return out


def paths(g, fill, hair_fill=None):
    """SVG <path> elements for a mark: solids and hairlines (both filled shapes, nothing stroked)."""
    s = f'<path fill="{fill}" d="{g["solid"]}"/>'
    if g["hair"]:
        s += f'<path fill="{hair_fill or fill}" d="{g["hair"]}"/>'
    return s


def svg_doc(g, box, fill, pad=0.0, bg=None, title="MODE"):
    x0, y0, x1, y1 = box
    vb = f"{f(x0 - pad)} {f(y0 - pad)} {f(x1 - x0 + 2 * pad)} {f(y1 - y0 + 2 * pad)}"
    back = f'<rect x="{f(x0 - pad)}" y="{f(y0 - pad)}" width="{f(x1 - x0 + 2 * pad)}" height="{f(y1 - y0 + 2 * pad)}" fill="{bg}"/>' if bg else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" role="img" aria-label="{title}">'
            f'<title>{title}</title>{back}{paths(g, fill)}</svg>')
