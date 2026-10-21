"""Packaging artwork, drawn in millimetres: sachet (front/back), 10-sachet carton (six panels + dieline),
D2C mailer, tumbler wrap. The logo never changes. Each mode is named on the pack, with its own ground and a thin
band in its tint; every pack carries the same hero, the cup (D), drawn big and tone on tone."""
import os
import mark
import brand
from brand import CARBON, PAPER, OAT, ROAST, TONIC, KRAFT, SKUS, MODES, TAGLINE, mix

SVG_NS = 'xmlns="http://www.w3.org/2000/svg"'

# ------------------------------------------------------------------ formats (mm)
SACHET = dict(w=60.0, h=88.0, seal=3.5, bleed=2.0)
CARTON = dict(w=64.0, h=92.0, d=34.0, glue=9.0, tuck=15.0, dust=20.0, bleed=2.0)
MAILER = dict(w=220.0, h=160.0, d=70.0)


def sku(key):
    return next(s for s in SKUS if s["key"] == key)


def f(v):
    return mark.f(v)


# ------------------------------------------------------------------ building blocks
def logo(x, y, w, fill, small=False):
    """The MO/DE stack, top-left at (x, y), w mm wide. Below 15 mm wide the small-size cut is used."""
    g, box = mark.stack(6.0 if (small or w < 15) else None)
    k = w / (box[2] - box[0])
    return (f'<g transform="translate({f(x - box[0] * k)} {f(y - box[1] * k)}) scale({k:.5f})">{mark.paths(g, fill)}</g>',
            (box[3] - box[1]) * k)


def hero(letter, x, y, w, fill, hw=None):
    """One letter of the mark, big. (x, y) is the top-left of the letter's box. hw: hairline weight at that size."""
    g, box = mark.letters(hw)[letter]
    k = w / (box[2] - box[0])
    return f'<g transform="translate({f(x - box[0] * k)} {f(y - box[1] * k)}) scale({k:.5f})">{mark.paths(g, fill)}</g>', (box[3] - box[1]) * k


def text(x, y, s, size, fill, cls="r", anchor="start", ls=0.0, op=1.0):
    a = f' text-anchor="{anchor}"' if anchor != "start" else ""
    l = f' letter-spacing="{f(ls)}"' if ls else ""
    o = f' opacity="{op}"' if op != 1 else ""
    return f'<text x="{f(x)}" y="{f(y)}" font-size="{f(size)}" fill="{fill}" class="{cls}"{a}{l}{o}>{s}</text>'


def lines(x, y, rows, size, fill, lead=1.35, cls="r", op=1.0, anchor="start"):
    return "".join(text(x, y + i * size * lead, r, size, fill, cls, anchor, op=op) for i, r in enumerate(rows))


def rule(x0, x1, y, fill, op=0.35, w=0.2):
    return f'<rect x="{f(x0)}" y="{f(y - w / 2)}" width="{f(x1 - x0)}" height="{f(w)}" fill="{fill}" opacity="{op}"/>'


def barcode(x, y, w, h, digits="5 000000 000000"):
    """A placeholder EAN-13 block on white (bars are illustrative; generate the real code from the GTIN)."""
    import random
    rnd = random.Random(7)
    bars, cx = [], x + 2.2
    mods = [1, 0, 1] + [rnd.choice((0, 1)) for _ in range(42)] + [0, 1, 0, 1, 0] + [rnd.choice((0, 1)) for _ in range(42)] + [1, 0, 1]
    mw = (w - 4.4) / len(mods)
    for i, b in enumerate(mods):
        if b:
            long_ = i < 3 or 45 <= i < 50 or i >= len(mods) - 3
            bars.append(f'<rect x="{f(cx + i * mw)}" y="{f(y + 1.4)}" width="{f(mw)}" height="{f(h - (2.8 if long_ else 5.0))}" fill="#000"/>')
    return (f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" fill="#fff"/>' + "".join(bars)
            + text(x + w / 2, y + h - 1.0, digits, 1.9, "#000", "mono", "middle"))


