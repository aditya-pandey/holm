"""Logos 1 (Crossfade) and 2 (Notch): masters, story frames and construction diagrams as SVG strings."""
import os
from shapely.geometry import box, Polygon
from shapely.ops import unary_union
from shapely import affinity
from letters import H, M, X, D, E, bar, place, to_d, svg, P
import crossfade as cf
import notch as nt

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
C = {"carbon": "#151515", "paper": "#F3F1EC", "stone": "#85888B", "silver": "#C9CACB", "white": "#FFFFFF",
     "tonic": "#0E7C66", "guide": "#2F6BFF"}
MODES = [  # key, name, colour, line
    ("wake", "WAKE", "#3C7FCB", "For a sharp start."),
    ("active", "ACTIVE", "#0F8A5F", "For the push."),
    ("zen", "ZEN", "#4E6E86", "For deep focus."),
    ("vital", "VITAL", "#5E8A26", "For a midday reset."),
    ("calm", "CALM", "#9A7758", "For a slow evening."),
]
MODE = {m[0]: m for m in MODES}


def g(geom, fill, x=0.0, y=0.0, k=1.0, base=H):
    """Place a y-up geometry with its baseline at y (SVG), scaled by k."""
    return P(to_d(geom, x, y + base * k, k), fill)


# ================================================================== 1 · CROSSFADE
CF = cf.wordmark()
CF_W = CF["width"]


def cf_word(x=0, y=0, width=None, steady="currentColor", out="currentColor", inc="currentColor"):
    k = (width / CF_W) if width else 1.0
    return g(CF["steady"], steady, x, y, k) + g(CF["out"], out, x, y, k) + g(CF["in"], inc, x, y, k)


def cf_symbol(x, y, size, out="currentColor", inc="currentColor"):
    o, i = cf.crossfade_x()
    k = size / H
    ox = x + (size - cf.XW * k) / 2
    return g(o, out, ox, y, k) + g(i, inc, ox, y, k)


def cf_svg(scheme="colour", pad=8):
    s = {"colour": (C["carbon"], C["stone"], C["tonic"]), "mono": ("#000",) * 3,
         "reversed": (C["white"], "#8F9295", "#3FB79A"), "white": (C["white"],) * 3}[scheme]
    return svg((-pad, -pad, CF_W + 2 * pad, H + 2 * pad), cf_word(0, 0, None, *s), "MXDE")


def cf_frames(ink="currentColor", muted="#9A9C9F", accent=C["tonic"]):
    Wf, Hf = 360, 220
    frames = []
    k = 270 / CF_W
    y0 = (Hf - H * k) / 2

    def fr(body):
        return svg((0, 0, Wf, Hf), body)

    # 1 the name, plain
    x_plain, _ = X(cf.S, cf.XW)
    plain = unary_union([CF["steady"], place(x_plain, CF["x_at"])])
    frames.append(("Start with the name. MXDE, said Mode. The X is the letter that changes.",
                   fr(g(plain, ink, 45, y0, k))))
    # 2 the hard cut
    ax = '<path d="M70 170H300M70 170V50" stroke="{m}" stroke-width="1.5" fill="none"/>'.format(m=muted)
    hard = '<path d="M70 150H180V70H300" stroke="{i}" stroke-width="6" fill="none" stroke-linejoin="miter"/>'.format(i=ink)
    lab = (f'<text x="74" y="190" font-size="11" fill="{muted}" class="lab">time</text>'
           f'<text x="74" y="44" font-size="11" fill="{muted}" class="lab">state</text>'
           f'<text x="188" y="122" font-size="12" fill="{ink}" class="lab">hard cut: spike, then crash</text>')
    frames.append(("A light switch is a hard cut. That is how strong coffee feels: a spike, then a crash.", fr(ax + hard + lab)))
    # 3 the crossfade diagram
    lines = (f'<line x1="90" y1="60" x2="280" y2="165" stroke="{muted}" stroke-width="5"/>'
             f'<line x1="90" y1="165" x2="280" y2="60" stroke="{ink}" stroke-width="5"/>'
             f'<text x="92" y="52" font-size="11" fill="{muted}" class="lab">fading out</text>'
             f'<text x="230" y="52" font-size="11" fill="{ink}" class="lab">fading in</text>')
    frames.append(("In every edit suite and DJ mixer, a smooth switch is a crossfade. One track falls as the next one rises.",
                   fr(ax + lines)))
    # 4 weight = volume (geometry is y-up, so flip the diagram's y)
    o = bar((90, Hf - 55), (280, Hf - 160), 22, 7)
    i_ = bar((90, Hf - 160), (280, Hf - 55), 7, 22)
    t = (P(to_d(o.difference(i_.buffer(3, join_style="mitre")), 0, Hf), muted) + P(to_d(i_, 0, Hf), ink) +
         f'<text x="92" y="44" font-size="11" fill="{muted}" class="lab">loud → quiet</text>'
         f'<text x="215" y="44" font-size="11" fill="{ink}" class="lab">quiet → loud</text>')
    frames.append(("Give each line the weight of its volume. Loud is heavy, quiet is light; the new one passes over the old.", fr(ax + t)))
    # 5 it is an X
    frames.append(("That diagram is already an X. Put it in the name; keep M, D and E steady around it.",
                   fr(cf_word(45, y0, 270, ink, ink, ink))))
    # 6 colour the switch
    m = MODE["wake"]
    frames.append(("What you leave goes grey. What you switch into takes the mode's colour.",
                   fr(cf_word(45, y0 - 14, 270, ink, muted, m[2]) +
                      f'<text x="46" y="{y0 + H * k + 26}" font-size="15" fill="{m[2]}" class="modename">→ WAKE</text>')))
    return frames


