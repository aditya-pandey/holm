"""The MXDE identity, told as a reel: a single self-contained HTML page (presentation/mxde-identity.html)."""
import html
import json
import os
from build import WORD_W, SLOT_X, KCUT, STEM, MODE_TILE, MODE_GAP
from geom import H
from palette import PALETTE, MODES, contrast, hex_rgb
from marks import wordmark, tile, tile_d, words, mode_lockup, lockup_height, tagline, MODE, MODE_KEYS, C, _letters_d
from text import text_path
from diagrams import story_frames, construction, clear_space, growth, routes_svg, misuse
from mockups import ALL as MOCKS, FONT_LINK_WEB, TEXT_CSS, COPY

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
HEAD = "Archivo-Expanded-SemiBold.ttf"


def svg(w, h, body, label, cls=""):
    c = f' class="{cls}"' if cls else ""
    return f'<svg{c} xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:g} {h:g}" role="img" aria-label="{html.escape(label)}">{body}</svg>'


def mock(name):
    s, w, h = MOCKS[name]()
    return s.replace("<svg ", '<svg class="mock" ', 1)


# ---------------------------------------------------------------- hero: the switch
def hero_svg():
    ty = H + MODE_GAP
    ts = MODE_TILE
    nx = SLOT_X + ts + 0.32 * ts
    vh = ty + ts + 2
    names = {}
    for k in MODE_KEYS:
        d, _ = text_path(MODE[k]["name"], HEAD, nx, ty + ts, ts, 0.06)
        names[k] = d
    tag_d, _ = text_path("SwitchYourMode", "Archivo-Medium.ttf", 0, ty + ts, 0.24 * H, 0.02)  # same as the tagline lockup
    names["x"] = tag_d
    tiles = {k: tile_d(k) for k in ["x"] + MODE_KEYS}
    small = {k: tile_d(k, small=True) for k in MODE_KEYS}
    body = (f'<path d="{_letters_d}" fill="currentColor"/>'
            f'<g class="slot-g"><path id="slot" transform="translate({SLOT_X:g} 0)" d="{tiles["x"]}" fill="var(--slot)"/></g>'
            f'<g class="line-g"><path id="mtile" transform="translate({SLOT_X:g} {ty:g}) scale({ts / H:.5f})" d="" fill="var(--slot)"/>'
            f'<path id="mname" d="{tag_d}" fill="currentColor"/></g>')
    data = {"tiles": tiles, "small": small, "names": names}
    return svg(WORD_W, vh, body, "MXDE wordmark with a switchable mode slot", "hero-svg"), data


