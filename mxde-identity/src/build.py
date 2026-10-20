"""Build every MXDE logo, icon and mode asset from the geometry in geom.py.

    python3 src/build.py            # SVG masters + manifest of render jobs
    node src/render.mjs build/jobs.json   # PNG / PDF from those masters
"""
import json
import os
from shapely.ops import unary_union
from geom import H, letter_M, letter_D, letter_E, letter_X_box, mode_tile, place, to_path
from palette import PALETTE, MODES, colour
from text import text_path, text_width

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
STEM = 18.0                 # stem weight, 18% of cap height (chosen from the 10/14/18/22 study)
KCUT = 0.62 * STEM          # width of the X cut in the slot
GAPS = (20.5, 20.5, 19.0)   # M–X, X–D, D–E (D's chamfers open space, so D–E sits tighter)
HEAD = "Archivo-Expanded-SemiBold.ttf"
TAG = "Archivo-Medium.ttf"

CARBON, WHITE, PAPER, TONIC, SILVER = (colour(n) for n in ("Carbon", "White", "Paper", "Tonic", "Silver"))
JOBS = []


def out(*p):
    path = os.path.join(ROOT, *p)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    return path


# ---------------------------------------------------------------- the wordmark

def wordmark_parts():
    M, wm = letter_M(STEM)
    X, wx = letter_X_box(STEM, gap=KCUT / STEM)
    D, wd = letter_D(STEM)
    E, we = letter_E(STEM)
    x = 0.0
    xs = []
    for adv, gap in zip((wm, wx, wd, we), GAPS + (0,)):
        xs.append(x)
        x += adv + gap
    letters = unary_union([place(M, xs[0]), place(D, xs[2]), place(E, xs[3])])
    slot = place(X, xs[1])
    return letters, slot, x, xs[1]


LETTERS, SLOT, WORD_W, SLOT_X = wordmark_parts()


def svg(vw, vh, body, title):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {vw:g} {vh:g}" role="img" aria-label="{title}">'
            f'<title>{title}</title>{body}</svg>\n')


def P(d, fill):
    return f'<path fill="{fill}" d="{d}"/>'


SCHEMES = {
    # name: (letters, slot, text, background-for-preview)
    "fullcolour": (CARBON, TONIC, CARBON, PAPER),
    "carbon": (CARBON, CARBON, CARBON, PAPER),
    "black": ("#000000", "#000000", "#000000", "#FFFFFF"),
    "white": (WHITE, WHITE, WHITE, CARBON),
    "tonic": (TONIC, TONIC, TONIC, PAPER),
    "silver": (SILVER, SILVER, SILVER, CARBON),
}


def wordmark_body(cl, cx, oy=H):
    return P(to_path(LETTERS, 0, oy), cl) + P(to_path(SLOT, 0, oy), cx)


def tagline_body(ct, y_top, tag="SwitchYourMode", cap=0.24 * H):
    d, w = text_path(tag, TAG, 0, y_top + cap, cap, tracking=0.02)
    return P(d, ct), w


def write(path, content):
    with open(path, "w") as f:
        f.write(content)


def build_logos():
    for name, (cl, cx, ct, bg) in SCHEMES.items():
        p = out("logo", "svg", f"mxde-wordmark-{name}.svg")
        write(p, svg(WORD_W, H, wordmark_body(cl, cx), "MXDE"))
        JOBS.extend(png_set(p, "logo/png", [400, 800, 1600, 3200], WORD_W / H))
        JOBS.append(pdf_job(p, WORD_W, H))

        gap = 0.42 * H
        tb, tw = tagline_body(ct, H + gap)
        vh = H + gap + 0.24 * H + 0.06 * H  # descender room for y
        p = out("logo", "svg", f"mxde-wordmark-tagline-{name}.svg")
        write(p, svg(WORD_W, vh, wordmark_body(cl, cx) + tb, "MXDE — SwitchYourMode"))
        JOBS.extend(png_set(p, "logo/png", [800, 1600], WORD_W / vh))
        JOBS.append(pdf_job(p, WORD_W, vh))

    for name, fill in (("carbon", CARBON), ("white", WHITE), ("tonic", TONIC), ("black", "#000000")):
        p = out("logo", "svg", f"mxde-monogram-{name}.svg")
        write(p, svg(H, H, P(to_path(mode_tile("x", KCUT), 0, H), fill), "MXDE monogram"))
        JOBS.extend(png_set(p, "logo/png", [64, 128, 256, 512, 1024], 1))
        JOBS.append(pdf_job(p, H, H))


# ---------------------------------------------------------------- icons

