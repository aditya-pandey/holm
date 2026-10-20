"""Text → SVG path outlines (fontTools), including instances of variable fonts."""
import os
from functools import lru_cache
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen

FONTS = os.path.join(os.path.dirname(__file__), "..", "fonts")


@lru_cache(maxsize=None)
def font(name, axes=None):
    f = TTFont(os.path.join(FONTS, name))
    if axes:
        from fontTools.varLib.instancer import instantiateVariableFont
        f = instantiateVariableFont(f, dict(axes), inplace=False)
    return f


def cap(f):
    return getattr(f["OS/2"], "sCapHeight", 0) or f["head"].unitsPerEm * 0.7


def glyphs(s, fontname, x, baseline, capheight, tracking=0.0, axes=None):
    """Per-glyph outlines: [(char, d, bbox, advance)] in SVG coords (y down). tracking in cap-height units."""
    f = font(fontname, tuple(sorted(axes.items())) if axes else None)
    gs, cmap, hmtx = f.getGlyphSet(), f.getBestCmap(), f["hmtx"]
    k = capheight / cap(f)
    out, cx = [], x
    for ch in s:
        g = cmap[ord(ch)]
        pen = SVGPathPen(gs)
        gs[g].draw(TransformPen(pen, (k, 0, 0, -k, cx, baseline)))
        bp = BoundsPen(gs)
        gs[g].draw(bp)
        b = bp.bounds or (0, 0, 0, 0)
        adv = hmtx[g][0] * k
        out.append((ch, pen.getCommands(), (cx + b[0] * k, baseline - b[3] * k, cx + b[2] * k, baseline - b[1] * k), adv))
        cx += adv + tracking * capheight
    return out


def outline(s, fontname, x, baseline, capheight, tracking=0.0, axes=None, steps=10):
    """The same text as a shapely geometry (curves flattened), for boolean cuts. Holes via even-odd."""
    from fontTools.pens.basePen import BasePen
    from shapely.geometry import Polygon
    from shapely.ops import unary_union
    f = font(fontname, tuple(sorted(axes.items())) if axes else None)
    gs, cmap, hmtx = f.getGlyphSet(), f.getBestCmap(), f["hmtx"]
    k = capheight / cap(f)

    class Flat(BasePen):
        def __init__(self, gs):
            super().__init__(gs)
            self.rings, self.cur = [], []

        def _moveTo(self, p):
            self.cur = [p]

        def _lineTo(self, p):
            self.cur.append(p)

        def _curveToOne(self, p1, p2, p3):
            p0 = self.cur[-1]
            for i in range(1, steps + 1):
                t = i / steps
                a, b, c, d = (1 - t) ** 3, 3 * (1 - t) ** 2 * t, 3 * (1 - t) * t * t, t ** 3
                self.cur.append((a * p0[0] + b * p1[0] + c * p2[0] + d * p3[0], a * p0[1] + b * p1[1] + c * p2[1] + d * p3[1]))

        def _qCurveToOne(self, p1, p2):
            p0 = self.cur[-1]
            for i in range(1, steps + 1):
                t = i / steps
                a, b, c = (1 - t) ** 2, 2 * (1 - t) * t, t * t
                self.cur.append((a * p0[0] + b * p1[0] + c * p2[0], a * p0[1] + b * p1[1] + c * p2[1]))

        def _closePath(self):
            if len(self.cur) > 2:
                self.rings.append(self.cur)
            self.cur = []

        _endPath = _closePath

    geoms, cx = [], x
    for ch in s:
        g = cmap[ord(ch)]
        pen = Flat(gs)
        gs[g].draw(TransformPen(pen, (k, 0, 0, -k, cx, baseline)))
        shape = None
        for ring in pen.rings:
            p = Polygon(ring).buffer(0)
            shape = p if shape is None else shape.symmetric_difference(p)
        if shape is not None:
            geoms.append(shape)
        cx += hmtx[g][0] * k + tracking * capheight
    return unary_union(geoms)


def text(s, fontname, x, baseline, capheight, tracking=0.0, axes=None):
    gl = glyphs(s, fontname, x, baseline, capheight, tracking, axes)
    d = "".join(g[1] for g in gl)
    ink = (min(g[2][0] for g in gl), min(g[2][1] for g in gl), max(g[2][2] for g in gl), max(g[2][3] for g in gl))
    return d, ink
