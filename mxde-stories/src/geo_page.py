"""MODE · three geometric options (after Fletcher and Hollenstein) → presentation/mode-geometric.html"""
import html
import os
from shapely.geometry import box
from shapely import affinity
from letters import svg, P
import geo
from five_six import d_of, word
from three_four import sachet, SW, SH

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
K = "#151515"
CREAM = "#F6F2EA"
COL = {"wake": "#E39B2D", "active": "#D2462E", "zen": "#2E6E5B", "vital": "#7FA83A", "calm": "#3D4F7A"}
NAME = {m: m.upper() for m in geo.MODES}
LINE = {"wake": "Rising. For a sharp start.", "active": "Forward. For the push.", "zen": "Whole. For deep focus.",
        "vital": "Growing. For a midday reset.", "calm": "Resting. For a slow evening."}
FONT = "InstrumentSans-SemiBold.ttf"
esc = html.escape


def paths(parts, fill=K, colour=None, skip=()):
    out = ""
    for k, g in parts.items():
        if k in skip:
            continue
        f = colour.get(k, fill) if colour else fill
        out += P(d_of(g), f)
    return out


def fit(body, bounds, x, y, w):
    """Place artwork with given bounds (minx, miny, maxx, maxy) at (x, y), scaled to width w."""
    bx0, by0, bx1, by1 = bounds
    k = w / (bx1 - bx0)
    return f'<g transform="translate({x:.2f} {y:.2f}) scale({k:.4f}) translate({-bx0:.2f} {-by0:.2f})">{body}</g>', (by1 - by0) * k


def wm(kind, mode=None, ink=K):
    if kind == "A":
        p, w = geo.one_half_final()
        return paths(p, ink), (0, 0, w, 100)
    if kind == "B":
        p, w, _ = geo.slot_o(mode=mode)
        return paths(p, ink, {"fill": COL[mode]} if mode else None), (0, 0, w, 100)
    p, w = geo.block_final(mode=mode)
    return paths(p, ink, {"O": COL[mode]} if mode else None), (0, 0, w, w)


def S(vb, body, cls="mk"):
    return svg(vb, body).replace("<svg ", f'<svg class="{cls}" ', 1)


# ------------------------------------------------------------------ frames
def frames_A():
    Wf, Hf = 360, 220
    fr = lambda b: S((0, 0, Wf, Hf), b, "fr")
    out = [("Start with one shape: half a circle.", fr(P(d_of(geo.half(180, 140, 70, "up")), "currentColor")))]
    m = geo.place(geo.one_half_final()[0]["M"], 0, 0)
    out.append(("Turn two of them up and you have an m.", fr(fit(P(d_of(m), "currentColor"), m.bounds, 80, 110, 200)[0])))
    p, w = geo.one_half_final()
    mo = paths({k: p[k] for k in ("M", "O")}, "currentColor")
    out.append(("Turn two to face outward: the O.", fr(fit(mo, (0, 0, p["O"].bounds[2], 100), 50, 70, 260)[0])))
    out.append(("One faces forward: D. One faces back, cut twice: E.", fr(fit(paths(p, "currentColor"), (0, 0, w, 100), 30, 70, 300)[0])))
    out.append(("Six turns of one shape spell MODE.", fr(fit(paths(p, "currentColor"), (0, 0, w, 100), 30, 70, 300)[0]
                                                        + f'<text x="180" y="190" font-size="12" text-anchor="middle" fill="#8C8780" class="lab">6 × the same half-circle</text>')))
    kit = "".join(P(d_of(geo.mode_shape(m, 40 + i * 70, 110, 28)), COL[m]) for i, m in enumerate(geo.MODES))
    labs = "".join(f'<text x="{40 + i * 70}" y="168" font-size="10" text-anchor="middle" fill="{COL[m]}" class="lab">{NAME[m]}</text>' for i, m in enumerate(geo.MODES))
    out.append(("Turn it once more for each mode: rising, forward, whole, growing, resting.", fr(kit + labs)))
    return out


