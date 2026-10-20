"""Stage 2 — three wordmark routes, black on white."""
import os
from shapely.ops import unary_union
from geom import H, letter_M, letter_D, letter_E, letter_X_crossover, letter_X_box, letter_X_shift, letter_X_plain, place, to_path

OUT = os.path.join(os.path.dirname(__file__), "..", "concepts")
os.makedirs(OUT, exist_ok=True)


def wordmark(letters, gaps):
    """letters: [(geom, advance)], gaps: spacing after each letter (len-1)."""
    x, parts = 0.0, []
    for i, (g, adv) in enumerate(letters):
        parts.append(place(g, x))
        x += adv + (gaps[i] if i < len(gaps) else 0)
    return unary_union(parts), x


def write_svg(geom, width, name, pad=0.22, title="MXDE"):
    p = pad * H
    vw, vh = width + 2 * p, H + 2 * p
    d = to_path(geom, ox=p, oy=p + H)
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {vw:g} {vh:g}" role="img" aria-label="{title}">'
           f'<title>{title}</title><path fill="#000" d="{d}"/></svg>\n')
    with open(os.path.join(OUT, name), "w") as f:
        f.write(svg)
    return svg


def route(xfn, w, gaps, **kw):
    M, wm = letter_M(w)
    X, wx = xfn(w, **kw)
    D, wd = letter_D(w)
    E, we = letter_E(w)
    return wordmark([(M, wm), (X, wx), (D, wd), (E, we)], gaps)


if __name__ == "__main__":
    # Route A — Crossover: the X as a crossing point; one bar passes over the other.
    g, wdt = route(letter_X_crossover, 17, [14, 14, 22])
    write_svg(g, wdt, "route-a-crossover.svg")
    # Route B — Slot: the O's square footprint, the X cut out of it. Reads "Mode", spells MXDE.
    g, wdt = route(letter_X_box, 18, [20, 20, 22])
    write_svg(g, wdt, "route-b-slot.svg")
    # Weight study on route B, light to bold.
    for w in (10, 14, 18, 22):
        g, wdt = route(letter_X_box, w, [16 + w * 0.25] * 2 + [18 + w * 0.25], gap=0.62)
        write_svg(g, wdt, f"weight-study-b-{w}.svg")
    # Route C — Shift: the X split at the waist and thrown sideways, like a switch.
    g, wdt = route(letter_X_shift, 16, [14, 14, 22])
    write_svg(g, wdt, "route-c-shift.svg")
    # Reference: the unmodified straight-line build, for the story's "before".
    g, wdt = route(letter_X_plain, 17, [14, 14, 22])
    write_svg(g, wdt, "reference-plain.svg")
    print("ok")
