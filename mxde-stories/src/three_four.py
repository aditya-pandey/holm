"""Logos 3 (Ring) and 4 (Mug): masters, story frames, construction, Easysnap-style sachet mockups."""
import math
import os
from shapely.geometry import Point, box
from shapely import affinity
from letters import H, D as D_letter, X as X_letter, place, to_d, svg, P
from type import text
import ring as rg
import mug as mg

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
K = "#1A1715"          # warm black
CREAM = "#F4EFE6"
ESP = "#5B3A22"        # espresso: the ring's edge
WASH = "#8B6542"
MUG = "#6B4226"
GUIDE = "#2F6BFF"
MUTED = "#8C8780"


def gp(geom, fill, x=0.0, y=0.0, k=1.0, extra=""):
    """Place y-up geometry (baseline 0, cap 100) with its top-left at (x, y), scale k."""
    return P(to_d(geom, x, y + H * k, k), fill, extra)


def word(s, font, x, baseline, cap, fill, tracking=0.0):
    d, ink = text(s, font, x, baseline, cap, tracking)
    return P(d, fill), ink


# ================================================================== 3 · RING
RG = rg.mark()
RG_W = RG["width"]
TIDE = rg.tide(RG["cx"], rg.RING_C[1])


def ring_word(x=0, y=0, width=None, ink=K, edge=ESP, wash=WASH, hero=True):
    k = (width / RG_W) if width else 1.0
    b = gp(RG["tone"], wash, x, y, k, ' opacity=".26"')
    if hero:
        b += gp(TIDE, edge, x, y, k, ' opacity=".28"')
    b += gp(RG["letters"], ink, x, y, k) + gp(RG["edge"], edge, x, y, k)
    return b


def ring_lockup(x=0, y=0, width=None, ink=K, edge=ESP, wash=WASH, hero=True, sub=None):
    """Wordmark with COFFEE set under the X, inside the stain's reach."""
    k = (width / RG_W) if width else 1.0
    b = ring_word(x, y, width, ink, edge, wash, hero)
    label, ink_box = text("COFFEE", "InstrumentSans-Medium.ttf", 0, 0, 13, 0.32)
    lw = ink_box[2] - ink_box[0]
    lx = x + (RG_W / 2) * k - lw * k / 2
    d, _ = text("COFFEE", "InstrumentSans-Medium.ttf", 0, 0, 13, 0.32)
    b += f'<path transform="translate({lx:.2f} {y + (H + 44) * k:.2f}) scale({k:.4f})" fill="{sub or ink}" d="{d}"/>'
    return b


RING_VB = (-12, -36, RG_W + 24, H + 92)


def ring_svg(scheme="colour"):
    s = {"colour": (K, ESP, WASH, True), "mono": ("#000", "#000", "#000", False), "reversed": (CREAM, "#C9A273", "#C9A273", True)}[scheme]
    bg = f'<rect x="{RING_VB[0]}" y="{RING_VB[1]}" width="{RING_VB[2]}" height="{RING_VB[3]}" fill="{K}"/>' if scheme == "reversed" else ""
    return svg(RING_VB, bg + ring_lockup(0, 0, None, *s), "MXDE coffee")


def ring_symbol(x, y, size, ink=K, edge=ESP, wash=WASH):
    """The O stamp: the ring and its X, for icons and seals."""
    cx, cy = RG["cx"], rg.RING_C[1]
    R = rg.RING_R + 4
    k = size / (2 * R)
    ox = x + size / 2 - cx * k
    oy = y + size / 2 - (H - cy) * k
    xs = RG["letters"].intersection(box(cx - R, -40, cx + R, 140))
    return (gp(RG["tone"], wash, ox, oy, k, ' opacity=".26"') + gp(xs, ink, ox, oy, k) + gp(RG["edge"], edge, ox, oy, k))