def frames_B():
    Wf, Hf = 360, 220
    fr = lambda b: S((0, 0, Wf, Hf), b, "fr")
    p, w, (cx, cy) = geo.slot_o()
    solid = dict(p)
    solid["O"] = geo.disc(cx, cy, 50)
    out = [("MODE, built from squares and half-circles.", fr(fit(paths(solid, "currentColor"), (0, 0, w, 100), 40, 70, 280)[0]))]
    out.append(("Empty the O. Leave two thin arcs.", fr(fit(paths(p, "currentColor"), (0, 0, w, 100), 40, 70, 280)[0])))
    for m, cap in (("wake", "The O is a slot. Fill it with the mode you're in: Wake rises."),
                   ("zen", "Zen fills it whole."), ("calm", "Calm rests at the bottom.")):
        pm, w, _ = geo.slot_o(mode=m)
        out.append((cap, fr(fit(paths(pm, "currentColor", {"fill": COL[m]}), (0, 0, w, 100), 40, 70, 280)[0])))
    row = ""
    for i, m in enumerate(geo.MODES):
        ring = geo.slot_o(mode=m)[0]
        sub = {"O": ring["O"], "fill": ring["fill"]}
        b, h = fit(paths(sub, "currentColor", {"fill": COL[m]}), (114, 0, 214, 100), 22 + i * 66, 80, 54)
        row += b + f'<text x="{49 + i * 66}" y="160" font-size="9.5" text-anchor="middle" fill="{COL[m]}" class="lab">{NAME[m]}</text>'
    out.append(("Five modes, one word.", fr(row)))
    return out


def frames_C():
    Wf, Hf = 360, 220
    fr = lambda b: S((0, 0, Wf, Hf), b, "fr")
    p, w = geo.block_final()
    s, g = 100.0, 8.0
    row = {"M": p["M"], "O": p["O"], "D": geo.place(p["D"], 2 * s + 2 * g, -(s + g)), "E": geo.place(p["E"], 2 * s + 2 * g, -(s + g))}
    out = [("Four letters, four tiles of the same size.", fr(fit(paths(row, "currentColor"), (0, 0, 4 * s + 3 * g, s), 30, 80, 300)[0]))]
    out.append(("Stack them: MO over DE.", fr(fit(paths(p, "currentColor"), (0, 0, w, w), 120, 30, 120)[0])))
    out.append(("One square. A stamp you can put on anything.", fr(fit(paths(p, "currentColor"), (0, 0, w, w), 105, 18, 150)[0])))
    for m, cap in (("wake", "The O tile turns with the mode. Wake rises."), ("active", "Active moves forward."), ("calm", "Calm rests.")):
        pm, w = geo.block_final(mode=m)
        out.append((cap, fr(fit(paths(pm, "currentColor", {"O": COL[m]}), (0, 0, w, w), 120, 30, 120)[0])))
    return out


def reel(frames, rid, start=None):
    start = len(frames) - 2 if start is None else start
    stage = "".join(f'<div class="frame" data-i="{i}"{" data-on" if i == start else ""}>{s}</div>' for i, (_, s) in enumerate(frames))
    thumbs = "".join(f'<li><button type="button" class="th{" on" if i == start else ""}" data-i="{i}" aria-label="Frame {i + 1}">{s}'
                     f'<span>{esc(c)}</span></button></li>' for i, (c, s) in enumerate(frames))
    return (f'<div class="reel" id="{rid}"><div class="stage">{stage}</div><p class="stage-cap" aria-live="polite">{esc(frames[start][0])}</p>'
            f'<div class="reel-ctl"><button type="button" class="ghost play" aria-pressed="false">Play the flow</button></div>'
            f'<ol class="thumbs" style="grid-template-columns:repeat({len(frames)},minmax(0,1fr))">{thumbs}</ol></div>')


# ------------------------------------------------------------------ sachets
def sachet_A(m, uid, x, y, w):
    body, b = wm("A")
    logo, _ = fit(body, b, 40, 44, 150)
    c = (logo + f'<text x="{SW - 40}" y="64" font-size="9.5" text-anchor="end" fill="{K}" class="lab">COFFEE</text>'
         + P(d_of(geo.mode_shape(m, SW / 2, 172, 74)), COL[m])
         + word(NAME[m], FONT, 100, 0.14, K, 40, 300, 0.30)[0]
         + f'<text x="40" y="322" font-size="12" fill="{K}" class="body">{LINE[m]}</text>'
         f'<text x="40" y="392" font-size="9.5" fill="{K}" class="lab" opacity=".75">COFFEE CONCENTRATE · 15 ML · FOLD · SQUEEZE · POUR</text>')
    return sachet(c, CREAM, uid, x, y, w)