# ------------------------------------------------------------------ pictograms (8 mm cells, 0.35 mm lines)
def picto(kind, x, y, ink, s=1.0):
    st = f'fill="none" stroke="{ink}" stroke-width="{f(0.38 / s)}" stroke-linecap="round" stroke-linejoin="round"'
    g = f'<g transform="translate({f(x)} {f(y)}) scale({f(s)})">'
    if kind == "fold":     # a sachet with its snap line, the top half bending back
        g += (f'<rect x="1.2" y="1.0" width="5.6" height="8" rx="0.8" {st}/>'
              f'<path d="M1.2 5H6.8" {st} stroke-dasharray="0.6 0.5"/>'
              f'<path d="M7.8 2.2c1.6 0.9 1.6 4.1 0 5" {st}/><path d="M7.2 6.6l0.6 0.7 0.8-0.5" {st}/>')
    elif kind == "squeeze":  # folded into a V, one drop out of the point
        g += (f'<path d="M1.4 1.4L4.5 6.4L7.6 1.4" {st}/><path d="M2.8 1.4L4.5 4.4L6.2 1.4" {st}/>'
              f'<path d="M4.5 7.6c-0.5 0.7-0.75 1.1-0.75 1.45a0.75 0.75 0 0 0 1.5 0c0-0.35-0.25-0.75-0.75-1.45z" fill="{ink}"/>')
    elif kind == "pour":    # the brand's cup, a drop above it
        cup, h = hero("D", 0.9, 3.4, 7.0, ink)
        g += cup + f'<path d="M3.6 0.4c-0.5 0.7-0.75 1.1-0.75 1.45a0.75 0.75 0 0 0 1.5 0c0-0.35-0.25-0.75-0.75-1.45z" fill="{ink}"/>'
    return g + "</g>"


# ------------------------------------------------------------------ SACHET
def _doc(w, h, body, bleed, bg, title):
    b = bleed
    return (f'<svg {SVG_NS} width="{f(w + 2 * b)}mm" height="{f(h + 2 * b)}mm" viewBox="{f(-b)} {f(-b)} {f(w + 2 * b)} {f(h + 2 * b)}">'
            f'<title>{title}</title>{brand.SVG_STYLE}<rect x="{f(-b)}" y="{f(-b)}" width="{f(w + 2 * b)}" height="{f(h + 2 * b)}" fill="{bg}"/>{body}</svg>')


def hero_at(letter, right, bottom, w):
    """Hero placement rule: the cup sits whole in the bottom-right corner, its right edge on `right`."""
    _, box = mark.letters()[letter]
    k = w / (box[2] - box[0])
    return right - w, bottom - (box[3] - box[1]) * k, w


def band(w, h, s, label_left, label_right, bleed):
    """The mode band: the tint across the top, the mode's name in it."""
    return (f'<rect x="{f(-bleed - 1)}" y="{f(-bleed - 1)}" width="{f(w + 2 * bleed + 2)}" height="{f(h + bleed + 1)}" fill="{s["tint"]}"/>'
            + text(6.2, h - 2.15, label_left, 1.9, "#F4F2ED", "monom", ls=0.2)
            + text(w - 6.2, h - 2.15, label_right, 1.9, "#F4F2ED", "mono", "end", ls=0.12))


def sachet_front(key, bleed=None):
    s, S = sku(key), SACHET
    b = S["bleed"] if bleed is None else bleed
    ink = s["ink"]
    x0, y0, w = hero_at("D", S["w"] + 0.6, S["h"] - 5.2, 46.0)
    big, _ = hero("D", x0, y0, w, s["hero"], hw=3.4)
    body = big + band(S["w"], 7.4, s, s["name"].upper() + " MODE", "15 ML", b)
    lg, lh = logo(6.2, 11.6, 17.0, ink)
    body += lg
    body += text(6.0, 37.4, s["name"], 6.4, ink, "h", ls=-0.08)
    body += text(6.2, 41.6, s["line"].upper().rstrip("."), 1.85, ink, "mono", ls=0.14, op=0.85)
    # the snap line: two small notches in the seal, at the crease
    my = S["h"] / 2
    body += (f'<path d="M0 {f(my - 1.1)}L1.7 {f(my)}L0 {f(my + 1.1)}Z" fill="{ink}" opacity=".55"/>'
             f'<path d="M{f(S["w"])} {f(my - 1.1)}L{f(S["w"] - 1.7)} {f(my)}L{f(S["w"])} {f(my + 1.1)}Z" fill="{ink}" opacity=".55"/>')
    return _doc(S["w"], S["h"], body, b, s["ground"], f"MODE {s['name']} sachet, front")


