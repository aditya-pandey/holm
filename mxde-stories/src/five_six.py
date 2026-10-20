"""Logos 5 (Bloom) and 6 (Drop) for MODE: masters, story frames, construction, sachet mockups."""
import math
import os
from shapely.geometry import Point, box
from shapely import affinity
from letters import to_d, svg, P
from type import text
import bloom as bl
import drop as dr
from three_four import sachet, SW, SH

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
INK = "#1E1B18"
CREAM = "#FBF7EF"
PAPER = "#F5F0E8"
GUIDE = "#2F6BFF"
MUTED = "#8C8780"
MODES = bl.MODES
NAMES = {"wake": "WAKE", "active": "ACTIVE", "zen": "ZEN", "vital": "VITAL", "calm": "CALM"}
LINES = {"wake": "For a sharp start.", "active": "For the push.", "zen": "For deep focus.", "vital": "For a midday reset.", "calm": "For a slow evening."}


def d_of(g):
    """Path data for geometry already in SVG coordinates (y down)."""
    g = g.buffer(0)
    polys = [g] if g.geom_type == "Polygon" else [p for p in g.geoms if p.geom_type == "Polygon"]
    out = []
    for p in polys:
        for r in [p.exterior] + list(p.interiors):
            pts = list(r.coords)[:-1]
            out.append("M" + "L".join(f"{x:.2f} {y:.2f}" for x, y in pts) + "Z")
    return "".join(out)


def word(s, font, cap, tracking, fill, x=0, baseline=0, k=1.0):
    d, ink = text(s, font, 0, 0, cap, tracking)
    return f'<path transform="translate({x:.2f} {baseline:.2f}) scale({k:.4f})" fill="{fill}" d="{d}"/>', (ink[2] - ink[0]) * k


# ================================================================== 5 · BLOOM
# every mode colour comes from the coffee plant
BLOOM = {"wake": "#D99A2B", "active": "#B23A30", "zen": "#2F5D3A", "vital": "#7DA23A", "calm": "#6B4226"}
BLOOM_FONT = "Newsreader-Regular.ttf"
PET = bl.petals()


def flower(x, y, size, lit=None, ink=INK, solid=None, outline_w=3.4):
    """The five-bean flower. lit=None draws the master (all solid); a mode lights its petal and outlines the rest."""
    k = size / 200
    parts = []
    for m, (b, plain) in PET.items():
        if lit is None:
            parts.append(P(d_of(b), solid or ink))
        elif m == lit:
            parts.append(P(d_of(b), BLOOM[m] if solid is None else solid))
        else:
            parts.append(P(d_of(bl.outline(plain, outline_w)), ink))
    return f'<g transform="translate({x:.2f} {y:.2f}) scale({k:.4f})">{"".join(parts)}</g>'


def bloom_lockup(x=0, y=0, w=260, ink=INK, lit=None, sub=True, solid=None):
    """Stacked: the flower over MODE, COFFEE below. Returns (svg, height)."""
    fs = w * 0.52
    b = [flower(x + (w - fs) / 2, y, fs, lit, ink, solid)]
    mw, mwid = word("MODE", BLOOM_FONT, 100, 0.14, ink)
    k = (w * 0.86) / mwid
    yb = y + fs + w * 0.06 + 100 * k
    mw, _ = word("MODE", BLOOM_FONT, 100, 0.14, ink, x + (w - mwid * k) / 2, yb, k)
    b.append(mw)
    h = yb - y
    if sub:
        cw, cwid = word("COFFEE", "InstrumentSans-Medium.ttf", 100, 0.42, ink)
        kc = (w * 0.34) / cwid
        cw, _ = word("COFFEE", "InstrumentSans-Medium.ttf", 100, 0.42, ink, x + (w - cwid * kc) / 2, yb + w * 0.11, kc)
        b.append(cw)
        h = yb + w * 0.11 - y
    return "".join(b), h + 4


