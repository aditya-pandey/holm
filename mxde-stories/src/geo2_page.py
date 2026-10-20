"""MODE, one brand: three geometric logos → presentation/mode-three.html"""
import html
import os
from shapely.geometry import box
from letters import svg, P
import geo
import geo2
from five_six import d_of
from three_four import sachet, SW, SH

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
K = "#151515"
CREAM = "#F4EFE6"
COFFEE = "#3A2618"
esc = html.escape


def draw(parts, fill=K):
    return "".join(P(d_of(g), fill) for g in parts.values())


def S(vb, body, cls=""):
    c = f' class="{cls}"' if cls else ""
    return svg(vb, body).replace("<svg ", f"<svg{c} ", 1)


def fit(body, bounds, x, y, w):
    bx0, by0, bx1, by1 = bounds
    k = w / (bx1 - bx0)
    return f'<g transform="translate({x:.2f} {y:.2f}) scale({k:.4f}) translate({-bx0:.2f} {-by0:.2f})">{body}</g>', (by1 - by0) * k


OPTS = {
    "1": dict(name="Two Shapes", after="after Alan Fletcher",
              make=lambda: geo2.two_shapes(),
              idea=["MODE is two shapes, each used twice. A comb is the E; turn it a quarter and it's the m. A circle is the O; cut it in half and it's the D.",
                    "Square, circle, half, square. The word has a rhythm you can draw from memory, and nothing in it is decoration.",
                    "It's the plainest way to say what the name says: one thing, put a different way."],
              works=["Reads MODE at a glance, even at 16 px.", "Four heavy silhouettes: unmistakable on a small sachet, embossed or printed in one colour.",
                     "The construction explains itself in a sentence, which makes it easy to remember and repeat."],
              watch=["The m is a lowercase form among capitals. That's the charm, but set it with care beside other type.",
                     "Heavy marks need air: keep a clear space of half a letter all round."]),
    "2": dict(name="Lines", after="after Lance Wyman's Mexico 68",
              make=lambda: geo2.lines_open(),
              idea=["MODE is never solid. Each letter is three parallel strokes that follow its skeleton and stop open at the ends: the M a triple zigzag, the O three rings, the E a triple bracket.",
                    "Lines like these vibrate. The word seems to hum, the way a good coffee hums along in the background of a morning.",
                    "It's the most expressive of the three: a logo that can run off the edge of a pack, or turn into a pattern."],
              works=["Instantly distinctive: nothing in coffee looks like it.", "Becomes a pattern for free: extend the lines and the pack is covered.",
                     "Light and airy, so it feels fresh rather than heavy."],
              watch=["Fine lines close up below about 24 px. Use the single-line cut (shown below) for icons and tiny print.",
                     "Line logos depend on print quality; specify the minimum line weight with the printer."]),
    "3": dict(name="Counters", after="after the negative space of Fletcher and Hollenstein",
              make=lambda: geo2.counters(),
              idea=["One black bar, four cuts. Only the counters (the holes inside letters) are cut out: a V for the M, a circle for the O, a half-circle for the D, two slots for the E.",
                    "You read the name from what's missing. It takes a beat, and that beat is the moment people remember.",
                    "On the sachet the bar becomes a band, like a seal across the pack. The ground colour shows through the counters."],
              works=["A real 'aha' logo: the kind people point out to each other.", "A band works everywhere: across a sachet, as tape on a box, as a sticker.",
                     "Stencil-ready: it can be cut, punched, embossed or burned."],
              watch=["It reads a beat slower than the other two. Keep it large on first contact, and set the name in plain type nearby at first.",
                     "Always keep the whole bar. Cropping it loses the M or the E."]),
}


def plate(k, ink=K, bg="#FFFFFF", caption=True):
    o = OPTS[k]
    parts, w = o["make"]()
    vb = (-12, -12, w + 24, 124)
    mark = S(vb, draw(parts, ink), "plate-mark")
    cap = (f'<figcaption><b>MODE</b><span>{esc(o["name"])}</span></figcaption>' if caption else "")
    return f'<figure class="plate" style="background:{bg}">{mark}{cap}</figure>'


