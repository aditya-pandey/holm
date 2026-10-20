"""MODE after Hollenstein's L'Echoppe: three marks → presentation/mode-echoppe.html"""
import html
import os
from shapely.geometry import box
from shapely.ops import unary_union
from shapely import affinity
from letters import P
from five_six import d_of
from three_four import sachet, SW, SH
from geo import half, arc_line, disc
import echoppe as ec
from geo2_page import S, fit, TEMPLATE

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
K = "#151515"
CREAM = "#F4EFE6"
COFFEE = "#3A2618"
KRAFT = "#CDAA80"
esc = html.escape


def draw(parts, fill=K, op=None):
    o = f' opacity="{op}"' if op is not None else ""
    return "".join(P(d_of(g), fill, o) for g in parts.values() if g is not None and not g.is_empty)


def bounds(parts):
    return unary_union([g for g in parts.values() if g is not None and not g.is_empty]).bounds


def vb_of(parts, pad=8):
    b = bounds(parts)
    return (b[0] - pad, b[1] - pad, b[2] - b[0] + 2 * pad, b[3] - b[1] + 2 * pad)


OPTS = {
    "1": dict(name="Quarters", sub="lowercase, in Hollenstein's own letters",
              idea=["Hollenstein drew an e: a half-disc, a quarter-disc and one hairline closing the bowl. I kept that e exactly as he drew it, and built the other three letters of mode from the same parts.",
                    "The m is two quarter shoulders on two squares, cut at the centre line where the e is cut. The o is a cup, half full: poured solid below, a hairline above. The d's ascender is a hairline that rises off the stem and curls over, like steam off the cup beside it.",
                    "Read it once and it says mode. Look again and there is a coffee in it, with the steam still rising."],
              works=["It reads mode at a glance: the shapes are the letters, not a puzzle.",
                     "The coffee is in the word, not added on: a half-full cup and its steam, both made from type.",
                     "Lowercase and round, so it feels warm and easy to live with, like an everyday drink."],
              watch=["Hairlines vanish at small sizes. At 32 px and below, use the small-size cut, which draws them heavier: icons, favicons, tiny print.",
                     "The steam sets the top of the logo. Give it clear space above, or it looks cramped."]),
    "2": dict(name="Hold & Finish", sub="capitals, half solid, half line",
              idea=["The reference has one rule at its heart: the solid shapes hold the letter, and a hairline finishes it. The 5 is a square and a line. The e is two solids and a line.",
                    "Here that rule is the whole logo. In every capital, the solid part holds the letter and a hairline completes it. M: the shoulders hold, the legs are lines. O: half solid, half line. D: a stem and a line. E: a stem and three lines.",
                    "It's a cup half poured, letter by letter, and a pack can be designed the same way: half solid, half line."],
              works=["One rule, applied four times: easy to explain, hard to forget.",
                     "Capitals give it authority on shelf. The hairlines keep it light rather than heavy.",
                     "The rule carries to the pack: fill half the sachet and leave the other half open."],
              watch=["The hairlines are the letters' second halves; if they disappear, it reads as four blocks. Use the heavier cut at 32 px and below.",
                     "Print the hairlines no thinner than 0.25 mm."]),
    "3": dict(name="Pour", sub="the reference's composition, re-read as a coffee",
              idea=["L'Echoppe has a cast: a square at top left, a half-disc, and hairline arcs that fly off it. It reads as 5é, and also as a little still life.",
                    "Pour keeps that cast and puts it to work. The square is the sachet. Its hairline arcs over and pours into the half-disc, which is the cup. A second hairline rises off the cup as steam, and a third is the handle.",
                    "Underneath, set the way the reference sets L'Echoppe: MODE in bold, Coffee in regular. Just the name and coffee."],
              works=["A real symbol: the whole product story in four shapes, from sachet to cup.",
                     "Works without the name: on the sachet's tear notch, as an app icon, on a cup sleeve.",
                     "The type is plain, so the symbol stays the hero."],
              watch=["It's a symbol plus a name, not a wordmark. Always lock up the two together at first.",
                     "The handle and steam are hairlines; use the heavier cut at 32 px and below."]),
}