def bloom_horizontal(x=0, y=0, h=60, ink=INK, lit=None):
    b = [flower(x, y, h, lit, ink)]
    mw, mwid = word("MODE", BLOOM_FONT, 100, 0.14, ink)
    k = (h * 0.5) / 100
    b.append(word("MODE", BLOOM_FONT, 100, 0.14, ink, x + h * 1.18, y + h * 0.5 + 50 * k, k)[0])
    return "".join(b), h * 1.18 + mwid * k


def bloom_svg(scheme="colour", lit=None):
    ink, bg = {"colour": (INK, None), "mono": ("#000", None), "reversed": (CREAM, INK)}[scheme]
    body, h = bloom_lockup(20, 16, 260, ink, lit, solid=("#000" if scheme == "mono" and lit else None))
    bgr = f'<rect width="300" height="{h + 40}" fill="{bg}"/>' if bg else ""
    return svg((0, 0, 300, h + 40), bgr + body, "MODE coffee")


def natural_flower(x, y, size, ink):
    """A plain five-petal coffee blossom, for the first frame of the story."""
    k = size / 200
    parts = []
    for i in range(5):
        ang = -90 + 72 * i
        petal = affinity.scale(Point(0, 0).buffer(1, resolution=64), 17, 40)
        petal = affinity.rotate(petal, ang + 90, origin=(0, 0))
        r = math.radians(ang)
        petal = affinity.translate(petal, 100 + 42 * math.cos(r), 100 + 42 * math.sin(r))
        parts.append(P(d_of(petal.difference(petal.buffer(-3.2))), ink))
    for i in range(5):
        r = math.radians(-54 + 72 * i)
        parts.append(f'<line x1="100" y1="100" x2="{100 + 20 * math.cos(r):.1f}" y2="{100 + 20 * math.sin(r):.1f}" stroke="{ink}" stroke-width="2.4"/>'
                     f'<circle cx="{100 + 22 * math.cos(r):.1f}" cy="{100 + 22 * math.sin(r):.1f}" r="3.4" fill="{ink}"/>')
    return f'<g transform="translate({x:.2f} {y:.2f}) scale({k:.4f})">{"".join(parts)}</g>'


def bloom_frames():
    Wf, Hf = 360, 220
    fr = lambda b: svg((0, 0, Wf, Hf), b)
    fx, fy, fs = 110, 30, 140
    out = [("Before it's a bean, coffee is a flower: white, scented like jasmine, open for two or three days.",
            fr(natural_flower(fx, fy, fs, "currentColor")))]
    nums = ""
    for i in range(5):
        r = math.radians(-90 + 72 * i)
        nums += f'<text x="{fx + fs / 2 + 92 * math.cos(r) * fs / 200:.1f}" y="{fy + fs / 2 + 92 * math.sin(r) * fs / 200 + 4:.1f}" font-size="12" text-anchor="middle" fill="{GUIDE}" class="lab">{i + 1}</text>'
    out.append(("An arabica blossom usually has five petals.", fr(natural_flower(fx, fy, fs, "currentColor") + nums)))
    names = ""
    for i, m in enumerate(MODES):
        r = math.radians(-90 + 72 * i)
        names += f'<text x="{fx + fs / 2 + 112 * math.cos(r) * fs / 200:.1f}" y="{fy + fs / 2 + 112 * math.sin(r) * fs / 200 + 4:.1f}" font-size="10" text-anchor="middle" fill="{BLOOM[m]}" class="lab">{NAMES[m]}</text>'
    out.append(("MODE has five modes. One for each petal.", fr(natural_flower(fx, fy, fs, "currentColor") + names)))
    beans = "".join(P(d_of(bl.outline(plain, 3.2)), "currentColor") for b, plain in PET.values())
    out.append(("Swap each petal for the bean it will become.", fr(f'<g transform="translate({fx} {fy}) scale({fs / 200})">{beans}</g>')))
    body, h = bloom_lockup(118, 22, 124, "currentColor")
    out.append(("All five together are the brand: MODE, from the flower coffee comes from.", fr(body)))
    body, h = bloom_lockup(118, 22, 124, "currentColor", lit="zen")
    out.append(("Each mode lights its own petal. This is Zen.", fr(body)))
    return out