def sachet_B(m, uid, x, y, w):
    body, b = wm("B", m)
    logo, _ = fit(body, b, 34, 120, 232)
    c = (f'<text x="34" y="66" font-size="9.5" fill="{K}" class="lab">COFFEE CONCENTRATE</text>' + logo
         + word(NAME[m], FONT, 100, 0.14, COL[m], 34, 300, 0.30)[0]
         + f'<text x="34" y="322" font-size="12" fill="{K}" class="body">{LINE[m]}</text>'
         f'<text x="34" y="392" font-size="9.5" fill="{K}" class="lab" opacity=".75">15 ML · FOLD · SQUEEZE · POUR</text>')
    return sachet(c, CREAM, uid, x, y, w)


def sachet_C(m, uid, x, y, w):
    body, b = wm("C", m)
    logo, _ = fit(body, b, 60, 50, 180)
    c = (logo + word(NAME[m], FONT, 100, 0.14, K, 60, 300, 0.30)[0]
         + f'<rect x="60" y="314" width="40" height="5" fill="{COL[m]}"/>'
         f'<text x="60" y="340" font-size="12" fill="{K}" class="body">{LINE[m]}</text>'
         f'<text x="60" y="392" font-size="9.5" fill="{K}" class="lab" opacity=".75">COFFEE CONCENTRATE · 15 ML</text>')
    return sachet(c, CREAM, uid, x, y, w)


def board(fn, kind):
    W, Hh = 1600, 560
    b = [f'<rect width="{W}" height="{Hh}" fill="#E7E1D6"/>']
    for i, m in enumerate(geo.MODES):
        b.append(fn(m, f"{kind}{i}", 40 + i * 308, 50, 270))
    return S((0, 0, W, Hh), "".join(b), "mock")


def icon(kind, bg=K, fg=CREAM, mode=None):
    if kind == "A":
        g = geo.mode_shape(mode or "zen", 90, 90, 56) if mode else geo.one_half_final()[0]["O"]
        if not mode:
            body, h = fit(P(d_of(g), fg), g.bounds, 40, 40, 100)
        else:
            body = P(d_of(g), fg)
    elif kind == "B":
        p, w, (cx, cy) = geo.slot_o(mode=mode or "wake")
        sub = {"O": p["O"], "fill": p["fill"]}
        body, h = fit(paths(sub, fg, {"fill": COL[mode or "wake"]}), (cx - 50, cy - 50, cx + 50, cy + 50), 40, 40, 100)
    else:
        p, w = geo.block_final()
        body, h = fit(paths(p, fg), (0, 0, w, w), 36, 36, 108)
    return S((0, 0, 180, 180), f'<rect width="180" height="180" rx="40" fill="{bg}"/>' + body, "ic")


