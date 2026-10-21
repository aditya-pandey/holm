"""The MODE brand guidelines: one HTML source → interactive page (guidelines/mode-brand-guidelines.html) and a
16:9 print PDF. Every diagram is generated from the master geometry in mark.py."""
import html
import os
import shutil
from PIL import Image
import mark
import brand
import pack
from brand import ROOT, PALETTE, MODES, TAGLINE, CARBON, PAPER, OAT, ROAST, TONIC, GRAPHITE, STONE, SILVER, KRAFT

G = os.path.join(ROOT, "guidelines")
A = os.path.join(G, "assets")
esc = html.escape
VERSION = "Version 1.0 · October 2026"


# ------------------------------------------------------------------ assets: compressed copies for the page
def asset(src_rel, name, w=None, q=84):
    os.makedirs(A, exist_ok=True)
    im = Image.open(os.path.join(ROOT, src_rel))
    if w and im.width > w:
        im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
    if im.mode in ("RGBA", "LA"):
        bg = Image.new("RGB", im.size, (244, 242, 237))
        bg.paste(im, mask=im.split()[-1])
        im = bg
    im.convert("RGB").save(os.path.join(A, name), "JPEG", quality=q, optimize=True, progressive=True)
    return f"assets/{name}"


# ------------------------------------------------------------------ SVG helpers
def vb(box, pad=0):
    return f"{mark.f(box[0] - pad)} {mark.f(box[1] - pad)} {mark.f(box[2] - box[0] + 2 * pad)} {mark.f(box[3] - box[1] + 2 * pad)}"


def logo(fill=CARBON, cls="lg", w=None, pad=0, extra=""):
    g, box = mark.stack(w)
    return f'<svg class="{cls}" viewBox="{vb(box, pad)}" role="img" aria-label="MODE">{mark.paths(g, fill)}{extra}</svg>'


def letter(l, fill=CARBON, cls="lt"):
    g, box = mark.letters()[l]
    return f'<svg class="{cls}" viewBox="{vb(box, 2)}" aria-hidden="true">{mark.paths(g, fill)}</svg>'


def construction():
    """The stack with its grid: radius, cut, hairline, gaps, legs."""
    g, box = mark.stack()
    col, row = 112.0, 112.0
    t = TONIC
    dash = f'fill="none" stroke="{t}" stroke-width=".7" stroke-dasharray="3 2.4"'
    ln = f'stroke="{t}" stroke-width=".6"'
    lab = lambda x, y, s, a="middle": f'<text x="{x}" y="{y}" font-size="6.2" fill="{t}" text-anchor="{a}" class="mono">{s}</text>'
    o = [f'<path fill="{CARBON}" opacity=".9" d="{g["solid"]}"/><path fill="{CARBON}" d="{g["hair"]}"/>']
    o.append(f'<circle cx="{col + 50}" cy="50" r="50" {dash}/><circle cx="{col + 50}" cy="{row + 50}" r="50" {dash}/>')
    for x in (0, 100, col, col + 103):
        o.append(f'<path d="M{x} -18V{row + 118}" {ln} opacity=".45"/>')
    for y in (0, 50, 100, row, row + 100):
        o.append(f'<path d="M-30 {y}H{col + 130}" {ln} opacity=".45"/>')
    o.append(f'<path d="M{col + 50} 50L{col + 50 + 35.36} {50 - 35.36}" {ln}/>' + lab(col + 92, 10, "R 50", "start"))
    o.append(lab(106, -22, "gap 12") + lab(-34, 111, "gap 12", "end"))
    o.append(lab(10, -8, "leg 20") + f'<path d="M0 -4H20" {ln}/>')
    o.append(lab(-34, 52, "half", "end") + lab(-34, 4, "0", "end") + lab(-34, 98, "100", "end") + lab(-34, row + 102, "212", "end"))
    o.append(lab(col + 51.5, -8, "cut 3") + lab(col + 52, row + 122, "hairline 2.2"))
    return f'<svg class="dia" viewBox="-80 -36 340 300" role="img" aria-label="Construction of the MODE mark">{"".join(o)}</svg>'


def clearspace():
    g, box = mark.stack()
    p = 2 * mark.LEG
    x0, y0, x1, y1 = box[0] - p, box[1] - p, box[2] + p, box[3] + p
    t = TONIC
    legs = ""
    for (x, y) in ((box[0] - p, box[1] - p), (box[2], box[1] - p), (box[0] - p, box[3]), (box[2], box[3])):
        legs += f'<rect x="{x}" y="{y}" width="{p}" height="{p}" fill="{t}" opacity=".14"/>'
    return (f'<svg class="dia" viewBox="{x0 - 10} {y0 - 10} {x1 - x0 + 20} {y1 - y0 + 20}" role="img" aria-label="Clear space">'
            f'<rect x="{x0}" y="{y0}" width="{x1 - x0}" height="{y1 - y0}" fill="none" stroke="{t}" stroke-width=".8" stroke-dasharray="4 3"/>{legs}'
            f'{mark.paths(g, CARBON)}<text x="{x0 + p / 2}" y="{y0 + p / 2 + 2}" font-size="8" text-anchor="middle" fill="{t}" class="mono">40</text></svg>')


