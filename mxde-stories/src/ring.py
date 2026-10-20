"""Logo 3 — RING.

Everyone asks how to say MXDE. Put your coffee down on it. When you lift the cup, it leaves a ring,
and the ring sits round the X: M(O)DE. The O in Mode is written by the coffee.
"""
import math
from shapely.geometry import Polygon, Point, box
from shapely.ops import unary_union
from letters import H, M, X, D, E, place, to_d, svg, P

S = 12.5                    # a light, even stem so the ring leads
SPACE = (40.0, 40.0, 17.0)  # wide around the X: the ring needs room
XW = 82.0
RING_R = 71.0               # mean radius of the outer edge
RING_C = (0.0, 47.0)        # offset from the X centre: a cup is never set down dead centre


def wordmark(s=S):
    m, wm = M(s, W=88.0)
    x, wx = X(s, W=XW)
    d, wd = D(s, W=80.0)
    e, we = E(s, W=58.0)
    xs = [0.0]
    for adv, sp in zip((wm, wx, wd), SPACE):
        xs.append(xs[-1] + adv + sp)
    letters = unary_union([place(m, xs[0]), place(x, xs[1]), place(d, xs[2]), place(e, xs[3])])
    return {"letters": letters, "width": xs[3] + we, "x_mid": xs[1] + wx / 2}


def _wobble(theta, terms):
    return sum(a * math.sin(k * theta + ph) for k, a, ph in terms)


def ring(cx, cy, R=RING_R, n=360):
    """A coffee-cup ring: a sharp, dark outer edge of uneven weight (where the coffee dried) and a
    faint inner wash. Deterministic wobble so every master is identical."""
    shape = [(1, 1.6, 0.4), (2, 1.1, 2.1), (3, 0.6, 4.0), (5, 0.35, 1.2)]       # out-of-round
    weight = [(1, 1.9, 5.1), (2, 0.9, 0.7), (4, 0.5, 2.6)]                      # edge thickness wobble
    outer, inner, wash = [], [], []
    for i in range(n):
        t = 2 * math.pi * i / n
        r = R + _wobble(t, shape)
        w = 4.2 + _wobble(t, weight)
        # the edge thins to almost nothing over a short arc at upper left, where the cup was lifted first
        lift = math.exp(-((math.atan2(math.sin(t - 2.45), math.cos(t - 2.45))) / 0.32) ** 2)
        w = max(0.9, w * (1 - 0.78 * lift))
        outer.append((cx + r * math.cos(t), cy + r * math.sin(t)))
        inner.append((cx + (r - w) * math.cos(t), cy + (r - w) * math.sin(t)))
        rw = r - w - 9 - 3 * math.sin(2 * t + 1.0)
        wash.append((cx + rw * math.cos(t), cy + rw * math.sin(t)))
    edge = Polygon(outer).difference(Polygon(inner))
    tone = Polygon(inner).difference(Polygon(wash))
    return edge, tone


def mark(s=S):
    w = wordmark(s)
    cx = w["x_mid"] + RING_C[0]
    edge, tone = ring(cx, RING_C[1])
    return {**w, "edge": edge, "tone": tone, "cx": cx}


def tide(cx, cy, R=RING_R - 1.5, n=240):
    """A faint second ring, slightly offset: the cup was set down twice. Colour hero only."""
    pts_o, pts_i = [], []
    for i in range(n + 1):
        t = math.radians(150 + 175 * i / n)       # a partial arc, top-left to right
        r = R + 0.8 * math.sin(3 * t + 0.5)
        w = 1.6 + 0.9 * math.sin(2 * t)
        pts_o.append((cx + 4.5 + r * math.cos(t), cy - 3.5 + r * math.sin(t)))
        pts_i.append((cx + 4.5 + (r - w) * math.cos(t), cy - 3.5 + (r - w) * math.sin(t)))
    return Polygon(pts_o + pts_i[::-1]).buffer(0)