def bloom_construction():
    W, Hh = 520, 300
    b = [f'<g transform="translate(40 30)">', flower(0, 0, 240, None, INK)]
    b.append(f'<circle cx="120" cy="120" r="{bl.DIST * 1.2:.1f}" fill="none" stroke="{GUIDE}" stroke-width=".8" stroke-dasharray="3 2"/>')
    for i in range(5):
        r = math.radians(-90 + 72 * i)
        b.append(f'<line x1="120" y1="120" x2="{120 + 118 * math.cos(r):.1f}" y2="{120 + 118 * math.sin(r):.1f}" stroke="{GUIDE}" stroke-width=".6"/>')
    b.append("</g>")
    notes = [("Five beans at 72°", "each long axis points out from the centre"),
             ("Bean 39 × 68", "an ellipse; centre 47 from the middle"),
             ("Crease 3.8 wide", "a gentle S cut through each bean"),
             ("Unlit petals", "3.4 outline, so the mode reads in one colour")]
    for i, (h_, t_) in enumerate(notes):
        b.append(f'<text x="320" y="{70 + i * 50}" font-size="12" fill="{GUIDE}" class="lab">{h_}</text>'
                 f'<text x="320" y="{86 + i * 50}" font-size="11" fill="{MUTED}" class="body">{t_}</text>')
    return svg((0, 0, W, Hh), "".join(b), "Bloom construction")


def bloom_sachet(m, uid, x, y, w, rot=0):
    body, h = bloom_lockup(70, 46, 160, INK, lit=m, sub=False)
    nm, nw = word(NAMES[m], BLOOM_FONT, 100, 0.18, INK)
    k = 30 / 100
    c = (body +
         word(NAMES[m], BLOOM_FONT, 100, 0.18, INK, (SW - nw * k) / 2, 286, k)[0] +
         f'<text x="{SW / 2}" y="308" font-size="12" text-anchor="middle" fill="{INK}" class="body" opacity=".85">{LINES[m]}</text>'
         f'<rect x="{SW / 2 - 18}" y="326" width="36" height="3" fill="{BLOOM[m]}"/>'
         f'<text x="{SW / 2}" y="372" font-size="9.5" text-anchor="middle" fill="{INK}" class="lab" opacity=".75">COFFEE CONCENTRATE · 15 ML</text>'
         f'<text x="{SW / 2}" y="390" font-size="9.5" text-anchor="middle" fill="{BLOOM[m]}" class="lab">FOLD · SQUEEZE · POUR</text>')
    return sachet(c, CREAM, uid, x, y, w, rot)


def bloom_back(m):
    body, h = bloom_lockup(40, 40, 90, INK, lit=m, sub=False)
    return (body + f'<text x="150" y="70" font-size="10" fill="{INK}" class="lab">{NAMES[m]} MODE</text>'
            f'<text x="150" y="88" font-size="10" fill="{INK}" class="body" opacity=".8">{LINES[m]}</text>'
            f'<text x="40" y="190" font-size="11" fill="{INK}" class="lab">HOW TO OPEN</text>'
            f'<text x="40" y="214" font-size="11" fill="{INK}" class="body">1  Fold in half at the line.</text>'
            f'<text x="40" y="232" font-size="11" fill="{INK}" class="body">2  Squeeze with one hand and pour</text>'
            f'<text x="56" y="248" font-size="11" fill="{INK}" class="body">into 150 ml of water or milk.</text>'
            f'<text x="40" y="300" font-size="9.5" fill="{INK}" class="body" opacity=".8">Coffee flowers have five petals.</text>'
            f'<text x="40" y="314" font-size="9.5" fill="{INK}" class="body" opacity=".8">This sachet is the {["first", "second", "third", "fourth", "fifth"][MODES.index(m)]}.</text>'
            f'<text x="40" y="360" font-size="8.5" fill="{INK}" class="body" opacity=".7">Ingredients: arabica coffee extract (water, coffee).</text>'
            f'<text x="{SW - 40}" y="{SH - 40}" font-size="10" text-anchor="end" fill="{INK}" class="lab">15 ml ℮</text>')