def ring_frames():
    Wf, Hf = 360, 220
    k = 270 / RG_W
    y0 = (Hf - H * k) / 2 - 6
    x0 = 45
    fr = lambda b: svg((0, 0, Wf, Hf), b)
    plain = gp(RG["letters"], "currentColor", x0, y0, k)
    out = [("MXDE. Everyone asks how to say it.", fr(plain + f'<text x="{Wf / 2}" y="{y0 + H * k + 30}" font-size="12" text-anchor="middle" fill="{MUTED}" class="lab">m-x-d-e? mix-dee?</text>'))]
    # cup from above, set down on the X
    cx = x0 + RG["cx"] * k
    cy = y0 + (H - rg.RING_C[1]) * k
    cup = (f'<circle cx="{cx + 4}" cy="{cy + 5}" r="{rg.RING_R * k + 15}" fill="#000" opacity=".08"/>'
           f'<circle cx="{cx}" cy="{cy}" r="{rg.RING_R * k + 12}" fill="#FFFFFF" stroke="#D9D2C6"/>'
           f'<circle cx="{cx}" cy="{cy}" r="{rg.RING_R * k - 1}" fill="#4A2E1B"/>'
           f'<circle cx="{cx - 6}" cy="{cy - 6}" r="{rg.RING_R * k - 9}" fill="#8A5A34" opacity=".55"/>'
           f'<rect x="{cx + rg.RING_R * k + 10}" y="{cy - 7}" width="26" height="14" rx="7" fill="#FFFFFF" stroke="#D9D2C6"/>')
    out.append(("Put your coffee down on it.", fr(plain + cup)))
    lifted = cup.replace(f'cx="{cx}', f'cx="{cx + 120}').replace(f'cy="{cy}', f'cy="{cy - 95}').replace(f'cx="{cx + 4}', f'cx="{cx + 124}').replace(f'cy="{cy + 5}', f'cy="{cy - 90}').replace(f'cx="{cx - 6}', f'cx="{cx + 114}').replace(f'cy="{cy - 6}', f'cy="{cy - 101}').replace(f'x="{cx + rg.RING_R * k + 10}"', f'x="{cx + 120 + rg.RING_R * k + 10}"').replace(f'y="{cy - 7}"', f'y="{cy - 102}"')
    stain = gp(RG["tone"], WASH, x0, y0, k, ' opacity=".26"') + gp(RG["edge"], ESP, x0, y0, k)
    out.append(("Pick it up again.", fr(plain + stain + lifted)))
    out.append(("It leaves a ring, right round the X.", fr(plain + stain)))
    hint = f'<text x="{cx}" y="{y0 + H * k + 34}" font-size="13" text-anchor="middle" fill="{ESP}" class="lab">/mōd/</text>'
    out.append(("The ring is the O. Now the word reads Mode.", fr(ring_word(x0, y0, 270, "currentColor") + hint)))
    out.append(("Coffee wrote the O. The logo is the proof.", fr(ring_lockup(x0, y0 - 6, 270, "currentColor"))))
    return out


def ring_construction():
    pad = 50
    W, Hh = RG_W + pad + 130, H + 2 * pad + 60
    cx, cy = RG["cx"], H - rg.RING_C[1]
    b = [f'<g transform="translate({pad} {pad + 10})">', ring_word(0, 0, None, K, ESP, WASH, False)]
    for y, lab in ((0, "cap 100"), (H, "baseline")):
        b.append(f'<line x1="-30" y1="{y}" x2="{RG_W + 30}" y2="{y}" stroke="{GUIDE}" stroke-width=".6" stroke-dasharray="3 2"/>'
                 f'<text x="{RG_W + 34}" y="{y + 3}" font-size="7" fill="{GUIDE}" class="lab">{lab}</text>')
    b.append(f'<circle cx="{cx}" cy="{cy}" r="{rg.RING_R}" fill="none" stroke="{GUIDE}" stroke-width=".6" stroke-dasharray="2 2"/>'
             f'<line x1="{cx}" y1="{cy}" x2="{cx + rg.RING_R}" y2="{cy}" stroke="{GUIDE}" stroke-width=".6"/>'
             f'<text x="{cx + 8}" y="{cy - 4}" font-size="7" fill="{GUIDE}" class="lab">r 71</text>'
             f'<text x="{cx - 70}" y="-24" font-size="7" fill="{GUIDE}" class="lab">edge 0.9–6.1: thin where the cup lifted first</text>'
             f'<text x="0" y="{H + 30}" font-size="7" fill="{GUIDE}" class="lab">stem 12.5, kept light so the ring leads · 40 units either side of the X, room for the stain</text>'
             f'<text x="0" y="{H + 46}" font-size="7.5" fill="{MUTED}" class="lab">The ring is drawn, not scanned: four sine terms make it out-of-round, three set the edge weight. Same shape in every file.</text>')
    b.append("</g>")
    return svg((0, 0, W, Hh), "".join(b), "Ring construction")