def misuse_tiles():
    tiles = []
    g, box = mark.stack()
    # 1 in a line
    parts, x = [], 0
    for fn in (mark.m, mark.o, mark.D, mark.e):
        gg, w = fn(x, 0)
        parts.append(mark.paths(gg, CARBON))
        x += w + 12
    tiles.append((f'<svg viewBox="-12 -10 {x + 12} 120">{"".join(parts)}</svg>', "Don't set the letters in a line. MODE is always MO over DE."))
    # 2 rearranged
    a, _ = mark.D(0, 0); b, _ = mark.e(112, 0); c, _ = mark.m(0, 112); d, _ = mark.o(112, 112)
    tiles.append((f'<svg viewBox="{vb(box, 12)}">{"".join(mark.paths(p, CARBON) for p in (a, b, c, d))}</svg>', "Don't rearrange or swap the letters."))
    # 3 closed e
    gg, _ = mark.stack()
    closed = mark.hairline_arc(112 + 53, 112 + 50, 16, 90, mark.W)
    tiles.append((f'<svg viewBox="{vb(box, 12)}">{mark.paths(gg, CARBON)}<path fill="{CARBON}" d="{closed}"/></svg>', "Don't close the e. A closed bowl reads as a second O."))
    # 4 recoloured
    cols = [TONIC, ROAST, STONE, "#B4532A"]
    a, _ = mark.m(0, 0); b, _ = mark.o(112, 0); c, _ = mark.D(0, 112); d, _ = mark.e(112, 112)
    tiles.append((f'<svg viewBox="{vb(box, 12)}">{"".join(mark.paths(p, k) for p, k in zip((a, b, c, d), cols))}</svg>', "Don't colour letters separately. The mark is always one colour."))
    # 5 stretched
    tiles.append((f'<svg viewBox="{vb(box, 12)}" preserveAspectRatio="none" style="aspect-ratio:1.55">{mark.paths(g, CARBON)}</svg>', "Don't stretch, squash or skew it."))
    # 6 outlined
    tiles.append((f'<svg viewBox="{vb(box, 12)}"><path d="{g["solid"]}" fill="none" stroke="{CARBON}" stroke-width="2"/><path d="{g["hair"]}" fill="none" stroke="{CARBON}" stroke-width="1"/></svg>', "Don't outline it."))
    # 7 effects
    tiles.append((f'<svg viewBox="{vb(box, 16)}"><defs><filter id="sh" x="-20%" y="-20%" width="140%" height="140%"><feDropShadow dx="5" dy="7" stdDeviation="3" flood-opacity=".45"/></filter></defs><g filter="url(#sh)">{mark.paths(g, CARBON)}</g></svg>', "Don't add shadows, glows, bevels or gradients."))
    # 8 low contrast
    tiles.append((f'<svg viewBox="{vb(box, 12)}" style="background:{OAT}">{mark.paths(g, "#BDB3A3")}</svg>', "Don't place it on low contrast. Use Carbon or Paper only."))
    return "".join(f'<figure class="mis"><div class="mis-art">{s}<span class="x" aria-hidden="true"></span></div><figcaption>{esc(t)}</figcaption></figure>' for s, t in tiles)


def swatches():
    out = ""
    for role, name, hx, pms, cmyk, use in PALETTE:
        r, g_, b = brand.hex_rgb(hx)
        ink = CARBON if brand.luminance(hx) > 0.35 else PAPER
        out += (f'<figure class="sw"><div class="chip" style="background:{hx};color:{ink}"><b>{name}</b><span class="mono">{role}</span></div>'
                f'<dl class="mono"><dt>HEX</dt><dd>{hx}</dd><dt>RGB</dt><dd>{r} {g_} {b}</dd><dt>CMYK</dt><dd>{" ".join(str(c) for c in cmyk)}</dd>'
                f'<dt>PMS</dt><dd>{esc(pms)}</dd></dl><figcaption>{esc(use)}</figcaption></figure>')
    return out


def tints():
    out = '<p class="mono tl">Mode tints · bands only</p>'
    for m in MODES:
        r, g_, b = brand.hex_rgb(m["tint"])
        c = brand.contrast("#F4F2ED", m["tint"])
        out += (f'<figure class="tint"><span style="background:{m["tint"]}">{m["name"].upper()}</span>'
                f'<figcaption class="mono">{m["tint"]} · {r} {g_} {b} · CMYK {" ".join(str(v) for v in m["cmyk"])} · PMS {esc(m["pms"])} · Paper text {c:.1f}:1</figcaption></figure>')
    return out


def contrast_rows():
    pairs = [("Carbon", "Paper"), ("Carbon", "Oat"), ("Paper", "Roast"), ("Paper", "Graphite"), ("Paper", "Carbon"),
             ("Tonic", "Paper"), ("White", "Tonic"), ("Graphite", "Paper"), ("Stone", "Paper")]
    H = brand.HEX
    rows = ""
    for fg, bg in pairs:
        c = brand.contrast(H[fg], H[bg])
        verdict = "AAA" if c >= 7 else "AA" if c >= 4.5 else "AA large" if c >= 3 else "Fail"
        rows += (f'<tr><td><span class="pair" style="background:{H[bg]};color:{H[fg]}">Aa</span></td><td>{fg} on {bg}</td>'
                 f'<td class="num">{c:.1f} : 1</td><td><span class="v v-{verdict.split()[0].lower()}">{verdict}</span></td></tr>')
    return rows


