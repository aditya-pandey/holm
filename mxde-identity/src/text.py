"""Outline text with fontTools so finished artwork never carries live <text>."""
import os
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

FONTS = os.path.join(os.path.dirname(__file__), "fonts")
_cache = {}


def font(name):
    if name not in _cache:
        _cache[name] = TTFont(os.path.join(FONTS, name))
    return _cache[name]


def cap_height(name):
    f = font(name)
    os2 = f["OS/2"]
    return getattr(os2, "sCapHeight", 0) or f["head"].unitsPerEm * 0.7


def text_path(s, fontname, x, baseline, cap, tracking=0.0):
    """Path data for `s` with cap height `cap` (user units), left edge x, baseline y (SVG y-down).
    tracking is in units of cap height. Returns (d, advance_width)."""
    f = font(fontname)
    gs = f.getGlyphSet()
    cmap = f.getBestCmap()
    scale = cap / cap_height(fontname)
    hmtx = f["hmtx"]
    pen = SVGPathPen(gs)
    cx = x
    for ch in s:
        gname = cmap[ord(ch)]
        tp = TransformPen(pen, (scale, 0, 0, -scale, cx, baseline))
        gs[gname].draw(tp)
        cx += hmtx[gname][0] * scale + tracking * cap
    width = cx - x - (tracking * cap if s else 0)
    return pen.getCommands(), width


def text_width(s, fontname, cap, tracking=0.0):
    return text_path(s, fontname, 0, 0, cap, tracking)[1]