# ================================================================== 4 · MUG
MG = mg.wordmark()
MG_W = MG["width"]


def mug_word(x=0, y=0, width=None, ink=K, mug=MUG):
    k = (width / MG_W) if width else 1.0
    return gp(MG["rest"], ink, x, y, k) + gp(MG["mug"], mug, x, y, k)


def mug_lockup(x=0, y=0, width=None, ink=K, mug=MUG, sub=None):
    k = (width / MG_W) if width else 1.0
    b = mug_word(x, y, width, ink, mug)
    d, ink_box = text("COFFEE", "Archivo-SemiCondensed-Medium.ttf", 0, 0, 17, 0.42)
    lw = ink_box[2] - ink_box[0]
    b += f'<path transform="translate({x + (MG_W - lw) * k:.2f} {y + (H + 40) * k:.2f}) scale({k:.4f})" fill="{sub or ink}" d="{d}"/>'
    return b


MUG_VB = (-10, -10, MG_W + 20, H + 62)


def mug_svg(scheme="colour"):
    s = {"colour": (K, MUG), "mono": ("#000", "#000"), "reversed": (CREAM, "#C08A5B")}[scheme]
    bg = f'<rect x="{MUG_VB[0]}" y="{MUG_VB[1]}" width="{MUG_VB[2]}" height="{MUG_VB[3]}" fill="{K}"/>' if scheme == "reversed" else ""
    return svg(MUG_VB, bg + mug_lockup(0, 0, None, *s), "MXDE coffee")


def mug_symbol(x, y, size, fill=MUG):
    d, wd = mg.mug_d()
    k = size / max(wd, H)
    return gp(d, fill, x + (size - wd * k) / 2, y + (size - H * k) / 2, k)


def mug_frames():
    Wf, Hf = 360, 220
    k = 270 / MG_W
    y0 = (Hf - H * k) / 2
    x0 = 45
    fr = lambda b: svg((0, 0, Wf, Hf), b)
    mx = MG["mug_x"]
    rest = gp(MG["rest"], "currentColor", x0, y0, k)
    d0, _ = D_letter(mg.S, W=84.0)
    plain_d = gp(place(d0, mx), "currentColor", x0, y0, k)
    out = [("Start with the name, set plainly.", fr(rest + plain_d))]
    sx, sy, sw = x0 + mx * k - 5, y0 - 5, 84 * k + 10
    sel = (f'<rect x="{sx}" y="{sy}" width="{sw}" height="{H * k + 10}" fill="none" stroke="{GUIDE}" stroke-width="1.1"/>'
           + "".join(f'<rect x="{px - 3}" y="{py - 3}" width="6" height="6" fill="#fff" stroke="{GUIDE}"/>' for px in (sx, sx + sw) for py in (sy, sy + H * k + 10)))
    out.append(("A D is a straight back and a round belly.", fr(rest + plain_d + sel)))
    step1, _ = mg.mug_d(rim_line=False, handle=(0.0, 1.0), out=40, t=17)
    out.append(("Thicken the back. It becomes the body of a mug.", fr(rest + gp(place(step1, mx), "currentColor", x0, y0, k))))
    step2, _ = mg.mug_d(rim_line=False)
    out.append(("Lift the belly off the ground. Now it's a handle.", fr(rest + gp(place(step2, mx), "currentColor", x0, y0, k))))
    out.append(("Add a rim and fill it with coffee.", fr(mug_word(x0, y0, 270, "currentColor"))))
    out.append(("The D is a mug. MXDE coffee.", fr(mug_lockup(x0, y0 - 10, 270, "currentColor"))))
    return out


