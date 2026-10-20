"""Presentation mockups (not production artwork). Each returns (svg, width, height).

Large type is outlined; small copy is live text styled by the classes in FONT_CSS_*.
"""
import math
from marks import wordmark, tile, words, words_width, mode_lockup, tagline, MODE, MODE_KEYS, C
from build import WORD_W
from geom import H

COPY = {  # working copy — functions and times to be confirmed by the brand team
    "wake": ("For a sharp start.", "Morning"),
    "active": ("For the push.", "Pre-workout"),
    "zen": ("For deep focus.", "Deep work"),
    "vital": ("For a midday reset.", "Midday"),
    "calm": ("For a slow evening.", "Evening"),
}

FONT_CSS_LOCAL = """
@font-face{font-family:'Archivo';font-weight:600;font-stretch:100%;src:url('{F}/Archivo-SemiBold.ttf')}
@font-face{font-family:'Archivo';font-weight:500;font-stretch:100%;src:url('{F}/Archivo-Medium.ttf')}
@font-face{font-family:'Archivo';font-weight:500;font-stretch:112.5%;src:url('{F}/Archivo-SemiExpanded-Medium.ttf')}
@font-face{font-family:'Archivo';font-weight:600;font-stretch:125%;src:url('{F}/Archivo-Expanded-SemiBold.ttf')}
@font-face{font-family:'Archivo';font-weight:700;font-stretch:125%;src:url('{F}/Archivo-Expanded-Bold.ttf')}
@font-face{font-family:'IBM Plex Sans';font-weight:400;src:url('{F}/PlexSans-Regular.ttf')}
@font-face{font-family:'IBM Plex Sans';font-weight:500;src:url('{F}/PlexSans-Medium.ttf')}
@font-face{font-family:'IBM Plex Sans Condensed';font-weight:500;src:url('{F}/PlexSansCondensed-Medium.ttf')}
"""
FONT_LINK_WEB = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
                 '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@100..125,400..700'
                 '&family=IBM+Plex+Sans:wght@400;500&family=IBM+Plex+Sans+Condensed:wght@500&display=swap">')
TEXT_CSS = """
.t-head{font-family:'Archivo',system-ui,sans-serif;font-weight:600;font-stretch:100%}
.t-mode{font-family:'Archivo',system-ui,sans-serif;font-weight:600;font-stretch:125%;letter-spacing:.06em}
.t-sub{font-family:'Archivo',system-ui,sans-serif;font-weight:500;font-stretch:112.5%;letter-spacing:.08em;text-transform:uppercase}
.t-body{font-family:'IBM Plex Sans',system-ui,sans-serif;font-weight:400}
.t-label{font-family:'IBM Plex Sans Condensed','IBM Plex Sans',system-ui,sans-serif;font-weight:500;letter-spacing:.04em;text-transform:uppercase;font-variant-numeric:tabular-nums}
"""


def _svg(w, h, body, label):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:g} {h:g}" role="img" aria-label="{label}">'
            f'{body}</svg>', w, h)