def cf_construction(ink="currentColor", guide=C["guide"], muted="#888B8D"):
    pad = 46
    W, Hh = CF_W + pad + 120, H + 2 * pad + 30
    b = [f'<g transform="translate({pad} {pad})">', cf_word(0, 0, None, ink, "#A9ABAE", ink)]
    sw = 0.6
    for y, lab in ((0, "cap 100"), (H, "baseline")):
        b.append(f'<line x1="-30" y1="{y}" x2="{CF_W + 30}" y2="{y}" stroke="{guide}" stroke-width="{sw}" stroke-dasharray="3 2"/>'
                 f'<text x="{CF_W + 34}" y="{y + 3}" font-size="7" fill="{guide}" class="lab">{lab}</text>')
    xa = CF["x_at"]
    # loud / quiet callouts
    b.append(f'<text x="{xa - 2}" y="-10" font-size="7" fill="{guide}" class="lab">full volume: {cf.LOUD * cf.S:.1f}</text>')
    b.append(f'<text x="{xa - 6}" y="{H + 16}" font-size="7" fill="{guide}" class="lab">silence: {cf.QUIET * cf.S:.1f}</text>')
    b.append(f'<text x="{xa + 34}" y="{H + 30}" font-size="7" fill="{guide}" class="lab">gap {cf.GAP:g}: the new state passes over the old</text>')
    b.append(f'<line x1="0" y1="{H + 8}" x2="{cf.S}" y2="{H + 8}" stroke="{guide}" stroke-width="1.2"/>'
             f'<text x="0" y="{H + 30}" font-size="7" fill="{guide}" class="lab">stem {cf.S:g}</text>')
    b.append(f'<text x="0" y="{H + 48}" font-size="7.5" fill="{muted}" class="lab">Cap height 100. Each X stroke tapers linearly from {cf.LOUD:.2f}× to {cf.QUIET:.2f}× the stem. M, D, E hold one weight.</text>')
    b.append("</g>")
    return svg((0, 0, W, Hh), "".join(b), "Crossfade construction")


def cf_mode_lockup(key, ink="currentColor", out=None, width=None):
    m = MODE[key]
    out = out or C["stone"]
    k = (width / CF_W) if width else 1
    body = cf_word(0, 0, None, ink, out, m[2])
    body += f'<text x="{CF["x_at"]}" y="{H + 52}" font-size="34" fill="{ink}" class="modename" letter-spacing="3">{m[1]}</text>'
    body += cf_symbol(CF["x_at"] - 44, H + 25, 30, out, m[2])
    return svg((-6, -6, CF_W + 12, H + 70), body, f"MXDE {m[1]}")


# ================================================================== 2 · NOTCH
NT = nt.wordmark()
NT_W = NT["width"]
NT_SYM = nt.symbol()
NT_SYM_SMALL = nt.symbol(teeth=False)


def nt_word(x=0, y=0, width=None, pack="currentColor", rest="currentColor", small=False):
    k = (width / NT_W) if width else 1.0
    pm = nt.pack_m(teeth=not small) if small else NT["pack"]
    return g(pm, pack, x, y, k) + g(NT["rest"], rest, x, y, k)


def nt_symbol(x, y, h, fill="currentColor", small=False):
    k = h / 132
    return g(NT_SYM_SMALL if small else NT_SYM, fill, x, y, k, base=132)