def build_icons():
    # Favicon: the slot reversed — Carbon square, X cut in Paper. A heavier cut (16% of size) survives 16 px.
    S = 64
    k = 0.16 * S
    # draw the cut explicitly in Paper so the icon reads on any tab colour, light or dark
    from shapely.geometry import box as _box
    cut = _box(0, 0, S, S).difference(mode_tile("x", k, S))
    body = f'<rect width="{S}" height="{S}" fill="{CARBON}"/>' + P(to_path(cut, 0, S), PAPER)
    p = out("icons", "favicon.svg")
    write(p, svg(S, S, body, "MXDE"))
    for px in (16, 32, 48, 180, 192):
        JOBS.append({"in": p, "out": f"icons/favicon-{px}.png", "w": px, "h": px})

    # App / profile icon: Paper slot on Carbon, slot at 46% so it survives a circular crop.
    S = 512
    t = 0.46 * S
    o = (S - t) / 2
    tile = place(mode_tile("x", 0.12 * t, t), o)
    from shapely import affinity
    tile = affinity.translate(tile, yoff=o)
    for name, bg, fg in (("carbon", CARBON, PAPER), ("paper", PAPER, CARBON), ("tonic", TONIC, PAPER)):
        p = out("icons", f"app-icon-{name}.svg")
        write(p, svg(S, S, f'<rect width="{S}" height="{S}" fill="{bg}"/>' + P(to_path(tile, 0, S), fg), "MXDE"))
        JOBS.append({"in": p, "out": f"icons/app-icon-{name}-512.png", "w": 512, "h": 512})
    JOBS.append({"in": out("icons", "app-icon-carbon.svg"), "out": "icons/apple-touch-icon-180.png", "w": 180, "h": 180})
    JOBS.append({"in": out("icons", "app-icon-carbon.svg"), "out": "icons/profile-picture-1080.png", "w": 1080, "h": 1080})


# ---------------------------------------------------------------- modes

MODE_TILE = 0.32 * H     # mode tile in the lockup: 32% of cap height (ACTIVE, the longest name, ends inside the E)
MODE_GAP = 0.36 * H      # wordmark → mode line


def mode_line(key, name, cl, ctile, y_top):
    """The mode line hangs from the X: tile left edge = slot left edge; name follows one cut-width later."""
    s = MODE_TILE
    tile = mode_tile(key, 0.15 * s, s)
    from shapely import affinity
    tile = affinity.translate(tile, xoff=SLOT_X, yoff=0)
    body = P(to_path(tile, 0, y_top + s), ctile)
    nx = SLOT_X + s + 0.32 * s
    d, w = text_path(name, HEAD, nx, y_top + s, s, tracking=0.06)
    return body + P(d, cl), nx + w


def build_modes():
    for key, name, hx, *_ in MODES:
        for scheme, (cl, cx, ct, bg) in (("fullcolour", (CARBON, hx, CARBON, PAPER)),
                                          ("carbon", (CARBON, CARBON, CARBON, PAPER)),
                                          ("white", (WHITE, WHITE, WHITE, CARBON)),
                                          ("reversed-colour", (WHITE, hx, WHITE, CARBON))):
            y = H + MODE_GAP
            line, right = mode_line(key, name, cl, cx, y)
            assert right <= WORD_W + 0.5, f"{name} overruns the wordmark ({right:.1f} > {WORD_W:.1f})"
            vh = y + MODE_TILE
            p = out("modes", "svg", f"mxde-lockup-{key}-{scheme}.svg")
            write(p, svg(WORD_W, vh, wordmark_body(cl, cx) + line, f"MXDE {name} Mode"))
            JOBS.extend(png_set(p, "modes/png", [1200], WORD_W / vh))
            JOBS.append(pdf_job(p, WORD_W, vh))
        for scheme, fill in (("colour", hx), ("carbon", CARBON), ("white", WHITE)):
            p = out("modes", "svg", f"mxde-tile-{key}-{scheme}.svg")
            write(p, svg(H, H, P(to_path(mode_tile(key, KCUT), 0, H), fill), f"{name} Mode"))
            JOBS.extend(png_set(p, "modes/png", [256, 1024], 1))
    # the master slot, for side-by-side use
    p = out("modes", "svg", "mxde-tile-x-carbon.svg")
    write(p, svg(H, H, P(to_path(mode_tile("x", KCUT), 0, H), CARBON), "MXDE"))


# ---------------------------------------------------------------- render jobs

def png_set(svg_path, folder, widths, aspect):
    base = os.path.splitext(os.path.basename(svg_path))[0]
    jobs = []
    for w in widths:
        h = round(w / aspect)
        jobs.append({"in": os.path.relpath(svg_path, ROOT), "out": f"{folder}/{base}-{w}w.png", "w": w, "h": h})
    return jobs


def pdf_job(svg_path, w, h):
    # 1 unit = 1 px; scale up so the PDF page is a sensible physical size (~ 4.2 in wide for the wordmark)
    k = 1.0
    rel = os.path.relpath(svg_path, ROOT)
    return {"in": rel, "out": rel.replace("/svg/", "/pdf/").replace(".svg", ".pdf"),
            "w": round(w * k), "h": round(h * k), "pdf": {"width": f"{w * k:.2f}px", "height": f"{h * k:.2f}px",
                                                         "preferCSSPageSize": False}}


if __name__ == "__main__":
    build_logos()
    build_icons()
    build_modes()
    os.makedirs(out("build", "x"), exist_ok=True)
    with open(out("build", "jobs.json"), "w") as f:
        json.dump(JOBS, f, indent=1)
    print(f"word width {WORD_W:.1f}, slot x {SLOT_X:.1f}, {len(JOBS)} render jobs")
