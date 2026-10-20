"""Logo 5 — BLOOM.

Before it's a bean, coffee is a flower: white, jasmine-scented, open for two or three days, and on
arabica it usually has five petals. MODE has five modes. So the mark is the coffee flower, drawn with
a coffee bean for every petal. Each mode lights its own petal.
"""
import math
from shapely.geometry import Point, LineString, box
from shapely.ops import unary_union
from shapely import affinity

MODES = ["wake", "active", "zen", "vital", "calm"]   # clockwise from the top: the order of a day
C = (100.0, 100.0)
DIST = 47.0      # petal centre from the flower centre
RX, RY = 19.5, 34.0
CREASE = 3.8     # width of the bean's crease
TWIST = 0.0      # extra rotation of each petal about its own centre


def bean(rx=RX, ry=RY, crease=CREASE, wave=4.2):
    """A coffee bean, long axis vertical, centred at 0,0: an ellipse with an S-shaped crease cut through it."""
    body = affinity.scale(Point(0, 0).buffer(1, resolution=96), rx, ry)
    pts = []
    n = 60
    for i in range(n + 1):
        t = -0.86 + 1.72 * i / n
        y = t * ry
        x = wave * math.sin(math.pi * t / 0.86)
        pts.append((x, y))
    cut = LineString(pts).buffer(crease / 2, cap_style="round", resolution=16)
    return body.difference(cut), body


def petals(twist=TWIST, dist=DIST, crease=CREASE):
    """Five beans arranged as the five petals. Returns {mode: (bean_with_crease, plain_outline)}."""
    out = {}
    b, plain = bean(crease=crease)
    for i, m in enumerate(MODES):
        ang = -90 + 72 * i            # SVG-style angle, 0 = right; top first
        rad = math.radians(ang)
        cx, cy = C[0] + dist * math.cos(rad), C[1] + dist * math.sin(rad)
        rot = ang + 90 + twist          # long axis points out from the centre
        out[m] = (affinity.translate(affinity.rotate(b, rot, origin=(0, 0)), cx, cy),
                  affinity.translate(affinity.rotate(plain, rot, origin=(0, 0)), cx, cy))
    return out


def outline(shape, w=3.2):
    """An outline of a petal for the unlit petals in a mode mark (one-colour safe)."""
    return shape.difference(shape.buffer(-w))