def plate(k, ink=K, bg="#FFFFFF", caption=True):
    parts = ec.mark(k)
    vb = vb_of(parts, 10)
    mark = S(vb, draw(parts, ink), "plate-mark" + (" sym" if k == "3" else ""))
    if not caption:
        cap = ""
    elif k == "3":
        cap = '<figcaption><b>MODE</b><span>Coffee</span></figcaption>'
    else:
        cap = f'<figcaption><b>{esc(OPTS[k]["name"])}</b><span>{esc(OPTS[k]["sub"])}</span></figcaption>'
    return f'<figure class="plate" style="background:{bg}">{mark}{cap}</figure>'


def kit(k):
    """The construction: each part named."""
    items = []
    if k == "1":
        for f, t in ((ec.m_, "m · two shoulders on two squares"), (ec.o_, "o · a cup, half full"),
                     (ec.d_, "d · the ascender is steam"), (ec.e_, "e · Hollenstein's e, unchanged")):
            g, w = f(0)
            items.append((g, t))
    elif k == "2":
        for f, t in ((ec.M_, "M · shoulders hold, legs are lines"), (ec.O_, "O · half solid, half line"),
                     (ec.D_, "D · a stem and a line"), (ec.E_, "E · a stem and three lines")):
            g, w = f(0)
            items.append((g, t))
    else:
        p = ec.pour()
        cx, top = 2 * ec.R + ec.G, ec.R + ec.G
        pieces = [(box(0, 0, ec.R, ec.R), "square · the sachet"),
                  (arc_line(ec.R + ec.G, ec.R, ec.R - ec.W / 2, -90, -4, ec.W), "hairline · the pour"),
                  (half(cx, top, ec.R, "down"), "half-disc · the cup"),
                  (arc_line(cx + 14 + ec.R, top - ec.A, ec.R, 180, 232, ec.W), "hairline · the steam")]
        out = ""
        vb = vb_of(p, 8)
        for g, t in pieces:
            body = draw(p, K, op=".14") + P(d_of(g), K)
            out += f'<figure class="k">{S(vb, body)}<figcaption>{esc(t)}</figcaption></figure>'
        return out
    out = ""
    for g, t in items:
        g = {kk: v for kk, v in g.items() if v is not None}
        out += f'<figure class="k">{S(vb_of(g, 6), draw(g))}<figcaption>{esc(t)}</figcaption></figure>'
    return out


def ladder(k):
    cells = ""
    for px, w in ((16, 9.0), (24, 7.0), (32, 4.5), (48, None)):
        parts = ec.mark(k, w)
        cells += f'<figure><div style="height:{px}px">{S(vb_of(parts, 2), draw(parts), "lad")}</div><figcaption>{px} px</figcaption></figure>'
    return f'<div class="ladder">{cells}</div>'


def placed(parts, x, y, w, fill):
    b = bounds(parts)
    return fit(draw(parts, fill), b, x, y, w)