def sachet_back(key, bleed=None):
    s, S = sku(key), SACHET
    b = S["bleed"] if bleed is None else bleed
    ink, W_ = s["ink"], S["w"]
    body = band(W_, 5.6, s, s["name"].upper() + " MODE", s["best"], b)
    lg, lh = logo(6.2, 9.0, 11.0, ink, small=True)
    body += lg
    body += text(W_ - 6.2, 13.2, s["name"], 3.3, ink, "h", "end")
    body += text(W_ - 6.2, 16.5, "COFFEE CONCENTRATE · 15 ML", 1.7, ink, "mono", "end", ls=0.1, op=0.8)
    body += rule(6.2, W_ - 6.2, 22.4, ink)
    for i, (k, cap) in enumerate((("fold", "1 FOLD"), ("squeeze", "2 SQUEEZE"), ("pour", "3 POUR"))):
        cx = 6.2 + i * 16.6
        body += picto(k, cx + 3.2, 24.6, ink)
        body += text(cx + 7.6, 37.6, cap, 1.8, ink, "mono", "middle", ls=0.12)
    body += lines(6.2, 42.8, ["Snap the sachet in half at the line,", "squeeze it into 150 ml of water or", "milk, hot or cold. Stir. Done."], 2.25, ink, lead=1.38)
    body += rule(6.2, W_ - 6.2, 52.4, ink)
    body += lines(6.2, 56.0, ["INGREDIENTS", "Arabica coffee extract", "(water, coffee).", "", "PER SACHET (15 ML)", "ENERGY 4 KCAL", "CAFFEINE " + s["caffeine"]], 1.75, ink, lead=1.55, cls="mono", op=0.9)
    body += barcode(33.6, 54.0, 20.2, 15.6)
    body += f'<rect x="6.2" y="74.6" width="22" height="6.0" fill="none" stroke="{ink}" stroke-width="0.2" opacity=".6"/>'
    body += text(7.2, 77.0, "BEST BEFORE / LOT", 1.5, ink, "mono", ls=0.1, op=0.7)
    body += lines(W_ - 6.2, 75.8, ["Recycle with soft plastics", "where facilities exist."], 1.6, ink, lead=1.45, cls="mono", op=0.75, anchor="end")
    return _doc(S["w"], S["h"], body, b, s["ground"], f"MODE {s['name']} sachet, back")


# ------------------------------------------------------------------ CARTON (10 sachets): six panels
def carton_front(key, bleed=0.0):
    s, C = sku(key), CARTON
    ink = s["ink"]
    x0, y0, w = hero_at("D", C["w"] + 0.6, C["h"] - 5.4, 48.0)
    big, _ = hero("D", x0, y0, w, s["hero"], hw=3.4)
    body = big + band(C["w"], 8.2, s, s["name"].upper() + " MODE", "10 × 15 ML", bleed)
    lg, lh = logo(6.0, 13.0, 21.0, ink)
    body += lg
    body += text(5.8, 44.0, s["name"], 7.6, ink, "h", ls=-0.1)
    body += text(6.0, 48.6, s["line"].upper().rstrip("."), 2.0, ink, "mono", ls=0.14, op=0.85)
    body += text(6.0, 52.0, "COFFEE CONCENTRATE", 2.0, ink, "mono", ls=0.14, op=0.6)
    return _doc(C["w"], C["h"], body, bleed, s["ground"], f"MODE {s['name']} carton, front")


