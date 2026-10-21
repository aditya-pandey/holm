"""MODE brand constants: palette, product range, type. One source of truth for every asset and the guidelines."""
import json
import os
import struct
import subprocess

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))

# role, name, hex, Pantone (nearest; check against a physical guide before print), CMYK starting values, use
PALETTE = [
    ("core", "Carbon", "#151515", "Neutral Black C", (0, 0, 0, 95), "The logo, type, structure"),
    ("core", "Graphite", "#4A4C4F", "Cool Gray 11 C", (0, 2, 0, 80), "Secondary type, cool grounds"),
    ("core", "Stone", "#888B8D", "Cool Gray 8 C", (2, 0, 0, 52), "Captions, rules, quiet detail"),
    ("core", "Silver", "#C8C9C7", "877 C (foil) / Cool Gray 3 C (flat)", (0, 0, 1, 24), "Foil on pack; flat grey on screen"),
    ("ground", "White", "#FFFFFF", "Paper white", (0, 0, 0, 0), "Screens, clean grounds"),
    ("ground", "Paper", "#F4F2ED", "Warm Gray 1 C, 30% tint", (2, 2, 5, 2), "The default ground"),
    ("warm", "Oat", "#E6DCCB", "7527 C", (8, 10, 18, 0), "Warm packaging ground"),
    ("warm", "Roast", "#4B3D2F", "7533 C", (30, 45, 60, 65), "Coffee brown: dark grounds, the pour"),
    ("accent", "Tonic", "#0E6B5E", "562 C", (88, 20, 60, 30), "Accent, 10% or less: links, small markers"),
]
HEX = {name: hx for _, name, hx, *_ in PALETTE}
CARBON, PAPER, OAT, ROAST, TONIC, GRAPHITE, STONE, SILVER = (HEX[k] for k in ("Carbon", "Paper", "Oat", "Roast", "Tonic", "Graphite", "Stone", "Silver"))
KRAFT = "#C9A57C"   # uncoated kraft board (a stock, not a brand colour)

# The range is the modes. The logo never changes; each mode is a name, a ground and a thin band in its tint.
# Tints come from the original brief's palette; lines, notes and caffeine are placeholders for the brand team.
MODES = [
    dict(key="wake", name="Wake", tint="#2771BE", pms="2727 C", cmyk=(78, 42, 0, 0), ground="#F4F2ED", ink="#151515",
         line="For a sharp start.", best="MORNING", notes="Bright · citrus, cocoa", caffeine="~110 MG"),
    dict(key="active", name="Active", tint="#0B8457", pms="340 C", cmyk=(90, 10, 75, 5), ground="#151515", ink="#F4F2ED",
         line="For the push.", best="BEFORE EFFORT", notes="Bold · dark chocolate", caffeine="~130 MG"),
    dict(key="zen", name="Zen", tint="#4F758B", pms="5405 C", cmyk=(70, 35, 22, 15), ground="#4A4C4F", ink="#F4F2ED",
         line="For deep focus.", best="DEEP WORK", notes="Clean · toasted nut, caramel", caffeine="~80 MG"),
    dict(key="vital", name="Vital", tint="#557F22", pms="7490 C", cmyk=(55, 10, 100, 10), ground="#E6DCCB", ink="#151515",
         line="For a midday reset.", best="MIDDAY", notes="Fresh · red fruit, honey", caffeine="~60 MG"),
    dict(key="calm", name="Calm", tint="#8C6A4E", pms="4645 C", cmyk=(25, 45, 62, 15), ground="#4B3D2F", ink="#F4F2ED",
         line="For a slow evening.", best="EVENING", notes="Soft · malt, low caffeine", caffeine="~15 MG"),
]
SKUS = MODES   # the range is the modes
TAGLINE = "#SwitchYourMode"


def hex_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def mix(a, b, t):
    """a → b by t (0..1)."""
    ra, rb = hex_rgb(a), hex_rgb(b)
    return "#" + "".join(f"{round(x + (y - x) * t):02X}" for x, y in zip(ra, rb))