def sachet_for(k):
    lab = lambda y, t, fill, op=1, anchor="start", x=40: (f'<text x="{x}" y="{y}" font-size="10" fill="{fill}" class="lab" '
                                                         f'text-anchor="{anchor}" opacity="{op}">{t}</text>')
    if k == "1":
        word, h = placed(ec.mark("1"), 40, 64, 196, K)
        g, _ = ec.o_(0)
        cup = fit(draw(g, K), (0, 0, 100, 100), 112, 252, 236)[0]
        c = (word + lab(150, "COFFEE CONCENTRATE", K) + lab(168, "15 ML · FOLD · SQUEEZE · POUR", K, .75) + cup)
        return sachet(c, CREAM, f"e{k}", 0, 0, 280)
    if k == "2":
        word, h = placed(ec.mark("2"), 40, 92, 220, K)
        c = (f'<rect x="0" y="{SH / 2}" width="{SW}" height="{SH / 2}" fill="{COFFEE}"/>'
             + lab(74, "COFFEE CONCENTRATE", K) + word
             + f'<line x1="40" x2="{SW - 40}" y1="{SH / 2 - 26}" y2="{SH / 2 - 26}" stroke="{K}" stroke-width="1"/>'
             + lab(SH / 2 - 36, "HALF SOLID, HALF LINE", K, .6)
             + lab(400, "15 ML · FOLD · SQUEEZE · POUR", CREAM, .85))
        return sachet(c, CREAM, f"e{k}", 0, 0, 280)
    sym, h = placed(ec.mark("3"), 70, 84, 160, K)
    c = (sym + f'<text x="{SW / 2}" y="{84 + h + 92}" font-size="25" text-anchor="middle" fill="{K}" class="wm">MODE</text>'
         f'<text x="{SW / 2}" y="{84 + h + 120}" font-size="21" text-anchor="middle" fill="{K}" class="wr">Coffee</text>'
         + lab(400, "15 ML · FOLD · SQUEEZE · POUR", K, .75, "middle", SW / 2))
    return sachet(c, KRAFT, f"e{k}", 0, 0, 280)


def icon(k):
    if k == "1":
        g, _ = ec.o_(0)
        b, h = fit(draw(g, CREAM), (0, 0, 100, 100), 45, 45, 90)
        return S((0, 0, 180, 180), f'<rect width="180" height="180" rx="40" fill="{K}"/>' + b, "ic")
    if k == "2":
        g, _ = ec.O_(0)
        b, h = fit(draw(g, CREAM), (0, 0, 103, 100), 43, 45, 92)
        return S((0, 0, 180, 180), f'<rect width="180" height="180" rx="40" fill="{COFFEE}"/>' + b, "ic")
    parts = ec.mark("3", 4.5)
    b, h = placed(parts, 30, 0, 120, K)
    return S((0, 0, 180, 180), f'<rect width="180" height="180" rx="40" fill="{CREAM}"/>'
             + f'<g transform="translate(0 {(180 - h) / 2:.1f})">{b}</g>', "ic")


def section(k):
    o = OPTS[k]
    return f"""
<section class="opt" id="o{k}"><div class="wrap">
  <p class="eyebrow">Design {k} · {esc(o["name"])}</p>
  {plate(k)}
  <div class="cols">
    <div><h2>{esc(o["name"])}</h2><div class="idea">{"".join(f"<p>{esc(p)}</p>" for p in o["idea"])}</div></div>
    <div><h3>How it's built</h3><div class="kit">{kit(k)}</div></div>
  </div>
  <div class="row3">
    <div><h3>At every size</h3>{ladder(k)}<p class="note">At 32 px and below, the hairlines are drawn heavier.</p></div>
    <div><h3>Reversed</h3>{plate(k, CREAM, K, caption=False)}</div>
    <div class="apps"><div>{S((0, 0, 300, 450), sachet_for(k), "sach")}</div><div>{icon(k)}</div></div>
  </div>
  <div class="cols"><div><h3>Why it works</h3><ul>{"".join(f"<li>{esc(w)}</li>" for w in o["works"])}</ul></div>
    <div><h3>Watch out for</h3><ul class="watch">{"".join(f"<li>{esc(w)}</li>" for w in o["watch"])}</ul></div></div>
</div></section>"""