def carton_back(key, bleed=0.0):
    s, C = sku(key), CARTON
    ink = s["ink"]
    body = band(C["w"], 5.6, s, s["name"].upper() + " MODE", s["best"], bleed)
    lg, _ = logo(6.0, 10.5, 13.0, ink, small=True)
    body += lg + text(C["w"] - 6, 15.0, s["name"], 3.4, ink, "h", "end")
    body += lines(6.0, 30.0, ["Five modes."], 4.6, ink, cls="h")
    body += lines(6.0, 36.4, ["One coffee for each state you want to", "be in. Pick the mode, fold, squeeze, pour."], 2.15, ink, lead=1.42, op=0.9)
    for i, m in enumerate(MODES):
        y = 46.0 + i * 5.2
        on = m["key"] == s["key"]
        body += f'<rect x="6" y="{f(y - 2.6)}" width="2.6" height="3.2" fill="{m["tint"]}"/>'
        body += text(10.6, y, m["name"], 2.6, ink, "h" if on else "r", op=1 if on else 0.6)
        body += text(C["w"] - 6, y, m["line"].upper().rstrip("."), 1.55, ink, "monom" if on else "mono", "end", ls=0.06, op=1 if on else 0.55)
    body += rule(6.0, C["w"] - 6, 73.4, ink)
    for i, (k, cap) in enumerate((("fold", "FOLD"), ("squeeze", "SQUEEZE"), ("pour", "POUR"))):
        cx = 6.0 + i * 15.0
        body += picto(k, cx, 76.2, ink, 0.72)
        body += text(cx + 7.6, 80.6, cap, 1.6, ink, "mono", ls=0.08)
    body += text(C["w"] - 6, 87.0, TAGLINE, 2.0, ink, "monom", "end", ls=0.04)
    return _doc(C["w"], C["h"], body, bleed, s["ground"], f"MODE {s['name']} carton, back")


def carton_side_a(key, bleed=0.0):
    """Product side: what the mode is for and how it tastes."""
    s, C = sku(key), CARTON
    ink = s["ink"]
    body = band(C["d"], 5.6, s, s["name"].upper(), "", bleed)
    body += text(4.5, 15.0, s["name"] + " mode", 3.8, ink, "h")
    body += lines(4.5, 19.6, ["COFFEE", "CONCENTRATE"], 1.75, ink, cls="mono", lead=1.45, op=0.85)
    body += rule(4.5, C["d"] - 4.5, 26.0, ink)
    words = s["line"].split(" ")
    rows, cur = [], ""
    for wd in words:
        if len(cur + " " + wd) > 15:
            rows.append(cur.strip())
            cur = wd
        else:
            cur += " " + wd
    rows.append(cur.strip())
    body += lines(4.5, 31.0, rows, 2.5, ink, lead=1.35)
    body += lines(4.5, 44.0, ["BEST AT", s["best"], "", "NOTES"] + s["notes"].replace(" · ", "\n").split("\n"), 1.75, ink, cls="mono", lead=1.55, op=0.85)
    g, h = hero("D", 4.5, C["h"] - 5.0 - 24.0 * 84.0 / 102.0, 24.0, s["hero"], hw=3.4)
    body += g
    return _doc(C["d"], C["h"], body, bleed, s["ground"], f"MODE {s['name']} carton, side A")