def option(letter, name, lineage, idea, story, frames, kit_note, bold_rows):
    a = wm(letter)
    hero = S((a[1][0] - 8, a[1][1] - 8, a[1][2] - a[1][0] + 16, a[1][3] - a[1][1] + 16), a[0], "hero-mark")
    rev = S((a[1][0] - 8, a[1][1] - 8, a[1][2] - a[1][0] + 16, a[1][3] - a[1][1] + 16), wm(letter, ink=CREAM)[0], "hero-mark")
    modes = ""
    for m in geo.MODES:
        if letter == "A":
            modes += f'<figure class="md">{S((0, 0, 200, 200), P(d_of(geo.mode_shape(m, 100, 100, 70)), COL[m]))}<figcaption>{NAME[m]}</figcaption></figure>'
        else:
            body, bb = wm(letter, m)
            modes += f'<figure class="md">{S((bb[0] - 6, bb[1] - 6, bb[2] - bb[0] + 12, bb[3] - bb[1] + 12), body)}<figcaption>{NAME[m]}</figcaption></figure>'
    ladder = "".join(f'<figure><div style="height:{px}px">{S((a[1][0] - 2, a[1][1] - 2, a[1][2] - a[1][0] + 4, a[1][3] - a[1][1] + 4), a[0], "lad")}</div><figcaption>{px} px</figcaption></figure>'
                     for px in (16, 24, 32, 48))
    fn = {"A": sachet_A, "B": sachet_B, "C": sachet_C}[letter]
    return f"""
<section class="logo" id="opt-{letter.lower()}">
  <div class="wrap">
    <header class="logo-head"><p class="eyebrow">Option {letter} · after {esc(lineage)}</p><h2>{esc(name)}</h2><p class="lede">{esc(idea)}</p></header>
    <div class="hero-panel">{hero}</div>
    <div class="variants"><div class="v v-paper">{a and S((a[1][0] - 8, a[1][1] - 8, a[1][2] - a[1][0] + 16, a[1][3] - a[1][1] + 16), wm(letter, ink="#000")[0])}</div><div class="v v-dark">{rev}</div></div>
    <div class="cols"><div><h3>The idea</h3><div class="story">{"".join(f"<p>{esc(p)}</p>" for p in story)}</div>
        <h3 class="mt">At every size</h3><div class="ladder">{ladder}</div><div class="icons">{icon(letter)}{icon(letter, CREAM, K, "zen") if letter != "C" else icon(letter, COL["zen"], CREAM)}</div></div>
      <div><h3>The flow</h3>{reel(frames, "reel-" + letter)}</div></div>
    <h3 class="mt">Five modes</h3><p class="note">{esc(kit_note)}</p><div class="modes">{modes}</div>
    <h3 class="mt">On the sachet</h3><div class="board">{board(fn, letter)}</div>
    <div class="cols mt"><div><h3>Why it works</h3><ul class="ticks">{"".join(f"<li>{esc(w)}</li>" for w in bold_rows[0])}</ul></div>
      <div><h3>Watch out for</h3><ul class="risks">{"".join(f"<li>{esc(r)}</li>" for r in bold_rows[1])}</ul></div></div>
  </div>
</section>"""