# ------------------------------------------------------------------ the document
def build():
    if os.path.isdir(A):
        shutil.rmtree(A)
    img = {}
    for n in ("sachets", "frontback", "carton", "range", "mailer-open", "mailer-closed", "tumbler"):
        img[n] = asset(f"packaging/renders/mode-{n}.png", f"render-{n}.jpg", 1800)
    for s in MODES:
        img[f"f-{s['key']}"] = asset(f"packaging/sachet/mode-sachet-{s['key']}-front.png", f"sachet-{s['key']}-front.jpg", 560, 88)
        img[f"b-{s['key']}"] = asset(f"packaging/sachet/mode-sachet-{s['key']}-back.png", f"sachet-{s['key']}-back.jpg", 560, 88)
    img["die"] = asset("packaging/carton/mode-carton-wake-dieline.png", "carton-dieline.jpg", 1600, 86)
    for n in ("instagram-post-logo", "instagram-post-modes", "instagram-post-sachets", "instagram-story", "ecommerce-tile-wake", "website-hero", "website-header"):
        img[n] = asset(f"digital/mode-{n}.png", f"{n}.jpg", 1400)
    img["lid"] = asset("packaging/mailer/mode-mailer-lid.png", "mailer-lid.jpg", 1000)
    img["inside"] = asset("packaging/mailer/mode-mailer-inside-lid.png", "mailer-inside.jpg", 1000)
    img["app"] = asset("icon/png/mode-app-icon-rounded-512.png", "app-icon.jpg", 512, 90)
    img["profile"] = asset("icon/png/mode-profile-1080.png", "profile.jpg", 600, 88)

    favs = "".join(f'<figure class="fav"><img src="data:image/png;base64,{_b64(f"icon/png/favicon-{px}.png")}" width="{px}" height="{px}" alt="Favicon {px} px"><figcaption class="mono">{px} px</figcaption></figure>' for px in (16, 32, 48))

    pages = []
    P = lambda cls, inner, label: pages.append(f'<section class="pg {cls}" aria-label="{esc(label)}"><div class="in">{inner}</div></section>')

    # 1 cover
    P("cover", f'<div class="cover-mark">{logo(CARBON, "lg")}</div><div class="cover-txt"><p class="mono eyebrow">Brand guidelines</p>'
               f'<h1>MODE</h1><p class="lede">Coffee concentrate, in single-serve sachets. The mark, the colours, the type, and how all of it goes onto a sachet, a carton and a screen.</p>'
               f'<p class="mono small">{VERSION}</p></div>', "Cover")
    # 2 contents
    toc = [("The idea", "idea"), ("The mark", "mark"), ("Construction", "construction"), ("The four letters", "letters"), ("Clear space and size", "space"),
           ("Small sizes", "small"), ("Colour versions", "versions"), ("Misuse", "misuse"), ("Colour", "colour"), ("Contrast", "contrast"),
           ("Typography", "type"), ("The modes", "range"), ("Sachet", "sachet"), ("Sachet in use", "sachet-renders"), ("Carton", "carton"),
           ("Carton dieline", "dieline"), ("Mailer", "mailer"), ("Tumbler", "tumbler"), ("Social", "social"), ("Web", "web"), ("Files", "files")]
    P("contents", '<p class="mono eyebrow">Contents</p><ol class="toc">' + "".join(f'<li><a href="#{a}">{esc(t)}</a></li>' for t, a in toc) + "</ol>", "Contents")
    # 3 idea
    P("idea", '<a id="idea"></a><div class="split"><div><p class="mono eyebrow">The idea</p><h2>Every letter of MODE is a coffee.</h2>'
              '<div class="prose"><p>The mark borrows its grammar from Albert Hollenstein\'s L\'Echoppe monogram: a square, a half-disc and a quarter-disc, all cut from one radius, separated by a thin cut, and finished by hairlines of the same radius. Nothing else is allowed in.</p>'
              '<p>With that kit, each letter of MODE becomes a coffee and still reads as its letter. The m is a square of coffee that drips. The o is half poured, from the side. The D is a cup on its saucer. The e is Hollenstein\'s own e, left open: the one letter that isn\'t a drink.</p>'
              '<p>Stacked MO over DE, the four make a compact block that sits in a corner of a sachet the way a seal sits on a letter. The mark never changes: the five modes (Wake, Active, Zen, Vital, Calm) are named on the pack, never drawn into the letters.</p></div></div>'
              f'<div class="idea-art">{logo(CARBON, "lg")}</div></div>', "The idea")
    # 4 the mark
    P("mark-pg", f'<a id="mark"></a><p class="mono eyebrow">The mark</p><div class="duo"><figure class="plate" style="background:{PAPER}">{logo(CARBON, "lg")}<figcaption class="mono">Primary · Carbon on Paper</figcaption></figure>'
                 f'<figure class="plate" style="background:{CARBON}">{logo(PAPER, "lg")}<figcaption class="mono" style="color:{PAPER}">Reversed · Paper on Carbon</figcaption></figure></div>'
                 '<p class="note">One mark, no separate wordmark. The stack is the logo. It reads in two rows, MO then DE, and is always used whole.</p>', "The mark")
    # 5 construction
    P("cons", '<a id="construction"></a><div class="split"><div><p class="mono eyebrow">Construction</p><h2>One radius, one cut, one hairline.</h2>'
              '<div class="prose"><p>Each letter is 100 units tall. Everything else follows from that.</p></div>'
              '<table class="spec"><tbody>'
              '<tr><th>Radius</th><td>50: half a letter. Every curve in the mark uses it, except the cup\'s belly (60) and handle (17).</td></tr>'
              '<tr><th>Cut</th><td>3 between solids that meet: the o\'s halves, the e\'s half-disc and quarter.</td></tr>'
              '<tr><th>Hairline</th><td>2.2 with round ends; 6 in the small-size cut.</td></tr>'
              '<tr><th>Gaps</th><td>12 between the columns and between the rows.</td></tr>'
              '<tr><th>Legs</th><td>20 wide, ending in half-disc drops. The m\'s arches stop exactly halfway.</td></tr>'
              '<tr><th>Overall</th><td>224 × 212. The saucer overhangs the left edge by 9 on purpose; align to the m, not the saucer.</td></tr>'
              f'</tbody></table></div><div class="dia-wrap">{construction()}</div></div>', "Construction")
    # 6 letters
    rows = [("m", "A square of coffee that drips", "Two arches are bitten up to the halfway line. The three legs end in drops."),
            ("o", "Half poured, from the side", "The right half is solid. The left half is a hairline, so the o reads as a glass half full."),
            ("D", "A cup on its saucer", "The straight back is the stem, the round belly is the bowl. The handle sits small and high; the saucer is a hairline."),
            ("e", "Hollenstein's e, left open", "A half-disc and a quarter, with only the start of the hairline. The bowl stays open, so it can never close into a second o.")]
    cells = "".join(f'<figure class="let"><div class="let-art">{letter(l)}</div><figcaption><b>{esc(t)}</b><span>{esc(s)}</span></figcaption></figure>' for l, t, s in rows)
    P("letters-pg", f'<a id="letters"></a><p class="mono eyebrow">The four letters</p><h2>Each still reads as its letter.</h2><div class="quad">{cells}</div>', "The four letters")
    # 7 clear space & min size
    g_small, box_small = mark.stack(6.0)
    P("space-pg", '<a id="space"></a><div class="split"><div><p class="mono eyebrow">Clear space and size</p><h2>Two drips of air on every side.</h2>'
                  '<div class="prose"><p>Keep a clear space of 40 units around the mark: twice the width of one of the m\'s legs. Nothing else (type, edges, folds, other marks) goes inside it. The files ending in <code>-clearspace</code> include it.</p></div>'
                  '<table class="spec"><tbody><tr><th>Print</th><td>12 mm wide minimum. Under 15 mm, use the small-size cut.</td></tr>'
                  '<tr><th>Screen</th><td>40 px wide minimum for the full mark; 32 px and below, the small-size cut.</td></tr>'
                  '<tr><th>Tiny</th><td>Below 24 px, use the monogram (the m alone).</td></tr></tbody></table></div>'
                  f'<div class="dia-wrap">{clearspace()}</div></div>', "Clear space and size")
    # 8 small sizes
    ladder = "".join(f'<figure><div style="height:{px}px">{logo(CARBON, "lad", 6.0 if px <= 32 else None)}</div><figcaption class="mono">{px} px</figcaption></figure>' for px in (24, 32, 48, 72, 120))
    P("small-pg", '<a id="small"></a><p class="mono eyebrow">Small sizes</p><h2>Heavier hairlines when it gets small.</h2>'
                  f'<div class="ladder">{ladder}</div>'
                  f'<div class="smallrow"><figure class="cell"><div class="mono-art">{letter("m")}</div><figcaption><b>Monogram</b><span>The m alone: the top-left block of the mark. For favicons, embossing and anything under 24 px.</span></figcaption></figure>'
                  f'<figure class="cell"><div class="favs">{favs}</div><figcaption><b>Favicon</b><span>16 px uses the monogram; 32 and 48 px use the small-size cut.</span></figcaption></figure>'
                  f'<figure class="cell"><img src="{img["app"]}" alt="App icon" class="app"><figcaption><b>App icon</b><span>Paper on Carbon, full bleed. The platform applies its own corner mask.</span></figcaption></figure></div>', "Small sizes")
    # 9 versions
    vers = [(PAPER, CARBON, "Carbon on Paper"), (OAT, CARBON, "Carbon on Oat"), (CARBON, PAPER, "Paper on Carbon"), (ROAST, PAPER, "Paper on Roast"),
            (GRAPHITE, PAPER, "Paper on Graphite"), (KRAFT, CARBON, "Carbon on kraft, one colour"), (CARBON, SILVER, "Silver foil on Carbon"), ("#FFFFFF", "#000000", "Black, one colour")]
    P("vers", '<a id="versions"></a><p class="mono eyebrow">Colour versions</p><h2>One colour at a time.</h2><div class="vgrid">'
              + "".join(f'<figure style="background:{bg}">{logo(fg, "lg")}<figcaption class="mono" style="color:{fg}">{esc(t)}</figcaption></figure>' for bg, fg, t in vers)
              + "</div>", "Colour versions")
    # 10 misuse
    P("mis-pg", f'<a id="misuse"></a><p class="mono eyebrow">Misuse</p><h2>Please don\'t.</h2><div class="misgrid">{misuse_tiles()}</div>', "Misuse")
    # 11 colour
    P("col", '<a id="colour"></a><p class="mono eyebrow">Colour</p><h2>Neutrals do the work. Tonic is the one accent.</h2>'
             f'<div class="swgrid">{swatches()}</div><div class="tints">{tints()}</div>'
             '<div class="ratio" aria-label="Colour proportions"><span style="flex:46;background:#F4F2ED">Grounds 45%</span><span style="flex:22;background:#E6DCCB">Warm 20%</span>'
             '<span style="flex:20;background:#4B3D2F;color:#F4F2ED">Roast 20%</span><span style="flex:10;background:#151515;color:#F4F2ED">Core 10%</span><span style="flex:4;background:#0E6B5E;color:#fff">≤5%</span></div>'
             '<p class="note">Pantone and CMYK are starting values. Proof every colour on the real stock before print. Silver is a foil on pack and a flat grey on screen.</p>', "Colour")
    # 12 contrast
    P("con", '<a id="contrast"></a><div class="split"><div><p class="mono eyebrow">Contrast</p><h2>Readable first.</h2>'
             '<div class="prose"><p>Body text on screen needs 4.5 : 1 (WCAG AA). Large type and the mark need 3 : 1. Stone is for captions and rules on Paper only, never for body text.</p></div></div>'
             f'<div class="tbl"><table class="ctab"><thead><tr><th></th><th>Pair</th><th>Ratio</th><th>WCAG</th></tr></thead><tbody>{contrast_rows()}</tbody></table></div></div>', "Contrast")
    # 13 type
    P("typ", '<a id="type"></a><p class="mono eyebrow">Typography</p><div class="split"><div>'
             '<p class="spec-a">Instrument Sans</p><p class="spec-b">Aa Bb Cc 0123</p><p class="small">Primary. Headlines, product names, body copy. Regular 400, Medium 500, SemiBold 600. Free (SIL Open Font License) on Google Fonts.</p>'
             '<p class="spec-a mono-face">IBM Plex Mono</p><p class="spec-b mono-face">Aa Bb 0123</p><p class="small">Secondary. Labels, data, ingredients and the small print on pack, always in capitals with open tracking. Free (SIL OFL).</p></div>'
             '<div class="tbl"><table class="spec hier"><thead><tr><th>Style</th><th>Screen</th><th>Print</th><th>Set as</th></tr></thead><tbody>'
             '<tr><td class="h-d">Display</td><td>64–104 / 1.0</td><td>24–36 pt</td><td>SemiBold, −2% tracking</td></tr>'
             '<tr><td class="h-1">Headline</td><td>40 / 1.05</td><td>16–20 pt</td><td>SemiBold, −1%</td></tr>'
             '<tr><td class="h-2">Subhead</td><td>24 / 1.25</td><td>11 pt</td><td>Medium</td></tr>'
             '<tr><td>Body</td><td>17 / 1.55</td><td>7.5–9 pt</td><td>Regular</td></tr>'
             '<tr><td class="mono h-l">LABEL</td><td>12–14, +14%</td><td>5–6 pt, +16%</td><td>Plex Mono, capitals</td></tr>'
             '<tr><td>Caption</td><td>13 / 1.4</td><td>6 pt</td><td>Regular, Graphite</td></tr>'
             '</tbody></table><p class="note">On a sachet, mandatory text keeps an x-height of at least 0.9 mm (Plex Mono at 5 pt). Check the labelling rules where you sell.</p></div></div>', "Typography")
    # 14 modes
    flats5 = "".join(f'<img src="{img["f-" + m["key"]]}" alt="{m["name"]} mode sachet">' for m in MODES)
    rows = ""
    for m in MODES:
        r, g_, b_ = brand.hex_rgb(m["tint"])
        rows += (f'<tr><td><span class="mchip" style="background:{m["ground"]};border-top:6px solid {m["tint"]}"></span></td>'
                 f'<td><b>{m["name"]}</b></td><td>{esc(m["line"])}</td><td class="mono">{esc(m["best"])}</td>'
                 f'<td class="num">{m["tint"]} · PMS {esc(m["pms"])}</td></tr>')
    P("rng", '<a id="range"></a><div class="split wide-r"><div><p class="mono eyebrow">The modes</p><h2>One mark. Five modes, named.</h2>'
             '<div class="prose"><p>The range is the modes. The mark is the same on every pack; the mode is named, never drawn into the letters.</p>'
             '<p>Each mode has four cues: its name, set large; a line that says what it\'s for; a ground from the palette; and a thin band in its tint across the top, with the name in it. The band is the only place a mode tint appears, so the tints stay well under a tenth of any pack.</p>'
             '<p>Names are always printed, so modes stay apart in one-colour print and for colour-blind customers. A sixth mode needs only a name, a line and a tint.</p>'
             f'<p><b>{TAGLINE}</b> is the sign-off: written as one word, used on the carton back, the mailer and social.</p>'
             '<p class="small">Lines, notes and caffeine values are placeholders for the brand team to confirm.</p></div></div>'
             f'<div class="tbl"><table class="spec modes"><thead><tr><th></th><th>Mode</th><th>For</th><th>Best at</th><th>Tint</th></tr></thead><tbody>{rows}</tbody></table>'
             f'<div class="flats5">{flats5}</div></div></div>', "The modes")
    # 15 sachet flats
    flats = "".join(f'<figure><img src="{img["f-" + s["key"]]}" alt="{s["name"]} mode sachet front"><figcaption class="mono">{s["name"]}</figcaption></figure>' for s in MODES)
    P("sach", '<a id="sachet"></a><p class="mono eyebrow">Sachet</p><div class="split wide-r"><div><h2>60 × 88 mm, a snap line across the middle.</h2>'
              '<table class="spec"><tbody><tr><th>Format</th><td>60 × 88 mm finished, heat seal 3.5 mm on all sides, bleed 2 mm</td></tr>'
              '<tr><th>Front</th><td>Mode band in its tint · mark 17 mm wide · mode name · its line · the cup, tone on tone</td></tr>'
              '<tr><th>Back</th><td>How to (fold, squeeze, pour) · ingredients · per-sachet values · barcode on white · lot and best-before box</td></tr>'
              '<tr><th>Stock</th><td>Matte laminate film, reverse printed. Snap line marked by two notches in the seal.</td></tr>'
              f'<tr><th>Files</th><td><code>packaging/sachet/</code> SVG, PDF with bleed, PNG</td></tr></tbody></table>'
              f'<figure class="back"><img src="{img["b-zen"]}" alt="Zen mode sachet back"><figcaption class="mono">Zen · back</figcaption></figure></div>'
              f'<div class="flats">{flats}</div></div>', "Sachet")
    # 16 sachet renders
    P("full sach-r", f'<a id="sachet-renders"></a><figure class="hero-img"><img src="{img["sachets"]}" alt="The five mode sachets on a table"></figure>'
                     f'<div class="caprow"><p class="mono eyebrow">Sachet in use</p><figure class="mini"><img src="{img["frontback"]}" alt="Wake sachet, front and back"></figure></div>', "Sachet in use")
    # 17 carton
    P("cart", '<a id="carton"></a><div class="split wide-r"><div><p class="mono eyebrow">Carton</p><h2>Ten sachets, the same system.</h2>'
              '<table class="spec"><tbody><tr><th>Format</th><td>64 × 92 × 34 mm, reverse tuck end, 350 gsm GC1 board, matte varnish</td></tr>'
              '<tr><th>Front</th><td>Mode band · mark 21 mm · mode name · line · the cup, tone on tone</td></tr>'
              '<tr><th>Back</th><td>"Five modes." · all five listed, this one highlighted · how to · #SwitchYourMode</td></tr>'
              '<tr><th>Sides</th><td>A: what the mode is for, best time, notes · B: ingredients, nutrition, barcode, lot</td></tr>'
              '<tr><th>Top</th><td>Mark centred: the face you see on a shelf from above</td></tr></tbody></table></div>'
              f'<figure class="hero-img"><img src="{img["carton"]}" alt="Wake and Calm cartons with sachets"></figure></div>'
              f'<figure class="hero-img strip"><img src="{img["range"]}" alt="The five mode cartons in a row"></figure>', "Carton")
    # 18 dieline
    P("die", f'<a id="dieline"></a><p class="mono eyebrow">Carton dieline</p><figure class="die-img"><img src="{img["die"]}" alt="Wake carton dieline with artwork"></figure>'
             '<p class="note">Magenta is the cut, cyan dashed the folds. Bleed 2 mm; keep text 3 mm inside every fold. Confirm the die with the converter before artwork goes final; a blank die is in <code>packaging/carton/</code>.</p>', "Carton dieline")
    # 19 mailer
    P("mail", '<a id="mailer"></a><div class="split wide-r"><div><p class="mono eyebrow">Mailer</p><h2>The unboxing.</h2>'
              '<div class="prose"><p>A kraft mailer printed one colour outside (the mark in Carbon, flexo) and flooded Roast inside the lid, so the first thing you see on opening is the four letters and the line that explains them.</p></div>'
              '<table class="spec"><tbody><tr><th>Format</th><td>220 × 160 × 70 mm, E-flute kraft, holds three cartons</td></tr>'
              '<tr><th>Outside</th><td>Mark 64 mm, centred on the lid · one line of Plex Mono</td></tr>'
              '<tr><th>Inside lid</th><td>Roast flood · the four letters · "Every letter of MODE is a coffee." · the five modes · #SwitchYourMode</td></tr></tbody></table>'
              f'<div class="pair2"><img src="{img["lid"]}" alt="Mailer lid artwork"><img src="{img["inside"]}" alt="Mailer inside-lid artwork"></div></div>'
              f'<div class="stack2"><img src="{img["mailer-open"]}" alt="Open mailer with cartons"><img src="{img["mailer-closed"]}" alt="Closed mailer"></div></div>', "Mailer")
    # 20 tumbler
    P("full tumb", f'<a id="tumbler"></a><figure class="hero-img"><img src="{img["tumbler"]}" alt="MODE tumbler with a Zen sachet and carton"></figure>'
                   '<div class="caprow"><p class="mono eyebrow">Tumbler</p><p class="note">Carbon powder coat, the mark in Paper at 30 mm, centred on the front. Wrap artwork for a 75 mm tumbler is in <code>packaging/tumbler/</code>.</p></div>', "Tumbler")
    # 21 social
    P("soc", '<a id="social"></a><p class="mono eyebrow">Social</p><div class="socgrid">'
             f'<figure><img src="{img["instagram-post-logo"]}" alt="Instagram post: the mark"><figcaption class="mono">Post · the mark</figcaption></figure>'
             f'<figure><img src="{img["instagram-post-modes"]}" alt="Instagram post: the five modes"><figcaption class="mono">Post · the modes</figcaption></figure>'
             f'<figure><img src="{img["instagram-post-sachets"]}" alt="Instagram post: fold, squeeze, pour"><figcaption class="mono">Post · the product</figcaption></figure>'
             f'<figure class="story"><img src="{img["instagram-story"]}" alt="Instagram story"><figcaption class="mono">Story</figcaption></figure>'
             f'<figure><img src="{img["profile"]}" alt="Profile picture" class="round"><figcaption class="mono">Profile · circle-safe</figcaption></figure>'
             f'<figure><img src="{img["ecommerce-tile-wake"]}" alt="E-commerce product tile"><figcaption class="mono">E-commerce tile</figcaption></figure></div>', "Social")
    # 22 web
    P("web", f'<a id="web"></a><p class="mono eyebrow">Web</p><figure class="hero-img"><img src="{img["website-hero"]}" alt="Website hero"></figure>'
             f'<figure class="hdr"><img src="{img["website-header"]}" alt="Website header and favicon in a browser tab"></figure>'
             '<p class="note">Tonic is reserved for the one action that matters on a screen (here, Shop the range). Header mark 44–58 px wide.</p>', "Web")
    # 23 files
    files = [("logo/", "SVG, PDF and PNG (512, 1024, 2048) in Carbon, Paper, Roast, black and white · small-size cut · monogram · with clear space"),
             ("icon/", "App icon (1024, 512, 192, 180) · favicon.svg, favicon.ico (16/32/48) · profile pictures"),
             ("colour/", "mode-palette.ase (Adobe swatches) · .json · .css custom properties"),
             ("packaging/sachet/", "Front and back for all five modes: SVG, print PDF with 2 mm bleed, PNG"),
             ("packaging/carton/", "Dielines with artwork for all five modes, plus a blank die: SVG, PDF, PNG"),
             ("packaging/mailer/ · tumbler/", "Lid, inside lid and tumbler wrap artwork"),
             ("packaging/renders/", "Seven 3D renders, 1800 × 1200"),
             ("digital/", "Instagram posts and story, e-commerce tile, website hero and header"),
             ("fonts/", "Instrument Sans and IBM Plex Mono (SIL Open Font License)"),
             ("src/", "The generators. Edit mark.py or brand.py and rebuild: every file regenerates from one source")]
    P("files-pg", '<a id="files"></a><p class="mono eyebrow">Files</p><h2>What\'s in the kit.</h2><table class="spec files"><tbody>'
                  + "".join(f'<tr><th><code>{esc(a)}</code></th><td>{esc(b)}</td></tr>' for a, b in files)
                  + '</tbody></table><p class="note">Masters are SVG and PDF with true arcs and outlined hairlines. They open in Illustrator, Figma and Affinity; save as AI or EPS from there if a printer asks for it. Text in packaging files is live: install the fonts in /fonts first.</p>', "Files")
    # 24 back
    P("back-pg", f'<div class="cover-mark small-mark">{logo(PAPER, "lg")}</div><p class="mono" style="color:{PAPER}">MODE · {VERSION}</p>', "Back cover")

    page = TEMPLATE.replace("{{PAGES}}", "".join(pages))
    out = os.path.join(G, "mode-brand-guidelines.html")
    open(out, "w").write(page)
    return out, img