def mug_construction():
    pad = 50
    W, Hh = MG_W + pad + 130, H + 2 * pad + 60
    mx = MG["mug_x"]
    b = [f'<g transform="translate({pad} {pad + 10})">', mug_word(0, 0, None, K, MUG)]
    for y, lab in ((0, "cap 100"), (H, "baseline")):
        b.append(f'<line x1="-30" y1="{y}" x2="{MG_W + 30}" y2="{y}" stroke="{GUIDE}" stroke-width=".6" stroke-dasharray="3 2"/>'
                 f'<text x="{MG_W + 34}" y="{y + 3}" font-size="7" fill="{GUIDE}" class="lab">{lab}</text>')
    hy0, hy1 = H - mg.HANDLE[1] * H, H - mg.HANDLE[0] * H
    b.append(f'<line x1="{mx}" y1="{H + 10}" x2="{mx + mg.BODY_W}" y2="{H + 10}" stroke="{GUIDE}" stroke-width="1"/>'
             f'<text x="{mx}" y="{H + 22}" font-size="7" fill="{GUIDE}" class="lab">body 44 = the stem</text>'
             f'<line x1="{mx + mg.BODY_W + mg.HANDLE_OUT + 8}" y1="{hy0}" x2="{mx + mg.BODY_W + mg.HANDLE_OUT + 8}" y2="{hy1}" stroke="{GUIDE}" stroke-width="1"/>'
             f'<text x="{mx + 52}" y="{H + 22}" font-size="7" fill="{GUIDE}" class="lab">handle 4–90% of the height, reach 44, thickness 17</text>'
             f'<text x="{mx - 30}" y="-8" font-size="7" fill="{GUIDE}" class="lab">rim line 4.2, 6.5 below the top</text>'
             f'<text x="0" y="{H + 38}" font-size="7.5" fill="{MUTED}" class="lab">M, X, E: stem 17. The handle is as thick as a stem, so the mug belongs to the alphabet around it. Foot radius 7.</text>')
    b.append("</g>")
    return svg((0, 0, W, Hh), "".join(b), "Mug construction")


# ================================================================== Easysnap-style sachet
SW, SH, SR, SEAL = 300.0, 440.0, 26.0, 17.0


def sachet(content, ground, uid, x=0, y=0, w=SW, rot=0, seal_tone="#000", seal_op=0.10):
    """Flat portrait sachet with a heat-sealed border, a fold line across the middle and soft pillowing."""
    k = w / SW
    cx, cy = SW / 2, SH / 2
    defs = (f'<defs><clipPath id="c{uid}"><rect x="{SEAL}" y="{SEAL}" width="{SW - 2 * SEAL}" height="{SH - 2 * SEAL}" rx="{SR - 10}"/></clipPath>'
            f'<pattern id="h{uid}" width="3.2" height="3.2" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="1.1" height="3.2" fill="{seal_tone}" opacity="{seal_op}"/></pattern>'
            f'<radialGradient id="g{uid}" cx=".42" cy=".38" r=".75"><stop offset="0" stop-color="#fff" stop-opacity=".22"/><stop offset=".7" stop-color="#fff" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".10"/></radialGradient>'
            f'<linearGradient id="f{uid}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#000" stop-opacity="0"/><stop offset=".5" stop-color="#000" stop-opacity=".16"/><stop offset=".52" stop-color="#fff" stop-opacity=".28"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient></defs>')
    seal = (f'<path fill-rule="evenodd" d="M{SR} 0H{SW - SR}Q{SW} 0 {SW} {SR}V{SH - SR}Q{SW} {SH} {SW - SR} {SH}H{SR}Q0 {SH} 0 {SH - SR}V{SR}Q0 0 {SR} 0Z'
            f'M{SEAL + 10} {SEAL}H{SW - SEAL - 10}Q{SW - SEAL} {SEAL} {SW - SEAL} {SEAL + 10}V{SH - SEAL - 10}Q{SW - SEAL} {SH - SEAL} {SW - SEAL - 10} {SH - SEAL}H{SEAL + 10}Q{SEAL} {SH - SEAL} {SEAL} {SH - SEAL - 10}V{SEAL + 10}Q{SEAL} {SEAL} {SEAL + 10} {SEAL}Z" fill="url(#h{uid})"/>')
    body = (f'<rect x="7" y="11" width="{SW}" height="{SH}" rx="{SR}" fill="#000" opacity=".14"/>'
            f'<rect width="{SW}" height="{SH}" rx="{SR}" fill="{ground}"/>'
            f'<g clip-path="url(#c{uid})">{content}</g>'
            + seal +
            f'<rect width="{SW}" height="{SH}" rx="{SR}" fill="url(#g{uid})"/>'
            f'<rect x="{SEAL}" y="{cy - 9}" width="{SW - 2 * SEAL}" height="18" fill="url(#f{uid})"/>'
            f'<path d="M{SEAL - 6} {cy}l8 -5v10z M{SW - SEAL + 6} {cy}l-8 -5v10z" fill="{seal_tone}" opacity=".35"/>')
    t = f'translate({x:.1f} {y:.1f}) rotate({rot} {SW * k / 2:.1f} {SH * k / 2:.1f}) scale({k:.4f})'
    return f'<g transform="{t}">{defs}{body}</g>'


