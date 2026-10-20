"""Logo 4 — MUG.

A D is a straight back and a round belly. Thicken the back, shrink the belly and lift it off the
ground, and the D is a coffee mug seen from the side: the body is the stem, the handle is the bowl.
"""
from shapely.geometry import Point, box
from shapely.ops import unary_union
from shapely import affinity
from letters import H, M, X, E, place, to_d, svg, P

S = 17.0                      # stem of M, X, E
BODY_W = 44.0                 # the mug's body = the D's stem, thickened
FOOT_R = 7.0                  # the body's bottom corners are rounded, like a mug
RIM = 6.5                     # a thin line across the top: the rim, and the coffee just below it
HANDLE = (0.04, 0.90)         # the handle spans almost the full height, so the D still reads as a D
HANDLE_OUT = 44.0             # how far the handle reaches out
HANDLE_T = 17.0               # handle thickness = the stem
SPACE = (14.0, 16.0, 18.0)


def mug_d(body_w=BODY_W, handle=HANDLE, out=HANDLE_OUT, t=HANDLE_T, rim=RIM, foot=FOOT_R, rim_line=True):
    """The mug-D. Returns (shape, advance width)."""
    # body with rounded bottom corners
    body = unary_union([box(0, foot, body_w, H), box(foot, 0, body_w - foot, foot),
                        Point(foot, foot).buffer(foot, resolution=32), Point(body_w - foot, foot).buffer(foot, resolution=32)])
    if rim_line:
        body = body.difference(box(-1, H - rim - 4.2, body_w + 1, H - rim))
    # handle: a D-shaped loop, flat side against the body
    y0, y1 = handle[0] * H, handle[1] * H
    hh = y1 - y0
    ry = hh / 2
    loop_outer = affinity.scale(Point(0, 0).buffer(1, resolution=64), out, ry)
    loop_outer = affinity.translate(loop_outer, body_w - 2, y0 + ry).intersection(box(body_w - 2, -1, body_w + out + 1, H + 1))
    loop_inner = affinity.scale(Point(0, 0).buffer(1, resolution=64), out - t, ry - t * 0.92)
    loop_inner = affinity.translate(loop_inner, body_w - 2, y0 + ry)
    handle_shape = loop_outer.difference(loop_inner)
    return unary_union([body, handle_shape]), body_w - 2 + out


def wordmark(s=S):
    m, wm = M(s, W=94.0)
    x, wx = X(s, W=86.0)
    d, wd = mug_d()
    e, we = E(s, W=60.0)
    xs = [0.0]
    for adv, sp in zip((wm, wx, wd), SPACE):
        xs.append(xs[-1] + adv + sp)
    rest = unary_union([place(m, xs[0]), place(x, xs[1]), place(e, xs[3])])
    return {"rest": rest, "mug": place(d, xs[2]), "width": xs[3] + we, "mug_x": xs[2]}
