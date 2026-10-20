"""Logo 2 — THE NOTCH.

Every MXDE moment starts with a tear at the notch. Move that notch to the centre of the top seal,
cut it deep, and the silhouette of the sachet becomes a solid M. The pack is the first letter of the name.
"""
from shapely.geometry import Polygon
from shapely.ops import unary_union
from letters import H, M, X, D, E, place, to_d, svg, P

W_PACK = 96.0       # the M-sachet, at cap height
OPEN = 0.46         # notch opening at the top, × width
DEPTH = 0.56        # notch depth, × height
TEETH_TOP = 3       # crimp teeth per shoulder
TEETH_BOT = 8       # crimp teeth along the bottom seal
TOOTH = 3.6         # crimp depth
S = 22.0            # stem of X, D, E
SPACE = (13.0, 13.0, 16.0)


def zig(x0, x1, y, n, depth, down=True):
    """Zig-zag points from x0 to x1 along y; teeth point away from the pack (outward)."""
    pts = []
    tw = (x1 - x0) / n
    for i in range(n):
        a = x0 + i * tw
        pts.append((a, y))
        pts.append((a + tw / 2, y - depth if down else y + depth))
    return pts


def pack_m(W=W_PACK, Hh=H, open_=OPEN, depth=DEPTH, teeth=True, tooth=TOOTH):
    a = W * (1 - open_) / 2
    apex = (W / 2, Hh - depth * Hh)
    t = tooth if teeth else 0
    pts = []
    # top-left shoulder, left to right, teeth cut downward into the seal
    pts += zig(0, a, Hh, TEETH_TOP if teeth else 1, t) if teeth else [(0, Hh)]
    pts += [(a, Hh), apex, (W - a, Hh)]
    pts += zig(W - a, W, Hh, TEETH_TOP if teeth else 1, t)[1:] if teeth else []
    pts += [(W, Hh), (W, 0)]
    # bottom seal, right to left, teeth cut upward
    if teeth:
        n = TEETH_BOT
        tw = W / n
        for i in range(n):
            xa = W - i * tw
            pts.append((xa, 0))
            pts.append((xa - tw / 2, t))
    pts.append((0, 0))
    return Polygon(pts).buffer(0)


def wordmark(teeth=True, s=S, depth=DEPTH):
    m = pack_m(teeth=teeth, depth=depth)
    x, wx = X(s, W=86.0)
    d, wd = D(s, W=82.0)
    e, we = E(s, W=60.0)
    xs = [0.0]
    for adv, sp in zip((W_PACK, wx, wd), SPACE):
        xs.append(xs[-1] + adv + sp)
    rest = unary_union([place(x, xs[1]), place(d, xs[2]), place(e, xs[3])])
    return {"pack": m, "rest": rest, "width": xs[3] + we}


def symbol(teeth=True, W=100.0, Hh=132.0):
    """The sachet in its real proportion (about 3:4) for icons, seals and the die-cut."""
    return pack_m(W=W, Hh=Hh, open_=0.44, depth=0.46, teeth=teeth, tooth=4.2)
