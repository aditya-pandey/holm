"""Logo masters, icons, favicons and the colour files."""
import json
import os
from PIL import Image
import mark
import brand
from brand import ROOT, CARBON, PAPER, ROAST, OAT, TONIC

L = os.path.join(ROOT, "logo")
I = os.path.join(ROOT, "icon")
C = os.path.join(ROOT, "colour")
B = os.path.join(ROOT, "build")
SMALL_W = 6.0   # hairline weight in the small-size cut (32 px and below on screen, under 15 mm in print)

VARIANTS = [   # file stem, fill, note
    ("mode-logo-carbon", CARBON, "Primary. On Paper, White, Oat and light photography."),
    ("mode-logo-paper", PAPER, "Reversed. On Carbon, Roast, Graphite and dark photography."),
    ("mode-logo-roast", ROAST, "Warm one-colour. On Paper and Oat."),
    ("mode-logo-black", "#000000", "One colour, pure black: newsprint, stamps, embossing dies."),
    ("mode-logo-white", "#FFFFFF", "One colour, pure white: screen overlays, white ink, foil masks."),
]


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as fh:
        fh.write(text)


def logos():
    jobs = []
    for small in (False, True):
        g, box = mark.stack(SMALL_W if small else None)
        w, h = box[2] - box[0], box[3] - box[1]
        for stem, fill, _ in VARIANTS:
            name = stem + ("-small" if small else "")
            svg = mark.svg_doc(g, box, fill, title="MODE")
            write(f"{L}/svg/{name}.svg", svg)
            if small:
                continue
            for px in (512, 1024, 2048):
                jobs.append({"in": f"logo/svg/{name}.svg", "out": f"logo/png/{name}-{px}.png", "w": px, "h": round(px * h / w)})
            jobs.append({"in": f"logo/svg/{name}.svg", "out": f"logo/pdf/{name}.pdf", "w": round(w * 2), "h": round(h * 2),
                         "pdf": {"width": f"{round(w * 2)}px", "height": f"{round(h * 2)}px", "preferCSSPageSize": False}})
        if small:
            for stem, fill, _ in VARIANTS[:2]:
                jobs.append({"in": f"logo/svg/{stem}-small.svg", "out": f"logo/png/{stem}-small-128.png", "w": 128, "h": round(128 * h / w)})
    # with clear space built in (two m-legs on every side), for placing in layouts without guesswork
    g, box = mark.stack()
    pad = 2 * mark.LEG
    write(f"{L}/svg/mode-logo-carbon-clearspace.svg", mark.svg_doc(g, box, CARBON, pad=pad))
    write(f"{L}/svg/mode-logo-paper-clearspace.svg", mark.svg_doc(g, box, PAPER, pad=pad))
    return jobs


def tile(fill, ground, size, w=None, scale=0.6, radius=0.0, circle=False):
    """The mark centred on a square (or circle) of ground colour."""
    g, box = mark.stack(w)
    bw, bh = box[2] - box[0], box[3] - box[1]
    k = size * scale / max(bw, bh)
    tx = (size - bw * k) / 2 - box[0] * k
    ty = (size - bh * k) / 2 - box[1] * k
    shape = (f'<circle cx="{size / 2}" cy="{size / 2}" r="{size / 2}" fill="{ground}"/>' if circle else
             f'<rect width="{size}" height="{size}" rx="{radius * size}" fill="{ground}"/>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {size} {size}">{shape}'
            f'<g transform="translate({tx:.3f} {ty:.3f}) scale({k:.5f})">{mark.paths(g, fill)}</g></svg>')


def icons():
    jobs = []
    write(f"{I}/mode-app-icon.svg", tile(PAPER, CARBON, 1024, scale=0.56))
    write(f"{I}/mode-app-icon-rounded.svg", tile(PAPER, CARBON, 1024, scale=0.56, radius=0.225))
    for px in (1024, 512, 192, 180):
        jobs.append({"in": "icon/mode-app-icon.svg", "out": f"icon/png/mode-app-icon-{px}.png", "w": px, "h": px})
    jobs.append({"in": "icon/mode-app-icon-rounded.svg", "out": "icon/png/mode-app-icon-rounded-512.png", "w": 512, "h": 512})
    # favicon: small cut, mark larger in the tile (16 px uses the monogram, see monogram())
    write(f"{I}/favicon.svg", tile(PAPER, CARBON, 64, w=SMALL_W, scale=0.78, radius=0.18))
    for px in (32, 48, 64):
        jobs.append({"in": "icon/favicon.svg", "out": f"icon/png/favicon-{px}.png", "w": px, "h": px})
    # social profile picture: circle-safe
    write(f"{I}/mode-profile.svg", tile(PAPER, CARBON, 1080, scale=0.44))
    write(f"{I}/mode-profile-oat.svg", tile(CARBON, OAT, 1080, scale=0.44))
    jobs += [{"in": "icon/mode-profile.svg", "out": "icon/png/mode-profile-1080.png", "w": 1080, "h": 1080},
             {"in": "icon/mode-profile-oat.svg", "out": "icon/png/mode-profile-oat-1080.png", "w": 1080, "h": 1080}]
    return jobs


def favicon_ico():
    imgs = [Image.open(f"{I}/png/favicon-{px}.png").convert("RGBA") for px in (16, 32, 48)]
    imgs[2].save(f"{I}/favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)], append_images=imgs[:2])


def colour():
    rows = []
    for role, name, hx, pms, cmyk, use in brand.PALETTE:
        rows.append(dict(role=role, name=name, hex=hx, rgb=brand.hex_rgb(hx), cmyk=cmyk, pantone=pms, use=use))
    write(f"{C}/mode-palette.json", json.dumps(rows, indent=2))
    css = ":root{\n" + "".join(f"  --mode-{r['name'].lower()}: {r['hex']};\n" for r in rows) + "}\n"
    write(f"{C}/mode-palette.css", css)
    groups = [("MODE core", [(r["name"], r["hex"]) for r in rows if r["role"] in ("core", "ground")]),
              ("MODE warm + accent", [(r["name"], r["hex"]) for r in rows if r["role"] in ("warm", "accent")])]
    brand.write_ase(f"{C}/mode-palette.ase", groups)


def monogram():
    """The m alone: the logo's top-left block, for 16-24 px and other tiny spaces."""
    g, _ = mark.m()
    box = (0, 0, 100, 100)
    for stem, fill in (("mode-monogram-carbon", CARBON), ("mode-monogram-paper", PAPER), ("mode-monogram-black", "#000000"), ("mode-monogram-white", "#FFFFFF")):
        write(f"{L}/svg/{stem}.svg", mark.svg_doc(g, box, fill, title="MODE monogram"))
    k = 64 * 0.64 / 100
    t = (64 - 100 * k) / 2
    write(f"{I}/favicon-16.svg", f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="11" fill="{CARBON}"/>'
          f'<g transform="translate({t} {t}) scale({k})">{mark.paths(g, PAPER)}</g></svg>')
    return [{"in": "logo/svg/mode-monogram-carbon.svg", "out": "logo/png/mode-monogram-carbon-512.png", "w": 512, "h": 512},
            {"in": "logo/svg/mode-monogram-paper.svg", "out": "logo/png/mode-monogram-paper-512.png", "w": 512, "h": 512},
            {"in": "icon/favicon-16.svg", "out": "icon/png/favicon-16.png", "w": 16, "h": 16}]


if __name__ == "__main__":
    jobs = logos() + icons()
    brand.render(jobs, "logo")
    brand.render(monogram(), "mono")
    favicon_ico()
    colour()
    print(len(jobs), "renders")