def grammar():
    """What I took from the reference, drawn in its own parts."""
    R, G, W = ec.R, ec.G, ec.W
    cells = [
        (P(d_of(unary_union([box(0, 0, R, R), half(R + G + R, R, R, "left").intersection(box(R + G, 0, 2 * R + G, 2 * R)),
                             ec.quarter(2 * R + 2 * G, R, R, "ne")])), K), (-4, -4, 3 * R + 12, 2 * R + 8),
         "Three solids, one radius", "A square, a half-disc and a quarter-disc. The square's side is the circle's radius."),
        (P(d_of(unary_union([half(R, R, R, "left"), half(R + 3 * G, R, R, "right")])), K), (-4, -4, 2 * R + 3 * G + 8, 2 * R + 8),
         "Solids never touch", "A thin cut always runs between two shapes. The cut is where you read the joins."),
        (P(d_of(unary_union([ec.quarter(0, R, R, "ne"), arc_line(0, R, R - W, 10, 90, W * 1.6)])), K), (-6, -4, R + 14, 2 * R + 8),
         "Hairlines finish the letter", "An arc on the same radius completes what the solids leave out."),
        (P(d_of(ec.pour()["solid"]), K) + P(d_of(ec.pour()["hair"]), K), vb_of(ec.pour(), 6),
         "It reads two ways", "5é is also a little picture. A good mark from this kit should be a word and a thing."),
    ]
    out = ""
    for body, vb, t, s in cells:
        out += f'<figure class="g">{S(vb, body)}<figcaption><b>{esc(t)}</b><span>{esc(s)}</span></figcaption></figure>'
    return f'<div class="grammar">{out}</div>'


EXTRA_CSS = """
.wm{font-family:'Instrument Sans',system-ui,sans-serif;font-weight:700;letter-spacing:.01em}
.wr{font-family:'Instrument Sans',system-ui,sans-serif;font-weight:400}
.plate .plate-mark.sym{width:min(100%,300px)}
.grammar{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px;margin-top:28px}
.g{margin:0;background:var(--surface);border:1px solid var(--line);padding:18px;display:grid;gap:14px;align-content:start}
.g svg{height:72px;width:auto;max-width:100%;color:#151515}
:root[data-theme="dark"] .g svg path,.g svg path{fill:var(--ink)}
.g figcaption{display:grid;gap:4px;font-size:14px}
.g figcaption span{color:var(--muted)}
.note{font-size:13px;color:var(--muted);margin-top:8px}
@media (max-width:860px){.grammar{grid-template-columns:repeat(2,minmax(0,1fr))}}
"""


def build():
    toc = ""
    for k, o in OPTS.items():
        parts = ec.mark(k)
        toc += f'<a href="#o{k}">{S(vb_of(parts, 6), draw(parts))}<span>Design {k} · {esc(o["name"])}</span></a>'
    body = f"""
<header class="intro"><div class="wrap">
  <p class="eyebrow">MODE · after Albert Hollenstein, L'Echoppe</p>
  <h1>Three marks from one small kit.</h1>
  <p class="lede">Hollenstein's L'Echoppe mark uses one square, two pieces of a circle and three hairlines, and it reads as a number, a letter and a picture at once. I took only its grammar, nothing else, and drew MODE three ways with it.</p>
  <h3 style="margin-top:40px">What I took from it</h3>
  {grammar()}
  <nav class="toc" aria-label="Designs">{toc}</nav>
</div></header>
{section("1")}{section("2")}{section("3")}
<section class="close"><div class="wrap"><h3>My pick</h3>
  <p>Quarters is the one I'd take forward. It's the closest to the spirit of the reference: real letters made from pure parts, and a coffee hidden in the word. Pour is the strongest symbol and the best if you want an icon that works without the name. Hold &amp; Finish is the boldest on a shelf. Tell me which to develop.</p></div></section>"""
    page = (TEMPLATE.replace("<title>MODE Three Marks</title>", "<title>MODE After Echoppe</title>")
            .replace("</style>", EXTRA_CSS + "</style>").replace("{{BODY}}", body))
    out = os.path.join(ROOT, "presentation", "mode-echoppe.html")
    open(out, "w").write(page)
    return out, len(page)


if __name__ == "__main__":
    p, n = build()
    print(p, f"{n / 1024:.0f} KB")