def luminance(h):
    def ch(c):
        c /= 255
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = hex_rgb(h)
    return 0.2126 * ch(r) + 0.7152 * ch(g) + 0.0722 * ch(b)


for s in SKUS:
    s["hero"] = mix(s["ground"], s["ink"], 0.13 if luminance(s["ground"]) > 0.4 else 0.19)   # the big letter: tone on tone


def contrast(a, b):
    la, lb = sorted((luminance(a), luminance(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def write_ase(path, groups):
    """Adobe Swatch Exchange. groups: [(group_name, [(swatch_name, hex)])]."""
    def ustr(s):
        return struct.pack(">H", len(s) + 1) + (s + "\0").encode("utf-16-be")
    blocks = []
    for gname, swatches in groups:
        body = ustr(gname)
        blocks.append(struct.pack(">HI", 0xC001, len(body)) + body)
        for sname, hx in swatches:
            r, g, b = (c / 255 for c in hex_rgb(hx))
            body = ustr(sname) + b"RGB " + struct.pack(">fff", r, g, b) + struct.pack(">H", 2)
            blocks.append(struct.pack(">HI", 0x0001, len(body)) + body)
        blocks.append(struct.pack(">HI", 0xC002, 0))
    with open(path, "wb") as fh:
        fh.write(b"ASEF" + struct.pack(">HHI", 1, 0, len(blocks)) + b"".join(blocks))


# Fonts: both free under the SIL Open Font License, on Google Fonts. Local copies in /fonts for offline rendering.
FONTS = [("Instrument Sans", "Primary: headlines, product names, body", "https://fonts.google.com/specimen/Instrument+Sans"),
         ("IBM Plex Mono", "Secondary: labels, data, ingredients, small print", "https://fonts.google.com/specimen/IBM+Plex+Mono")]


def font_face(rel="../fonts"):
    faces = [("Instrument Sans", 400, "InstrumentSans-Regular.ttf"), ("Instrument Sans", 500, "InstrumentSans-Medium.ttf"),
             ("Instrument Sans", 600, "InstrumentSans-SemiBold.ttf"), ("IBM Plex Mono", 400, "PlexMono-Regular.ttf"),
             ("IBM Plex Mono", 500, "PlexMono-Medium.ttf")]
    return "".join(f"@font-face{{font-family:'{n}';font-weight:{w};src:url('{rel}/{fn}') format('truetype')}}" for n, w, fn in faces)


SVG_STYLE = ("<style>.h{font-family:'Instrument Sans',sans-serif;font-weight:600}.r{font-family:'Instrument Sans',sans-serif;font-weight:400}"
             ".md{font-family:'Instrument Sans',sans-serif;font-weight:500}.mono{font-family:'IBM Plex Mono',monospace;font-weight:400}"
             ".monom{font-family:'IBM Plex Mono',monospace;font-weight:500}</style>")


def render(jobs, tag="jobs"):
    """Render HTML/SVG files to PNG/PDF with headless Chromium (src/render.mjs)."""
    p = os.path.join(ROOT, "build", f"{tag}.json")
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w") as fh:
        json.dump(jobs, fh)
    subprocess.run(["node", os.path.join(ROOT, "src", "render.mjs"), p], check=True, cwd=ROOT,
                   env={**os.environ, "NODE_PATH": "/opt/node22/lib/node_modules"})


def html_wrap(svg, w, h, bg="transparent", rel="../fonts"):
    """An SVG inside a page that loads the local fonts, sized exactly w×h CSS px."""
    return (f"<!doctype html><html><head><meta charset='utf-8'><style>{font_face(rel)}html,body{{margin:0;background:{bg};overflow:hidden}}"
            f"body>svg{{display:block;width:{w}px;height:{h}px}}</style></head><body>{svg}</body></html>")
