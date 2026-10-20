"""2D presentation mockups for logos 1 and 2 (not production artwork)."""
from shapely import affinity
from letters import H, to_d, svg, P
import crossfade as cf
import notch as nt
from two_marks import C, MODES, MODE, g, cf_word, cf_symbol, CF_W, nt_word, NT_W, sachet_outline

# what fades out → what fades in, per mode (working copy, to confirm)
FADE = {"wake": ("sleep", "sharp"), "active": ("desk", "drive"), "zen": ("noise", "focus"),
        "vital": ("slump", "fresh"), "calm": ("rush", "rest")}


def wrap(w, h, body, label, bg=None):
    b = f'<rect width="{w}" height="{h}" fill="{bg}"/>' if bg else ""
    return svg((0, 0, w, h), b + body, label).replace("<svg ", '<svg class="mock" ', 1)


def shadow(d, dx=7, dy=10, op=0.12):
    return f'<path d="{d}" transform="translate({dx} {dy})" fill="#000" opacity="{op}"/>'


# ================================================================== CROSSFADE
def cf_sachet(key, x=0, y=0, w=300):
    """Pillow sachet, Paper ground. The big X carries the switch: grey stroke = what fades out, colour = what fades in."""
    m = MODE[key]
    W, Hh = 300, 420
    k = w / W
    shape = sachet_outline(W, Hh, teeth=20, tooth=7)
    d = to_d(shape, 0, Hh)
    out, inn = FADE[key]
    b = [shadow(d), f'<path d="{d}" fill="{C["paper"]}"/>',
         f'<rect x="0" y="20" width="{W}" height="1" fill="#000" opacity=".07"/><rect x="0" y="{Hh - 21}" width="{W}" height="1" fill="#000" opacity=".07"/>',
         cf_word(26, 44, 132, C["carbon"], C["stone"], m[2]),
         f'<text x="{W - 26}" y="66" font-size="9.5" text-anchor="end" fill="{C["carbon"]}" class="lab">#SwitchYourMode</text>',
         cf_symbol(48, 96, 204, C["stone"], m[2]),
         f'<text x="40" y="94" font-size="10" fill="{C["stone"]}" class="lab">{out}</text>',
         f'<text x="{W - 40}" y="94" font-size="10" fill="{m[2]}" text-anchor="end" class="lab">{inn}</text>',
         f'<text x="26" y="342" font-size="30" fill="{C["carbon"]}" class="modename" letter-spacing="2.5">{m[1]}</text>',
         f'<text x="27" y="364" font-size="12" fill="{C["carbon"]}" class="body">{m[3]}</text>',
         f'<text x="27" y="392" font-size="8.5" fill="#55585C" class="lab">FUNCTIONAL COFFEE CONCENTRATE · 1 SACHET · 18 ML</text>']
    return f'<g transform="translate({x} {y}) scale({k:.4f})">{"".join(b)}</g>'


def can_shape(cx, top, w, h):
    """A slim can silhouette (2D): lid, neck, body, base."""
    r = w / 2
    neck = w * 0.86 / 2
    return (f'M{cx - neck} {top}H{cx + neck}L{cx + r} {top + h * 0.06}V{top + h - h * 0.025}'
            f'Q{cx + r} {top + h} {cx + r - 8} {top + h}H{cx - r + 8}Q{cx - r} {top + h} {cx - r} {top + h - h * 0.025}'
            f'V{top + h * 0.06}Z')


def can_shading(cx, top, w, h, uid):
    r = w / 2
    return (f'<defs><linearGradient id="sh{uid}" x1="0" x2="1"><stop offset="0" stop-color="#000" stop-opacity=".45"/>'
            f'<stop offset=".18" stop-color="#fff" stop-opacity=".18"/><stop offset=".32" stop-color="#fff" stop-opacity="0"/>'
            f'<stop offset=".75" stop-color="#000" stop-opacity=".05"/><stop offset="1" stop-color="#000" stop-opacity=".5"/></linearGradient></defs>'
            f'<path d="{can_shape(cx, top, w, h)}" fill="url(#sh{uid})"/>'
            f'<rect x="{cx - w * 0.43}" y="{top - 9}" width="{w * 0.86}" height="10" fill="#B9BBBD"/>'
            f'<rect x="{cx - w * 0.43}" y="{top - 9}" width="{w * 0.86}" height="10" fill="url(#sh{uid})" opacity=".8"/>')