def sachet_back(ink, accent, logo, note):
    """Back of pack: how to open, in two pictograms, plus the ingredient line."""
    def fold_icon(x, y, ink):
        return (f'<g transform="translate({x} {y})" fill="none" stroke="{ink}" stroke-width="2.4" stroke-linejoin="round" stroke-linecap="round">'
                f'<rect x="8" y="2" width="44" height="64" rx="6"/><path d="M8 34H52" stroke-dasharray="4 3"/>'
                f'<path d="M60 18c10 6 10 26 0 32" /><path d="M56 46l4 5 5-4"/></g>')

    def squeeze_icon(x, y, ink):
        return (f'<g transform="translate({x} {y})" fill="none" stroke="{ink}" stroke-width="2.4" stroke-linejoin="round" stroke-linecap="round">'
                f'<path d="M10 4L30 34L50 4"/><path d="M30 34V46"/><circle cx="30" cy="56" r="4" fill="{accent}" stroke="none"/>'
                f'<path d="M2 18l8 4M58 18l-8 4"/></g>')
    return (logo +
            f'<text x="40" y="170" font-size="11.5" fill="{ink}" class="lab">HOW TO OPEN</text>'
            + fold_icon(46, 184, ink) + squeeze_icon(170, 186, ink) +
            f'<text x="40" y="282" font-size="11" fill="{ink}" class="body">1  Fold in half at the line.</text>'
            f'<text x="40" y="300" font-size="11" fill="{ink}" class="body">2  Squeeze with one hand and pour</text>'
            f'<text x="56" y="316" font-size="11" fill="{ink}" class="body">into 150 ml of water or milk.</text>'
            f'<text x="40" y="350" font-size="8.5" fill="{ink}" opacity=".75" class="body">Ingredients: arabica coffee extract (water, coffee).</text>'
            f'<text x="40" y="364" font-size="8.5" fill="{ink}" opacity=".75" class="body">{note}</text>'
            f'<text x="{SW - 40}" y="{SH - 40}" font-size="10" text-anchor="end" fill="{ink}" class="lab">15 ml ℮</text>')


SKUS = [("ESPRESSO", "Dark and short."), ("COLD BREW", "Smooth, slow-steeped."), ("DECAF", "All of the taste, none of the buzz.")]


def ring_sachet_front(sku, ground, ink, edge, wash, uid, x, y, w, rot=0):
    name, line = sku
    big = (f'<g transform="translate(205 395) scale(2.15)" opacity=".16">' + gp(RG["edge"], edge, -RG["cx"], -(H - rg.RING_C[1]), 1)
           + "</g>")
    c = (big + ring_lockup(52, 66, 196, ink, edge, wash) +
         f'<text x="{SW / 2}" y="268" font-size="17" text-anchor="middle" fill="{ink}" class="sku" letter-spacing="3">{name}</text>'
         f'<text x="{SW / 2}" y="290" font-size="11.5" text-anchor="middle" fill="{ink}" class="body" opacity=".8">{line}</text>'
         f'<text x="{SW / 2}" y="372" font-size="9.5" text-anchor="middle" fill="{ink}" class="lab" opacity=".75">COFFEE CONCENTRATE · ONE SHOT</text>'
         f'<text x="{SW / 2}" y="392" font-size="9.5" text-anchor="middle" fill="{edge}" class="lab">FOLD · SQUEEZE · POUR</text>')
    return sachet(c, ground, uid, x, y, w, rot)


