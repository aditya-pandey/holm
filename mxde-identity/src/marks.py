"""Inline SVG fragments of the MXDE marks, for mockups, the presentation and the guidelines."""
from shapely import affinity
from geom import H, mode_tile, to_path
from build import LETTERS, SLOT, WORD_W, SLOT_X, KCUT, MODE_TILE, MODE_GAP
from palette import MODES, colour
from text import text_path, text_width

MODE_KEYS = [m[0] for m in MODES]
MODE = {m[0]: {"key": m[0], "name": m[1], "hex": m[2], "pms": m[3], "cmyk": m[4], "glyph": m[5], "idea": m[6], "mood": m[7]}
        for m in MODES}
HEAD = "Archivo-Expanded-SemiBold.ttf"

_letters_d = to_path(LETTERS, 0, H)
_slot_d = to_path(SLOT, 0, H)
_tile_d = {k: to_path(mode_tile(k, KCUT), 0, H) for k in ["x"] + MODE_KEYS}
# a heavier cut for tiles drawn small (≤ 48 px / ≤ 12 mm)
_tile_small_d = {k: to_path(mode_tile(k, 0.15 * H), 0, H) for k in ["x"] + MODE_KEYS}


def wordmark(x, y, width, letters="currentColor", slot=None, slot_key="x", cls=""):
    """Wordmark with its top-left at (x, y), scaled to `width`. slot_key swaps a mode tile into the slot."""
    s = width / WORD_W
    slot = slot or letters
    sd = _slot_d if slot_key == "x" else None
    tile = "" if sd else f'<path transform="translate({SLOT_X:g} 0)" d="{_tile_d[slot_key]}" fill="{slot}"/>'
    sp = f'<path d="{sd}" fill="{slot}"/>' if sd else ""
    c = f' class="{cls}"' if cls else ""
    return (f'<g{c} transform="translate({x:g} {y:g}) scale({s:.5f})"><path d="{_letters_d}" fill="{letters}"/>'
            f'{sp}{tile}</g>')


def tile(key, x, y, size, fill, small=None, cls=""):
    s = size / H
    small = size < 60 if small is None else small
    d = (_tile_small_d if small else _tile_d)[key]
    c = f' class="{cls}"' if cls else ""
    return f'<path{c} transform="translate({x:g} {y:g}) scale({s:.5f})" d="{d}" fill="{fill}"/>'


def tile_d(key, small=False):
    return (_tile_small_d if small else _tile_d)[key]


def words(s, x, baseline, cap, fill, font=HEAD, tracking=0.06, anchor="start"):
    if anchor != "start":
        w = text_width(s, font, cap, tracking)
        x = x - (w if anchor == "end" else w / 2)
    d, w = text_path(s, font, x, baseline, cap, tracking)
    return f'<path d="{d}" fill="{fill}"/>'


def words_width(s, cap, font=HEAD, tracking=0.06):
    return text_width(s, font, cap, tracking)


def mode_lockup(x, y, width, key, letters="currentColor", tint=None):
    """Wordmark + mode line hanging from the X, as in modes/svg."""
    m = MODE[key]
    tint = tint or m["hex"]
    s = width / WORD_W
    ty = H + MODE_GAP
    ts = MODE_TILE
    nx = SLOT_X + ts + 0.32 * ts
    inner = (f'<path d="{_letters_d}" fill="{letters}"/><path d="{_slot_d}" fill="{tint}"/>'
             f'<path transform="translate({SLOT_X:g} {ty:g}) scale({ts / H:.5f})" d="{_tile_small_d[key]}" fill="{tint}"/>'
             + words(m["name"], nx, ty + ts, ts, letters))
    return f'<g transform="translate({x:g} {y:g}) scale({s:.5f})">{inner}</g>'


def lockup_height(width):
    return (H + MODE_GAP + MODE_TILE) * width / WORD_W


def tagline(x, baseline, cap, fill, text="SwitchYourMode", font="Archivo-Medium.ttf"):
    return words(text, x, baseline, cap, fill, font=font, tracking=0.02)


C = {n: colour(n) for n in ("Carbon", "Graphite", "Stone", "Silver", "White", "Paper", "Oat", "Roast", "Tonic")}