def cf_can(key, x=0, y=0, w=200, uid="a"):
    m = MODE[key]
    Wc, Hc = 200, 430
    k = w / Wc
    cx, top, cw, ch = 100, 30, 150, 380
    b = [f'<ellipse cx="{cx}" cy="{top + ch + 6}" rx="{cw * 0.62}" ry="9" fill="#000" opacity=".16"/>',
         f'<path d="{can_shape(cx, top, cw, ch)}" fill="{C["carbon"]}"/>',
         cf_word(cx - 58, top + 52, 116, C["white"], "#6E7174", m[2]),
         cf_symbol(cx - 66, top + 120, 132, "#55585B", m[2]),
         f'<text x="{cx - 58}" y="{top + 300}" font-size="26" fill="{C["white"]}" class="modename" letter-spacing="2">{m[1]}</text>',
         f'<text x="{cx - 58}" y="{top + 320}" font-size="10" fill="#B9BBBD" class="body">{m[3]}</text>',
         f'<text x="{cx - 58}" y="{top + 350}" font-size="7.5" fill="#8F9295" class="lab">READY TO DRINK · 250 ML</text>',
         can_shading(cx, top, cw, ch, uid)]
    return f'<g transform="translate({x} {y}) scale({k:.4f})">{"".join(b)}</g>'


def cf_app_icon(x, y, s, r=0.225):
    return (f'<g transform="translate({x} {y})"><rect width="{s}" height="{s}" rx="{s * r}" fill="{C["carbon"]}"/>'
            f'{cf_symbol(s * 0.24, s * 0.24, s * 0.52, "#8F9295", "#3FB79A")}</g>')


def cf_board():
    """Packaging board: five sachets + two cans."""
    W, Hh = 1600, 980
    b = []
    for i, (k, *_r) in enumerate(MODES):
        b.append(cf_sachet(k, 40 + i * 300, 40, 270))
    b.append(cf_can("wake", 330, 470, 210, "w"))
    b.append(cf_can("calm", 560, 470, 210, "c"))
    b.append(cf_app_icon(860, 560, 180))
    # IG post
    m = MODE["zen"]
    px, py, ps = 1110, 470, 460
    b.append(f'<g transform="translate({px} {py})"><rect width="{ps}" height="{ps}" fill="{C["paper"]}"/>'
             + cf_symbol(110, 70, 240, C["stone"], m[2])
             + f'<text x="40" y="372" font-size="26" fill="{C["carbon"]}" class="head">Noise fades out.</text>'
             + f'<text x="40" y="404" font-size="26" fill="{m[2]}" class="head">Focus fades in.</text>'
             + f'<text x="40" y="436" font-size="12" fill="#55585C" class="lab">ZEN MODE · #SWITCHYOURMODE</text></g>')
    b.append(f'<text x="860" y="770" font-size="13" fill="#55585C" class="lab">APP / PROFILE ICON</text>')
    return wrap(W, Hh, "".join(b), "Crossfade applications", "#E7E3DB")


# ================================================================== NOTCH
def nt_sachet(key, x=0, y=0, w=300):
    """The die-cut pack: its silhouette is the M. Full-bleed mode colour."""
    m = MODE[key]
    W, Hh = 300, 396
    k = w / W
    shape = nt.pack_m(W=W, Hh=Hh, open_=0.44, depth=0.46, teeth=True, tooth=9)
    d = to_d(shape, 0, Hh)
    apex_y = Hh * 0.46
    b = [shadow(d), f'<path d="{d}" fill="{m[2]}"/>',
         f'<rect x="0" y="26" width="{W}" height="1.2" fill="#000" opacity=".12"/>',
         f'<rect x="0" y="{Hh - 26}" width="{W}" height="1.2" fill="#000" opacity=".12"/>',
         f'<text x="{W / 2}" y="{apex_y + 16}" font-size="9" fill="#fff" text-anchor="middle" class="lab" opacity=".85">TEAR ↓</text>',
         nt_word(24, 226, 150, "#fff", "#fff"),
         f'<text x="24" y="318" font-size="38" fill="#fff" class="modename2" letter-spacing="1.5">{m[1]}</text>',
         f'<text x="25" y="340" font-size="12" fill="#fff" class="body">{m[3]}</text>',
         f'<text x="25" y="364" font-size="8.5" fill="#fff" opacity=".8" class="lab">FUNCTIONAL COFFEE CONCENTRATE · 18 ML</text>']
    return f'<g transform="translate({x} {y}) scale({k:.4f})">{"".join(b)}</g>'


