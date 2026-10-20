"""Explanatory diagrams shared by the guidelines PDF and the presentation page. All return SVG strings."""
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from geom import H
from build import WORD_W, SLOT_X, KCUT, STEM, GAPS, MODE_TILE, MODE_GAP
from marks import wordmark, tile, words, mode_lockup, lockup_height, tagline, MODE, MODE_KEYS, C
from text import font, cap_height

BOLD = "Archivo-Expanded-Bold.ttf"


def _svg(w, h, body, label, cls=""):
    c = f' class="{cls}"' if cls else ""
    return f'<svg{c} xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:g} {h:g}" role="img" aria-label="{label}">{body}</svg>'


def stock_word(s, x, baseline, cap, tracking=0.04):
    """Per-glyph outlines of `s` in Archivo Expanded Bold: [(char, d, (xmin, ymin, xmax, ymax))] in SVG coords."""
    f = font(BOLD)
    gs, cmap, hmtx = f.getGlyphSet(), f.getBestCmap(), f["hmtx"]
    k = cap / cap_height(BOLD)
    out, cx = [], x
    for ch in s:
        g = cmap[ord(ch)]
        pen = SVGPathPen(gs)
        gs[g].draw(TransformPen(pen, (k, 0, 0, -k, cx, baseline)))
        bp = BoundsPen(gs)
        gs[g].draw(bp)
        x0, y0, x1, y1 = bp.bounds
        out.append((ch, pen.getCommands(), (cx + x0 * k, baseline - y1 * k, cx + x1 * k, baseline - y0 * k)))
        cx += hmtx[g][0] * k + tracking * cap
    return out


def story_frames(ink="currentColor", accent=None, ground="none"):
    """Six frames, in the manner of a logo-process reel: the word, the change, the reveal, the switch."""
    accent = accent or C["Tonic"]
    W, Hh = 360, 220
    cap, base = 56, 138
    frames = []

    def frame(body):
        bg = f'<rect width="{W}" height="{Hh}" fill="{ground}"/>' if ground != "none" else ""
        return _svg(W, Hh, bg + body, "story frame", "frame")

    def centred(glyphs):
        x0 = glyphs[0][2][0]
        x1 = glyphs[-1][2][2]
        return (W - (x1 - x0)) / 2 - x0

    g = stock_word("MODE", 0, base, cap)
    dx = centred(g)
    word = "".join(f'<path transform="translate({dx:.2f} 0)" d="{d}" fill="{ink}"/>' for _, d, _ in g)
    frames.append(("Start with the word people should say.", frame(word)))

    ox0, oy0, ox1, oy1 = g[1][2]
    ox0 += dx
    ox1 += dx
    hs = 7
    handles = "".join(f'<rect x="{x - hs / 2:.1f}" y="{y - hs / 2:.1f}" width="{hs}" height="{hs}" fill="#fff" stroke="#2F6BFF" stroke-width="1.4"/>'
                      for x in (ox0, (ox0 + ox1) / 2, ox1) for y in (oy0, (oy0 + oy1) / 2, oy1) if not (x == (ox0 + ox1) / 2 and y == (oy0 + oy1) / 2))
    sel = (f'<rect x="{ox0:.1f}" y="{oy0:.1f}" width="{ox1 - ox0:.1f}" height="{oy1 - oy0:.1f}" fill="none" stroke="#2F6BFF" stroke-width="1.4"/>'
           + handles)
    frames.append(("The O is the letter that changes.", frame(word + sel)))

    sq = cap  # square on the cap height, centred on the O
    sx = (ox0 + ox1) / 2 - sq / 2
    rest = "".join(f'<path transform="translate({dx:.2f} 0)" d="{d}" fill="{ink}"/>' for i, (_, d, _) in enumerate(g) if i != 1)
    frames.append(("Square it. A slot, not a letter.", frame(rest + f'<rect x="{sx:.1f}" y="{base - cap}" width="{sq}" height="{sq}" fill="{ink}"/>')))

    frames.append(("Cut the X in. It reads Mode and spells MXDE.",
                   frame(rest + tile("x", sx, base - cap, sq, accent))))

    ww = 300
    frames.append(("Redraw M, D and E from straight lines to match.",
                   frame(wordmark((W - ww) / 2, base - ww / WORD_W * H, ww, ink, accent))))

    lw = 300
    lh = lockup_height(lw)
    frames.append(("Switch the slot. One brand, many modes.",
                   frame(mode_lockup((W - lw) / 2, (Hh - lh) / 2 + 4, lw, "calm", ink))))
    return frames