def bloom_board():
    W, Hh = 1600, 1040
    b = [f'<rect width="{W}" height="{Hh}" fill="#E8EDE3"/>']
    for i, m in enumerate(MODES):
        b.append(bloom_sachet(m, f"bf{i}", 40 + i * 308, 40, 270))
    b.append(sachet(bloom_back("zen"), CREAM, "bb0", 60, 560, 250, rot=-7))
    b.append(bloom_sachet("zen", "bf9", 250, 540, 250, rot=5))
    # app icon
    b.append(f'<g transform="translate(600 600)"><rect width="200" height="200" rx="45" fill="{BLOOM["zen"]}"/>{flower(30, 30, 140, None, CREAM, CREAM)}</g>')
    b.append(f'<text x="600" y="838" font-size="13" fill="{INK}" class="lab">APP / PROFILE ICON</text>')
    # social post
    post = [f'<rect width="420" height="420" fill="{CREAM}"/>', flower(110, 40, 200, None, INK)]
    for i, m in enumerate(MODES):
        post.append(f'<g transform="translate({30 + i * 76} 290)">' + flower(0, 0, 56, m, INK) + f'<text x="28" y="76" font-size="10" text-anchor="middle" fill="{BLOOM[m]}" class="lab">{NAMES[m]}</text></g>')
    post.append(f'<text x="30" y="400" font-size="15" fill="{INK}" class="body">Coffee is a flower first. Five petals, five modes.</text>')
    b.append(f'<g transform="translate(860 560)">{"".join(post)}</g>')
    b.append(f'<text x="860" y="1006" font-size="13" fill="{INK}" class="lab">SOCIAL POST</text>')
    return svg((0, 0, W, Hh), "".join(b), "Bloom applications").replace("<svg ", '<svg class="mock" ', 1)


# ================================================================== 6 · DROP
# the day in coffee: black first thing, milkier by evening
TONE = {"wake": "#1F1410", "active": "#4A2A18", "zen": "#6B4428", "vital": "#9A6638", "calm": "#C49A6C"}
VERB = {"wake": "falling", "active": "in flight", "zen": "floating", "vital": "bouncing", "calm": "resting"}
DROP_FONT = "InstrumentSans-SemiBold.ttf"


def drop_shape(m, x, y, size, fill):
    k = size / 100
    return P(to_d(dr.drop(m), x, y + 100 * k, k), fill)


def strip(x, y, size, fill=INK, tones=False, gap=0.18):
    return "".join(drop_shape(m, x + i * size * (1 + gap), y, size, TONE[m] if tones else fill) for i, m in enumerate(MODES))


def drop_lockup(x=0, y=0, w=320, ink=INK, tones=True, sub=True):
    """MODE over the five states. Returns (svg, height)."""
    mw, mwid = word("MODE", DROP_FONT, 100, 0.10, ink)
    k = w / mwid
    b = [word("MODE", DROP_FONT, 100, 0.10, ink, x, y + 100 * k, k)[0]]
    size = w / (5 + 4 * 0.18)
    b.append(strip(x, y + 100 * k + w * 0.07, size, ink, tones))
    h = 100 * k + w * 0.07 + size
    if sub:
        cw, cwid = word("COFFEE", "InstrumentSans-Medium.ttf", 100, 0.42, ink)
        kc = (w * 0.26) / cwid
        b.append(word("COFFEE", "InstrumentSans-Medium.ttf", 100, 0.42, ink, x, y + h + w * 0.09, kc)[0])
        h += w * 0.09
    return "".join(b), h + 4


def drop_mark(x, y, h, ink=INK, drop_fill=None, m="wake"):
    """Horizontal: one drop beside MODE. For small spaces."""
    b = [drop_shape(m, x, y, h, drop_fill or ink)]
    mw, mwid = word("MODE", DROP_FONT, 100, 0.10, ink)
    k = (h * 0.62) / 100
    b.append(word("MODE", DROP_FONT, 100, 0.10, ink, x + h * 1.05, y + h * 0.81, k)[0])
    return "".join(b), h * 1.05 + mwid * k


