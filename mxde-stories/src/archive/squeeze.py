"""Logo 4 — ONE SQUEEZE.

The sachet opens with one hand: fold it, squeeze it, and the coffee comes out in a single stream.
So the name is written the same way: one unbroken line of coffee, from the first stroke of the m
to the drop that forms at the end of the e.
"""
import math
from shapely.geometry import LineString, Point, Polygon
from shapely.ops import unary_union

XH = 56.0      # x-height
ASC = 98.0     # ascender of the d
W = 10.5       # the stream's width
R = 13.6       # radius of the m's arches
GAP = 15.0     # baseline run between letters


def arc(cx, cy, r, a0, a1, n=48):
    """Points along a circular arc, angles in degrees, counter-clockwise if a1 > a0."""
    return [(cx + r * math.cos(math.radians(a0 + (a1 - a0) * i / n)), cy + r * math.sin(math.radians(a0 + (a1 - a0) * i / n)))
            for i in range(n + 1)]


def path():
    """The single line, as an ordered list of points (y-up). Retraced segments overlap and disappear."""
    h, r = XH, R
    p = []
    # m: one stem, two arches, all on one line
    p += [(0, h), (0, 0), (0, h - r)]
    p += arc(r, h - r, r, 180, 0)
    p += [(2 * r, 0), (2 * r, h - r)]
    p += arc(3 * r, h - r, r, 180, 0)
    p += [(4 * r, 0)]
    # x: up the rising stroke, back to the crossing, out to each remaining arm
    x0 = 4 * r + GAP
    x1 = x0 + 46
    xc = (x0 + x1) / 2
    p += [(x0, 0), (x1, h), (xc, h / 2), (x0, h), (xc, h / 2), (x1, 0)]
    # d: round the bowl, up the ascender and back down
    br = h / 2
    dcx = x1 + GAP + br
    p += [(dcx, 0)]
    p += arc(dcx, br, br, -90, 270)
    p += arc(dcx, br, br, 270, 360, 12)[1:]
    p += [(dcx + br, ASC), (dcx + br, 0)]
    # e: along the base, round the lower-left, across the bar, then all the way round to the open end
    ecx = dcx + br + GAP + br
    p += [(ecx, 0)]
    p += arc(ecx, br, br, 270, 180, 24)[1:]
    p += [(ecx + br, br)]
    p += arc(ecx, br, br, 0, 318, 96)[1:]
    end_angle = 318
    return p, (ecx, br, br, end_angle), dcx + br + GAP + 2 * br


def drop(x, y, angle_deg, size):
    """A teardrop hanging from (x, y): round body, tip toward the line."""
    a = math.radians(angle_deg)
    # body centre a little beyond the tip along the direction of travel
    bx, by = x + math.cos(a) * size * 1.15, y + math.sin(a) * size * 1.15
    body = Point(bx, by).buffer(size * 0.62, resolution=48)
    tip = Polygon([(x, y), (bx + math.cos(a + math.pi / 2) * size * 0.6, by + math.sin(a + math.pi / 2) * size * 0.6),
                   (bx - math.cos(a + math.pi / 2) * size * 0.6, by - math.sin(a + math.pi / 2) * size * 0.6)])
    return unary_union([body, tip])


def mark(w=W):
    pts, (ecx, ecy, er, ea), width = path()
    line = LineString(pts).buffer(w / 2, cap_style="round", join_style="round", resolution=24)
    # the last of the stream gathers into a drop that hangs from the open end of the e
    ex = ecx + er * math.cos(math.radians(ea))
    ey = ecy + er * math.sin(math.radians(ea))
    d = drop(ex, ey, -62, w * 1.05)
    return {"line": line, "drop": d, "width": width + w, "ink": unary_union([line, d])}