def build():
    A = option("A", "One Half", "Alan Fletcher's Design Objectives",
               "Every letter of MODE is the same half-circle, turned. Two face up for the m, two face out for the O, one faces forward for the D, one faces back with two cuts for the E.",
               ["Six turns of one shape spell the name. That's the brand in one sentence: one coffee, turned into whatever mode you need.",
                "The modes come out of the same kit. Turn the half-circle once more and you get each mode's sign: rising for Wake, forward for Active, whole for Zen, growing for Vital, resting for Calm.",
                "Nothing in it is a coffee cliché. It's a precise little system you can draw from memory, which is exactly why people remember it."],
               frames_A(),
               "One half-circle, five positions. Rising, forward, whole, turned up and on, resting. Every sign has its own silhouette, so the modes read apart in one colour.",
               (["The construction is the story: one shape, turned. It explains itself in a sentence.",
                 "The mode signs come from the same kit as the letters, so the range always looks like one family.",
                 "Big, simple shapes print well on a small sachet, emboss cleanly and survive 16 px.",
                 "It has a playful lowercase m against capital O, D, E: friendly without being cute."],
                ["The m is twice as wide as the other letters, so the word is long. On tight spaces use the O on its own.",
                 "Half-circle alphabets have history (Fletcher's DO is the obvious ancestor). This one is specific to MODE, but a trademark search should check.",
                 "Vital's turned half-circle is the least obvious of the five signs; it may need the name beside it at first."]))
    B = option("B", "The Slot", "Albert Hollenstein's L'Echoppe",
               "Solid M, D and E from squares and half-circles. The O is two thin arcs: an open slot, and each mode fills it with its own shape.",
               ["The O is the only round, open letter in MODE, so it becomes the place where the state changes. Two thin arcs hold it open, the way Hollenstein's fine lines hold his solid shapes.",
                "Empty, it's the brand. Filled, it's a mode: Wake rises inside it, Zen fills it whole, Calm settles at the bottom.",
                "On every sachet the word stays the same and only the slot changes. You can tell which mode you're holding from across the room."],
               frames_B(),
               "The same five signs as Option A, placed inside the O. The word never changes, only what's in the slot.",
               (["The word stays readable in every mode. Only one letter changes, and it changes on purpose.",
                 "Solid shapes and thin lines together give it a crafted, editorial feel: premium, not playful.",
                 "The empty O is a simple, ownable icon on its own."],
                ["The thin arcs need care at small sizes. Below about 20 px, use the solid version of the O.",
                 "The solid M with its V notch is heavy. It balances against D and E, but keep plenty of space around the logo."]))
    C = option("C", "Block", "both, compressed into a stamp",
               "MO over DE: four tiles of one square, each a letter from the same kit. A stamp, ready for a sachet, a seal or an app icon.",
               ["A square is the most useful shape a small brand can own: it fits a sachet corner, a sticker, an app icon, a box seal.",
                "Each tile is one letter: an m with two arches, a full O, a D from a square and a half-circle, an E cut twice. Stacked, they read MODE in one block.",
                "The O tile is the switch. In each mode it turns into that mode's sign."],
               frames_C(),
               "The O tile shows the mode. The other three tiles never change, so the stamp is always recognisable.",
               (["Compact and square: the strongest of the three for small spaces and icons.",
                 "Reads MODE in one look, top to bottom.",
                 "Works as a seal: emboss it, stamp it on kraft, print it in one colour."],
                ["Stacked words read a beat slower than a single line. Pair it with a horizontal wordmark for headlines.",
                 "The m tile's arches are small. Below 24 px they fill in, but the block still reads."]))
    page = open(os.path.join(ROOT, "presentation", "mxde-logos-3-4.html")).read()
    a = page.index('<header class="intro">')
    b = page.index("<footer>")
    head = """
<header class="intro"><div class="wrap">
  <p class="eyebrow">MODE · geometric letters · three options</p>
  <h1>MODE, from a box of shapes.</h1>
  <p class="lede">After Alan Fletcher's Design Objectives and Albert Hollenstein's L'Echoppe: letters built from half-circles, squares and thin arcs, where one gap or one turn tells the story. Three options, one system of mode signs shared by all of them.</p>
  <nav class="method" aria-label="The three options" style="grid-template-columns:repeat(3,minmax(0,1fr))">
    <a href="#opt-a"><span>Option A · after Fletcher</span><b>One Half</b><span>Every letter is the same half-circle, turned.</span></a>
    <a href="#opt-b"><span>Option B · after Hollenstein</span><b>The Slot</b><span>The O is an open slot each mode fills.</span></a>
    <a href="#opt-c"><span>Option C · a stamp</span><b>Block</b><span>MO over DE in one square; the O tile turns.</span></a>
  </nav>
</div></header>"""
    tail = """
<section class="compare"><div class="wrap">
  <p class="eyebrow">My pick</p><h2 style="font-size:clamp(28px,4vw,44px)">Option A, with C as its stamp</h2>
  <div class="next"><p>One Half has the best story: one shape, turned, is the whole brand, and the mode signs fall straight out of it. Block is the natural partner for tight spaces: the same kit, stacked into a square for the sachet corner and the app icon. The Slot is the most elegant of the three, and the right choice if you want the word to stay fixed while only the O changes.</p>
  <p>Tell me which one to take further, or what to mix.</p></div>
</div></section>"""
    page = page[:a] + head + A + B + C + tail + page[b:]
    page = page.replace("<title>MXDE Logos Three and Four</title>", "<title>MODE Geometric Options</title>")
    page = page.replace("MXDE logo exploration, logos 3 and 4. The marks are drawn from geometry; COFFEE is set in Instrument Sans and Archivo.",
                        "MODE, geometric letter options after Alan Fletcher and Albert Hollenstein. Drawn from half-circles, squares and arcs; mode names set in Instrument Sans.")
    page = page.replace(".modes{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:10px}",
                        ".modes{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:10px}\n.md{margin:0;background:#fff;border:1px solid var(--line);padding:14px;display:grid;gap:8px;color:#151515}.md figcaption{font-size:12px;letter-spacing:.08em;color:var(--muted)}\n.hero-panel .hero-mark{max-height:340px}\n.variants .v svg{max-height:180px;width:auto;max-width:100%;margin:0 auto;display:block}")
    page = page.replace('.th span{display:none}', '.th span{display:none} .th .fr{color:#151515}')
    out = os.path.join(ROOT, "presentation", "mode-geometric.html")
    open(out, "w").write(page)
    return out, len(page)


if __name__ == "__main__":
    p, n = build()
    print(p, f"{n / 1024:.0f} KB")
