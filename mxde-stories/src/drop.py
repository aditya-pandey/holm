"""Logo 6 — FIVE STATES OF A DROP.

MODE is a concentrate: a sachet is a few drops of coffee. And a drop is always the same liquid, but its
shape tells you what it's doing: falling, in flight, floating, splashing, resting. Five states, five modes.
"""
import math
from shapely.geometry import Point, Polygon, box
from shapely.ops import unary_union
from shapely import affinity

MODES = ["wake", "active", "zen", "vital", "calm"]
S = 100.0  # every state is drawn to sit in the same 100 × 100 cell, on one baseline


def teardrop(cx, cy_body, r, tip_h, n=180):
    """A drop: circular body of radius r centred at (cx, cy_body), tapering smoothly to a tip tip_h above
    the body centre (y up). The sides are tangent to the circle, so there is no kink."""
    # tangent points from the tip to the circle
    d = tip_h
    tang = math.asin(r / d)                    # tangent points sit at 90° ± acos(r/d), i.e. at this angle from +x
    pts = [(cx, cy_body + d)]
    # right side: straight-ish tangent line then the circle round the bottom
    for i in range(n + 1):
        t = tang - (2 * tang + math.pi) * i / n   # sweep from right tangent round the bottom to left tangent
        pts.append((cx + r * math.cos(t), cy_body + r * math.sin(t)))
    return Polygon(pts).buffer(0)


def state(m):
    """Shape for each mode, in a 100-unit cell, baseline y = 0, y up."""
    if m == "wake":      # falling: the classic drop, tip up
        return teardrop(50, 33, 30, 70)
    if m == "active":    # in flight: longer, leaning forward
        g = teardrop(0, 0, 27, 92)
        g = affinity.rotate(g, -38, origin=(0, 0))
        b = g.bounds
        return affinity.translate(g, 50 - (b[0] + b[2]) / 2, 2 - b[1])
    if m == "zen":       # floating: in zero gravity a drop is a perfect sphere
        return Point(50, 40).buffer(36, resolution=128)
    if m == "vital":     # bouncing: squashed by the landing, already back in the air, its shadow below
        body = affinity.translate(affinity.scale(Point(0, 0).buffer(1, resolution=128), 41, 25), 50, 47)
        shadow = affinity.translate(affinity.scale(Point(0, 0).buffer(1, resolution=64), 27, 2.6), 50, 3)
        return unary_union([body, shadow])
    if m == "calm":      # resting: a bead sitting on the surface, wide and low
        dome = affinity.translate(affinity.scale(Point(0, 0).buffer(1, resolution=128), 44, 30), 50, 0)
        return dome.intersection(box(0, 0, 100, 40))
    raise ValueError(m)


def highlight(m):
    """A curved glint on the upper left of each drop: reads as liquid, not as an eye."""
    pos = {"wake": (50, 33, 30), "active": None, "zen": (50, 40, 36), "vital": (46, 47, 30), "calm": (50, 0, 30)}
    if m == "active":
        g = state(m)
        c = g.centroid
        cx, cy, r = c.x - 7, c.y - 7, 21
    else:
        cx, cy, r = pos[m]
    outer = Point(cx, cy).buffer(r * 0.74, resolution=64)
    inner = Point(cx + r * 0.16, cy - r * 0.16).buffer(r * 0.74, resolution=64)
    glint = outer.difference(inner).intersection(box(cx - r, cy, cx + r * 0.05, cy + r))
    if m == "calm":
        glint = affinity.scale(glint, 1.3, 0.75, origin=(cx, cy)).intersection(box(0, 6, 100, 40))
    return glint


def drop(m, with_light=True):
    g = state(m)
    return g.difference(highlight(m)) if with_light else g