def _b64(rel):
    import base64
    return base64.b64encode(open(os.path.join(ROOT, rel), "rb").read()).decode()


TEMPLATE = r"""<title>MODE Brand Guidelines</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Instrument+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap">
<style>
/* Layout: a 16:9 page per section in print; on screen the same pages stack and reflow. Single light theme by choice:
   this is a print document, and the swatches must render true. */
:root{
  --paper:#F4F2ED; --oat:#E6DCCB; --carbon:#151515; --graphite:#4A4C4F; --stone:#888B8D; --roast:#4B3D2F; --tonic:#0E6B5E; --line:#DDD7CC;
  --sans:'Instrument Sans',system-ui,-apple-system,'Segoe UI',sans-serif; --mono:'IBM Plex Mono',ui-monospace,'SFMono-Regular',Menlo,monospace;
  color-scheme:light;
}
*{box-sizing:border-box}
body{background:var(--paper);color:var(--carbon);font-family:var(--sans);font-size:16px;line-height:1.5;margin:0}
h1,h2{font-weight:600;letter-spacing:-.02em;text-wrap:balance;margin:0}
h1{font-size:clamp(56px,9vw,128px);line-height:.95}
h2{font-size:clamp(26px,3.2vw,42px);line-height:1.08;max-width:22ch}
p{margin:0}
img{max-width:100%;display:block}
code{font-family:var(--mono);font-size:.86em;background:#E9E4DA;padding:.05em .35em;border-radius:3px}
a{color:inherit}
a:focus-visible{outline:2px solid var(--tonic);outline-offset:3px}
.mono{font-family:var(--mono);text-transform:uppercase;letter-spacing:.14em;font-size:12px}
.mono-face{font-family:var(--mono)}
.eyebrow{color:var(--graphite);margin-bottom:14px}
.small{font-size:13px;color:var(--graphite)}
.note{font-size:14px;color:var(--graphite);max-width:80ch;margin-top:18px}
.prose{display:grid;gap:12px;max-width:60ch;margin-top:18px;font-size:16.5px}
svg{display:block}
.lg{width:100%;height:auto}

.pg{border-bottom:1px solid var(--line);padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}
.pg>.in{max-width:1280px;margin:0 auto;padding-block:clamp(40px,6vw,80px)}
.split{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:clamp(24px,4vw,64px);align-items:center}
.split.wide-r{grid-template-columns:minmax(0,.85fr) minmax(0,1.15fr);align-items:start}
.split>*{min-width:0}

/* cover */
.cover .in{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:clamp(28px,6vw,96px);align-items:center;min-height:min(80vh,760px)}
.cover-mark{max-width:440px;width:100%}
.cover-txt{display:grid;gap:22px}
.lede{font-size:clamp(18px,1.6vw,21px);max-width:38ch;color:var(--graphite)}
.back-pg{background:var(--carbon)}
.back-pg .in{display:grid;justify-items:center;gap:28px;padding-block:96px}
.small-mark{max-width:180px}

/* contents */
.toc{columns:3 220px;column-gap:40px;padding:0;margin:0;list-style:none;counter-reset:t}
.toc li{counter-increment:t;break-inside:avoid;padding:9px 0;border-top:1px solid var(--line);display:flex;gap:14px;font-size:18px}
.toc li::before{content:counter(t,decimal-leading-zero);font-family:var(--mono);font-size:12px;color:var(--stone);padding-top:5px}
.toc a{text-decoration:none}
.toc a:hover{text-decoration:underline}

.idea-art{max-width:420px;justify-self:center;width:100%}
.duo{display:grid;grid-template-columns:1fr 1fr;gap:16px}
.plate{margin:0;padding:clamp(28px,5vw,72px);display:grid;gap:28px;justify-items:center}
.plate .lg{max-width:300px}
.plate figcaption{color:var(--graphite)}

.dia-wrap{background:#fff;border:1px solid var(--line);padding:clamp(12px,2vw,28px)}
.dia{width:100%;height:auto}
.dia .mono{font-family:var(--mono);letter-spacing:.06em;text-transform:none}
table{border-collapse:collapse;width:100%}
.spec{margin-top:22px;font-size:14.5px}
.spec th{text-align:left;font-weight:600;padding:9px 18px 9px 0;vertical-align:top;white-space:nowrap;border-top:1px solid var(--line)}
.spec td{padding:9px 0;border-top:1px solid var(--line);color:var(--graphite)}

.quad{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:16px;margin-top:28px}
.let{margin:0;display:grid;gap:16px;align-content:start}
.let-art{background:#fff;border:1px solid var(--line);aspect-ratio:1;display:grid;place-items:center;padding:20%}
.lt{width:100%;height:auto;max-height:100%}
.let figcaption,.cell figcaption{display:grid;gap:6px;font-size:14.5px}
.let figcaption span,.cell figcaption span{color:var(--graphite)}

.ladder{display:flex;flex-wrap:wrap;align-items:flex-end;gap:36px;background:#fff;border:1px solid var(--line);padding:28px;margin-top:24px}
.ladder figure{margin:0;display:grid;gap:8px}
.lad{height:100%;width:auto}
.ladder figcaption{color:var(--stone)}
.smallrow{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px;margin-top:16px}
.cell{margin:0;background:#fff;border:1px solid var(--line);padding:22px;display:grid;gap:16px;align-content:start}
.mono-art{width:64px}
.favs{display:flex;align-items:flex-end;gap:22px}
.fav{margin:0;display:grid;gap:6px;justify-items:start}
.fav img{image-rendering:pixelated}
.fav figcaption{color:var(--stone)}
.app{width:84px;border-radius:19px}

.vgrid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px;margin-top:26px}
.vgrid figure{margin:0;padding:clamp(20px,3vw,40px) clamp(20px,3vw,40px) 18px;display:grid;gap:18px;justify-items:center;border:1px solid var(--line)}
.vgrid .lg{max-width:120px}
.vgrid figcaption{font-size:10.5px;text-align:center}

.misgrid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:14px;margin-top:26px}
.mis{margin:0;display:grid;gap:10px;align-content:start}
.mis-art{position:relative;background:#fff;border:1px solid var(--line);aspect-ratio:1.25;display:grid;place-items:center;padding:14%}
.mis-art svg{width:100%;height:auto;max-height:100%}
.x{position:absolute;top:10px;right:10px;width:22px;height:22px;border-radius:50%;background:#B42318}
.x::before,.x::after{content:"";position:absolute;left:5px;top:10px;width:12px;height:2px;background:#fff;transform:rotate(45deg)}
.x::after{transform:rotate(-45deg)}
.mis figcaption{font-size:13.5px;color:var(--graphite)}

.swgrid{display:grid;grid-template-columns:repeat(9,minmax(0,1fr));gap:10px;margin-top:24px}
.sw{margin:0;display:grid;gap:10px;align-content:start}
.chip{aspect-ratio:.9;padding:12px;display:flex;flex-direction:column;justify-content:space-between;border:1px solid rgba(0,0,0,.06)}
.chip b{font-size:15px}
.chip .mono{font-size:9.5px;opacity:.8}
.sw dl{display:grid;grid-template-columns:auto 1fr;gap:2px 8px;margin:0;font-size:9.5px;letter-spacing:.04em;text-transform:none}
.sw dt{color:var(--stone)}
.sw dd{margin:0;font-variant-numeric:tabular-nums;overflow-wrap:anywhere}
.sw figcaption{font-size:12px;color:var(--graphite)}
.ratio{display:flex;height:44px;margin-top:22px;border:1px solid var(--line);overflow:hidden}
.ratio span{display:flex;align-items:center;padding:0 10px;font-family:var(--mono);font-size:10.5px;letter-spacing:.06em;white-space:nowrap;overflow:hidden}

.tbl{overflow-x:auto}
.ctab{font-size:15px}
.ctab th{text-align:left;font-family:var(--mono);font-size:11px;letter-spacing:.12em;text-transform:uppercase;color:var(--stone);font-weight:400;padding:8px 10px;border-bottom:1px solid var(--line)}
.ctab td{padding:9px 10px;border-bottom:1px solid var(--line)}
.num{font-variant-numeric:tabular-nums;font-family:var(--mono);font-size:13px}
.pair{display:inline-grid;place-items:center;width:46px;height:32px;font-weight:600;border:1px solid rgba(0,0,0,.08)}
.v{font-family:var(--mono);font-size:11px;padding:3px 8px;border-radius:99px;letter-spacing:.06em}
.v-aaa,.v-aa{background:#DCEBE7;color:#0B5247}
.v-fail{background:#F6DEDB;color:#8E1B12}

.spec-a{font-size:clamp(30px,3.4vw,46px);font-weight:600;letter-spacing:-.02em;margin-top:6px}
.spec-b{font-size:clamp(40px,5vw,72px);line-height:1.05;margin-bottom:8px}
.spec-a.mono-face{margin-top:30px;letter-spacing:0}
.hier td,.hier th{font-size:14px}
.hier thead th{font-family:var(--mono);font-size:11px;letter-spacing:.12em;text-transform:uppercase;color:var(--stone);font-weight:400}
.h-d{font-size:28px!important;font-weight:600}.h-1{font-size:21px!important;font-weight:600}.h-2{font-size:17px!important;font-weight:500}.h-l{font-size:11px!important}

.skus{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px}
.sku{margin:0;display:grid;gap:10px}
.sku-chip{aspect-ratio:1.35;position:relative;overflow:hidden;padding:18px}
.sku-chip .lt{position:absolute;right:-2%;bottom:6%;width:62%}
.sku-chip b{position:relative;font-size:20px}
.sku figcaption{font-size:13.5px;color:var(--graphite)}

.flats{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:10px}
.flats5{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:8px;margin-top:18px}
.mchip{display:inline-block;width:34px;height:26px;border:1px solid rgba(0,0,0,.08)}
.modes td{vertical-align:middle;padding-right:12px}
.modes thead th{font-family:var(--mono);font-size:11px;letter-spacing:.12em;text-transform:uppercase;color:var(--stone);font-weight:400;border-top:0}
.tints{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:10px;margin-top:16px}
.tints .tl{grid-column:1/-1;color:var(--graphite)}
.tint{margin:0;display:grid;gap:6px}
.tint span{display:flex;align-items:center;height:30px;padding:0 10px;color:#F4F2ED;font-family:var(--mono);font-size:10.5px;letter-spacing:.16em}
.tint figcaption{font-size:9.5px;letter-spacing:.03em;text-transform:none;color:var(--graphite)}
.flats figure,.back{margin:0;display:grid;gap:8px}
.flats figcaption,.back figcaption{color:var(--stone);font-size:10.5px}
.back{max-width:200px;margin-top:22px}
.hero-img{margin:0}
.hero-img img{width:100%}
.strip{margin-top:16px}
.caprow{display:flex;flex-wrap:wrap;align-items:flex-start;justify-content:space-between;gap:16px;margin-top:16px}
.mini{margin:0;max-width:380px}
.die-img{margin:0;background:#fff;border:1px solid var(--line);padding:12px}
.die-img img{max-height:70vh;margin:0 auto;width:auto}
.pair2{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:20px}
.stack2{display:grid;gap:12px}
.socgrid{display:grid;grid-template-columns:repeat(6,minmax(0,1fr));gap:12px;margin-top:20px;align-items:start}
.socgrid figure{margin:0;display:grid;gap:8px}
.socgrid figcaption{font-size:10.5px;color:var(--stone)}
.round{border-radius:50%}
.hdr{margin:14px 0 0;border:1px solid var(--line)}
.files th{min-width:0}

@media (max-width:900px){
  .split,.split.wide-r,.cover .in{grid-template-columns:minmax(0,1fr)}
  .quad,.vgrid,.misgrid,.flats,.tints{grid-template-columns:repeat(2,minmax(0,1fr))}
  .flats5{grid-template-columns:repeat(3,minmax(0,1fr))}
  .swgrid{grid-template-columns:repeat(3,minmax(0,1fr))}
  .socgrid{grid-template-columns:repeat(2,minmax(0,1fr))}
  .smallrow{grid-template-columns:minmax(0,1fr)}
  .duo{grid-template-columns:minmax(0,1fr)}
  .spec th{white-space:normal}
  .ratio span{font-size:9px;padding:0 5px}
}
@media (prefers-reduced-motion:reduce){*{scroll-behavior:auto}}

/* print: one section per 16:9 page */
@page{size:1600px 900px;margin:0}
@media print{
  body{width:1600px}
  .pg{width:1600px;height:900px;overflow:hidden;break-after:page;border:0;padding:0}
  .pg>.in{max-width:none;height:900px;padding:64px 88px}
  .cover .in{min-height:0}
  .back-pg .in{align-content:center}
  .sach-r .in,.tumb .in{padding:0;position:relative}
  .sach-r .hero-img img,.tumb .hero-img img{height:900px;object-fit:cover}
  .sach-r .caprow{position:absolute;left:88px;right:88px;bottom:48px;margin:0;align-items:flex-end}
  .tumb .caprow{position:absolute;left:88px;top:56px;margin:0;display:grid;gap:10px;max-width:440px}
  .sach-r .mini{max-width:330px;box-shadow:0 2px 16px rgba(0,0,0,.12)}
  .cart .hero-img img{max-height:470px;object-fit:cover}
  .cart .strip img{max-height:290px;object-fit:cover}
  .cart .strip{margin-top:10px}
  .die-img img{max-height:640px}
  .stack2 img{max-height:370px;width:100%;object-fit:cover}
  .web .hero-img img{max-height:500px;object-fit:cover}
  .web .hdr img{max-height:150px;object-fit:cover;object-position:top}
  .socgrid figure img{max-height:520px;object-fit:cover}
}
</style>
{{PAGES}}
"""


if __name__ == "__main__":
    out, img = build()
    print(out, f"{os.path.getsize(out) / 1024:.0f} KB", len(img), "images")