def nt_svg(scheme="colour", pad=8, small=False):
    s = {"colour": (C["tonic"], C["carbon"]), "mono": ("#000", "#000"), "reversed": ("#3FB79A", C["white"]),
         "white": (C["white"], C["white"])}[scheme]
    return svg((-pad, -pad, NT_W + 2 * pad, H + 2 * pad), nt_word(0, 0, None, *s, small=small), "MXDE")


def sachet_outline(W, Hh, teeth=14, tooth=5, notch=None):
    """Plain pillow sachet, serrated top and bottom; optional small side tear notch."""
    pts = []
    tw = W / teeth
    for i in range(teeth):
        pts += [(i * tw, Hh), (i * tw + tw / 2, Hh - tooth)]
    pts.append((W, Hh))
    if notch:
        y = Hh - notch
        pts += [(W, y + 5), (W - 7, y), (W, y - 5)]
    pts.append((W, 0))
    for i in range(teeth):
        pts += [(W - i * tw, 0), (W - i * tw - tw / 2, tooth)]
    pts.append((0, 0))
    return Polygon(pts).buffer(0)


def nt_frames(ink="currentColor", muted="#9A9C9F", accent=C["tonic"]):
    Wf, Hf = 360, 220
    frames = []

    def fr(body):
        return svg((0, 0, Wf, Hf), body)

    sw, sh = 104, 138
    sx, sy = (Wf - sw) / 2, (Hf - sh) / 2
    plain = sachet_outline(sw, sh, teeth=12, tooth=4.5, notch=22)
    frames.append(("Start with the object, not the name: a sachet. It is where the brand is held, torn and photographed.",
                   fr(g(plain, ink, sx, sy, 1, sh))))
    # notch selected
    nx, ny = sx + sw - 7, sy + 22
    sel = (f'<rect x="{nx - 12}" y="{ny - 12}" width="24" height="24" fill="none" stroke="{C["guide"]}" stroke-width="1.2"/>'
           + "".join(f'<rect x="{px - 3}" y="{py - 3}" width="6" height="6" fill="#fff" stroke="{C["guide"]}" stroke-width="1.1"/>'
                     for px in (nx - 12, nx + 12) for py in (ny - 12, ny + 12))
           + f'<text x="{nx + 18}" y="{ny + 4}" font-size="11" fill="{C["guide"]}" class="lab">tear here</text>')
    frames.append(("Every MXDE moment starts at the notch. It is the most-used detail on the pack, and nobody looks at it.",
                   fr(g(plain, ink, sx, sy, 1, sh) + sel)))
    # notch moved to the top centre
    small = nt.pack_m(W=sw, Hh=sh, open_=0.14, depth=0.10, teeth=True, tooth=4.5)
    frames.append(("Move the notch to the centre of the top seal.", fr(g(small, ink, sx, sy, 1, sh))))
    # cut deep: it becomes an M
    deep = nt.pack_m(W=sw, Hh=sh, open_=0.44, depth=0.46, teeth=True, tooth=4.5)
    guide = (f'<text x="{sx + sw + 16}" y="{sy + 60}" font-size="44" fill="none" stroke="{C["guide"]}" stroke-width="1" class="ghost">M</text>')
    frames.append(("Cut it deep. The silhouette of the pack becomes a solid M.", fr(g(deep, ink, sx, sy, 1, sh) + guide)))
    # the wordmark
    k = 270 / NT_W
    y0 = (Hf - H * k) / 2
    frames.append(("The pack is the first letter of the name. X, D and E are drawn to its weight.",
                   fr(nt_word(45, y0, 270, ink, ink))))
    # five modes
    row = ""
    pw, ph = 46, 61
    gap = 12
    x0 = (Wf - (5 * pw + 4 * gap)) / 2
    for i, m in enumerate(MODES):
        row += g(nt.pack_m(W=pw, Hh=ph, open_=0.44, depth=0.46, teeth=True, tooth=2.4), m[2], x0 + i * (pw + gap), 70, 1, ph)
        row += f'<text x="{x0 + i * (pw + gap) + pw / 2}" y="152" font-size="9" fill="{ink}" text-anchor="middle" class="lab">{m[1]}</text>'
    frames.append(("Five modes, five packs. Lined up, they read as a row of Ms.", fr(row)))
    return frames