def routes_svg(ink="currentColor"):
    """The three concept routes as drawn in concepts/, for side-by-side comparison."""
    import re
    import os
    root = os.path.join(os.path.dirname(__file__), "..", "concepts")
    out = {}
    for key, fn in (("a", "route-a-crossover.svg"), ("b", "route-b-slot.svg"), ("c", "route-c-shift.svg")):
        s = open(os.path.join(root, fn)).read()
        s = s.replace('fill="#000"', f'fill="{ink}"').replace("<svg ", '<svg class="route" ')
        s = re.sub(r"<title>.*?</title>", "", s)
        out[key] = s
    return out


def construction(ink="currentColor", guide="#2F6BFF", muted="#888B8D"):
    pad = 60
    W, Hh = WORD_W + pad + 110, H + 2 * pad + 20
    oy = pad + 10
    g = [f'<g transform="translate({pad} {oy})">']
    g.append(wordmark(0, 0, WORD_W, ink, ink))
    sw = 0.5
    # cap and baseline
    for y, lab in ((0, "cap height 100"), (H, "baseline 0")):
        g.append(f'<line x1="-40" y1="{y}" x2="{WORD_W + 40}" y2="{y}" stroke="{guide}" stroke-width="{sw}" stroke-dasharray="3 2"/>')
        g.append(f'<text x="{WORD_W + 42}" y="{y + 3}" font-size="7" fill="{guide}" class="t-label">{lab}</text>')
    # stem
    g.append(f'<line x1="0" y1="{H + 10}" x2="{STEM}" y2="{H + 10}" stroke="{guide}" stroke-width="{sw * 2}"/>')
    g.append(f'<text x="0" y="{H + 22}" font-size="7" fill="{guide}" class="t-label">stem {STEM:g}</text>')
    # slot and cut
    g.append(f'<rect x="{SLOT_X}" y="0" width="{H}" height="{H}" fill="none" stroke="{guide}" stroke-width="{sw}"/>')
    g.append(f'<text x="{SLOT_X}" y="{H + 22}" font-size="7" fill="{guide}" class="t-label">slot 100 × 100 · cut {KCUT:.1f}</text>')
    for (x1, y1, x2, y2) in ((SLOT_X, 0, SLOT_X + H, H), (SLOT_X, H, SLOT_X + H, 0)):
        g.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{guide}" stroke-width="{sw}" stroke-dasharray="2 2"/>')
    # 45 and 60 degrees
    g.append(f'<text x="{SLOT_X + 4}" y="{H / 2 + 3}" font-size="7" fill="#fff" class="t-label">45°</text>')
    g.append(f'<text x="{STEM + 3}" y="{14}" font-size="7" fill="{guide}" class="t-label">60°</text>')
    # D chamfer
    dx0 = SLOT_X + H + GAPS[1]
    g.append(f'<text x="{dx0 + 60}" y="-6" font-size="7" fill="{guide}" class="t-label">chamfer 30 · 45°</text>')
    # spacing
    xs = [0, SLOT_X, dx0, dx0 + 84 + GAPS[2]]
    rights = [102, SLOT_X + H, dx0 + 84]
    for i, gap in enumerate(GAPS):
        x0, x1 = rights[i], xs[i + 1]
        g.append(f'<rect x="{x0}" y="{-24}" width="{x1 - x0}" height="12" fill="{guide}" opacity=".18"/>')
        g.append(f'<text x="{(x0 + x1) / 2}" y="{-15}" font-size="7" fill="{guide}" text-anchor="middle" class="t-label">{gap:g}</text>')
    g.append(f'<text x="0" y="{H + 44}" font-size="7.5" fill="{muted}" class="t-label">Units: cap height = 100. Angles: 0°, 45°, 60°, 90° only. No curves.</text>')
    g.append("</g>")
    return _svg(W, Hh, "".join(g), "Wordmark construction")


