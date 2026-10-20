"""Logo 6 — LOOKING BACK.

The first thing that looks back at you every morning is your coffee. Seen from above, a cup is an eye:
the rim is the white, the coffee is the iris, the light on the crema is the catchlight. Eyes are also
the plainest way people show what state they're in, so each mode has its own eyelid.
"""
import math
from shapely.geometry import Point, Polygon, box, LineString
from shapely.ops import unary_union
from shapely import affinity

CX, CY = 92.0, 100.0   # cup centre in a 200 × 200 box (y down, SVG coordinates)
R = 66.0               # outer edge of the rim
RIM = 9.0
COFFEE = 48.0          # radius of the coffee
HANDLE = dict(x0=CX + R - 4, w=34.0, h=38.0, t=9.0)


def ring(cx, cy, r, w, res=128):
    return Point(cx, cy).buffer(r, resolution=res).difference(Point(cx, cy).buffer(r - w, resolution=res))


def handle():
    h = HANDLE
    outer = box(h["x0"], CY - h["h"] / 2, h["x0"] + h["w"], CY + h["h"] / 2).buffer(0)
    outer = outer.buffer(h["h"] / 2 - 0.1, join_style="round").intersection(box(h["x0"], -1, 400, 400))
    inner = box(h["x0"], CY - h["h"] / 2 + h["t"], h["x0"] + h["w"] - h["t"], CY + h["h"] / 2 - h["t"])
    inner = inner.buffer(h["h"] / 2 - h["t"] - 0.1, join_style="round")
    return outer.difference(inner).difference(Point(CX, CY).buffer(R - 2, resolution=128))


def catchlight(dx=-17.0, dy=-18.0, r=10.5):
    return Point(CX + dx, CY + dy).buffer(r, resolution=64)


def lid(state):
    """The eyelid for each mode, as (cover, lash): cover hides the coffee, lash is the lid's edge."""
    disc = Point(CX, CY).buffer(COFFEE + 0.5, resolution=128)
    if state in ("logo", "wake"):
        return None, None
    if state == "calm":          # heavy-lidded: the lid rests half way down, a soft curve
        edge_y = CY - 4
        cover = box(CX - 80, CY - 80, CX + 80, edge_y).union(
            affinity.scale(Point(CX, edge_y).buffer(1, resolution=96), COFFEE, 9).intersection(box(0, edge_y, 400, 400)))
    elif state == "zen":         # closed: only a curved line of the coffee shows, like a resting eye
        cover = disc.difference(affinity.translate(affinity.scale(Point(0, 0).buffer(1, resolution=96), COFFEE * 0.96, 14), CX, CY + 22))
        cover = cover.union(box(CX - 80, CY - 80, CX + 80, CY + 8).intersection(disc))
    elif state == "active":      # focused: the lid comes down at an angle, like a set brow
        cover = Polygon([(CX - 60, CY - 70), (CX + 60, CY - 70), (CX + 60, CY - 30), (CX - 60, CY - 2)])
    elif state == "vital":       # bright: wide open, nothing covers it (a second catchlight does the work)
        return None, None
    else:
        return None, None
    cover = cover.intersection(disc)
    lash = cover.buffer(3.2).difference(cover.buffer(-0.1)).intersection(disc.buffer(-0.1)).difference(cover)
    return cover, lash


def mark(state="logo"):
    """Returns the ink shapes and knock-outs for a state. All coordinates SVG-style (y down), 200 box."""
    rim = ring(CX, CY, R, RIM)
    coffee = Point(CX, CY).buffer(COFFEE, resolution=128)
    cover, lash = lid(state)
    lights = [catchlight()]
    if state == "vital":
        lights.append(catchlight(dx=14.0, dy=-24.0, r=5.0))
    if state == "wake":
        lights = [catchlight(r=12.5)]
    visible = coffee
    if cover is not None:
        visible = coffee.difference(cover)
        lights = [l.difference(cover) for l in lights]
    ink = unary_union([rim, handle(), visible] + ([lash] if lash is not None else []))
    for l in lights:
        ink = ink.difference(l)
    return ink