def _serrated(x, y, w, h, teeth=6.0):
    """Sachet outline: straight sides, zig-zag seals top and bottom."""
    n = int(w // teeth)
    tw = w / n
    top = [f"{x + i * tw / 2:.2f},{y + (0 if i % 2 == 0 else teeth * 0.55):.2f}" for i in range(2 * n + 1)]
    bot = [f"{x + w - i * tw / 2:.2f},{y + h - (0 if i % 2 == 0 else teeth * 0.55):.2f}" for i in range(2 * n + 1)]
    return " ".join(top + bot)


SACHET_W, SACHET_H = 300, 440   # canonical pack canvas (≈ 75 × 110 mm flat pouch, dimensions to be confirmed)


def sachet_art(key, x=0, y=0, w=SACHET_W, ground=None, shadow=True):
    """One sachet front, drawn on the canonical canvas and scaled to width `w` at (x, y)."""
    m = MODE[key]
    g = ground or C["Paper"]
    ink = C["Carbon"]
    W, Hh, pad = SACHET_W, SACHET_H, 26
    parts = []
    if shadow:
        parts.append(f'<polygon points="{_serrated(6, 10, W, Hh)}" fill="#000" opacity=".10"/>')
    parts.append(f'<polygon points="{_serrated(0, 0, W, Hh)}" fill="{g}"/>')
    for yy in (16, Hh - 16):  # seal crimp
        parts.append(f'<rect x="0" y="{yy - 4}" width="{W}" height="8" fill="#000" opacity=".035"/>')
    parts.append(f'<rect x="0" y="30" width="{W}" height="1" fill="#000" opacity=".06"/>')
    parts.append(f'<rect x="0" y="{Hh - 31}" width="{W}" height="1" fill="#000" opacity=".06"/>')
    parts.append(wordmark(pad, 52, W * 0.52, ink, m["hex"]))
    parts.append(f'<text class="t-label" font-size="8.5" fill="{C["Graphite"]}" transform="translate({W - 14} {Hh - 48}) rotate(-90)">#SwitchYourMode</text>')
    ts = W * 0.38   # mode tile ≈ 10% of the face
    ty = 128
    parts.append(tile(key, pad, ty, ts, m["hex"]))
    parts.append(words(m["name"], pad, ty + ts + 50, 26, ink))
    parts.append(f'<text class="t-label" x="{pad}" y="{ty + ts + 74}" font-size="10" fill="{C["Graphite"]}">{COPY[key][1]} · {m["name"].title()} Mode</text>')
    parts.append(f'<text class="t-body" x="{pad}" y="{ty + ts + 93}" font-size="12" fill="{ink}">{COPY[key][0]}</text>')
    parts.append(f'<rect x="{pad}" y="{Hh - 84}" width="{W - 2 * pad - 14}" height="1" fill="{ink}" opacity=".18"/>')
    parts.append(f'<text class="t-label" x="{pad}" y="{Hh - 66}" font-size="8.5" fill="{C["Graphite"]}">Functional coffee concentrate</text>')
    parts.append(f'<text class="t-label" x="{pad}" y="{Hh - 53}" font-size="8.5" fill="{C["Graphite"]}">1 sachet · 18 ml</text>')
    k = w / W
    return f'<g transform="translate({x:g} {y:g}) scale({k:.5f})">{"".join(parts)}</g>'


def sachet(key):
    return _svg(340, 480, f'<rect width="340" height="480" fill="{C["Oat"]}"/>' + sachet_art(key, 20, 20), f"{key} sachet")


def sachet_row():
    W, Hh = 1500, 560
    body = [f'<rect width="{W}" height="{Hh}" fill="{C["Oat"]}"/>']
    for i, k in enumerate(MODE_KEYS):
        body.append(sachet_art(k, 30 + i * 292, 60, 262))
    return _svg(W, Hh, "".join(body), "Five sachets")


def thumbnail_grid():
    """The at-a-glance test: five product tiles at e-commerce thumbnail size, then in one colour."""
    W, Hh = 1000, 470
    body = [f'<rect width="{W}" height="{Hh}" fill="#fff"/>']
    for row, mono in enumerate((False, True)):
        for i, k in enumerate(MODE_KEYS):
            x, y = 20 + i * 196, 20 + row * 225
            body.append(f'<rect x="{x}" y="{y}" width="180" height="210" fill="{C["Paper"]}"/>')
            art = sachet_art(k, x + 45, y + 16, 90, shadow=False)
            if mono:
                art = f'<g style="filter:grayscale(1)">{art}</g>'
            body.append(art)
            body.append(f'<text class="t-label" x="{x + 12}" y="{y + 190}" font-size="11" fill="{C["Carbon"]}">{MODE[k]["name"].title()} Mode</text>')
    return _svg(W, Hh, "".join(body), "Thumbnail grid")


def ecom_tile(key="zen"):
    W = 1080
    body = [f'<rect width="{W}" height="{W}" fill="{C["Paper"]}"/>',
            f'<rect x="0" y="{W * 0.72}" width="{W}" height="{W * 0.28}" fill="{C["Oat"]}"/>',
            sachet_art(key, 330, 130, 420),
            tile(key, 60, 60, 56, MODE[key]["hex"]),
            words(MODE[key]["name"], 136, 116, 22, C["Carbon"]),
            f'<text class="t-label" x="60" y="1020" font-size="24" fill="{C["Graphite"]}">Box of 10 sachets</text>']
    return _svg(W, W, "".join(body), "E-commerce tile")


def carton():
    W, Hh = 1200, 820
    fx, fy, fw, fh = 240, 250, 560, 420   # front face
    dx, dy = 220, -130                    # depth vector (oblique)
    ink, ground = C["Carbon"], C["Paper"]
    body = [f'<rect width="{W}" height="{Hh}" fill="{C["Oat"]}"/>',
            f'<polygon points="{fx + 20},{fy + fh + 18} {fx + fw + dx + 40},{fy + fh + dy + 18} {fx + fw + dx + 80},{fy + fh + dy + 60} {fx + 60},{fy + fh + 60}" fill="#000" opacity=".08"/>']
    # top face
    body.append(f'<polygon points="{fx},{fy} {fx + dx},{fy + dy} {fx + fw + dx},{fy + dy} {fx + fw},{fy}" fill="{ground}"/>')
    # side face with the five mode tiles stacked (the range at a glance)
    body.append(f'<polygon points="{fx + fw},{fy} {fx + fw + dx},{fy + dy} {fx + fw + dx},{fy + fh + dy} {fx + fw},{fy + fh}" fill="#E9E5DC"/>')
    # front face
    body.append(f'<rect x="{fx}" y="{fy}" width="{fw}" height="{fh}" fill="{ink}"/>')
    body.append(wordmark(fx + 44, fy + 48, 260, C["White"], C["Tonic"]))
    body.append(words("THE MODE SET", fx + 44, fy + 162, 15, C["White"]))
    for i, k in enumerate(MODE_KEYS):
        body.append(tile(k, fx + 44 + i * 64, fy + 214, 48, MODE[k]["hex"]))
    body.append(f'<text class="t-label" x="{fx + 44}" y="{fy + 318}" font-size="13" fill="{C["Silver"]}">5 modes · 30 sachets of functional coffee concentrate</text>')
    body.append(f'<rect x="{fx + 44}" y="{fy + 344}" width="{fw - 88}" height="1" fill="{C["Stone"]}"/>')
    body.append(f'<text class="t-label" x="{fx + 44}" y="{fy + 378}" font-size="13" fill="{C["White"]}">#SwitchYourMode</text>')
    # side face artwork, sheared onto the oblique plane
    k = dy / dx
    side = []
    for i, key in enumerate(MODE_KEYS):
        side.append(tile(key, 26, 40 + i * 70, 44, MODE[key]["hex"]))
        side.append(words(MODE[key]["name"], 84, 40 + i * 70 + 32, 13, ink))
    body.append(f'<g transform="matrix(1 {k:.4f} 0 1 {fx + fw} {fy})">{"".join(side)}</g>')
    return _svg(W, Hh, "".join(body), "Outer carton")


def web_hero():
    W, Hh = 1440, 720
    ink = C["Carbon"]
    body = [f'<rect width="{W}" height="{Hh}" fill="{C["Paper"]}"/>',
            wordmark(64, 36, 120, ink, C["Tonic"]),
            f'<text class="t-sub" x="760" y="58" font-size="13" fill="{ink}">Modes</text>',
            f'<text class="t-sub" x="870" y="58" font-size="13" fill="{ink}">How it works</text>',
            f'<text class="t-sub" x="1040" y="58" font-size="13" fill="{ink}">Subscribe</text>',
            f'<rect x="1220" y="34" width="156" height="36" fill="none" stroke="{ink}" stroke-width="1.5"/>',
            f'<text class="t-sub" x="1298" y="58" font-size="13" fill="{ink}" text-anchor="middle">Cart (0)</text>',
            f'<rect x="64" y="96" width="{W - 128}" height="1" fill="{ink}" opacity=".15"/>',
            f'<text class="t-sub" x="64" y="186" font-size="14" fill="{C["Tonic"]}">Functional coffee · single-serve concentrate</text>',
            f'<text class="t-head" x="60" y="262" font-size="64" fill="{ink}" letter-spacing="-1">The right coffee</text>',
            f'<text class="t-head" x="60" y="334" font-size="64" fill="{ink}" letter-spacing="-1">for the state you</text>',
            f'<text class="t-head" x="60" y="406" font-size="64" fill="{ink}" letter-spacing="-1">want to be in.</text>',
            f'<text class="t-body" x="64" y="462" font-size="19" fill="{C["Graphite"]}">Five modes, one for each need of the day. Tear, pour, switch.</text>',
            f'<rect x="64" y="510" width="232" height="56" fill="{C["Tonic"]}"/>',
            f'<text class="t-sub" x="180" y="544" font-size="14" fill="#fff" text-anchor="middle">Find your mode</text>',
            f'<text class="t-label" x="330" y="544" font-size="14" fill="{ink}">#SwitchYourMode</text>']
    for i, k in enumerate(MODE_KEYS):
        x = 752 + i * 128
        y = 150 + (i % 2) * 70
        body.append(sachet_art(k, x, y, 118))
    for i, k in enumerate(MODE_KEYS):
        x = 760 + i * 128
        body.append(tile(k, x, 600, 26, MODE[k]["hex"]))
        body.append(f'<text class="t-label" x="{x + 34}" y="619" font-size="12" fill="{ink}">{MODE[k]["name"]}</text>')
    return _svg(W, Hh, "".join(body), "Website hero")


def browser_header():
    W, Hh = 1200, 300
    ink = C["Carbon"]
    body = [f'<rect width="{W}" height="{Hh}" fill="#DADBDD"/>',
            # tab strip
            f'<rect x="0" y="0" width="{W}" height="46" fill="#DADBDD"/>',
            *[f'<rect x="{18 + i * 20}" y="17" width="12" height="12" fill="#B9BBBF"/>' for i in range(3)],
            f'<polygon points="90,46 100,10 340,10 350,46" fill="#fff"/>',
            tile("x", 112, 20, 16, ink, small=True),
            f'<text class="t-body" x="138" y="33" font-size="13" fill="{ink}">MXDE — SwitchYourMode</text>',
            f'<text class="t-body" x="322" y="33" font-size="13" fill="{C["Stone"]}">×</text>',
            f'<polygon points="350,46 358,16 520,16 528,46" fill="#E6E7E9"/>',
            f'<rect x="372" y="24" width="14" height="14" fill="#9A9CA0"/>',
            f'<text class="t-body" x="394" y="35" font-size="13" fill="#6B6E73">Other tab</text>',
            # url bar
            f'<rect x="0" y="46" width="{W}" height="48" fill="#fff"/>',
            f'<rect x="120" y="54" width="{W - 240}" height="32" fill="#F0F1F2"/>',
            f'<text class="t-body" x="140" y="75" font-size="14" fill="#55585D">mxde · shop</text>',
            # site header
            f'<rect x="0" y="94" width="{W}" height="206" fill="{C["Paper"]}"/>',
            wordmark(48, 128, 112, ink, C["Tonic"]),
            *[f'<text class="t-sub" x="{x}" y="150" font-size="12" fill="{ink}">{t}</text>' for x, t in ((640, "Modes"), (740, "How it works"), (900, "Subscribe"), (1050, "Cart (0)"))],
            f'<rect x="48" y="184" width="{W - 96}" height="1" fill="{ink}" opacity=".15"/>']
    for i, k in enumerate(MODE_KEYS):
        x = 48 + i * 224
        body.append(tile(k, x, 214, 40, MODE[k]["hex"]))
        body.append(words(MODE[k]["name"], x + 54, 246, 15, ink))
    return _svg(W, Hh, "".join(body), "Website header and favicon")


def ig_post(key="active"):
    """The switch, as a social post: the slot takes the mode's tile."""
    W = 1080
    m = MODE[key]
    ink = C["Carbon"]
    body = [f'<rect width="{W}" height="{W}" fill="{C["Paper"]}"/>',
            wordmark(120, 330, 840, ink, m["hex"], slot_key=key),
            words(m["name"] + " MODE", 124, 640, 40, ink),
            f'<text class="t-body" x="124" y="700" font-size="34" fill="{C["Graphite"]}">{COPY[key][0]}</text>',
            f'<rect x="124" y="880" width="832" height="2" fill="{ink}" opacity=".15"/>',
            f'<text class="t-label" x="124" y="944" font-size="30" fill="{ink}">#SwitchYourMode</text>',
            tile("x", 900, 906, 56, ink)]
    return _svg(W, W, "".join(body), "Instagram post")


def ig_story(key="calm"):
    W, Hh = 1080, 1920
    m = MODE[key]
    body = [f'<rect width="{W}" height="{Hh}" fill="{C["Carbon"]}"/>',
            wordmark(96, 180, 300, C["Paper"], m["hex"]),
            tile(key, 96, 560, 520, m["hex"]),
            words(m["name"], 96, 1230, 110, C["Paper"]),
            f'<text class="t-body" x="100" y="1320" font-size="44" fill="{C["Silver"]}">{COPY[key][0]}</text>',
            f'<text class="t-label" x="100" y="1400" font-size="32" fill="{C["Stone"]}">{COPY[key][1]} · 20:00 onward (to confirm)</text>',
            f'<rect x="96" y="1640" width="{W - 192}" height="96" fill="none" stroke="{C["Paper"]}" stroke-width="3"/>',
            f'<text class="t-sub" x="{W / 2}" y="1700" font-size="32" fill="{C["Paper"]}" text-anchor="middle">Switch to {m["name"].title()}</text>']
    return _svg(W, Hh, "".join(body), "Instagram story")


def ig_profile():
    W, Hh = 1080, 560
    ink = C["Carbon"]
    r = 150
    body = [f'<rect width="{W}" height="{Hh}" fill="#fff"/>',
            f'<defs><clipPath id="pfp"><circle cx="{80 + r}" cy="{70 + r}" r="{r}"/></clipPath></defs>',
            f'<g clip-path="url(#pfp)"><rect x="80" y="70" width="{2 * r}" height="{2 * r}" fill="{ink}"/>'
            + tile("x", 80 + r - 0.46 * r, 70 + r - 0.46 * r, 0.92 * r, C["Paper"]) + '</g>',
            f'<text class="t-head" x="440" y="130" font-size="40" fill="{ink}">mxde</text>',
            *[f'<text class="t-head" x="{440 + i * 190}" y="210" font-size="36" fill="{ink}">{n}</text>'
              f'<text class="t-body" x="{440 + i * 190}" y="246" font-size="24" fill="{C["Graphite"]}">{l}</text>'
              for i, (n, l) in enumerate((("5", "modes"), ("—", "followers"), ("—", "following")))],
            f'<text class="t-body" x="80" y="430" font-size="28" fill="{ink}">Functional coffee. One brand, many modes.</text>',
            f'<text class="t-body" x="80" y="472" font-size="28" fill="{C["Tonic"]}">#SwitchYourMode</text>']
    return _svg(W, Hh, "".join(body), "Instagram profile")


def tumbler():
    W, Hh = 800, 900
    ink = C["Carbon"]
    cx = W / 2
    top, bot, y0, y1 = 300, 236, 180, 820
    lid = f'<polygon points="{cx - top / 2 - 6},{y0 - 60} {cx + top / 2 + 6},{y0 - 60} {cx + top / 2 + 6},{y0} {cx - top / 2 - 6},{y0}" fill="{C["Graphite"]}"/>'
    lid += f'<rect x="{cx - 50}" y="{y0 - 74}" width="100" height="14" fill="{C["Graphite"]}"/>'
    bodyp = f'<polygon points="{cx - top / 2},{y0} {cx + top / 2},{y0} {cx + bot / 2},{y1} {cx - bot / 2},{y1}" fill="{ink}"/>'
    sheen = f'<polygon points="{cx - top / 2 + 22},{y0} {cx - top / 2 + 40},{y0} {cx - bot / 2 + 34},{y1} {cx - bot / 2 + 18},{y1}" fill="#fff" opacity=".06"/>'
    body = [f'<rect width="{W}" height="{Hh}" fill="{C["Oat"]}"/>',
            f'<rect x="{cx - bot / 2 - 10}" y="{y1}" width="{bot + 80}" height="18" fill="#000" opacity=".08"/>',
            bodyp, sheen, lid,
            tile("x", cx - 70, 330, 140, C["Silver"]),
            wordmark(cx - 82, 560, 164, C["Silver"]),
            f'<text class="t-label" x="{cx}" y="640" font-size="14" fill="{C["Stone"]}" text-anchor="middle">#SwitchYourMode</text>']
    return _svg(W, Hh, "".join(body), "Tumbler")


ALL = {
    **{f"sachet-{k}": (lambda k=k: sachet(k)) for k in MODE_KEYS},
    "sachets-all": sachet_row,
    "thumbnail-grid": thumbnail_grid,
    "carton": carton,
    "ecom-tile": ecom_tile,
    "web-hero": web_hero,
    "web-header-favicon": browser_header,
    "instagram-post": ig_post,
    "instagram-story": ig_story,
    "instagram-profile": ig_profile,
    "tumbler": tumbler,
}