def clear_space(ink="currentColor", guide="#2F6BFF"):
    u = H * 0.5  # half the slot
    pad = 20
    W, Hh = WORD_W + 2 * u + 2 * pad, H + 2 * u + 2 * pad
    ox, oy = pad + u, pad + u
    b = [f'<rect x="{pad}" y="{pad}" width="{WORD_W + 2 * u}" height="{H + 2 * u}" fill="{guide}" opacity=".07"/>',
         f'<rect x="{pad}" y="{pad}" width="{WORD_W + 2 * u}" height="{H + 2 * u}" fill="none" stroke="{guide}" stroke-width=".8" stroke-dasharray="4 3"/>',
         wordmark(ox, oy, WORD_W, ink, ink)]
    for x, y in ((pad, pad), (pad + WORD_W + u, pad), (pad, pad + H + u), (pad + WORD_W + u, pad + H + u)):
        b.append(tile("x", x + u * 0.25, y + u * 0.25, u * 0.5, guide))
    b.append(f'<text x="{pad + 4}" y="{pad + u - 6}" font-size="8" fill="{guide}" class="t-label">½ slot</text>')
    return _svg(W, Hh, "".join(b), "Clear space")


def misuse(ink=None):
    ink = ink or C["Carbon"]
    W, Hh = 220, 120
    ww = 170
    y = (Hh - ww / WORD_W * H) / 2
    x = (W - ww) / 2
    cx, cy = W / 2, Hh / 2
    base = wordmark(x, y, ww, ink, C["Tonic"])
    items = [
        ("Don't stretch or squash.", f'<g transform="translate({cx} {cy}) scale(1.25 .72) translate({-cx} {-cy})">{base}</g>'),
        ("Don't rotate or slant.", f'<g transform="rotate(-10 {cx} {cy})">{base}</g>'),
        ("Don't outline the letters.", f'<g style="fill:none;stroke:{ink};stroke-width:1.2">{base.replace(f"fill=\"{ink}\"", "fill=\"none\"").replace("fill=\"" + C["Tonic"] + "\"", "fill=\"none\"")}</g>'),
        ("Don't add shadows, glows or gradients.", f'<defs><filter id="ds"><feDropShadow dx="3" dy="4" stdDeviation="2" flood-opacity=".45"/></filter></defs><g filter="url(#ds)">{base}</g>'),
        ("Don't colour M, D or E. Only the slot changes.", wordmark(x, y, ww, MODE["wake"]["hex"], MODE["vital"]["hex"])),
        ("Don't retype the name in a font.", f'<text x="{cx}" y="{cy + 14}" font-size="40" text-anchor="middle" class="t-head" fill="{ink}">MXDE</text>'),
        ("Don't put mode tiles in the slot on packs. ▲ reads MADE.", wordmark(x, y, ww, ink, MODE["wake"]["hex"], slot_key="wake")),
        ("Don't place on low-contrast grounds.", f'<rect width="{W}" height="{Hh}" fill="{C["Silver"]}"/>' + wordmark(x, y, ww, C["Stone"], C["Stone"])),
    ]
    out = []
    for cap, body in items:
        out.append((cap, _svg(W, Hh, f'<rect width="{W}" height="{Hh}" fill="{C["Paper"]}"/>' + body, cap)))
    return out


def growth(ink="currentColor"):
    """How a sixth and seventh mode would join: same square, same cut width, new cut."""
    from geom import mode_tile, to_path
    from shapely.geometry import box
    from shapely.ops import unary_union
    from geom import stroke
    S = H
    k = KCUT
    extra = {
        "▼  e.g. RECOVER": box(0, 0, S, S).difference(unary_union([stroke((0, S), (S / 2, 0), k, ext=60), stroke((S / 2, 0), (S, S), k, ext=60)])),
        "◀  e.g. RESET": box(0, 0, S, S).difference(unary_union([stroke((S, S), (0, S / 2), k, ext=60), stroke((0, S / 2), (S, 0), k, ext=60)])),
        "⊥  e.g. GROUND": box(0, 0, S, S).difference(unary_union([box(S / 2 - k / 2, S / 3, S / 2 + k / 2, S + 1), box(-1, S / 3 - k / 2, S + 1, S / 3 + k / 2)])),
    }
    cells = []
    for name, geom in extra.items():
        cells.append((name, _svg(S, S, f'<path d="{to_path(geom, 0, S)}" fill="{ink}"/>', name)))
    return cells
