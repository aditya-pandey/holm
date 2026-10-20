"""MXDE colour system: one source of truth for every asset, the guidelines and the ASE swatch file."""
import json
import os
import struct

# role, name, hex, nearest Pantone (verify against a physical guide before print), CMYK starting values
PALETTE = [
    # Core neutrals — logo, type, structure
    ("core", "Carbon", "#151515", "Neutral Black C", (0, 0, 0, 95)),
    ("core", "Graphite", "#4A4C4F", "Cool Gray 11 C", (0, 2, 0, 80)),
    ("core", "Stone", "#888B8D", "Cool Gray 8 C", (2, 0, 0, 52)),
    ("core", "Silver", "#C8C9C7", "877 C (metallic foil) / Cool Gray 3 C (flat)", (0, 0, 1, 24)),
    # Light grounds — backgrounds, breathing room
    ("ground", "White", "#FFFFFF", "— (paper white)", (0, 0, 0, 0)),
    ("ground", "Paper", "#F4F2ED", "Warm Gray 1 C at 30% tint", (2, 2, 5, 2)),
    # Warm neutrals — coffee warmth, packaging grounds
    ("warm", "Oat", "#E6DCCB", "7527 C", (8, 10, 18, 0)),
    ("warm", "Roast", "#4B3D2F", "7533 C", (30, 45, 60, 65)),
    # Accent — highlights, calls to action (≤10% of any layout)
    ("accent", "Tonic", "#0E6B5E", "562 C", (88, 20, 60, 30)),
]

# Mode tints: secondary accents, used only where a mode is named. Each pairs with its glyph.
MODES = [
    # key, name, hex, Pantone, CMYK, glyph, idea, mood
    ("wake", "WAKE", "#2771BE", "2727 C", (78, 42, 0, 0), "▲", "The X stands up — a rising peak.", "Crisp, bright, sharp"),
    ("active", "ACTIVE", "#0B8457", "340 C", (90, 10, 75, 5), "▶", "The X points forward — momentum.", "Energetic, forward-moving"),
    ("zen", "ZEN", "#4F758B", "5405 C", (70, 35, 22, 15), "|||", "The bars stand upright — an aligned, focused mind.", "Still, centred, balanced"),
    ("vital", "VITAL", "#557F22", "7490 C", (55, 10, 100, 10), "+", "The X turns upright — replenish, add.", "Fresh, restorative, alive"),
    ("calm", "CALM", "#8C6A4E", "4645 C", (25, 45, 62, 15), "≡", "The bars lie down — a body at rest.", "Soft, slow, quiet"),
]


def hex_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def luminance(h):
    def ch(c):
        c /= 255
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = hex_rgb(h)
    return 0.2126 * ch(r) + 0.7152 * ch(g) + 0.0722 * ch(b)


def contrast(a, b):
    la, lb = sorted((luminance(a), luminance(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def colour(name):
    for row in PALETTE:
        if row[1] == name:
            return row[2]
    for m in MODES:
        if m[1].lower() == name.lower() or m[0] == name:
            return m[2]
    raise KeyError(name)


def write_ase(path, groups):
    """Adobe Swatch Exchange. groups: [(group_name, [(swatch_name, hex)])] — RGB process swatches."""
    def ustr(s):
        b = (s + "\0").encode("utf-16-be")
        return struct.pack(">H", len(s) + 1) + b

    blocks = []
    for gname, swatches in groups:
        body = ustr(gname)
        blocks.append(struct.pack(">HI", 0xC001, len(body)) + body)
        for sname, hx in swatches:
            r, g, b = (c / 255 for c in hex_rgb(hx))
            body = ustr(sname) + b"RGB " + struct.pack(">fff", r, g, b) + struct.pack(">H", 2)  # 2 = normal
            blocks.append(struct.pack(">HI", 0x0001, len(body)) + body)
        blocks.append(struct.pack(">HI", 0xC002, 0))
    with open(path, "wb") as f:
        f.write(b"ASEF" + struct.pack(">HHI", 1, 0, len(blocks)) + b"".join(blocks))


def export(outdir):
    os.makedirs(outdir, exist_ok=True)
    data = {"brand": [], "modes": [], "text_pairings": []}
    for role, name, hx, pms, cmyk in PALETTE:
        data["brand"].append({"role": role, "name": name, "hex": hx, "rgb": hex_rgb(hx), "cmyk": cmyk, "pantone": pms})
    for key, name, hx, pms, cmyk, glyph, idea, mood in MODES:
        data["modes"].append({"key": key, "name": name, "hex": hx, "rgb": hex_rgb(hx), "cmyk": cmyk, "pantone": pms,
                              "glyph": glyph, "idea": idea, "mood": mood})
    pairs = [("Carbon", "White"), ("Carbon", "Paper"), ("Carbon", "Oat"), ("Carbon", "Silver"), ("White", "Carbon"),
             ("Graphite", "Paper"), ("Stone", "White"), ("Stone", "Carbon"), ("Roast", "Oat"), ("White", "Tonic"),
             ("Tonic", "Paper"), ("Paper", "Roast")]
    pairs += [(m[1], "Paper") for m in MODES] + [("White", m[1]) for m in MODES]
    for fg, bg in pairs:
        c = contrast(colour(fg), colour(bg))
        data["text_pairings"].append({"text": fg, "ground": bg, "ratio": round(c, 2),
                                      "AA_body": c >= 4.5, "AA_large_or_graphic": c >= 3.0})
    with open(os.path.join(outdir, "mxde-palette.json"), "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    write_ase(os.path.join(outdir, "mxde-palette.ase"), [
        ("MXDE Core", [(n, h) for r, n, h, *_ in PALETTE if r in ("core", "ground")]),
        ("MXDE Warm", [(n, h) for r, n, h, *_ in PALETTE if r == "warm"]),
        ("MXDE Accent", [(n, h) for r, n, h, *_ in PALETTE if r == "accent"]),
        ("MXDE Modes", [(f"{m[1].title()} Mode", m[2]) for m in MODES]),
    ])
    return data


if __name__ == "__main__":
    d = export(os.path.join(os.path.dirname(__file__), "..", "colour"))
    for p in d["text_pairings"]:
        print(f'{p["text"]:>9} on {p["ground"]:<8} {p["ratio"]:5.2f}  body:{"AA" if p["AA_body"] else "--"}  large/graphic:{"AA" if p["AA_large_or_graphic"] else "--"}')