def build():
    hero, hero_data = hero_svg()
    modes_js = {k: {"name": MODE[k]["name"], "hex": MODE[k]["hex"], "mood": MODE[k]["mood"], "idea": MODE[k]["idea"],
                    "copy": COPY[k][0], "when": COPY[k][1]} for k in MODE_KEYS}

    chips = '<button type="button" class="chip-btn is-on" data-mode="x" aria-pressed="true">' + svg(H, H, f'<path d="{tile_d("x", True)}" fill="currentColor"/>', "X") + '<span>MXDE</span></button>'
    for k in MODE_KEYS:
        chips += (f'<button type="button" class="chip-btn" data-mode="{k}" aria-pressed="false" style="--c:{MODE[k]["hex"]}">'
                  + svg(H, H, f'<path d="{tile_d(k, True)}" fill="var(--c)"/>', MODE[k]["name"]) + f'<span>{MODE[k]["name"].title()}</span></button>')

    # ------------------------------------------------ the reel
    frames = story_frames(ink="currentColor", accent="var(--tonic-on-dark)")
    stage = "".join(f'<div class="stage-frame" data-i="{i}"{"" if i == 4 else " hidden"}>{s}</div>' for i, (_, s) in enumerate(frames))
    thumbs = "".join(f'<li><button type="button" class="thumb{" is-on" if i == 4 else ""}" data-i="{i}" aria-label="Frame {i + 1}: {html.escape(c)}">{s}'
                     f'<span class="cap"><b>{i + 1:02d}</b> {html.escape(c)}</span></button></li>' for i, (c, s) in enumerate(frames))

    # ------------------------------------------------ routes
    r = routes_svg("currentColor")
    routes = [
        ("a", "Crossover", "One bar of the X passes over the other: a crossing point.",
         "Reads as an X, but the break pulls the eye to M-X-D-E, and the gap fills in below 24 px.", False),
        ("b", "Slot", "The O becomes a square slot with the X cut into it. It reads Mode and spells MXDE.",
         "The only route that reads 'Mode' first. At 16 px the slot is a dark O. Up close it's an X.", True),
        ("c", "Shift", "The X splits at its waist and the top half slides over, like a switch being thrown.",
         "Has momentum, but the jog reads as a glitch and does nothing for 'Mode'.", False),
    ]
    route_cards = "".join(
        f'<article class="route{" is-pick" if pick else ""}"><div class="route-art">{r[k]}</div>'
        f'<div class="route-txt"><p class="eyebrow">Route {k.upper()}{" · recommended" if pick else ""}</p><h3>{name}</h3><p>{idea}</p><p class="verdict">{verdict}</p></div></article>'
        for k, name, idea, verdict, pick in routes)

    # ------------------------------------------------ small sizes
    ladder = "".join(f'<figure><div class="lad" style="height:{px}px">{svg(WORD_W, H, wordmark(0, 0, WORD_W, "currentColor", "currentColor"), "MXDE", "lad-svg")}</div><figcaption>{px} px</figcaption></figure>'
                     for px in (12, 16, 24, 32, 48, 72))

    # ------------------------------------------------ modes
    mode_cards = ""
    for k in MODE_KEYS:
        m = MODE[k]
        mode_cards += (f'<article class="mode-card" style="--c:{m["hex"]}">'
                       f'<div class="mode-tiles">{svg(H, H, tile(k, 0, 0, H, "var(--c)"), m["name"])}{svg(H, H, tile(k, 0, 0, H, "currentColor"), m["name"] + " one colour")}</div>'
                       f'<h3 class="mode-name">{m["name"]}</h3><p>{m["idea"]}</p>'
                       f'<p class="muted">{m["mood"]} · {COPY[k][1]} <span class="tbc">to confirm</span></p>'
                       f'<p class="codes">{m["hex"]} · Pantone {m["pms"]}</p></article>')
    lockups = "".join(f'<figure class="lockup">{svg(WORD_W, lockup_height(WORD_W), mode_lockup(0, 0, WORD_W, k, "currentColor"), MODE[k]["name"] + " lockup")}</figure>' for k in MODE_KEYS)
    lockups += f'<figure class="lockup rev">{svg(WORD_W, lockup_height(WORD_W), mode_lockup(0, 0, WORD_W, "calm", C["Paper"]), "Calm lockup reversed")}</figure>'
    grow = "".join(f'<figure class="grow">{s}<figcaption>{html.escape(n)}</figcaption></figure>' for n, s in growth("currentColor"))

    # ------------------------------------------------ palette
    def swatch(name, hx, pms, cmyk, role):
        rr, gg, bb = hex_rgb(hx)
        on = C["Carbon"] if contrast(hx, C["Carbon"]) > contrast(hx, "#FFFFFF") else "#FFFFFF"
        return (f'<li class="sw" style="--sw:{hx};--on:{on}"><div class="sw-chip"><span>{name}</span>'
                f'<button type="button" class="copy" data-copy="{hx}" aria-label="Copy {hx}">{hx}</button></div>'
                f'<dl><dt>RGB</dt><dd>{rr} {gg} {bb}</dd><dt>CMYK</dt><dd>{" ".join(map(str, cmyk))}</dd><dt>Pantone</dt><dd>{pms}</dd><dt>Role</dt><dd>{role}</dd></dl></li>')
    role_names = {"core": "Core neutral", "ground": "Light ground", "warm": "Warm neutral", "accent": "Accent ≤10%"}
    swatches = "".join(swatch(n, h, p, c, role_names[r]) for r, n, h, p, c in PALETTE)
    mode_sw = "".join(swatch(m[1].title(), m[2], m[3], m[4], "Mode tint") for m in MODES)

    # ------------------------------------------------ misuse
    mis = "".join(f'<figure class="mis">{s}<figcaption>{html.escape(c)}</figcaption></figure>' for c, s in misuse())

    # ------------------------------------------------ assemble
    page = TEMPLATE
    repl = {
        "{{FONTS}}": FONT_LINK_WEB, "{{TEXTCSS}}": TEXT_CSS, "{{HERO}}": hero, "{{CHIPS}}": chips,
        "{{DATA}}": json.dumps({"hero": hero_data, "modes": modes_js}),
        "{{STAGE}}": stage, "{{THUMBS}}": thumbs, "{{ROUTES}}": route_cards, "{{LADDER}}": ladder,
        "{{CONSTRUCTION}}": construction("currentColor", "var(--guide)", "var(--muted)"),
        "{{CLEAR}}": clear_space("currentColor", "var(--guide)"),
        "{{MODECARDS}}": mode_cards, "{{LOCKUPS}}": lockups, "{{GROW}}": grow,
        "{{SWATCHES}}": swatches, "{{MODESW}}": mode_sw, "{{MISUSE}}": mis,
        "{{M_SACHETS}}": mock("sachets-all"), "{{M_GRID}}": mock("thumbnail-grid"), "{{M_CARTON}}": mock("carton"),
        "{{M_ECOM}}": mock("ecom-tile"), "{{M_HERO}}": mock("web-hero"), "{{M_HEADER}}": mock("web-header-favicon"),
        "{{M_POST}}": mock("instagram-post"), "{{M_STORY}}": mock("instagram-story"), "{{M_PROFILE}}": mock("instagram-profile"),
        "{{M_TUMBLER}}": mock("tumbler"),
        "{{STEM}}": f"{STEM:g}", "{{KCUT}}": f"{KCUT:.1f}",
        "{{TAGLOCK}}": svg(WORD_W, H * 1.72, wordmark(0, 0, WORD_W, "currentColor", "var(--accent)") + tagline(0, H + 0.42 * H + 0.24 * H, 0.24 * H, "currentColor"), "Tagline lockup"),
        "{{MONO}}": svg(H, H, tile("x", 0, 0, H, "currentColor"), "Monogram"),
        "{{APP}}": svg(512, 512, f'<rect width="512" height="512" fill="{C["Carbon"]}"/>' + tile("x", 138.24, 138.24, 235.52, C["Paper"]), "App icon"),
        "{{FAV}}": svg(64, 64, f'<rect width="64" height="64" fill="{C["Carbon"]}"/>' + f'<path d="M0 0" />' + tile("x", 0, 0, 64, "none"), "Favicon"),
        "{{WM}}": svg(WORD_W, H, wordmark(0, 0, WORD_W, "currentColor", "var(--accent)"), "MXDE"),
    }
    # favicon drawn the same way as icons/favicon.svg
    fav = open(os.path.join(ROOT, "icons", "favicon.svg")).read()
    repl["{{FAV}}"] = fav.replace("<svg ", '<svg class="fav" ', 1)
    for k, v in repl.items():
        page = page.replace(k, v)
    out = os.path.join(ROOT, "presentation", "mxde-identity.html")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w") as f:
        f.write(page)
    return out, len(page)