def kit(k):
    """The construction in one small diagram."""
    if k == "1":
        e = geo2.comb()
        c = geo.disc(50, 50, 50)
        items = [(P(d_of(e), K), "comb = E"), (P(d_of(geo.place(geo.affinity.rotate(e, 90, origin=(50, 50)), 0)), K), "comb, turned = m"),
                 (P(d_of(c), K), "circle = O"), (P(d_of(geo.half(25, 50, 50, "right")), K), "circle, halved = D")]
        return "".join(f'<figure class="k">{S((-6, -6, 112, 112), b)}<figcaption>{esc(t)}</figcaption></figure>' for b, t in items)
    if k == "2":
        from shapely.geometry import LineString
        from geo2 import _strokes
        sk = LineString([(10, 100), (10, 10), (50, 64), (90, 10), (90, 100)])
        one = _strokes(sk, [0], 3.8)
        three = _strokes(sk, [-9, 0, 9], 3.8).intersection(box(-1, 0, 101, 100))
        items = [(P(d_of(one), K), "one skeleton"), (P(d_of(three), K), "three parallels, open ends"),
                 (draw(geo2.lines_open(n=1, pitch=0, w=12)[0]) and S((-8, -8, 454, 116), draw(geo2.lines_open(n=1, pitch=0, w=12)[0])), "small cut: one heavy line")]
        out = ""
        for b, t in items[:2]:
            out += f'<figure class="k">{S((-6, -6, 112, 112), b)}<figcaption>{esc(t)}</figcaption></figure>'
        out += f'<figure class="k wide">{items[2][0]}<figcaption>{esc(items[2][1])}</figcaption></figure>'
        return out
    bar = geo2.counters()[0]["bar"]
    full = box(0, 0, bar.bounds[2], 100)
    cuts = full.difference(bar)
    return (f'<figure class="k wide">{S((-6, -6, bar.bounds[2] + 12, 112), P(d_of(full), K))}<figcaption>one bar</figcaption></figure>'
            f'<figure class="k wide">{S((-6, -6, bar.bounds[2] + 12, 112), P(d_of(cuts), K))}<figcaption>four counters: V, circle, half-circle, two slots</figcaption></figure>')


def ladder(k):
    o = OPTS[k]
    parts, w = o["make"]()
    small = geo2.lines_open(n=1, pitch=0, w=12) if k == "2" else (parts, w)
    cells = ""
    for px in (16, 24, 32, 48):
        p, ww = small if px < 32 else (parts, w)
        cells += f'<figure><div style="height:{px}px">{S((-2, -2, ww + 4, 104), draw(p), "lad")}</div><figcaption>{px} px</figcaption></figure>'
    return f'<div class="ladder">{cells}</div>'


def sachet_for(k):
    o = OPTS[k]
    parts, w = o["make"]()
    if k == "1":
        mark, h = fit(draw(parts, K), (0, 0, w, 100), 40, 70, 220)
        pattern = ""
        unit = [geo2.comb(), geo.disc(50, 50, 50), geo.half(0, 50, 50, "right"), geo2.comb()]
        for i in range(4):
            pattern += fit(draw({"a": [geo.affinity.rotate(geo2.comb(), 90, origin=(50, 50)), geo.disc(50, 50, 50), geo.half(25, 50, 50, "right"), geo2.comb()][i]}, "#D9CBB5"), (0, 0, 100, 100), 40 + i * 58, 300, 46)[0]
        c = (mark + f'<text x="40" y="150" font-size="10" fill="{K}" class="lab">COFFEE CONCENTRATE</text>' + pattern
             + f'<text x="40" y="392" font-size="9.5" fill="{K}" class="lab" opacity=".75">15 ML · FOLD · SQUEEZE · POUR</text>')
        return sachet(c, CREAM, f"s{k}", 0, 0, 280)
    if k == "2":
        mark, h = fit(draw(parts, CREAM), (0, 0, w, 100), 40, 120, 220)
        stripes = "".join(f'<rect x="0" y="{300 + i * 13}" width="{SW}" height="4.2" fill="{CREAM}" opacity=".9"/>' for i in range(4))
        c = (stripes + mark + f'<text x="40" y="96" font-size="10" fill="{CREAM}" class="lab">COFFEE CONCENTRATE</text>'
             + f'<text x="40" y="392" font-size="9.5" fill="{CREAM}" class="lab" opacity=".8">15 ML · FOLD · SQUEEZE · POUR</text>')
        return sachet(c, COFFEE, f"s{k}", 0, 0, 280, seal_tone="#fff", seal_op=0.14)
    band, h = fit(draw(parts, K), (0, 0, w, 100), 0, 176, SW)
    c = (f'<rect x="0" y="0" width="{SW}" height="{SH}" fill="#C8A27A"/>' + band
         + f'<text x="40" y="96" font-size="10" fill="{K}" class="lab">COFFEE CONCENTRATE</text>'
         + f'<text x="40" y="392" font-size="9.5" fill="{K}" class="lab" opacity=".8">15 ML · FOLD · SQUEEZE · POUR</text>')
    return sachet(c, "#C8A27A", f"s{k}", 0, 0, 280)