def nt_can(key, x=0, y=0, w=200, uid="n"):
    """Paper can; the mode band's top edge is notched, so the colour block is the pack-M."""
    m = MODE[key]
    Wc, Hc = 200, 430
    k = w / Wc
    cx, top, cw, ch = 100, 30, 150, 380
    band_top = top + ch * 0.30
    bx0, bx1 = cx - cw / 2, cx + cw / 2
    notch_w = cw * 0.44
    band = (f'M{bx0} {band_top}H{cx - notch_w / 2}L{cx} {band_top + ch * 0.22}L{cx + notch_w / 2} {band_top}H{bx1}'
            f'V{top + ch}H{bx0}Z')
    b = [f'<ellipse cx="{cx}" cy="{top + ch + 6}" rx="{cw * 0.62}" ry="9" fill="#000" opacity=".16"/>',
         f'<clipPath id="cl{uid}"><path d="{can_shape(cx, top, cw, ch)}"/></clipPath>',
         f'<path d="{can_shape(cx, top, cw, ch)}" fill="{C["paper"]}"/>',
         f'<path d="{band}" fill="{m[2]}" clip-path="url(#cl{uid})"/>',
         nt_word(cx - 56, top + 44, 112, C["carbon"], C["carbon"]),
         f'<text x="{cx - 56}" y="{top + 300}" font-size="32" fill="#fff" class="modename2">{m[1]}</text>',
         f'<text x="{cx - 56}" y="{top + 320}" font-size="10" fill="#fff" class="body">{m[3]}</text>',
         f'<text x="{cx - 56}" y="{top + 350}" font-size="7.5" fill="#fff" opacity=".85" class="lab">READY TO DRINK · 250 ML</text>',
         can_shading(cx, top, cw, ch, uid)]
    return f'<g transform="translate({x} {y}) scale({k:.4f})">{"".join(b)}</g>'


def nt_app_icon(x, y, s, fill=None, r=0.225):
    fill = fill or C["tonic"]
    sym = nt.symbol(teeth=True)
    kk = s * 0.56 / 132
    return (f'<g transform="translate({x} {y})"><rect width="{s}" height="{s}" rx="{s * r}" fill="{fill}"/>'
            + g(sym, "#fff", (s - 100 * kk) / 2, s * 0.22, kk, base=132) + "</g>")


def nt_board():
    W, Hh = 1600, 980
    b = []
    for i, (k, *_r) in enumerate(MODES):
        b.append(nt_sachet(k, 40 + i * 300, 50, 270))
    b.append(nt_can("active", 330, 470, 210, "na"))
    b.append(nt_can("zen", 560, 470, 210, "nz"))
    b.append(nt_app_icon(860, 560, 180))
    # IG post: a flat-lay row of packs
    px, py, ps = 1110, 470, 460
    post = [f'<rect width="{ps}" height="{ps}" fill="{C["carbon"]}"/>',
            f'<text x="26" y="70" font-size="30" fill="#fff" class="head2">Five modes. One shape.</text>']
    for i, (k, *_r) in enumerate(MODES):
        post.append(f'<g transform="rotate({(-3, 2, -1, 3, -2)[i]} {14 + i * 87 + 42} 200)">{nt_sachet(k, 14 + i * 87, 140, 84)}</g>')
    post.append(f'<text x="26" y="340" font-size="18" fill="#A9ABAE" class="body">Tear the notch. Pour. Switch.</text>')
    post.append(f'<text x="26" y="424" font-size="12" fill="#A9ABAE" class="lab">#SWITCHYOURMODE</text>')
    b.append(f'<g transform="translate({px} {py})">{"".join(post)}</g>')
    b.append(f'<text x="860" y="770" font-size="13" fill="#55585C" class="lab">APP / PROFILE ICON</text>')
    return wrap(W, Hh, "".join(b), "Notch applications", "#E7E3DB")