def drop_svg(scheme="colour"):
    ink, tones, bg = {"colour": (INK, True, None), "mono": ("#000", False, None), "reversed": (CREAM, False, INK)}[scheme]
    body, h = drop_lockup(20, 20, 300, ink, tones)
    bgr = f'<rect width="340" height="{h + 40}" fill="{bg}"/>' if bg else ""
    return svg((0, 0, 340, h + 40), bgr + body, "MODE coffee")


def drop_frames():
    Wf, Hf = 360, 220
    fr = lambda b: svg((0, 0, Wf, Hf), b)
    out = []
    sach = (f'<rect x="150" y="18" width="60" height="84" rx="8" fill="none" stroke="currentColor" stroke-width="3"/>'
            f'<line x1="156" y1="60" x2="204" y2="60" stroke="currentColor" stroke-width="1.6" stroke-dasharray="4 3"/>')
    out.append(("A sachet of MODE is a few drops of coffee, concentrated.", fr(sach + drop_shape("wake", 165, 120, 30, "currentColor"))))
    out.append(("A drop is always the same coffee.", fr(drop_shape("wake", 140, 40, 90, "currentColor"))))
    outl = "".join(f'<g opacity=".28">{drop_shape(m, 28 + i * 64, 80, 52, "currentColor")}</g>' for i, m in enumerate(MODES))
    out.append(("But its shape shows what it's doing.", fr(drop_shape("wake", 28, 80, 52, "currentColor") + outl)))
    lab = "".join(f'<text x="{28 + i * 64 + 26}" y="160" font-size="10" text-anchor="middle" fill="{MUTED}" class="lab">{VERB[m]}</text>' for i, m in enumerate(MODES))
    out.append(("Falling. In flight. Floating. Bouncing. Resting.", fr(strip(28, 80, 52, "currentColor", gap=0.231) + lab)))
    lab2 = "".join(f'<text x="{28 + i * 64 + 26}" y="160" font-size="10" text-anchor="middle" fill="{TONE[m]}" class="lab">{NAMES[m]}</text>' for i, m in enumerate(MODES))
    out.append(("Five states of a drop. Five modes.", fr(strip(28, 80, 52, tones=True, gap=0.231) + lab2)))
    body, h = drop_lockup(90, 40, 180, "currentColor")
    out.append(("MODE: one coffee, five states.", fr(body)))
    return out


def drop_construction():
    W, Hh = 720, 260
    b = [f'<g transform="translate(30 40)">', strip(0, 0, 110, INK, gap=0.2)]
    b.append(f'<line x1="-10" y1="110" x2="680" y2="110" stroke="{GUIDE}" stroke-width=".7" stroke-dasharray="3 2"/>'
             f'<text x="0" y="128" font-size="10" fill="{GUIDE}" class="lab">one baseline, one 100-unit cell for every state</text>')
    notes = ["teardrop r 30, tip 70; sides tangent", "r 27, tip 92, leaning 38°", "sphere r 36", "squashed 82 × 50, lifted, contact shadow", "dome 88 × 30, flat on the surface"]
    for i, n in enumerate(notes):
        b.append(f'<text x="{i * 132 + 4}" y="152" font-size="9" fill="{MUTED}" class="body">{n}</text>')
    b.append(f'<text x="0" y="186" font-size="10" fill="{GUIDE}" class="lab">a curved glint on each drop, upper left: it reads as liquid, not as an eye</text>')
    b.append("</g>")
    return svg((0, 0, W, Hh), "".join(b), "Drop construction")