TEMPLATE = r"""<title>MXDE Brand Identity</title>
<meta name="claude:viewport-fit-sides" content="cover">
{{FONTS}}
<style>
/* Layout: a reel. Full-width bands, each one beat of the story, alternating Paper and a fixed Carbon "screening" band. */
:root{
  --bg:#F4F2ED; --surface:#FFFFFF; --card:#ECE9E2; --ink:#151515; --muted:#55585C; --line:#DEDAD2;
  --accent:#0E6B5E; --guide:#2F6BFF; --slot:var(--accent);
  --carbon:#151515; --paper:#F4F2ED; --silver:#C8C9C7; --stone:#888B8D; --tonic-on-dark:#3FA08E;
  --f-display:'Archivo',system-ui,sans-serif; --f-body:'IBM Plex Sans',system-ui,sans-serif; --f-util:'IBM Plex Sans Condensed','IBM Plex Sans',system-ui,sans-serif;
}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){
  --bg:#121212; --surface:#1B1B1B; --card:#1F1F1E; --ink:#F1EFEA; --muted:#A7A9AC; --line:#2C2C2B; --accent:#3FA08E; --guide:#7FA2FF; color-scheme:dark}}
:root[data-theme="dark"]{--bg:#121212; --surface:#1B1B1B; --card:#1F1F1E; --ink:#F1EFEA; --muted:#A7A9AC; --line:#2C2C2B; --accent:#3FA08E; --guide:#7FA2FF; color-scheme:dark}
*{box-sizing:border-box}
body{background:var(--bg);color:var(--ink);font-family:var(--f-body);font-size:16px;line-height:1.55;margin:0}
{{TEXTCSS}}
.wrap{max-width:1180px;margin:0 auto;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}
section{padding-block:clamp(56px,8vw,112px);border-top:1px solid var(--line)}
section.reel{background:var(--carbon);color:var(--paper);border-top:0}
h1,h2,h3{font-family:var(--f-display);font-weight:600;letter-spacing:-.01em;margin:0;text-wrap:balance}
h2{font-size:clamp(28px,4vw,44px);line-height:1.08;max-width:22ch}
h3{font-size:20px;line-height:1.2}
p{margin:0}
.eyebrow{font-family:var(--f-display);font-stretch:112.5%;font-weight:500;text-transform:uppercase;letter-spacing:.1em;font-size:12px;color:var(--muted)}
.reel .eyebrow{color:var(--stone)}
.lede{font-size:clamp(17px,1.6vw,20px);max-width:60ch;color:var(--muted);margin-top:16px}
.reel .lede{color:var(--silver)}
.head{display:grid;gap:12px;margin-bottom:clamp(28px,4vw,48px)}
.muted{color:var(--muted)}
.tbc{font-family:var(--f-util);font-weight:500;text-transform:uppercase;letter-spacing:.05em;font-size:11px;border:1px solid currentColor;padding:0 5px;margin-left:4px;white-space:nowrap}
svg{display:block;max-width:100%;height:auto}
button{font:inherit;color:inherit;cursor:pointer}
:focus-visible{outline:2px solid var(--guide);outline-offset:3px}

/* hero */
.hero{padding-block:clamp(40px,7vw,96px) clamp(40px,6vw,80px);border-top:0}
.hero-top{display:flex;justify-content:space-between;gap:16px;align-items:baseline;margin-bottom:clamp(32px,6vw,72px);flex-wrap:wrap}
.hero-svg{width:100%;color:var(--ink)}
.hero-svg .slot-g{transform-box:fill-box;transform-origin:center;transition:transform .18s cubic-bezier(.5,0,.75,0)}
.hero-svg.flip .slot-g{transform:scaleX(0)}
.hero-svg #mtile,.hero-svg #mname{transition:opacity .2s}
.hero-svg.flip #mtile,.hero-svg.flip #mname{opacity:0}
.switch{display:flex;flex-wrap:wrap;gap:8px;margin-top:clamp(28px,4vw,44px)}
.chip-btn{display:flex;align-items:center;gap:8px;background:var(--surface);border:1px solid var(--line);padding:8px 14px 8px 10px;font-family:var(--f-display);font-weight:500;font-stretch:112.5%;text-transform:uppercase;letter-spacing:.08em;font-size:12px}
.chip-btn svg{width:18px;height:18px}
.chip-btn.is-on{border-color:var(--ink);box-shadow:inset 0 0 0 1px var(--ink)}
.hero-copy{display:grid;grid-template-columns:minmax(0,1.1fr) minmax(0,1fr);gap:clamp(24px,4vw,64px);margin-top:clamp(28px,4vw,48px);align-items:end}
.hero-copy h1{font-size:clamp(30px,4.4vw,52px);line-height:1.04}
.hero-copy h1 em{font-style:normal;color:var(--accent)}
#mode-readout{font-family:var(--f-util);font-weight:500;letter-spacing:.04em;text-transform:uppercase;font-size:13px;color:var(--muted);min-height:3.2em}

/* reel */
.stage{background:#1D1D1D;aspect-ratio:360/220;max-width:860px;margin:0 auto;color:var(--paper)}
.stage .frame{width:100%;height:100%}
.thumbs{list-style:none;padding:0;margin:20px 0 0;display:grid;grid-template-columns:repeat(6,minmax(0,1fr));gap:10px}
.thumb{background:#1D1D1D;border:1px solid #2A2A2A;padding:0;width:100%;text-align:left;color:var(--paper);display:flex;flex-direction:column;height:100%}
.thumb.is-on{border-color:var(--paper)}
.thumb .cap{font-size:12.5px;line-height:1.35;padding:8px 10px 10px;color:var(--silver)}
.thumb .cap b{font-family:var(--f-util);color:var(--paper);margin-right:4px}
.reel-ctl{display:flex;gap:12px;justify-content:center;margin-top:20px}
.ghost{background:none;border:1px solid currentColor;padding:8px 16px;font-family:var(--f-display);font-stretch:112.5%;font-weight:500;letter-spacing:.08em;text-transform:uppercase;font-size:12px}

/* routes */
.routes{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px}
.route{background:var(--surface);border:1px solid var(--line);display:flex;flex-direction:column}
.route.is-pick{border-color:var(--ink);box-shadow:inset 0 0 0 1px var(--ink)}
.route-art{padding:28px 22px;border-bottom:1px solid var(--line);color:var(--ink)}
.route-txt{padding:18px 22px 22px;display:grid;gap:8px;align-content:start}
.verdict{font-size:14px;color:var(--muted);border-top:1px dashed var(--line);padding-top:10px}

/* craft */
.two{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:clamp(24px,4vw,56px);align-items:start}
.panel{background:var(--surface);border:1px solid var(--line);padding:clamp(16px,2.4vw,28px)}
.ladder{display:flex;flex-wrap:wrap;align-items:flex-end;gap:22px}
.ladder figure{margin:0;display:grid;gap:6px}
.lad .lad-svg{height:100%;width:auto}
.ladder figcaption,.cap-s{font-family:var(--f-util);font-weight:500;font-size:12px;letter-spacing:.04em;text-transform:uppercase;color:var(--muted)}
.squint{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px;margin-top:20px}
.squint div{padding:18px;background:var(--card)}
.squint .blur svg{filter:blur(3px)}
.specs{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:1px;background:var(--line);border:1px solid var(--line);margin-top:20px}
.specs div{background:var(--surface);padding:14px 16px}
.specs b{display:block;font-family:var(--f-display);font-size:24px;font-variant-numeric:tabular-nums}
.specs span{font-size:13px;color:var(--muted)}
.diagram{color:var(--ink);overflow-x:auto}
.diagram svg{min-width:560px}
.kit{display:grid;grid-template-columns:2fr 1fr 1fr 1fr;gap:16px;margin-top:16px}
.kit figure{margin:0;background:var(--surface);border:1px solid var(--line);padding:22px;display:grid;gap:14px;align-content:space-between}
.kit .k-mono svg{width:72px}
.kit .fav,.kit .k-app svg{width:72px;height:72px}
.kit figcaption{font-size:14px;color:var(--muted)}

/* modes */
.modes{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:12px}
.mode-card{background:var(--surface);border:1px solid var(--line);padding:18px;display:grid;gap:8px;align-content:start}
.mode-tiles{display:grid;grid-template-columns:1fr 1fr;gap:8px;color:var(--ink)}
.mode-name{font-stretch:125%;letter-spacing:.06em;font-size:18px;margin-top:6px}
.mode-sign{font-size:13px;color:var(--muted);font-family:var(--f-util)}
.mode-card p{font-size:14px}
.codes{font-family:var(--f-util);font-size:12px;color:var(--muted);font-variant-numeric:tabular-nums}
.vision{display:flex;flex-wrap:wrap;gap:8px;margin:0 0 18px}
.vision button{background:var(--surface);border:1px solid var(--line);padding:6px 12px;font-size:13px}
.vision button[aria-pressed="true"]{border-color:var(--ink);box-shadow:inset 0 0 0 1px var(--ink)}
.modes-wrap[data-vision="grey"] .mode-card{filter:grayscale(1)}
.modes-wrap[data-vision="deut"] .mode-card{filter:url(#deut)}
.modes-wrap[data-vision="trit"] .mode-card{filter:url(#trit)}
.lockups{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px;margin-top:28px}
.lockup.rev{background:var(--carbon);border-color:var(--carbon)}
.lockup{margin:0;background:var(--surface);border:1px solid var(--line);padding:22px;color:var(--ink)}
.grow-row{display:flex;flex-wrap:wrap;gap:20px;margin-top:18px}
.grow{margin:0;width:110px;color:var(--muted)} .grow figcaption{font-size:12px;margin-top:6px}
.rules{margin:16px 0 0;padding-left:18px;display:grid;gap:8px;font-size:15px;max-width:60ch}

/* colour */
.swatches{list-style:none;padding:0;margin:0;display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:12px}
.swatches.brand{grid-template-columns:repeat(3,minmax(0,1fr))}
.sw{background:var(--surface);border:1px solid var(--line)}
.sw-chip{background:var(--sw);color:var(--on);height:108px;padding:12px;display:flex;flex-direction:column;justify-content:space-between;font-family:var(--f-display);font-weight:600;border-bottom:1px solid var(--line)}
.copy{align-self:flex-start;background:none;border:1px solid currentColor;color:inherit;font-family:var(--f-util);font-size:12px;padding:2px 8px;letter-spacing:.04em}
.sw dl{display:grid;grid-template-columns:auto 1fr;gap:2px 12px;margin:0;padding:12px;font-size:13px}
.sw dt{font-family:var(--f-util);color:var(--muted);text-transform:uppercase;font-size:11px;letter-spacing:.05em;padding-top:2px}
.sw dd{margin:0;font-variant-numeric:tabular-nums}
.ratio{display:flex;height:40px;margin-top:20px;font-family:var(--f-util);font-size:12px;text-transform:uppercase;letter-spacing:.05em;border:1px solid var(--line)}
.ratio div{display:flex;align-items:center;padding:0 12px;white-space:nowrap;overflow:hidden}
.toast{min-height:1.4em;font-size:13px;color:var(--muted);margin-top:10px}

/* type */
.type-grid{display:grid;grid-template-columns:minmax(0,1.2fr) minmax(0,1fr);gap:clamp(24px,4vw,56px)}
.spec-row{border-top:1px solid var(--line);padding:16px 0;display:grid;gap:4px}
.spec-row .cap-s{order:2}
.tablewrap{overflow-x:auto}
table{border-collapse:collapse;width:100%;font-size:14px}
th,td{text-align:left;padding:9px 12px 9px 0;border-bottom:1px solid var(--line);vertical-align:top}
th{font-family:var(--f-util);font-weight:500;text-transform:uppercase;letter-spacing:.05em;font-size:12px;color:var(--muted)}
td.n{font-variant-numeric:tabular-nums;white-space:nowrap}

/* applications */
.mock{width:100%;height:auto}
.apps{display:grid;gap:16px}
.apps .row{display:grid;gap:16px}
.r2{grid-template-columns:minmax(0,1fr) minmax(0,1fr)}
.r3{grid-template-columns:minmax(0,1fr) minmax(0,1fr) minmax(0,1fr)}
.r-story{grid-template-columns:minmax(0,.62fr) minmax(0,1fr) minmax(0,1fr);align-items:start}
.apps figure{margin:0;display:grid;gap:8px}
.apps figcaption{font-size:13px;color:var(--muted)}

/* misuse + handover */
.misuse{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px}
.mis{margin:0} .mis svg{border:1px solid var(--line)} .mis figcaption{font-size:13px;margin-top:6px}
.mis figcaption::before{content:"✕ ";color:#C0392B;font-weight:600}
.stages{list-style:none;padding:0;margin:0;display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:1px;background:var(--line);border:1px solid var(--line)}
.stages li{background:var(--surface);padding:18px;display:grid;gap:6px;align-content:start}
.stages .st{font-family:var(--f-util);font-weight:500;text-transform:uppercase;letter-spacing:.05em;font-size:12px;color:var(--muted)}
.stages .state{font-size:13px;color:var(--accent);font-weight:500}
.qs{columns:2;column-gap:40px;padding-left:18px;margin:0}
.qs li{margin-bottom:8px;break-inside:avoid}
footer{padding-block:48px 64px;border-top:1px solid var(--line);color:var(--muted);font-size:14px}
footer svg{width:120px;color:var(--ink);margin-bottom:14px}

@media (max-width:900px){
  .routes,.two,.type-grid,.hero-copy,.r3,.r-story{grid-template-columns:minmax(0,1fr)}
  .modes{grid-template-columns:repeat(2,minmax(0,1fr))}
  .kit{grid-template-columns:repeat(2,minmax(0,1fr))} .kit .k-tag{grid-column:1/-1}
  .thumbs{grid-template-columns:repeat(3,minmax(0,1fr))}
  .stages{grid-template-columns:minmax(0,1fr)}
  .misuse{grid-template-columns:repeat(2,minmax(0,1fr))}
  .specs{grid-template-columns:repeat(2,minmax(0,1fr))}
  .qs{columns:1}
  .lockups,.swatches,.swatches.brand{grid-template-columns:repeat(2,minmax(0,1fr))}
}
@media (max-width:520px){ .r2,.lockups{grid-template-columns:minmax(0,1fr)} }
@media (prefers-reduced-motion:reduce){ .hero-svg .slot-g,.hero-svg #mtile,.hero-svg #mname{transition:none} }
</style>

<svg width="0" height="0" style="position:absolute" aria-hidden="true">
  <filter id="deut"><feColorMatrix type="matrix" values="0.367 0.861 -0.228 0 0  0.280 0.673 0.047 0 0  -0.012 0.043 0.969 0 0  0 0 0 1 0"/></filter>
  <filter id="trit"><feColorMatrix type="matrix" values="1.256 -0.077 -0.179 0 0  -0.078 0.931 0.148 0 0  0.005 0.691 0.304 0 0  0 0 0 1 0"/></filter>
</svg>

<header class="hero">
  <div class="wrap">
    <div class="hero-top"><p class="eyebrow">MXDE · logo and brand identity · proposal</p><p class="eyebrow">October 2026</p></div>
    {{HERO}}
    <div class="switch" role="group" aria-label="Switch mode">{{CHIPS}}</div>
    <div class="hero-copy">
      <h1>MXDE is pronounced <em>Mode</em>. The X is the letter you switch.</h1>
      <div><p id="mode-readout" aria-live="polite">The slot stands in for the O. Pick a mode to switch it.</p>
        <p class="muted" style="margin-top:12px">Functional coffee in single-serve sachets. One brand, many modes. This page tells the identity's story, from the word to the system, and shows it on the places customers will meet it.</p></div>
    </div>
  </div>
</header>

<section class="reel" id="reel">
  <div class="wrap">
    <div class="head"><p class="eyebrow">The story in six frames</p><h2>One letter changes, and the brand lives in that letter.</h2>
      <p class="lede">Told the way a logo-process reel is told: start with the plain word, select the letter that matters, change it, then reveal the mark.</p></div>
    <div class="stage" aria-live="polite">{{STAGE}}</div>
    <ol class="thumbs">{{THUMBS}}</ol>
    <div class="reel-ctl"><button type="button" class="ghost" id="play" aria-pressed="false">Play the reel</button></div>
  </div>
</section>

<section id="routes">
  <div class="wrap">
    <div class="head"><p class="eyebrow">Stage 2 · Three routes, black on white</p><h2>Three ways to make the X the hero.</h2>
      <p class="lede">All three keep M, D and E straight and chamfered. They differ only in how the X carries "switch". Each was judged on whether it reads "Mode" before "M-X-D-E".</p></div>
    <div class="routes">{{ROUTES}}</div>
  </div>
</section>

<section id="craft">
  <div class="wrap">
    <div class="head"><p class="eyebrow">Stage 3 · Refinement</p><h2>Why it reads "Mode", even at 16 px.</h2>
      <p class="lede">The slot is the only solid shape in the word. Small or blurred, it reads as a heavy O between M and DE. Up close, the cut spells the X.</p></div>
    <div class="two">
      <div class="panel"><div class="ladder">{{LADDER}}</div>
        <div class="squint"><div>{{WM}}<p class="cap-s" style="margin-top:10px">As drawn</p></div><div class="blur">{{WM}}<p class="cap-s" style="margin-top:10px">Squint test: blurred</p></div></div></div>
      <div>
        <p>Every edge runs at 0°, 45°, 60° or 90°. The D is the only letter with a bowl, so it's drawn with two 45° chamfers, which keep it a D without a single curve.
          The M's V meets the baseline with a flat foot, so no point fills in when the mark is embossed.</p>
        <div class="specs"><div><b>{{STEM}}</b><span>stem, % of cap height</span></div><div><b>{{KCUT}}</b><span>X cut, wide enough for foil</span></div>
          <div><b>60°</b><span>M diagonals</span></div><div><b>16 px</b><span>minimum screen size</span></div></div>
        <p class="muted" style="margin-top:16px;font-size:14px">The weight was chosen from a study at 10, 14, 18 and 22. At 14 and below the slot outweighs the letters. At 22 the D's counter closes at 16 px.</p>
      </div>
    </div>
    <div class="diagram panel" style="margin-top:24px">{{CONSTRUCTION}}</div>
    <div class="kit">
      <figure class="k-tag">{{TAGLOCK}}<figcaption><b>Tagline lockup.</b> SwitchYourMode, one camel-case word, left-aligned under the M. Add # only on social and packs.</figcaption></figure>
      <figure class="k-mono">{{MONO}}<figcaption><b>Monogram.</b> The slot alone: seals, stamps, small spaces.</figcaption></figure>
      <figure class="k-app">{{APP}}<figcaption><b>App and profile icon.</b> Safe in a circle crop.</figcaption></figure>
      <figure>{{FAV}}<figcaption><b>Favicon.</b> Reversed, with a heavier cut for 16 px.</figcaption></figure>
    </div>
  </div>
</section>

<section id="modes">
  <div class="wrap">
    <div class="head"><p class="eyebrow">Mode sub-identity</p><h2>Every mode is the same square, cut differently.</h2>
      <p class="lede">The X's two cuts are rearranged into a new sign for each mode. All cuts share one width and one square, so the family stays one system. Each mode also has a tint, but the cut alone tells it apart, in one colour and for colour-blind customers.</p></div>
    <div class="modes-wrap" id="modes-wrap" data-vision="colour">
      <div class="vision" role="group" aria-label="Simulate how the modes are seen">
        <button type="button" data-v="colour" aria-pressed="true">Full colour</button>
        <button type="button" data-v="grey" aria-pressed="false">One colour / greyscale</button>
        <button type="button" data-v="deut" aria-pressed="false">Deuteranopia (approx.)</button>
        <button type="button" data-v="trit" aria-pressed="false">Tritanopia (approx.)</button>
      </div>
      <div class="modes">{{MODECARDS}}</div>
    </div>
    <div class="two" style="margin-top:36px">
      <div><h3>Zen and Calm, kept apart</h3><p class="muted" style="margin-top:8px">Zen's cuts stand upright: a mind that's aligned and focused. Calm's cuts lie down: a body at rest. They're perpendicular, and their tints are cool slate against warm clay.</p></div>
      <div><h3>The mode line hangs from the X</h3><p class="muted" style="margin-top:8px">In a mode lockup, the tile aligns with the slot, the name follows at the same height, and the slot takes the mode's tint. M, D and E never change colour.</p></div>
    </div>
    <div class="lockups">{{LOCKUPS}}</div>
    <div class="two" style="margin-top:36px">
      <div><h3>Room for a sixth and seventh mode</h3>
        <ol class="rules"><li>Two straight cuts, at the system's cut width, in the same square.</li><li>Must differ from every existing sign in silhouette at 24 px, in one colour.</li>
          <li>Avoid cuts that make the slot read as a letter (▲ reads A, ≡ reads E) wherever the tile sits next to the name.</li><li>A tint from the blue, green or warm-neutral families, with 4.5:1 for white text.</li></ol></div>
      <div class="grow-row">{{GROW}}</div>
    </div>
  </div>
</section>

<section id="colour">
  <div class="wrap">
    <div class="head"><p class="eyebrow">Colour</p><h2>Neutrals do the work. Colour marks the mode.</h2>
      <p class="lede">Grays and warm neutrals carry the brand. One accent, Tonic, a mineral green, adds freshness. Mode tints appear only where a mode is named. Keep accent and tint to about a tenth of any layout.</p></div>
    <ul class="swatches brand">{{SWATCHES}}</ul>
    <div class="ratio"><div style="flex:60;background:var(--paper);color:var(--carbon)">Grounds · 60%</div><div style="flex:30;background:var(--carbon);color:var(--paper)">Neutrals · 30%</div><div style="flex:10;background:#0E6B5E;color:#fff">≤10%</div></div>
    <h3 style="margin:40px 0 16px">Mode tints</h3>
    <ul class="swatches">{{MODESW}}</ul>
    <p class="toast" id="toast" aria-live="polite"></p>
    <p class="muted" style="font-size:14px;max-width:70ch">White text on every mode tint passes WCAG AA (4.5:1 or better). Each tint passes 3:1 on Paper, so it works for tiles and large type. Pantone references are the nearest matches and CMYK values are starting points. Confirm both against a physical guide and a press proof. Silver is both a print finish (877 C metallic foil) and a flat grey for screens.</p>
  </div>
</section>

<section id="type">
  <div class="wrap">
    <div class="head"><p class="eyebrow">Stage 4 · Typography</p><h2>Straight-cut type that stays legible on a sachet.</h2></div>
    <div class="type-grid">
      <div>
        <div class="spec-row"><p class="t-mode" style="font-size:clamp(28px,4.6vw,52px);line-height:1">WAKE · ACTIVE · ZEN</p><p class="cap-s">Archivo Expanded SemiBold · mode names, display · +6%</p></div>
        <div class="spec-row"><p class="t-head" style="font-size:clamp(24px,3vw,34px);line-height:1.12">The right coffee for the state you want to be in.</p><p class="cap-s">Archivo SemiBold · headlines</p></div>
        <div class="spec-row"><p class="t-sub" style="font-size:14px">Functional coffee · single-serve concentrate</p><p class="cap-s">Archivo SemiExpanded Medium · subheads, nav, buttons · +8%</p></div>
        <div class="spec-row"><p class="t-body" style="max-width:60ch">Tear the sachet, pour it over 150 ml of water or milk, and stir. Each mode is made for a different need at a different hour, so choose by how you want to feel next.</p><p class="cap-s">IBM Plex Sans Regular · body</p></div>
        <div class="spec-row"><p class="t-label" style="font-size:14px">Ingredients: coffee concentrate (water, arabica coffee) · values to be supplied</p><p class="cap-s">IBM Plex Sans Condensed Medium · labels, ingredient lists, nutrition panels</p></div>
      </div>
      <div>
        <div class="tablewrap"><table><thead><tr><th>Style</th><th>Screen</th><th>Pack</th></tr></thead><tbody>
          <tr><td>Display / mode</td><td class="n">48/52 px</td><td class="n">14–26 pt</td></tr>
          <tr><td>Headline</td><td class="n">32/38 px</td><td class="n">10–12 pt</td></tr>
          <tr><td>Subhead</td><td class="n">14/20 px</td><td class="n">7 pt</td></tr>
          <tr><td>Body</td><td class="n">16/24 px</td><td class="n">7 pt</td></tr>
          <tr><td>Caption</td><td class="n">13/18 px</td><td class="n">6 pt</td></tr>
          <tr><td>Label / panel</td><td class="n">12/16 px</td><td class="n">6 pt min.</td></tr></tbody></table></div>
        <p style="margin-top:20px"><b>Licensing:</b> Archivo and IBM Plex Sans are both under the SIL Open Font License. They're free for print, web, social and packaging, with no licence cost. The wordmark is custom-drawn and uses no font.</p>
        <p class="muted" style="margin-top:12px;font-size:14px">On small packs, mandatory text has legal minimums. For example, EU 1169/2011 requires a 1.2 mm x-height, or 0.9 mm under 80 cm². Check each market <span class="tbc">to confirm</span>.</p>
      </div>
    </div>
  </div>
</section>

<section id="applications">
  <div class="wrap">
    <div class="head"><p class="eyebrow">Applications · presentation mockups</p><h2>On the sachet, in the feed, at a glance.</h2>
      <p class="lede">These are mockups, not production artwork. Sachets assume a flat pouch of about 75 × 110 mm until dimensions are shared.</p></div>
    <div class="apps">
      <figure>{{M_SACHETS}}<figcaption>Single-serve sachet fronts, one per mode. Wordmark top, mode tile as the hero, name and function below.</figcaption></figure>
      <figure>{{M_GRID}}<figcaption>The at-a-glance test: five product thumbnails, then the same in greyscale. The cut alone tells the modes apart.</figcaption></figure>
      <div class="row r2"><figure>{{M_CARTON}}<figcaption>Outer carton for the five-mode set.</figcaption></figure><figure>{{M_ECOM}}<figcaption>Square e-commerce product tile.</figcaption></figure></div>
      <figure>{{M_HERO}}<figcaption>Website hero banner.</figcaption></figure>
      <figure>{{M_HEADER}}<figcaption>Website header and browser favicon.</figcaption></figure>
      <div class="row r-story"><figure>{{M_STORY}}<figcaption>Instagram story.</figcaption></figure>
        <figure>{{M_POST}}<figcaption>Instagram post: the slot switches into Active. Switch-ins are for motion and social only, never packs.</figcaption></figure>
        <div style="display:grid;gap:16px"><figure>{{M_PROFILE}}<figcaption>Profile picture.</figcaption></figure><figure>{{M_TUMBLER}}<figcaption>Tumbler: silver monogram and wordmark on Carbon.</figcaption></figure></div></div>
    </div>
  </div>
</section>

<section id="misuse">
  <div class="wrap">
    <div class="head"><p class="eyebrow">Guardrails</p><h2>What not to do.</h2></div>
    <div class="misuse">{{MISUSE}}</div>
  </div>
</section>

<section id="handover">
  <div class="wrap">
    <div class="head"><p class="eyebrow">Stage 5 · Handover and next steps</p><h2>Where this sits in the five-stage process.</h2>
      <p class="lede">This first pass compresses stages 1 to 4 into one proposal, so the brand team can react to a complete system. Decisions taken on the team's behalf are listed under each stage.</p></div>
    <ol class="stages">
      <li><span class="st">1 · Discovery</span><b>Brief read, assumptions logged</b><span class="state">Done, compressed</span><span class="muted" style="font-size:14px">The customer, mode functions and pack size are working assumptions. No separate moodboard yet.</span></li>
      <li><span class="st">2 · Concepts</span><b>Three routes, black on white</b><span class="state">Done</span><span class="muted" style="font-size:14px">Crossover, Slot and Shift, plus a weight study.</span></li>
      <li><span class="st">3 · Refinement</span><b>Slot route, palette, mode system</b><span class="state">Round 1 proposed</span><span class="muted" style="font-size:14px">Recommended route chosen on the team's behalf. Two feedback rounds still to run.</span></li>
      <li><span class="st">4 · System build</span><b>Type, lockups, mockups</b><span class="state">Drafted</span><span class="muted" style="font-size:14px">All touchpoints in the brief are mocked.</span></li>
      <li><span class="st">5 · Handover</span><b>Files and guidelines</b><span class="state">Starter set ready</span><span class="muted" style="font-size:14px">SVG, PDF, EPS and PNG masters, ICO, ASE and an 18-page guidelines PDF, all in the repository.</span></li>
    </ol>
    <div class="two" style="margin-top:40px">
      <div><h3>Open questions for the brand team</h3>
        <ul class="qs" style="margin-top:14px"><li>Who is the target customer, and what is the price positioning?</li><li>What are the sachet dimensions and finish: matte, foil or kraft?</li>
          <li>What are the exact function and time of day for each mode?</li><li>Which brands should we admire, and which should we avoid resembling?</li>
          <li>SwitchYourMode or #SwitchYourMode? Proposed: no # in lockups, # on social and packs.</li><li>Has a trademark check been done on the name? The slot mark needs one too.</li><li>What are the timeline and design budget?</li></ul></div>
      <div><h3>What to judge</h3>
        <ul class="qs" style="columns:1;margin-top:14px"><li>Does it read as "Mode" at first glance?</li><li>Is it built from straight, angular lines with minimal curves?</li>
          <li>Does it hold up at small sizes and in one colour?</li><li>Does the X carry the switch idea without feeling forced?</li><li>Does it feel premium and healthy, not like a café or an energy drink?</li><li>Can the five modes be told apart instantly?</li></ul></div>
    </div>
  </div>
</section>

<footer><div class="wrap">{{WM}}<p>MXDE identity proposal · v1.0 · Fonts: Archivo and IBM Plex Sans (SIL OFL). Wordmark drawn from straight lines only. A trademark search hasn't been done.</p></div></footer>

<script>
(function(){
  var D = {{DATA}};
  var svg = document.querySelector('.hero-svg');
  var slot = document.getElementById('slot'), mtile = document.getElementById('mtile'), mname = document.getElementById('mname');
  var readout = document.getElementById('mode-readout');
  var chips = document.querySelectorAll('.chip-btn');
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var root = document.documentElement;
  function apply(k){
    var m = D.modes[k];
    slot.setAttribute('d', D.hero.tiles[k]);
    mname.setAttribute('d', D.hero.names[k]);
    mtile.setAttribute('d', k === 'x' ? '' : D.hero.small[k]);
    root.style.setProperty('--slot', m ? m.hex : 'var(--accent)');
    readout.textContent = m ? (m.name + ' Mode · ' + m.when + ' · ' + m.mood + '. ' + m.idea) : 'The slot stands in for the O. Pick a mode to switch it.';
    chips.forEach(function(c){ var on = c.dataset.mode === k; c.classList.toggle('is-on', on); c.setAttribute('aria-pressed', on ? 'true' : 'false'); });
  }
  function sw(k){
    if (reduce){ apply(k); return; }
    svg.classList.add('flip');
    setTimeout(function(){ apply(k); svg.classList.remove('flip'); }, 190);
  }
  chips.forEach(function(c){ c.addEventListener('click', function(){ sw(c.dataset.mode); }); });

  // reel
  var frames = document.querySelectorAll('.stage-frame'), thumbs = document.querySelectorAll('.thumb');
  var cur = 4, timer = null, play = document.getElementById('play');
  function show(i){
    cur = i;
    frames.forEach(function(f){ f.hidden = (+f.dataset.i !== i); });
    thumbs.forEach(function(t){ t.classList.toggle('is-on', +t.dataset.i === i); });
  }
  function stop(){ if (timer){ clearInterval(timer); timer = null; } play.textContent = 'Play the reel'; play.setAttribute('aria-pressed','false'); }
  function start(){ show(0); timer = setInterval(function(){ show((cur + 1) % frames.length); }, 1500); play.textContent = 'Pause'; play.setAttribute('aria-pressed','true'); }
  thumbs.forEach(function(t){ t.addEventListener('click', function(){ stop(); show(+t.dataset.i); }); });
  play.addEventListener('click', function(){ timer ? stop() : start(); });

  // vision simulation
  var wrap = document.getElementById('modes-wrap');
  document.querySelectorAll('.vision button').forEach(function(b){
    b.addEventListener('click', function(){
      wrap.dataset.vision = b.dataset.v;
      document.querySelectorAll('.vision button').forEach(function(x){ x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); });
    });
  });

  // copy hex
  var toast = document.getElementById('toast');
  document.querySelectorAll('.copy').forEach(function(b){
    b.addEventListener('click', function(){
      var v = b.dataset.copy;
      try {
        navigator.clipboard.writeText(v).then(function(){ toast.textContent = 'Copied ' + v; }, function(){ toast.textContent = v + ' (select and copy)'; });
      } catch(e){ toast.textContent = v + ' (select and copy)'; }
    });
  });
})();
</script>
"""

if __name__ == "__main__":
    p, n = build()
    print(p, f"{n / 1024:.0f} KB")