def carton_side_b(key, bleed=0.0):
    """Legal side: ingredients, nutrition, barcode, lot."""
    s, C = sku(key), CARTON
    ink = s["ink"]
    body = band(C["d"], 5.6, s, "", "", bleed)
    body += lines(4.5, 12.5, ["INGREDIENTS", "Arabica coffee", "extract (water,", "coffee)."], 1.75, ink, cls="mono", lead=1.55, op=0.9)
    body += rule(4.5, C["d"] - 4.5, 22.0, ink)
    rows = [("PER SACHET", "15 ML"), ("ENERGY", "4 KCAL"), ("FAT", "0 G"), ("CARBS", "0.4 G"), ("SUGARS", "0 G"),
            ("PROTEIN", "0.2 G"), ("CAFFEINE", s["caffeine"])]
    for i, (a_, bb) in enumerate(rows):
        y = 26.0 + i * 3.0
        body += text(4.5, y, a_, 1.7, ink, "monom" if i == 0 else "mono", op=0.9)
        body += text(C["d"] - 4.5, y, bb, 1.7, ink, "monom" if i == 0 else "mono", "end", op=0.9)
    body += rule(4.5, C["d"] - 4.5, 47.4, ink)
    body += lines(4.5, 51.4, ["Store cool and dry.", "Best within 12 months.", "Values are placeholders:", "confirm with lab results."], 1.6, ink, cls="mono", lead=1.5, op=0.75)
    body += barcode(4.5, 60.0, C["d"] - 9.0, 16.0)
    body += f'<rect x="4.5" y="79.0" width="{f(C["d"] - 9.0)}" height="7.0" fill="none" stroke="{ink}" stroke-width="0.2" opacity=".6"/>'
    body += text(5.4, 81.6, "BEST BEFORE / LOT", 1.5, ink, "mono", ls=0.08, op=0.7)
    return _doc(C["d"], C["h"], body, bleed, s["ground"], f"MODE {s['name']} carton, side B")


def carton_top(key, bleed=0.0):
    s, C = sku(key), CARTON
    ink = s["ink"]
    lg, lh = logo(C["w"] / 2 - 8.5, C["d"] / 2 - 8.0, 17.0, ink)
    return _doc(C["w"], C["d"], lg + text(C["w"] - 5, C["d"] - 4.5, s["name"].upper() + " MODE", 1.9, ink, "mono", "end", ls=0.14, op=0.85)
                + f'<rect x="{f(-bleed)}" y="{f(-bleed)}" width="{f(C["w"] + 2 * bleed)}" height="{f(2.2 + bleed)}" fill="{s["tint"]}"/>',
                bleed, s["ground"], f"MODE {s['name']} carton, top")


def carton_bottom(key, bleed=0.0):
    s, C = sku(key), CARTON
    ink = s["ink"]
    g, h = hero("m", 6.0, C["d"] / 2 - 5.0, 10.0, ink)
    body = g + text(19.5, C["d"] / 2 - 0.6, s["name"].upper() + " MODE · 10 × 15 ML", 1.9, ink, "monom", ls=0.12)
    body += text(19.5, C["d"] / 2 + 3.4, "Recyclable board. Flatten before recycling.", 1.7, ink, "mono", op=0.7)
    return _doc(C["w"], C["d"], body, bleed, s["ground"], f"MODE {s['name']} carton, bottom")


def _inner(svg):
    """Strip the outer <svg> of a panel to nest it in the dieline."""
    a = svg.index(">", svg.index("<svg")) + 1
    return svg[a:svg.rindex("</svg>")]


def _poly_d(g):
    rings = [g] if g.geom_type == "Polygon" else list(g.geoms)
    out = ""
    for p in rings:
        for r in [p.exterior] + list(p.interiors):
            pts = list(r.coords)[:-1]
            out += "M" + "L".join(f"{f(x)} {f(y)}" for x, y in pts) + "Z"
    return out


def _tuck(x0, y0, w, h, round_at):
    """Tuck flap: a rectangle with its two outer corners rounded (r 4 mm), inset 0.8 mm at the sides."""
    from shapely.geometry import box as sbox, Point
    r, i = 4.0, 0.8
    if round_at == "top":
        core = sbox(x0 + i, y0 + r, x0 + w - i, y0 + h).union(sbox(x0 + i + r, y0, x0 + w - i - r, y0 + h))
        corners = [Point(x0 + i + r, y0 + r).buffer(r, 32), Point(x0 + w - i - r, y0 + r).buffer(r, 32)]
    else:
        core = sbox(x0 + i, y0, x0 + w - i, y0 + h - r).union(sbox(x0 + i + r, y0, x0 + w - i - r, y0 + h))
        corners = [Point(x0 + i + r, y0 + h - r).buffer(r, 32), Point(x0 + w - i - r, y0 + h - r).buffer(r, 32)]
    from shapely.ops import unary_union
    return unary_union([core] + corners)