def drop_sachet(m, uid, x, y, w, rot=0):
    light = TONE[m] in ("#9A6638", "#C49A6C")
    ink = INK if light else CREAM
    nm, nw = word(NAMES[m], DROP_FONT, 100, 0.10, ink)
    k = 34 / 100
    c = (word("MODE", DROP_FONT, 100, 0.10, ink, 40, 70, 0.30)[0] +
         f'<text x="{SW - 40}" y="68" font-size="9.5" text-anchor="end" fill="{ink}" class="lab" opacity=".8">COFFEE</text>' +
         drop_shape(m, 90, 92, 120, ink) +
         word(NAMES[m], DROP_FONT, 100, 0.10, ink, 40, 290, k)[0] +
         f'<text x="40" y="312" font-size="12" fill="{ink}" class="body" opacity=".9">{LINES[m]}</text>'
         f'<text x="40" y="330" font-size="10" fill="{ink}" class="lab" opacity=".7">A DROP, {VERB[m].upper()}</text>'
         f'<text x="40" y="392" font-size="9.5" fill="{ink}" class="lab" opacity=".8">COFFEE CONCENTRATE · 15 ML · FOLD · SQUEEZE · POUR</text>')
    return sachet(c, TONE[m], uid, x, y, w, rot, seal_tone="#fff" if not light else "#000", seal_op=0.14)


def drop_board():
    W, Hh = 1600, 1040
    b = [f'<rect width="{W}" height="{Hh}" fill="#ECE6DC"/>']
    for i, m in enumerate(MODES):
        b.append(drop_sachet(m, f"df{i}", 40 + i * 308, 40, 270))
    # glass of water, a drop of MODE about to land
    gx, gy = 120, 600
    b.append(f'<path d="M{gx} {gy}L{gx + 20} {gy + 330}H{gx + 200}L{gx + 220} {gy}" fill="#FFFFFF" fill-opacity=".55" stroke="#BFB8AC" stroke-width="3"/>'
             f'<path d="M{gx + 10} {gy + 150}L{gx + 20} {gy + 330}H{gx + 200}L{gx + 210} {gy + 150}Z" fill="#C49A6C" opacity=".35"/>'
             + drop_shape("wake", gx + 92, gy + 30, 40, TONE["wake"]) +
             f'<text x="{gx}" y="{gy + 380}" font-size="13" fill="{INK}" class="lab">ONE SACHET, ONE GLASS</text>')
    # app icons, one per state
    for i, m in enumerate(MODES):
        b.append(f'<g transform="translate({420 + i * 90} 640)"><rect width="76" height="76" rx="17" fill="{TONE[m]}"/>{drop_shape(m, 14, 14, 48, CREAM if i < 3 else INK)}</g>')
    b.append(f'<text x="420" y="748" font-size="13" fill="{INK}" class="lab">APP ICONS, ONE PER MODE</text>')
    post = [f'<rect width="420" height="420" fill="{CREAM}"/>', drop_lockup(40, 60, 340, INK)[0],
            f'<text x="40" y="330" font-size="22" fill="{INK}" class="head">Same coffee.</text>'
            f'<text x="40" y="360" font-size="22" fill="{TONE["vital"]}" class="head">Different state.</text>']
    b.append(f'<g transform="translate(900 560)">{"".join(post)}</g>')
    b.append(f'<text x="900" y="1006" font-size="13" fill="{INK}" class="lab">SOCIAL POST</text>')
    return svg((0, 0, W, Hh), "".join(b), "Drop applications").replace("<svg ", '<svg class="mock" ', 1)


def write_masters():
    d = os.path.join(ROOT, "logos", "05-bloom")
    os.makedirs(d, exist_ok=True)
    for s in ("colour", "mono", "reversed"):
        open(os.path.join(d, f"mode-bloom-lockup-{s}.svg"), "w").write(bloom_svg(s))
    for m in MODES:
        open(os.path.join(d, f"mode-bloom-{m}.svg"), "w").write(bloom_svg("colour", lit=m))
    open(os.path.join(d, "mode-bloom-symbol.svg"), "w").write(svg((0, 0, 200, 200), flower(0, 0, 200), "MODE"))
    d = os.path.join(ROOT, "logos", "06-drop")
    os.makedirs(d, exist_ok=True)
    for s in ("colour", "mono", "reversed"):
        open(os.path.join(d, f"mode-drop-lockup-{s}.svg"), "w").write(drop_svg(s))
    for m in MODES:
        open(os.path.join(d, f"mode-drop-{m}.svg"), "w").write(svg((-6, -6, 112, 112), drop_shape(m, 0, 0, 100, TONE[m]), f"MODE {NAMES[m]}"))


if __name__ == "__main__":
    write_masters()
    print("masters written")
