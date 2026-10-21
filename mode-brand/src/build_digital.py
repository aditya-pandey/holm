"""Digital touchpoints: Instagram post + story, e-commerce tile, website hero, website header with favicon."""
import os
import mark
import brand
from brand import ROOT, CARBON, PAPER, OAT, ROAST, TONIC, GRAPHITE, STONE

D = os.path.join(ROOT, "digital")
HB = os.path.join(ROOT, "build", "html")


def logo_svg(fill, w=None):
    g, box = mark.stack(w)
    vb = f"{mark.f(box[0])} {mark.f(box[1])} {mark.f(box[2] - box[0])} {mark.f(box[3] - box[1])}"
    return f'<svg class="logo" viewBox="{vb}" aria-label="MODE">{mark.paths(g, fill)}</svg>'


def letter_svg(l, fill):
    g, box = mark.letters()[l]
    vb = f"{mark.f(box[0])} {mark.f(box[1])} {mark.f(box[2] - box[0])} {mark.f(box[3] - box[1])}"
    return f'<svg class="let" viewBox="{vb}">{mark.paths(g, fill)}</svg>'


BASE = """<!doctype html><html><head><meta charset="utf-8"><style>{fonts}
*{{box-sizing:border-box;margin:0}}html,body{{overflow:hidden}}
body{{width:{w}px;height:{h}px;font-family:'Instrument Sans',sans-serif;color:{ink};background:{bg};position:relative}}
.mono{{font-family:'IBM Plex Mono',monospace;letter-spacing:.14em;text-transform:uppercase}}
svg{{display:block}}{css}</style></head><body>{body}</body></html>"""

R = "../../packaging/renders"


def page(name, w, h, bg, ink, body, css=""):
    os.makedirs(HB, exist_ok=True)
    p = os.path.join(HB, f"digital__{name}.html")
    open(p, "w").write(BASE.format(fonts=brand.font_face("../../fonts"), w=w, h=h, bg=bg, ink=ink, body=body, css=css))
    return {"in": os.path.relpath(p, ROOT), "out": f"digital/mode-{name}.png", "w": w, "h": h}