def dieline(key, art=True):
    """Reverse tuck-end carton, flat, inside facing down. Left to right: glue flap, back, side B, front, side A.
    Top tuck on the front, bottom tuck on the back, dust flaps on the sides. Cut solid, folds dashed, bleed 2 mm."""
    from shapely.geometry import box as sbox, Polygon
    from shapely.ops import unary_union
    s, C = sku(key), CARTON
    W, H, D, gl, tk, du = C["w"], C["h"], C["d"], C["glue"], C["tuck"], C["dust"]
    xb, xsb, xf, xsa = gl, gl + W, gl + W + D, gl + 2 * W + D
    tw_ = xsa + D
    y0 = tk + D                      # top of the body
    y1 = y0 + H                      # bottom of the body
    th_ = y1 + D + tk

    def dust(x, top):
        if top:
            return Polygon([(x + 0.4, y0), (x + 2.5, y0 - du), (x + D - 7, y0 - du), (x + D - 0.4, y0 - 3), (x + D - 0.4, y0)])
        return Polygon([(x + 0.4, y1), (x + 0.4 + 6.6, y1 + du), (x + D - 2.5, y1 + du), (x + D - 0.4, y1)]).union(
            Polygon([(x + 0.4, y1), (x + D - 0.4, y1), (x + D - 0.4, y1 + 3), (x + 0.4, y1 + 3)]))

    pieces = [Polygon([(xb, y0), (0, y0 + 6), (0, y1 - 6), (xb, y1)]),               # glue flap
              sbox(xb, y0, tw_, y1),                                               # body
              sbox(xf, tk, xf + W, y0), _tuck(xf, 0, W, tk + 0.01, "top"),         # top panel + tuck (front)
              sbox(xb, y1, xb + W, y1 + D), _tuck(xb, y1 + D - 0.01, W, tk + 0.01, "bottom"),   # bottom + tuck (back)
              dust(xsb, True), dust(xsa, True), dust(xsb, False), dust(xsa, False)]
    outline = unary_union(pieces).buffer(0)
    cut_d = _poly_d(outline)
    bleed_d = _poly_d(outline.buffer(C["bleed"], join_style="mitre"))
    pad = 12.0
    body = ""
    if art:
        g = s["ground"]
        art_ = f'<rect x="-4" y="-4" width="{f(tw_ + 8)}" height="{f(th_ + 8)}" fill="{g}"/>'
        for x, w, fn in ((xb, W, carton_back), (xsb, D, carton_side_b), (xf, W, carton_front), (xsa, D, carton_side_a)):
            art_ += f'<svg x="{f(x)}" y="{f(y0)}" width="{f(w)}" height="{f(H)}" viewBox="0 0 {f(w)} {f(H)}">{_inner(fn(key))}</svg>'
        art_ += f'<svg x="{f(xf)}" y="{f(tk)}" width="{f(W)}" height="{f(D)}" viewBox="0 0 {f(W)} {f(D)}">{_inner(carton_top(key))}</svg>'
        art_ += (f'<g transform="rotate(180 {f(xb + W / 2)} {f(y1 + D / 2)})"><svg x="{f(xb)}" y="{f(y1)}" width="{f(W)}" height="{f(D)}" '
                 f'viewBox="0 0 {f(W)} {f(D)}">{_inner(carton_bottom(key))}</svg></g>')
        body = f'<defs><clipPath id="bleed{key}"><path d="{bleed_d}"/></clipPath></defs><g clip-path="url(#bleed{key})">{art_}</g>'
    cut = 'fill="none" stroke="#E4007C" stroke-width="0.3"'
    fold = 'fill="none" stroke="#00A0E4" stroke-width="0.3" stroke-dasharray="2 1.2"'
    lines_ = f'<path d="{cut_d}" {cut}/>'
    folds = [(xb, y0, xb, y1), (xsb, y0, xsb, y1), (xf, y0, xf, y1), (xsa, y0, xsa, y1),
             (xf, y0, xf + W, y0), (xf, tk, xf + W, tk), (xsb, y0, xsb + D, y0), (xsa, y0, xsa + D, y0),
             (xb, y1, xb + W, y1), (xb, y1 + D, xb + W, y1 + D), (xsb, y1, xsb + D, y1), (xsa, y1, xsa + D, y1)]
    lines_ += "".join(f'<path d="M{f(a)} {f(b)}L{f(c)} {f(d)}" {fold}/>' for a, b, c, d in folds)
    ly = th_ + 9
    legend = (text(0, ly, f"MODE {s['name']} · 10-sachet carton · reverse tuck end · {f(W)} × {f(H)} × {f(D)} mm · art shown from outside", 3.0, CARBON, "md")
              + f'<path d="M0 {f(ly + 5)}h8" {cut}/>' + text(10, ly + 6, "cut", 2.6, CARBON, "mono")
              + f'<path d="M26 {f(ly + 5)}h8" {fold}/>' + text(36, ly + 6, "fold", 2.6, CARBON, "mono")
              + text(56, ly + 6, "bleed 2 mm outside the cut · keep text 3 mm inside folds · board 350 gsm GC1", 2.6, CARBON, "mono"))
    tw, th = tw_ + 2 * pad, th_ + 2 * pad + 18
    return (f'<svg {SVG_NS} width="{f(tw)}mm" height="{f(th)}mm" viewBox="{f(-pad)} {f(-pad)} {f(tw)} {f(th)}">'
            f'<title>MODE {s["name"]} carton dieline</title>{brand.SVG_STYLE}<rect x="{f(-pad)}" y="{f(-pad)}" width="{f(tw)}" height="{f(th)}" fill="#fff"/>'
            f'{body}{lines_}{legend}</svg>'), (tw, th)