def icon(k):
    if k == "1":
        g = {"o": geo.disc(60, 90, 34), "d": geo.half(100, 90, 34, "right")}
        body = draw(g, CREAM)
        return S((0, 0, 180, 180), f'<rect width="180" height="180" rx="40" fill="{K}"/>' + body, "ic")
    if k == "2":
        rings = geo2.lines_open()[0]["O"]
        b, h = fit(P(d_of(rings), CREAM), rings.bounds, 36, 36, 108)
        return S((0, 0, 180, 180), f'<rect width="180" height="180" rx="40" fill="{COFFEE}"/>' + b, "ic")
    sq = box(0, 0, 100, 100).difference(geo.disc(50, 50, 30))
    b, h = fit(P(d_of(sq), K), (0, 0, 100, 100), 30, 30, 120)
    return S((0, 0, 180, 180), f'<rect width="180" height="180" rx="40" fill="#C8A27A"/>' + b, "ic")


def section(k):
    o = OPTS[k]
    sach = sachet_for(k)
    return f"""
<section class="opt" id="o{k}"><div class="wrap">
  <p class="eyebrow">Option {k} · {esc(o["after"])}</p>
  {plate(k)}
  <div class="cols">
    <div><h2>{esc(o["name"])}</h2><div class="idea">{"".join(f"<p>{esc(p)}</p>" for p in o["idea"])}</div></div>
    <div><h3>How it's built</h3><div class="kit">{kit(k)}</div></div>
  </div>
  <div class="row3">
    <div><h3>At every size</h3>{ladder(k)}</div>
    <div><h3>Reversed</h3>{plate(k, CREAM, K, caption=False)}</div>
    <div class="apps"><div>{S((0, 0, 300, 450), sach, "sach")}</div><div>{icon(k)}</div></div>
  </div>
  <div class="cols"><div><h3>Why it works</h3><ul>{"".join(f"<li>{esc(w)}</li>" for w in o["works"])}</ul></div>
    <div><h3>Watch out for</h3><ul class="watch">{"".join(f"<li>{esc(w)}</li>" for w in o["watch"])}</ul></div></div>
</div></section>"""


