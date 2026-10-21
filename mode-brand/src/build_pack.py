"""Packaging flats: SVG + print PDF (with bleed) + PNG previews, and the textures the 3D scenes use."""
import os
import re
import brand
import pack
from brand import ROOT, SKUS

P = os.path.join(ROOT, "packaging")
HB = os.path.join(ROOT, "build", "html")
TEX = os.path.join(ROOT, "build", "tex")


def mm_size(svg):
    w = float(re.search(r'width="([\d.]+)mm"', svg).group(1))
    h = float(re.search(r'height="([\d.]+)mm"', svg).group(1))
    return w, h


def save(rel, svg):
    path = os.path.join(P, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, "w").write(svg)
    return path


def page(name, svg, px_per_mm):
    """HTML wrapper so fonts load; returns (html path, w px, h px)."""
    w, h = mm_size(svg)
    W, H = round(w * px_per_mm), round(h * px_per_mm)
    os.makedirs(HB, exist_ok=True)
    p = os.path.join(HB, name + ".html")
    open(p, "w").write(brand.html_wrap(svg, W, H, rel="../../fonts"))
    return os.path.relpath(p, ROOT), W, H


def jobs_for(rel_svg, svg, png_px_mm=12, pdf=True, tex=None, tex_px_mm=20, png=True):
    stem = os.path.splitext(rel_svg)[0]
    name = stem.replace("/", "__")
    out = []
    if png:
        hp, W, H = page(name, svg, png_px_mm)
        out.append({"in": hp, "out": f"packaging/{stem}.png", "w": W, "h": H})
    if pdf:
        w, h = mm_size(svg)
        hp2, W2, H2 = page(name + "__pdf", svg, 96 / 25.4)
        out.append({"in": hp2, "out": f"packaging/{stem}.pdf", "w": W2, "h": H2,
                    "pdf": {"width": f"{w}mm", "height": f"{h}mm", "preferCSSPageSize": False}})
    if tex:
        hp3, W3, H3 = page("tex__" + tex, svg, tex_px_mm)
        out.append({"in": hp3, "out": f"build/tex/{tex}.png", "w": W3, "h": H3})
    return out


def build():
    jobs = []
    for s in SKUS:
        k = s["key"]
        for side, fn in (("front", pack.sachet_front), ("back", pack.sachet_back)):
            svg = fn(k)
            rel = f"sachet/mode-sachet-{k}-{side}.svg"
            save(rel, svg)
            jobs += jobs_for(rel, svg)
            jobs += jobs_for(rel, fn(k, bleed=0), pdf=False, tex=f"sachet-{k}-{side}", png=False)
        for face, fn in (("front", pack.carton_front), ("back", pack.carton_back), ("sidea", pack.carton_side_a),
                         ("sideb", pack.carton_side_b), ("top", pack.carton_top), ("bottom", pack.carton_bottom)):
            svg = fn(k)
            jobs += jobs_for(f"carton/panels/{k}-{face}.svg", svg, pdf=False, tex=f"carton-{k}-{face}", png=False)
        svg, _ = pack.dieline(k)
        rel = f"carton/mode-carton-{k}-dieline.svg"
        save(rel, svg)
        jobs += jobs_for(rel, svg, png_px_mm=6)
        if k == SKUS[0]["key"]:
            svg, _ = pack.dieline(k, art=False)
            rel = "carton/mode-carton-dieline-blank.svg"
            save(rel, svg)
            jobs += jobs_for(rel, svg, png_px_mm=6)
    for name, fn in (("mailer/mode-mailer-lid", pack.mailer_top), ("mailer/mode-mailer-inside-lid", pack.mailer_inside),
                     ("tumbler/mode-tumbler-wrap", pack.tumbler_wrap)):
        svg = fn()
        save(name + ".svg", svg)
        jobs += jobs_for(name + ".svg", svg, png_px_mm=6, tex=os.path.basename(name), tex_px_mm=8)
    brand.render(jobs, "pack")
    return len(jobs)


if __name__ == "__main__":
    print(build(), "renders")