def nt_construction(ink="currentColor", guide=C["guide"], muted="#888B8D"):
    pad = 46
    W, Hh = NT_W + pad + 120, H + 2 * pad + 30
    a = nt.W_PACK * (1 - nt.OPEN) / 2
    apex_y = nt.DEPTH * H
    b = [f'<g transform="translate({pad} {pad})">', nt_word(0, 0, None, ink, ink)]
    sw = 0.6
    for y, lab in ((0, "cap 100"), (H, "baseline")):
        b.append(f'<line x1="-30" y1="{y}" x2="{NT_W + 30}" y2="{y}" stroke="{guide}" stroke-width="{sw}" stroke-dasharray="3 2"/>'
                 f'<text x="{NT_W + 34}" y="{y + 3}" font-size="7" fill="{guide}" class="lab">{lab}</text>')
    b.append(f'<line x1="{a}" y1="-8" x2="{nt.W_PACK - a}" y2="-8" stroke="{guide}" stroke-width="1"/>'
             f'<text x="{a}" y="-13" font-size="7" fill="{guide}" class="lab">notch {nt.OPEN:.0%} of width</text>')
    b.append(f'<line x1="{nt.W_PACK / 2}" y1="0" x2="{nt.W_PACK / 2}" y2="{apex_y}" stroke="#fff" stroke-width="0.8" stroke-dasharray="2 2"/>'
             f'<text x="{nt.W_PACK / 2 + 4}" y="{apex_y + 12}" font-size="7" fill="#fff" class="lab">depth {nt.DEPTH:.0%}</text>')
    b.append(f'<text x="0" y="{H + 16}" font-size="7" fill="{guide}" class="lab">crimp: {nt.TEETH_TOP} teeth per shoulder, {nt.TEETH_BOT} along the base, {nt.TOOTH:g} deep</text>')
    b.append(f'<text x="{nt.W_PACK + nt.SPACE[0] + 120}" y="-13" font-size="7" fill="{guide}" class="lab">X, D, E stem {nt.S:g}</text>')
    b.append(f'<text x="0" y="{H + 34}" font-size="7.5" fill="{muted}" class="lab">Cap height 100. The pack-M is 96 wide; below 24 px the crimp teeth are dropped and the silhouette stays.</text>')
    b.append("</g>")
    return svg((0, 0, W, Hh), "".join(b), "Notch construction")


def nt_mode_lockup(key, ink="currentColor"):
    m = MODE[key]
    body = nt_word(0, 0, None, m[2], ink)
    body += f'<text x="0" y="{H + 52}" font-size="34" fill="{ink}" class="modename2" letter-spacing="2">{m[1]}</text>'
    return svg((-6, -6, NT_W + 12, H + 70), body, f"MXDE {m[1]}")


def write_masters():
    out = {}
    for name, fn in (("01-crossfade", cf_svg), ("02-notch", nt_svg)):
        d = os.path.join(ROOT, "logos", name)
        os.makedirs(d, exist_ok=True)
        for scheme in ("colour", "mono", "reversed", "white"):
            p = os.path.join(d, f"mxde-{name[3:]}-wordmark-{scheme}.svg")
            open(p, "w").write(fn(scheme))
            out[p] = True
    open(os.path.join(ROOT, "logos", "02-notch", "mxde-notch-wordmark-small-cut.svg"), "w").write(nt_svg("mono", small=True))
    d = os.path.join(ROOT, "logos", "01-crossfade")
    open(os.path.join(d, "mxde-crossfade-symbol-colour.svg"), "w").write(svg((0, 0, 100, 100), cf_symbol(0, 0, 100, C["stone"], C["tonic"]), "MXDE"))
    open(os.path.join(d, "mxde-crossfade-symbol-mono.svg"), "w").write(svg((0, 0, 100, 100), cf_symbol(0, 0, 100, "#000", "#000"), "MXDE"))
    for k in MODE:
        open(os.path.join(d, f"mxde-crossfade-mode-{k}.svg"), "w").write(cf_mode_lockup(k, C["carbon"]))
    d = os.path.join(ROOT, "logos", "02-notch")
    open(os.path.join(d, "mxde-notch-symbol-mono.svg"), "w").write(svg((0, 0, 100, 132), nt_symbol(0, 0, 132, "#000"), "MXDE"))
    open(os.path.join(d, "mxde-notch-symbol-small.svg"), "w").write(svg((0, 0, 100, 132), nt_symbol(0, 0, 132, "#000", small=True), "MXDE"))
    for k in MODE:
        open(os.path.join(d, f"mxde-notch-mode-{k}.svg"), "w").write(nt_mode_lockup(k, C["carbon"]))
    return out


if __name__ == "__main__":
    write_masters()
    print("masters written")