# ------------------------------------------------------------------ MAILER (D2C box, kraft, one-colour flexo)
def mailer_top():
    M = MAILER
    lg, lh = logo(M["w"] / 2 - 32, M["h"] / 2 - 32 * 212 / 224 - 4, 64.0, CARBON)
    body = lg + text(M["w"] / 2, M["h"] - 16, "COFFEE CONCENTRATE · " + TAGLINE.upper(), 3.2, CARBON, "mono", "middle", ls=0.5, op=0.85)
    return _doc(M["w"], M["h"], body, 0, KRAFT, "MODE mailer, lid")


def mailer_inside():
    """Inside of the lid, seen on opening: Roast flood, the four letters, one line, the five modes, the tagline."""
    M = MAILER
    body = ""
    for i, l in enumerate("moDe"):
        g, h = hero(l, 18 + i * 48.5, 24 if l != "D" else 30, 40.0 if l != "D" else 46.0, mix(ROAST, PAPER, 0.18), hw=3.0)
        body += g
    body += text(M["w"] / 2, 92, "Every letter of MODE is a coffee.", 7.2, PAPER, "h", "middle", ls=-0.1)
    for i, m in enumerate(MODES):
        x = 30 + i * 40.0
        body += f'<rect x="{f(x - 13)}" y="108" width="26" height="1.6" fill="{m["tint"]}"/>' + text(x, 117, m["name"].upper(), 3.2, PAPER, "mono", "middle", ls=0.4)
    body += text(M["w"] / 2, 138, TAGLINE, 4.0, PAPER, "monom", "middle", ls=0.1, op=0.85)
    return _doc(M["w"], M["h"], body, 0, ROAST, "MODE mailer, inside lid")


def tumbler_wrap():
    """Flat wrap for a 75 mm tumbler (circumference ~236 mm × 150 mm). The mark sits at the centre front."""
    w, h = 236.0, 150.0
    lg, lh = logo(w / 2 - 15, h / 2 - 16, 30.0, PAPER)
    body = lg + text(w / 2, h - 18, "MODE", 3.4, PAPER, "mono", "middle", ls=1.2, op=0.6)
    return _doc(w, h, body, 0, CARBON, "MODE tumbler wrap")