def ring_board():
    W, Hh = 1600, 1000
    b = [f'<rect width="{W}" height="{Hh}" fill="#E9E2D6"/>']
    sk = [(SKUS[0], CREAM, K, ESP, WASH), (SKUS[1], "#D8C3A2", K, "#3E2716", "#6E4A2C"), (SKUS[2], "#22201E", CREAM, "#C9A273", "#C9A273")]
    for i, (sku, gr, ink, edge, wash) in enumerate(sk):
        bx = 60 + i * 300
        back = sachet(sachet_back(ink, edge, ring_lockup(40, 40, 120, ink, edge, wash), "Store cool. Best before: see seal."), gr, f"rb{i}", bx + 70, 70, 240, rot=9)
        b.append(back)
        b.append(ring_sachet_front(sku, gr, ink, edge, wash, f"rf{i}", bx, 40, 250))
    # flat-lay: cup from above, its rings on the table and on a pack
    cx, cy = 1260, 330
    b.append(f'<circle cx="{cx + 10}" cy="{cy + 14}" r="170" fill="#000" opacity=".10"/>'
             f'<circle cx="{cx}" cy="{cy}" r="168" fill="#FBF8F2" stroke="#DCD3C4" stroke-width="2"/>'
             f'<circle cx="{cx}" cy="{cy}" r="112" fill="#FFFFFF" stroke="#DCD3C4" stroke-width="2"/>'
             f'<circle cx="{cx}" cy="{cy}" r="96" fill="#3E2716"/><circle cx="{cx - 10}" cy="{cy - 10}" r="78" fill="#8A5A34" opacity=".55"/>'
             f'<circle cx="{cx - 20}" cy="{cy - 22}" r="40" fill="#C08A5B" opacity=".35"/>'
             f'<rect x="{cx + 108}" y="{cy - 14}" width="54" height="28" rx="14" fill="#FFFFFF" stroke="#DCD3C4" stroke-width="2"/>')
    # rings left on the table: the same ring as the logo
    for (tx, ty, s) in ((1040, 600, 1.55), (1330, 690, 1.2)):
        b.append(f'<g transform="translate({tx} {ty}) scale({s})" opacity=".85">'
                 + gp(RG["tone"], WASH, -RG["cx"], -(H - rg.RING_C[1]), 1, ' opacity=".22"')
                 + gp(RG["edge"], ESP, -RG["cx"], -(H - rg.RING_C[1]), 1) + "</g>")
    b.append(f'<text x="1040" y="860" font-size="15" fill="{K}" class="lab">FLAT-LAY: THE LOGO IS THE RING YOUR CUP LEAVES</text>')
    # app icon + social post
    b.append(f'<g transform="translate(60 640)"><rect width="200" height="200" rx="45" fill="{CREAM}"/>{ring_symbol(28, 28, 144)}</g>')
    b.append(f'<text x="60" y="878" font-size="13" fill="{K}" class="lab">APP / PROFILE ICON</text>')
    post = (f'<rect width="320" height="320" fill="{CREAM}"/>' + ring_word(30, 92, 260) +
            f'<text x="30" y="250" font-size="22" fill="{K}" class="head">Say it Mode.</text>'
            f'<text x="30" y="278" font-size="13" fill="{ESP}" class="lab">YOUR CUP ALREADY KNOWS</text>')
    b.append(f'<g transform="translate(320 600)">{post}</g>')
    b.append(f'<text x="320" y="948" font-size="13" fill="{K}" class="lab">SOCIAL POST</text>')
    return svg((0, 0, W, Hh), "".join(b), "Ring applications").replace("<svg ", '<svg class="mock" ', 1)


def mug_sachet_front(sku, ground, ink, mug, uid, x, y, w, rot=0, accent=None):
    name, line = sku
    c = (mug_lockup(46, 70, 208, ink, mug) +
         f'<text x="46" y="262" font-size="26" fill="{ink}" class="sku2">{name}</text>'
         f'<text x="46" y="284" font-size="11.5" fill="{ink}" class="body" opacity=".85">{line}</text>'
         + mug_symbol(184, 296, 92, mug) +
         f'<text x="46" y="392" font-size="9.5" fill="{ink}" class="lab" opacity=".8">ONE HAND · ONE SHOT</text>')
    return sachet(c, ground, uid, x, y, w, rot)