def build():
    jobs = []
    # 1 · Instagram post: the mark, alone
    jobs.append(page("instagram-post-logo", 1080, 1080, OAT, CARBON,
                     f'<div style="position:absolute;left:50%;top:47%;width:470px;transform:translate(-50%,-50%)">{logo_svg(CARBON)}</div>'
                     f'<p class="mono" style="position:absolute;left:0;right:0;bottom:88px;text-align:center;font-size:22px">Coffee concentrate · in sachets</p>'))
    # 2 · Instagram post: the five modes
    rows = "".join(f'<div class="r"><i style="background:{m["tint"]}"></i><b>{m["name"]}</b><span class="mono">{m["line"].rstrip(".")}</span></div>' for m in brand.MODES)
    jobs.append(page("instagram-post-modes", 1080, 1080, ROAST, PAPER,
                     f'<h1>Five modes.<br>Pick yours.</h1><div class="g">{rows}</div><p class="mono tag">{brand.TAGLINE}</p>',
                     "h1{position:absolute;left:90px;top:96px;font-weight:600;font-size:76px;line-height:1.02;letter-spacing:-.02em}"
                     ".g{position:absolute;left:90px;right:90px;top:400px;display:grid;gap:0}"
                     ".r{display:grid;grid-template-columns:28px 1fr auto;align-items:center;gap:24px;padding:22px 0;border-top:1px solid rgba(244,242,237,.22)}"
                     ".r i{width:28px;height:28px}.r b{font-size:42px;font-weight:500}.r span{font-size:18px;opacity:.75}"
                     ".tag{position:absolute;left:90px;bottom:80px;font-size:22px;text-transform:none;letter-spacing:.04em}"))
    # 3 · Instagram post: the product
    jobs.append(page("instagram-post-sachets", 1080, 1080, "#DCD5C9", CARBON,
                     f'<img src="{R}/mode-sachets.png" style="position:absolute;left:-360px;top:-40px;width:1800px">'
                     f'<p style="position:absolute;left:80px;top:84px;font-size:54px;font-weight:600;letter-spacing:-.02em;line-height:1.05">Fold. Squeeze.<br>Pour.</p>'
                     f'<div style="position:absolute;right:80px;bottom:80px;width:120px">{logo_svg(CARBON)}</div>'))
    # 4 · Story
    jobs.append(page("instagram-story", 1080, 1920, "#D9D2C6", CARBON,
                     f'<img src="{R}/mode-mailer-open.png" style="position:absolute;left:-560px;top:760px;width:2200px;-webkit-mask-image:linear-gradient(to bottom,transparent,#000 12%)">'
                     f'<div style="position:absolute;left:90px;top:150px;width:210px">{logo_svg(CARBON)}</div>'
                     f'<p style="position:absolute;left:90px;top:450px;font-size:76px;font-weight:600;letter-spacing:-.02em;line-height:1.02">Five modes.<br>One sachet each.</p>'
                     f'<p class="mono" style="position:absolute;left:90px;bottom:150px;font-size:24px">Swipe up · shop the range</p>'))
    # 5 · E-commerce tile (square, light, product centred)
    jobs.append(page("ecommerce-tile-wake", 1200, 1200, "#DED8CE", CARBON,
                     f'<img src="{R}/mode-carton.png" style="position:absolute;left:-330px;top:-30px;width:1880px">'
                     f'<p class="mono" style="position:absolute;left:56px;top:52px;font-size:20px;opacity:.75">MODE · Wake mode · 10 × 15 ml</p>'))
    # 6 · Website hero
    hero = (f'<header class="nav"><div style="width:58px">{logo_svg(CARBON)}</div><nav><a>Shop</a><a>How it works</a><a>About</a></nav>'
            f'<a class="cart mono">Cart (0)</a></header>'
            f'<div class="copy"><p class="mono" style="font-size:18px;opacity:.7">Coffee concentrate</p>'
            f'<h1>Good coffee,<br>folded into<br>a sachet.</h1>'
            f'<p class="sub">Fifteen millilitres of concentrate. Fold it, squeeze it into water or milk, hot or cold. Done in ten seconds.</p>'
            f'<a class="btn">Shop the range</a></div>'
            f'<img src="{R}/mode-range.png" class="shot">')
    jobs.append(page("website-hero", 1920, 1080, "#DCD5C9", CARBON, hero,
                     ".nav{position:absolute;left:0;right:0;top:0;height:110px;display:flex;align-items:center;gap:80px;padding:0 90px}"
                     ".nav nav{display:flex;gap:44px;font-size:21px;font-weight:500}.cart{margin-left:auto;font-size:17px}"
                     ".copy{position:absolute;left:90px;top:250px;width:640px;display:grid;gap:30px;z-index:2}"
                     "h1{font-size:104px;line-height:.98;letter-spacing:-.03em;font-weight:600}"
                     ".sub{font-size:25px;line-height:1.45;max-width:30ch;opacity:.85}"
                     f".btn{{justify-self:start;background:{TONIC};color:#fff;font-size:22px;font-weight:600;padding:20px 34px;border-radius:999px}}"
                     ".shot{position:absolute;right:-260px;top:120px;width:1650px;-webkit-mask-image:linear-gradient(to right,transparent 2%,#000 22%)}"))
    # 7 · Website header + favicon in a browser tab
    tab = (f'<div class="chrome"><div class="tab"><img src="../../icon/png/favicon-32.png" width="16" height="16"><span>MODE — Coffee concentrate</span><i>×</i></div></div>'
           f'<div class="bar"><span class="url">mode · shop</span></div>'
           f'<header class="nav"><div style="width:44px">{logo_svg(CARBON)}</div><nav><a>Shop</a><a>How it works</a><a>About</a></nav><a class="cart mono">Cart (0)</a></header>')
    jobs.append(page("website-header", 1440, 300, PAPER, CARBON, tab,
                     ".chrome{height:46px;background:#DFDAD1;padding:8px 14px 0}.tab{display:inline-flex;align-items:center;gap:10px;height:38px;padding:0 18px;"
                     "background:#F4F2ED;border-radius:10px 10px 0 0;font-size:14px}.tab i{font-style:normal;opacity:.5;margin-left:18px}"
                     ".bar{height:46px;background:#F4F2ED;border-bottom:1px solid #DFDAD1;display:flex;align-items:center;padding:0 18px}"
                     ".url{background:#E9E5DC;border-radius:999px;padding:6px 18px;font-size:14px;color:#4A4C4F}"
                     ".nav{height:208px;display:flex;align-items:center;gap:70px;padding:0 70px}.nav nav{display:flex;gap:40px;font-size:18px;font-weight:500}"
                     ".cart{margin-left:auto;font-size:14px}"))
    brand.render(jobs, "digital")
    return len(jobs)


if __name__ == "__main__":
    print(build(), "digital assets")