TEMPLATE = r"""<title>MODE Three Marks</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Instrument+Sans:wght@400;500;600;700&display=swap">
<style>
/* Layout: plates from a modernist reference book. Each option gets a white plate, then the reasoning beneath. */
:root{--bg:#EFEDE8;--surface:#FFFFFF;--ink:#151515;--muted:#5E5E5B;--line:#DAD6CE;--accent:#B4532A}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--bg:#121212;--surface:#1B1B1B;--ink:#EFEDE8;--muted:#A6A6A2;--line:#2E2E2D;color-scheme:dark}}
:root[data-theme="dark"]{--bg:#121212;--surface:#1B1B1B;--ink:#EFEDE8;--muted:#A6A6A2;--line:#2E2E2D;color-scheme:dark}
*{box-sizing:border-box}
body{background:var(--bg);color:var(--ink);font-family:'Instrument Sans',system-ui,sans-serif;font-size:16px;line-height:1.55;margin:0}
.wrap{max-width:1120px;margin:0 auto;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}
h1,h2,h3{margin:0;font-weight:600;letter-spacing:-.01em;text-wrap:balance}
h1{font-size:clamp(34px,5vw,60px);line-height:1.02;max-width:16ch}
h2{font-size:clamp(30px,4vw,44px);line-height:1.05;margin-bottom:14px}
h3{font-size:12px;text-transform:uppercase;letter-spacing:.1em;font-weight:600;margin-bottom:12px;color:var(--muted)}
p{margin:0}
svg{display:block;max-width:100%;height:auto}
.lab{font-family:'Instrument Sans',system-ui,sans-serif;font-weight:500;letter-spacing:.06em}
.eyebrow{font-size:12px;letter-spacing:.1em;text-transform:uppercase;color:var(--muted);font-weight:500;margin-bottom:14px}
.intro{padding-block:clamp(48px,8vw,96px) 24px}
.intro .lede{font-size:clamp(17px,1.7vw,20px);color:var(--muted);max-width:62ch;margin-top:18px}
.toc{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px;margin-top:32px}
.toc a{display:block;background:var(--surface);border:1px solid var(--line);color:inherit;text-decoration:none;padding:14px}
.toc a:hover{border-color:var(--ink)}
.toc svg{height:44px;width:auto;max-width:100%;color:#151515}
.toc span{display:block;font-size:13px;color:var(--muted);margin-top:10px}
section.opt{padding-block:clamp(48px,7vw,88px);border-top:1px solid var(--line)}
.plate{margin:0;padding:clamp(48px,9vw,120px) clamp(24px,10vw,140px) clamp(28px,5vw,56px);display:grid;gap:clamp(36px,6vw,72px);justify-items:center;border:1px solid var(--line)}
.plate .plate-mark{width:min(100%,560px)}
.plate figcaption{display:grid;justify-items:center;gap:2px;color:#151515;font-size:clamp(18px,2.4vw,26px);line-height:1.15}
.plate figcaption b{font-weight:700}
.plate figcaption span{font-weight:400}
.cols{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:clamp(24px,4vw,56px);margin-top:40px;align-items:start}
.idea{display:grid;gap:12px;font-size:17px;max-width:58ch}
.kit{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px}
.k{margin:0;background:var(--surface);border:1px solid var(--line);padding:12px;color:#151515}
.k svg{max-height:80px;width:auto;margin:0 auto}
.k.wide{grid-column:span 2}
.k figcaption{font-size:12px;color:var(--muted);margin-top:8px}
.row3{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr) minmax(0,1.1fr);gap:20px;margin-top:40px;align-items:start}
.row3 .plate{padding:32px 24px;gap:0}
.ladder{display:flex;flex-wrap:wrap;align-items:flex-end;gap:18px;background:var(--surface);border:1px solid var(--line);padding:20px;color:#151515}
.ladder figure{margin:0;display:grid;gap:6px}
.ladder .lad{height:100%;width:auto}
.ladder figcaption{font-size:12px;color:#6b6b68}
.apps{display:grid;grid-template-columns:minmax(0,1.4fr) minmax(0,1fr);gap:14px;align-items:end;background:#E5E0D6;padding:16px}
.apps .ic{width:100%;max-width:120px}
ul{margin:0;padding-left:20px;display:grid;gap:8px}
.watch li::marker{content:"! ";color:var(--accent);font-weight:700}
.close{padding-block:56px 72px;border-top:1px solid var(--line)}
.close p{max-width:68ch;font-size:17px}
@media (max-width:860px){.cols,.row3,.toc{grid-template-columns:minmax(0,1fr)} .kit{grid-template-columns:repeat(2,minmax(0,1fr))}}
</style>
{{BODY}}
"""


def build():
    toc = ""
    for k, o in OPTS.items():
        parts, w = o["make"]()
        toc += f'<a href="#o{k}">{S((-6, -6, w + 12, 112), draw(parts))}<span>Option {k} · {esc(o["name"])}</span></a>'
    body = f"""
<header class="intro"><div class="wrap">
  <p class="eyebrow">MODE · one brand · three marks</p>
  <h1>Just MODE. Three geometric marks.</h1>
  <p class="lede">No modes, no system: one name, drawn three different ways. Each follows a different logic, from the same tradition as Fletcher's Design Objectives and Hollenstein's L'Echoppe: a few pure shapes, one idea, nothing extra.</p>
  <nav class="toc" aria-label="Options">{toc}</nav>
</div></header>
{section("1")}{section("2")}{section("3")}
<section class="close"><div class="wrap"><h3>My pick</h3>
  <p>Two Shapes is the safest strong choice: it reads instantly and works everywhere. Counters is the one people will talk about. Lines is the most expressive, and the best if packaging and pattern matter most. Tell me which to take further.</p></div></section>"""
    page = TEMPLATE.replace("{{BODY}}", body)
    out = os.path.join(ROOT, "presentation", "mode-three.html")
    open(out, "w").write(page)
    return out, len(page)


if __name__ == "__main__":
    p, n = build()
    print(p, f"{n / 1024:.0f} KB")
