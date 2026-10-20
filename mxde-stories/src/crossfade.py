"""Logo 1 — CROSSFADE.

Every switch between two states is drawn, in every edit suite and DJ mixer, as a crossfade:
the outgoing signal falls while the incoming one rises, and the two lines cross. A crossfade is an X.
So the X in MXDE is drawn as one: each stroke's weight follows its volume.
"""
from shapely.geometry import box
from shapely.ops import unary_union
from letters import H, bar, M, D, E, place, to_d, svg, P

S = 15.0           # stem of M, D, E (15% of cap height)
XW = 90.0          # width of the X
LOUD = 1.30        # stroke weight at full volume, × stem
QUIET = 0.50       # stroke weight at silence, × stem
GAP = 3.2          # where the incoming stroke passes over the outgoing one
SPACE = (15.0, 15.0, 19.0)


def crossfade_x(s=S, W=XW, loud=LOUD, quiet=QUIET, gap=GAP):
    """Returns (outgoing, incoming) shapes. Outgoing: top-left (full) → bottom-right (silent).
    Incoming: bottom-left (silent) → top-right (full). Terminals cut level with cap height and baseline."""
    frame = box(0, 0, W, H)
    out_ = bar((0, H), (W, 0), loud * s, quiet * s, ext=30).intersection(frame)
    in_ = bar((0, 0), (W, H), quiet * s, loud * s, ext=30).intersection(frame)
    if gap:
        out_ = out_.difference(in_.buffer(gap, join_style="mitre"))
    return out_, in_


def wordmark(s=S, **kw):
    m, wm = M(s)
    o, i = crossfade_x(s, **kw)
    d, wd = D(s)
    e, we = E(s)
    xs = [0.0]
    for adv, sp in zip((wm, XW, wd), SPACE):
        xs.append(xs[-1] + adv + sp)
    steady = unary_union([place(m, xs[0]), place(d, xs[2]), place(e, xs[3])])
    return {"steady": steady, "out": place(o, xs[1]), "in": place(i, xs[1]), "width": xs[3] + we, "x_at": xs[1]}


def symbol(size=100.0, pad=0.0, **kw):
    o, i = crossfade_x(S, XW, **kw)
    k = (size - 2 * pad) / H
    from shapely import affinity
    o = affinity.translate(affinity.scale(o, k, k, origin=(0, 0)), pad + (size - 2 * pad - XW * k) / 2, pad)
    i = affinity.translate(affinity.scale(i, k, k, origin=(0, 0)), pad + (size - 2 * pad - XW * k) / 2, pad)
    return o, i