def mug_board():
    W, Hh = 1600, 1000
    b = [f'<rect width="{W}" height="{Hh}" fill="#E6DED1"/>']
    sk = [(SKUS[0], "#3B2618", CREAM, "#C08A5B"), (SKUS[1], "#1F2830", CREAM, "#B98F66"), (SKUS[2], CREAM, K, MUG)]
    for i, (sku, gr, ink, mugc) in enumerate(sk):
        bx = 60 + i * 300
        back = sachet(sachet_back(ink, mugc, mug_lockup(40, 40, 120, ink, mugc), "One hand to open, one hand on the handle."), gr, f"mb{i}", bx + 70, 70, 240, rot=9, seal_tone="#fff" if gr != CREAM else "#000", seal_op=0.14)
        b.append(back)
        b.append(mug_sachet_front(sku, gr, ink, mugc, f"mf{i}", bx, 40, 250))
    # side view: a folded sachet pours into a mug shaped exactly like the D
    d, wd = mg.mug_d()
    k = 2.6
    mx, my = 1140, 380
    b.append(f'<ellipse cx="{mx + wd * k / 2}" cy="{my + H * k + 6}" rx="{wd * k * 0.62}" ry="12" fill="#000" opacity=".12"/>')
    b.append(gp(d, MUG, mx, my, k))
    b.append(f'<path d="M{mx + 58} {my - 4}C{mx + 60} {my - 70} {mx + 66} {my - 120} {mx + 62} {my - 160}" stroke="#3B2618" stroke-width="7" fill="none" stroke-linecap="round"/>')
    tipx, tipy = mx + 62, my - 168
    b.append(f'<g transform="translate({tipx} {tipy})"><path d="M0 0L-58 -118" stroke="#3B2618" stroke-width="13" stroke-linecap="round"/>'
             f'<path d="M0 0L64 -112" stroke="#4E3322" stroke-width="13" stroke-linecap="round"/>'
             f'<path d="M-58 -118L-64 -130M64 -112L72 -122" stroke="#3B2618" stroke-width="13" stroke-linecap="round"/>'
             f'<text x="78" y="-60" font-size="13" fill="{K}" class="lab">sachet, folded at the line</text></g>')
    b.append(f'<text x="1040" y="860" font-size="15" fill="{K}" class="lab">FOLD, SQUEEZE, POUR: THE MUG IS THE D</text>')
    b.append(f'<g transform="translate(60 640)"><rect width="200" height="200" rx="45" fill="#3B2618"/>{mug_symbol(36, 36, 128, "#C08A5B")}</g>')
    b.append(f'<text x="60" y="878" font-size="13" fill="{K}" class="lab">APP / PROFILE ICON</text>')
    post = (f'<rect width="320" height="320" fill="#3B2618"/>' + mug_word(30, 70, 260, CREAM, "#C08A5B") +
            f'<text x="30" y="240" font-size="24" fill="{CREAM}" class="head2">ONE HAND. ONE SHOT.</text>'
            f'<text x="30" y="270" font-size="13" fill="#C08A5B" class="lab">FOLD · SQUEEZE · POUR</text>')
    b.append(f'<g transform="translate(320 600)">{post}</g>')
    b.append(f'<text x="320" y="948" font-size="13" fill="{K}" class="lab">SOCIAL POST</text>')
    return svg((0, 0, W, Hh), "".join(b), "Mug applications").replace("<svg ", '<svg class="mock" ', 1)


def write_masters():
    for name, fn, extra in (("03-ring", ring_svg, None), ("04-mug", mug_svg, None)):
        d = os.path.join(ROOT, "logos", name)
        os.makedirs(d, exist_ok=True)
        for scheme in ("colour", "mono", "reversed"):
            open(os.path.join(d, f"mxde-{name[3:]}-lockup-{scheme}.svg"), "w").write(fn(scheme))
    d = os.path.join(ROOT, "logos", "03-ring")
    open(os.path.join(d, "mxde-ring-wordmark-colour.svg"), "w").write(svg((-12, -36, RG_W + 24, H + 72), ring_word(), "MXDE"))
    open(os.path.join(d, "mxde-ring-symbol.svg"), "w").write(svg((0, 0, 160, 160), ring_symbol(8, 8, 144), "MXDE"))
    d = os.path.join(ROOT, "logos", "04-mug")
    open(os.path.join(d, "mxde-mug-wordmark-colour.svg"), "w").write(svg((-10, -10, MG_W + 20, H + 20), mug_word(), "MXDE"))
    open(os.path.join(d, "mxde-mug-symbol.svg"), "w").write(svg((0, 0, 140, 140), mug_symbol(6, 6, 128), "MXDE"))


if __name__ == "__main__":
    write_masters()
    print("masters written")
