"""MXDE brand guidelines — A4 landscape HTML, rendered to PDF by render.mjs."""
import json
import os
from build import WORD_W, KCUT, STEM, MODE_TILE, MODE_GAP
from geom import H
from palette import PALETTE, MODES, contrast, hex_rgb
from marks import wordmark, tile, words, mode_lockup, lockup_height, tagline, MODE, MODE_KEYS, C
from diagrams import story_frames, construction, clear_space, misuse, growth, routes_svg
from mockups import FONT_CSS_LOCAL, TEXT_CSS

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
FONTS = os.path.join(ROOT, "src", "fonts")
ASPECT = WORD_W / H


def svgwrap(w, h, body, label="", cls=""):
    c = f' class="{cls}"' if cls else ""
    return f'<svg{c} xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:g} {h:g}" role="img" aria-label="{label}">{body}</svg>'


def wm(width=412, letters="currentColor", slot=None, slot_key="x", cls="wm"):
    return svgwrap(WORD_W, H, wordmark(0, 0, WORD_W, letters, slot or letters, slot_key), "MXDE", cls)


def lock(key, letters="currentColor", cls="wm"):
    h = lockup_height(WORD_W)
    return svgwrap(WORD_W, h, mode_lockup(0, 0, WORD_W, key, letters), f"{key} lockup", cls)


def tag_lock(letters="currentColor", slot=None, cls="wm"):
    gap = 0.42 * H
    h = H + gap + 0.30 * H
    body = wordmark(0, 0, WORD_W, letters, slot or letters) + tagline(0, H + gap + 0.24 * H, 0.24 * H, letters)
    return svgwrap(WORD_W, h, body, "Wordmark with tagline", cls)


def mono(fill, size_cls="mono", key="x"):
    return svgwrap(H, H, tile(key, 0, 0, H, fill), "monogram", size_cls)


PAGES = []


def page(section, title, body, dark=False, num=True):
    PAGES.append((section, title, body, dark, num))


def build():
    PAGES.clear()
    # ------------------------------------------------------------ cover
    page("", "", f"""
      <div class="cover">
        <div class="cover-mark">{wm(letters=C['Paper'], slot=C['Tonic'])}</div>
        <div class="cover-meta">
          <p class="t-sub">Brand identity guidelines</p>
          <p class="t-body">Starter edition · v1.0 · October 2026 · Proposal pending sign-off</p>
        </div>
        <div class="cover-tag">{svgwrap(300, 40, tagline(0, 30, 24, C['Silver']), 'SwitchYourMode')}</div>
      </div>""", dark=True, num=False)

    # ------------------------------------------------------------ contents
    sections = [("01", "The idea"), ("02", "Wordmark"), ("03", "Construction"), ("04", "Clear space and minimum size"),
                ("05", "Lockups and icons"), ("06", "Colour variants and finishes"), ("07", "Misuse"), ("08", "Colour palette"),
                ("09", "Accessible pairings"), ("10", "Typography"), ("11", "Mode system"), ("12", "Mode lockups"),
                ("13", "Growing the system"), ("14", "Applications"), ("15", "Files and handover")]
    toc = "".join(f'<li><span class="t-label">{n}</span><span>{t}</span></li>' for n, t in sections)
    page("", "Contents", f"""
      <div class="cols-2">
        <div><h1 class="t-head">MXDE is pronounced <em>Mode</em>.</h1>
          <p class="lead">The X takes the place of the O. It stands for the variable: whichever mode you switch into after your coffee.
          Everything in this identity follows from that one swap.</p>
          <p>These guidelines cover the logo, colour, type and the mode system. Packaging artwork, dielines, the website,
          photography and campaign work follow once the identity is signed off.</p>
          <p class="note">Items marked <b>to confirm</b> are working assumptions from the brief, waiting on the brand team.</p></div>
        <ol class="toc">{toc}</ol>
      </div>""")

    # ------------------------------------------------------------ 01 idea
    frames = story_frames(ink=C["Carbon"])
    cells = "".join(f'<figure class="frame-cell">{svg}<figcaption><span class="t-label">{i + 1:02d}</span> {cap}</figcaption></figure>'
                    for i, (cap, svg) in enumerate(frames))
    page("01", "The idea", f"""
      <p class="lead narrow">Start from the word you want people to say, change one letter, and let that letter carry the brand.
      The round O becomes a square slot with an X cut into it. The slot keeps the O's place and weight, so the eye reads <b>Mode</b>.
      The X inside it spells MXDE and stands for the variable.</p>
      <div class="frames">{cells}</div>""")

    # ------------------------------------------------------------ 02 wordmark
    page("02", "Wordmark", f"""
      <div class="hero-mark">{wm(letters=C['Carbon'], slot=C['Tonic'])}</div>
      <div class="cols-3 small">
        <div><h3 class="t-sub">Built from straight lines</h3><p>Every edge runs at 0°, 45°, 60° or 90°. There are no curves in the mark.
          The D, the only letter with a bowl, is drawn with two 45° chamfers, so it stays a D without a round shape.</p></div>
        <div><h3 class="t-sub">The slot is the hero</h3><p>The slot is the only solid shape in the word. At small sizes it reads as a dark O,
          so the name reads <b>Mode</b>. Up close, the cut shows the X. In full colour, the slot carries the accent and M, D and E stay Carbon.</p></div>
        <div><h3 class="t-sub">One weight</h3><p>Stems are 18% of the cap height. Lighter weights lost the slot's mass against
          the letters, and heavier ones closed the D's counter at 16 px. The cut is 62% of a stem, wide enough for foil and emboss.</p></div>
      </div>""")

    # ------------------------------------------------------------ 03 construction
    r = routes_svg(C["Carbon"])
    page("03", "Construction", f"""
      <div class="diagram c">{construction(C['Carbon'], '#2F6BFF', C['Stone'])}</div>
      <div class="cols-3 small">
        <div><h3 class="t-sub">Metrics</h3><table class="spec"><tr><td>Cap height</td><td>100</td></tr><tr><td>Stem</td><td>{STEM:g}</td></tr>
          <tr><td>Horizontal strokes</td><td>16.2 (thinned 10% for optical balance)</td></tr><tr><td>Slot</td><td>100 × 100</td></tr><tr><td>X cut</td><td>{KCUT:.1f}</td></tr>
          <tr><td>Spacing M–X · X–D · D–E</td><td>20.5 · 20.5 · 19</td></tr><tr><td>Overall width</td><td>{WORD_W:g}</td></tr></table></div>
        <div><h3 class="t-sub">Routes explored</h3><div class="routes-mini">{r['a']}{r['b']}{r['c']}</div>
          <p class="note">A: Crossover. B: Slot (chosen). C: Shift. B was the only route that read as "Mode" before "M-X-D-E".</p></div>
        <div><h3 class="t-sub">Source of truth</h3><p>The geometry is generated from <code>src/geom.py</code>. Change a number there, rebuild,
          and every file, lockup and mockup updates together. Never edit an outlined master by hand.</p></div>
      </div>""")

    # ------------------------------------------------------------ 04 clear space
    ladder = "".join(f'<div class="ladder-cell"><div style="height:{px}px">{wm(letters=C["Carbon"], slot=C["Carbon"], cls="wm-px")}</div><span class="t-label">{px} px</span></div>'
                     for px in (12, 16, 24, 32, 48))
    page("04", "Clear space and minimum size", f"""
      <div class="cols-2">
        <div><div class="diagram">{clear_space(C['Carbon'], '#2F6BFF')}</div>
          <p class="small">Keep clear space of half the slot's width (half the cap height) on every side. Nothing else enters that zone,
          including the tagline. The tagline lockup has its own fixed spacing (section 05).</p></div>
        <div><h3 class="t-sub">Minimum sizes (cap height)</h3>
          <table class="spec"><tr><th>Use</th><th>Wordmark</th><th>Monogram</th></tr>
          <tr><td>Screen</td><td>16 px (66 px wide)</td><td>16 px favicon cut</td></tr>
          <tr><td>Offset / flexo print</td><td>3.5 mm (14.4 mm wide)</td><td>4 mm</td></tr>
          <tr><td>Foil stamp, emboss, deboss</td><td>5 mm (20.6 mm wide)</td><td>6 mm</td></tr></table>
          <p class="small">At 5 mm cap height the X cut is 0.56 mm and a stem is 0.9 mm, inside typical foil and emboss tolerances. Confirm with the converter once
          sachet dimensions and finishes are known (<b>to confirm</b>).</p>
          <div class="ladder">{ladder}</div>
          <p class="note">Below 16 px, use the monogram. Below 12 px, use the favicon drawing, which has a 16% cut.</p></div>
      </div>""")

    # ------------------------------------------------------------ 05 lockups
    icons = (f'<img src="../icons/favicon-16.png" width="16" height="16" alt="favicon 16"> <img src="../icons/favicon-32.png" width="32" height="32" alt="favicon 32">'
             f' <img src="../icons/favicon-48.png" width="48" height="48" alt="favicon 48">')
    page("05", "Lockups and icons", f"""
      <div class="grid-lockups">
        <figure><div class="lk">{wm(letters=C['Carbon'], slot=C['Tonic'])}</div><figcaption><b>Primary.</b> Horizontal wordmark. Use it wherever there is room.</figcaption></figure>
        <figure><div class="lk">{tag_lock(C['Carbon'], C['Tonic'])}</div><figcaption><b>Tagline lockup.</b> SwitchYourMode is set in Archivo Medium at 24% of the cap height,
          left-aligned to the M, 42% of the cap height below the baseline. Write it as one camel-case word. Add # only where it works as a hashtag (social, packs).</figcaption></figure>
        <figure><div class="lk">{lock('zen', C['Carbon'])}</div><figcaption><b>Mode lockup.</b> The mode line hangs from the X (section 12).</figcaption></figure>
        <figure class="row-icons"><div class="icons">{mono(C['Carbon'])}{mono(C['Tonic'])}
            <img class="app" src="../icons/app-icon-carbon-512.png" alt="app icon"><span class="fav">{icons}</span></div>
          <figcaption><b>Monogram, app icon, favicon.</b> The monogram is the slot on its own: for seals, stamps, the tumbler and small spaces.
          The app and profile icon sets the slot at 46% on Carbon, so it survives a circular crop. The favicon is the slot reversed out of a Carbon square, with a heavier cut.</figcaption></figure>
      </div>""")

    # ------------------------------------------------------------ 06 variants
    def sw(bg, fg, slot, label, extra=""):
        return (f'<figure class="variant" style="background:{bg};{extra}"><div class="lk">{wm(letters=fg, slot=slot)}</div>'
                f'<figcaption style="color:{fg}">{label}</figcaption></figure>')
    kraft = "background:linear-gradient(135deg,#C9A57D,#B8915F 60%,#C29C6E)"
    foil = "linear-gradient(120deg,#9EA1A3,#E6E7E8 40%,#A9ACAE 60%,#D9DADB)"
    page("06", "Colour variants and finishes", f"""
      <div class="variants">
        {sw(C['Paper'], C['Carbon'], C['Tonic'], 'Full colour · Carbon + Tonic on Paper')}
        {sw('#FFFFFF', '#000000', '#000000', 'One colour · Black on white')}
        {sw(C['Carbon'], C['White'], C['White'], 'Reversed · White on Carbon')}
        {sw(C['Carbon'], C['White'], C['Tonic'], 'Reversed full colour · White + Tonic on Carbon')}
        {sw(C['Tonic'], C['White'], C['White'], 'White on Tonic (CTAs, social)')}
        {sw(C['Oat'], C['Roast'], C['Roast'], 'Warm one colour · Roast on Oat')}
        <figure class="variant" style="{kraft}"><div class="lk">{wm(letters=C['Carbon'], slot=C['Carbon'])}</div><figcaption style="color:{C['Carbon']}">Kraft stock · Carbon, one colour</figcaption></figure>
        <figure class="variant" style="background:{C['Carbon']}"><div class="lk foil" style="--foil:{foil}">{wm(letters='url(#foil)', slot='url(#foil)')}</div><figcaption style="color:{C['Silver']}">Silver foil (Pantone 877 C) on Carbon</figcaption></figure>
      </div>
      <svg width="0" height="0" style="position:absolute"><defs><linearGradient id="foil" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#9EA1A3"/><stop offset=".4" stop-color="#ECEDEE"/><stop offset=".6" stop-color="#A9ACAE"/><stop offset="1" stop-color="#D9DADB"/></linearGradient></defs></svg>
      <p class="small">The sheen on the foil sample only simulates the finish. The artwork itself is always a flat, single-colour shape. On embossed or blind-debossed packs,
      emboss the whole wordmark at one depth. Don't sculpt the slot separately.</p>""")

    # ------------------------------------------------------------ 07 misuse
    mis = "".join(f'<figure class="mis">{svg}<figcaption>{cap}</figcaption></figure>' for cap, svg in misuse())
    page("07", "Misuse", f'<div class="misuse">{mis}</div>')

    # ------------------------------------------------------------ 08 palette
    def chip(role, name, hx, pms, cmyk, wide=False):
        r, g, b = hex_rgb(hx)
        fg = C["Carbon"] if contrast(hx, C["Carbon"]) > contrast(hx, "#FFFFFF") else "#FFFFFF"
        border = "border:1px solid #DDD;" if hx.upper() in ("#FFFFFF", "#F4F2ED") else ""
        return (f'<div class="chip{" wide" if wide else ""}" style="background:{hx};color:{fg};{border}"><b>{name}</b>'
                f'<span>{hx}</span><span>RGB {r} {g} {b}</span><span>CMYK {" ".join(str(c) for c in cmyk)}</span><span>Pantone {pms}</span></div>')
    roles = {"core": "Core neutrals · logo, type, structure", "ground": "Light grounds · backgrounds, breathing room",
             "warm": "Warm neutrals · coffee warmth, pack grounds", "accent": "Accent · highlights, calls to action"}
    groups = ""
    for role, label in roles.items():
        chips = "".join(chip(*row) for row in PALETTE if row[0] == role)
        groups += f'<div class="pal-group"><h3 class="t-sub">{label}</h3><div class="chips">{chips}</div></div>'
    page("08", "Colour palette", f"""
      {groups}
      <div class="ratio"><div style="flex:60;background:{C['Paper']}">Grounds 60%</div><div style="flex:30;background:{C['Carbon']};color:#fff">Neutrals 30%</div>
        <div style="flex:10;background:{C['Tonic']};color:#fff">≤10%</div></div>
      <p class="note">Keep accent and mode colour to about a tenth of any layout. Pantone references are the nearest matches and CMYK values are starting points. Approve both against a Pantone guide and a press proof.</p>""")

    # ------------------------------------------------------------ 09 accessibility
    pal = json.load(open(os.path.join(ROOT, "colour", "mxde-palette.json")))
    def ctable(items):
        head = '<tr><th>Text / mark</th><th>Ground</th><th>Ratio</th><th>AA body</th><th>AA large</th></tr>'
        body = "".join(f'<tr><td>{p["text"].title()}</td><td>{p["ground"].title()}</td><td class="num">{p["ratio"]:.2f}:1</td>'
                       f'<td>{"Pass" if p["AA_body"] else "—"}</td><td>{"Pass" if p["AA_large_or_graphic"] else "—"}</td></tr>' for p in items)
        return f'<table class="spec contrast">{head}{body}</table>'
    modes_upper = {m[1] for m in MODES}
    brand_pairs = [p for p in pal["text_pairings"] if p["text"] not in modes_upper and p["ground"] not in modes_upper]
    mode_pairs = [p for p in pal["text_pairings"] if p not in brand_pairs]
    page("09", "Accessible pairings", f"""
      <div class="cols-3"><div><h3 class="t-sub">Brand pairings</h3>{ctable(brand_pairs)}</div>
      <div><h3 class="t-sub">Mode pairings</h3>{ctable(mode_pairs)}<p class="note">AA body = 4.5:1 for normal text. AA large = 3:1 for large text and graphics (WCAG 2.1).</p></div>
      <div class="small"><h3 class="t-sub">Rules</h3>
        <p>Body copy, ingredients and nutrition panels: Carbon or Graphite on White, Paper or Oat only.</p>
        <p>Stone is for captions of 18 px / 14 pt bold and above, or for rules and dividers. It isn't for body text on light grounds.</p>
        <p>Mode colours pass 3:1 on Paper, so they work as tiles and large type. White text on a mode colour passes AA body (4.5:1),
          which makes buttons and chips safe. Don't set small mode-coloured text on Paper.</p>
        <p>Never rely on colour alone. Every mode tile carries its own cut, and every mode is named in words.</p></div></div>""")

    # ------------------------------------------------------------ 10 typography
    page("10", "Typography", f"""
      <div class="cols-2">
        <div class="specimen">
          <p class="t-mode" style="font-size:44px;line-height:1">WAKE ACTIVE ZEN</p>
          <p class="t-label" style="margin-top:4px">Archivo Expanded SemiBold · mode names, display</p>
          <p class="t-head" style="font-size:30px;line-height:1.1;margin-top:18px">The right coffee for the state you want to be in.</p>
          <p class="t-label">Archivo SemiBold · headlines</p>
          <p class="t-sub" style="font-size:12px;margin-top:14px">Functional coffee · single-serve concentrate</p>
          <p class="t-label">Archivo SemiExpanded Medium · subheads, nav, buttons</p>
          <p class="t-body" style="font-size:13px;line-height:1.5;margin-top:14px;max-width:62ch">Tear the sachet, pour it over 150 ml of water or milk, and stir.
          Each mode is made for a different need at a different hour, so choose by how you want to feel next.</p>
          <p class="t-label">IBM Plex Sans Regular · body copy</p>
          <table class="nutri"><tr><th colspan="2">Nutrition per sachet (18 ml) · values to be supplied</th></tr>
            <tr><td>Energy</td><td>— kJ / — kcal</td></tr><tr><td>Fat</td><td>— g</td></tr><tr><td>Carbohydrate</td><td>— g</td></tr><tr><td>Caffeine</td><td>— mg</td></tr></table>
          <p class="t-label">IBM Plex Sans Condensed Medium · labels, ingredient lists, nutrition panels</p>
        </div>
        <div class="small">
          <table class="spec"><tr><th>Style</th><th>Face</th><th>Screen</th><th>Pack</th><th>Tracking</th></tr>
            <tr><td>Display / mode</td><td>Archivo Exp. SemiBold, caps</td><td>48/52 px</td><td>14–26 pt</td><td>+6%</td></tr>
            <tr><td>Headline</td><td>Archivo SemiBold</td><td>32/38 px</td><td>10–12 pt</td><td>−1%</td></tr>
            <tr><td>Subhead</td><td>Archivo SemiExp. Medium, caps</td><td>14/20 px</td><td>7 pt</td><td>+8%</td></tr>
            <tr><td>Body</td><td>IBM Plex Sans Regular</td><td>16/24 px</td><td>7 pt</td><td>0</td></tr>
            <tr><td>Caption</td><td>IBM Plex Sans Regular</td><td>13/18 px</td><td>6 pt</td><td>0</td></tr>
            <tr><td>Label / panel</td><td>IBM Plex Sans Cond. Medium, caps, tabular</td><td>12/16 px</td><td>6 pt min.</td><td>+4%</td></tr></table>
          <h3 class="t-sub">Licensing</h3>
          <p>Archivo (Omnibus-Type) and IBM Plex Sans (IBM) are both under the SIL Open Font License 1.1. They're free for print, web, social, apps and packaging, with no licence cost.
          Sources: fonts.google.com/specimen/Archivo and fonts.google.com/specimen/IBM+Plex+Sans. The wordmark itself is custom-drawn and uses no font.</p>
          <h3 class="t-sub">Small-pack legibility</h3>
          <p>Mandatory label text has legal minimums. For example, EU 1169/2011 requires a 1.2 mm x-height, or 0.9 mm on packs whose largest face is under 80 cm².
          Plex Sans Condensed at 6 pt gives about 1.1 mm, so check the rules in each market you sell into (<b>to confirm</b>).</p>
        </div>
      </div>""")

    # ------------------------------------------------------------ 11 mode system
    rows = ""
    for k in MODE_KEYS:
        m = MODE[k]
        rows += (f'<div class="mode-row"><div class="mt">{mono(m["hex"], key=k)}</div><div class="mt">{mono(C["Carbon"], key=k)}</div>'
                 f'<div><p class="t-mode" style="font-size:20px">{m["name"]}</p><p class="small">{m["idea"]} Mood: {m["mood"].lower()}.</p></div>'
                 f'<div class="small codes">{m["hex"]} · Pantone {m["pms"]}<br>CMYK {" ".join(str(c) for c in m["cmyk"])}</div></div>')
    page("11", "Mode system", f"""
      <div class="cols-2"><div>
        <p class="lead">Every mode is the same square slot, cut differently. The cut is the mode.</p>
        <p class="small">The X's two cuts are rearranged into a new sign for each mode. All cuts share one width ({KCUT:.1f} on a 100 square, 15% when the tile is drawn small),
        so the family stays one system. Each mode also has a tint. The tint helps, but the cut alone is enough. Every mode stays distinct in one-colour print,
        in greyscale and for colour-blind customers.</p>
        <p class="small"><b>Zen and Calm.</b> Zen's cuts stand upright: a mind that's aligned and focused. Calm's cuts lie down: a body at rest.
        They are perpendicular, and their tints are cool slate against warm clay.</p></div>
        <div class="modes">{rows}</div></div>""")

    # ------------------------------------------------------------ 12 mode lockups
    lks = "".join(f'<figure class="mlk">{lock(k, C["Carbon"])}</figure>' for k in MODE_KEYS)
    lks += f'<figure class="mlk dark" style="background:{C["Carbon"]}">{svgwrap(WORD_W, lockup_height(WORD_W), mode_lockup(0, 0, WORD_W, "calm", C["White"]), "calm reversed", "wm")}</figure>'
    page("12", "Mode lockups", f"""
      <div class="cols-2"><div class="mlks">{lks}</div>
        <div class="small"><h3 class="t-sub">Fixed relationship</h3>
          <p>The mode line hangs from the X. The tile's left edge aligns with the slot's left edge. The tile and the mode name's cap height are both {MODE_TILE / H:.0%}
          of the wordmark's cap height. The line sits {MODE_GAP / H:.0%} of the cap height below the baseline, and the name starts {0.32:.0%} of a tile after the tile.</p>
          <p>In mode lockups, the slot takes the mode's tint, so the X switches into the mode. M, D and E never change colour.</p>
          <p>Names of up to six letters end inside the E. Longer future names may run past the E but keep every other measurement.</p>
          <h3 class="t-sub">Switching in, in motion only</h3>
          <p>In animation and social content, the slot can morph into a mode's tile and then return to the X. Never set a mode tile inside the wordmark on packs,
          the site header or anywhere the name has to be read. A slot showing the WAKE ▲ reads as "MADE".</p></div></div>""")

    # ------------------------------------------------------------ 13 growth
    gc = "".join(f'<figure class="grow">{svg}<figcaption class="t-label">{name}</figcaption></figure>' for name, svg in growth(C["Stone"]))
    page("13", "Growing the system", f"""
      <div class="cols-2"><div><p class="lead">A sixth or seventh mode needs no redesign: draw a new cut in the same square.</p>
        <ol class="small rules"><li>Use two straight cuts at the system's cut width, at 0°, 45°, 90° or along the square's diagonals and midpoints.</li>
        <li>The new sign must differ from all existing ones in silhouette at 24 px, in one colour. Test it in the thumbnail grid.</li>
        <li>Avoid cuts that turn the slot into a letter (▲ = A, ≡ = E) if the tile could ever sit beside the wordmark.</li>
        <li>Choose a tint from the blue–green–warm-neutral families with at least 4.5:1 for white text and 3:1 against Paper. Keep it clearly apart from its nearest neighbour.</li>
        <li>Name it in one word, ideally six letters or fewer.</li></ol></div>
        <div class="grow-row">{gc}</div></div>""")

    # ------------------------------------------------------------ 14 applications
    page("14", "Applications · packaging", f"""
      <img class="mock m-top" src="../mockups/mxde-mockup-sachets-all.png" alt="Five sachets">
      <div class="cols-2 m-row"><img class="mock" src="../mockups/mxde-mockup-carton.png" alt="Carton">
        <img class="mock" src="../mockups/mxde-mockup-thumbnail-grid.png" alt="Thumbnail test"></div>
      <p class="note">Presentation mockups, not production artwork. Sachet proportions assume a flat pouch of about 75 × 110 mm (<b>to confirm</b>).</p>""")
    page("14", "Applications · digital and lifestyle", f"""
      <div class="cols-3 mocks"><img class="mock" src="../mockups/mxde-mockup-web-hero.png" alt="Web hero">
        <img class="mock" src="../mockups/mxde-mockup-ecom-tile.png" alt="E-commerce tile">
        <img class="mock" src="../mockups/mxde-mockup-instagram-post.png" alt="Instagram post">
        <img class="mock" src="../mockups/mxde-mockup-web-header-favicon.png" alt="Website header">
        <img class="mock" src="../mockups/mxde-mockup-instagram-profile.png" alt="Instagram profile">
        <div class="pair"><img class="mock" src="../mockups/mxde-mockup-instagram-story.png" alt="Instagram story"><img class="mock" src="../mockups/mxde-mockup-tumbler.png" alt="Tumbler"></div></div>""")

    # ------------------------------------------------------------ 15 files
    page("15", "Files and handover", f"""
      <div class="cols-2 small"><div><table class="spec files">
        <tr><th>Folder</th><th>Contents</th></tr>
        <tr><td>logo/svg · pdf · eps · png</td><td>Wordmark and tagline lockup in full colour, carbon, black, white, tonic and silver. Monogram in carbon, white, tonic and black. PNGs are transparent, 400–3200 px wide.</td></tr>
        <tr><td>icons/</td><td>favicon.svg, favicon.ico (16/32/48), PNG 16–192, apple-touch-icon 180, app icons 512 (carbon, paper, tonic), profile picture 1080, site.webmanifest, head snippet</td></tr>
        <tr><td>modes/svg · pdf · png</td><td>Five mode lockups × full colour, carbon, white and reversed colour. Five mode tiles × colour, carbon and white.</td></tr>
        <tr><td>colour/</td><td>mxde-palette.json (HEX, RGB, CMYK, Pantone, contrast results), mxde-palette.ase (Adobe swatches)</td></tr>
        <tr><td>mockups/</td><td>All presentation mockups, PNG at 2×</td></tr>
        <tr><td>src/</td><td>Editable sources: geometry, palette, build scripts, fonts (OFL), mockup and guideline generators</td></tr></table></div>
      <div><h3 class="t-sub">Notes</h3>
        <p>Masters are outlined vector paths with no live text. The editable sources are the generator scripts. Change a value in <code>src/</code> and run <code>src/make.sh</code>.</p>
        <p>Native .ai files: the PDF masters open directly in Illustrator. Save them as .ai there if a supplier needs the native format.</p>
        <p>A trademark search on the name and the slot mark hasn't been done. Run one in each target market before launch.</p>
        <h3 class="t-sub">Open questions for the brand team</h3>
        <ul class="tight"><li>Target customer and price positioning</li><li>Sachet dimensions and finish (matte, foil, kraft)</li><li>Exact function and time of day for each mode</li>
        <li>Reference brands to admire and to avoid</li><li>SwitchYourMode vs #SwitchYourMode. Proposed: no # in lockups, # on social and packs.</li><li>Trademark check status</li><li>Timeline and budget</li></ul></div></div>""")


CSS = """
@page{size:297mm 210mm;margin:0}
*{box-sizing:border-box} html,body{margin:0;background:#fff;color:%(ink)s}
body{font-family:'IBM Plex Sans',sans-serif;font-size:10.5pt;line-height:1.45;-webkit-print-color-adjust:exact;print-color-adjust:exact}
.page{width:297mm;height:210mm;padding:14mm 16mm 16mm;position:relative;overflow:hidden;page-break-after:always;background:#fff;display:flex;flex-direction:column;gap:6mm}
.page.dark{background:%(carbon)s;color:%(paper)s}
.phead{display:flex;justify-content:space-between;align-items:baseline;border-bottom:1px solid #E2E0DA;padding-bottom:3mm}
.phead h2{margin:0;font-family:'Archivo';font-weight:600;font-size:20pt;letter-spacing:-.01em}
.phead .sec{font-family:'IBM Plex Sans Condensed';font-weight:500;letter-spacing:.06em;color:%(stone)s;font-size:9pt}
.pfoot{position:absolute;left:16mm;right:16mm;bottom:7mm;display:flex;justify-content:space-between;align-items:center;font-size:7.5pt;color:%(stone)s}
.pfoot svg{height:3.2mm;width:auto;color:%(ink)s}
.wm{width:100%%;height:auto;display:block}
.cover{display:grid;grid-template-rows:1fr auto auto;height:100%%;}
.cover-mark{align-self:center;width:70%%}
.cover-meta p{margin:2mm 0} .cover-meta .t-sub{font-size:13pt;color:%(silver)s}
.cover-tag svg{height:9mm;width:auto}
h1{font-size:30pt;line-height:1.08;margin:0 0 6mm;letter-spacing:-.01em} h1 em{font-style:normal;color:%(tonic)s}
h3{font-size:9pt;margin:0 0 2mm;color:%(ink)s}
.lead{font-size:14pt;line-height:1.35;margin:0 0 4mm} .narrow{max-width:190mm}
.small{font-size:9pt} .small p{margin:0 0 2.5mm} .note{font-size:8pt;color:%(graphite)s}
.cols-2{display:grid;grid-template-columns:1fr 1fr;gap:10mm;min-height:0}
.cols-3{display:grid;grid-template-columns:1fr 1fr 1fr;gap:8mm}
.toc{list-style:none;margin:0;padding:0;columns:1} .toc li{display:flex;gap:6mm;padding:1.6mm 0;border-bottom:1px solid #ECEAE4;font-size:11pt}
.frames{display:grid;grid-template-columns:repeat(3,1fr);gap:4mm;max-width:222mm}
.frame-cell{margin:0;background:%(paper)s} .frame-cell svg{display:block;width:100%%;height:auto}
.frame-cell figcaption{padding:2.5mm 3mm;font-size:9pt;border-top:1px solid #E5E2DB}
.hero-mark{padding:12mm 22mm;background:%(paper)s}
.diagram svg{width:100%%;height:auto;display:block} .diagram.c svg{max-height:80mm;width:auto;max-width:100%%;margin:0 auto}
.spec{border-collapse:collapse;width:100%%;font-size:8.5pt} .contrast{font-size:7.5pt} .contrast td{padding:1mm 2mm 1mm 0} .spec td,.spec th{border-bottom:1px solid #E5E2DB;padding:1.6mm 2mm 1.6mm 0;text-align:left;vertical-align:top}
.spec th{font-family:'IBM Plex Sans Condensed';font-weight:500;letter-spacing:.04em;text-transform:uppercase;font-size:7.5pt;color:%(graphite)s}
.contrast td.num{font-variant-numeric:tabular-nums}
.routes-mini{display:flex;flex-direction:column;gap:2mm;margin-bottom:2mm} .routes-mini svg{height:9mm;width:auto}
.ladder{display:flex;align-items:flex-end;gap:7mm;margin:4mm 0} .ladder-cell{display:flex;flex-direction:column;gap:1.5mm;align-items:flex-start}
.wm-px{height:100%%;width:auto;display:block}
.grid-lockups{display:grid;grid-template-columns:1fr 1fr;gap:7mm 12mm}
.grid-lockups figure{margin:0} .lk{background:%(paper)s;padding:8mm 10mm} .lk svg{max-height:34mm}
figcaption{font-size:8.5pt;margin-top:2mm}
.icons{display:flex;gap:6mm;align-items:center;background:%(paper)s;padding:6mm 8mm} .icons .mono{width:22mm;height:22mm} .icons .app{width:22mm;height:22mm}
.icons .fav{display:flex;gap:3mm;align-items:end}
.variants{display:grid;grid-template-columns:repeat(4,1fr);gap:4mm}
.variant{margin:0;padding:8mm 6mm 4mm;display:flex;flex-direction:column;gap:5mm;justify-content:space-between} .variant .lk{background:none;padding:0}
.variant figcaption{font-size:7.5pt;margin:0}
.misuse{display:grid;grid-template-columns:repeat(4,1fr);gap:6mm}
.mis{margin:0} .mis svg{width:100%%;height:auto;display:block;outline:1px solid #E5E2DB}
.mis figcaption::before{content:'✕  ';color:#C0392B;font-weight:600}
.pal-group h3{margin-bottom:1.5mm} .page:has(.pal-group){gap:4mm} .chips{display:flex;gap:3mm}
.chip{flex:1;min-height:14mm;padding:3mm;display:flex;flex-direction:column;font-size:7pt;line-height:1.35} .chip b{font-size:9pt;margin-bottom:auto;font-family:'Archivo'}
.ratio{display:flex;height:8mm;font-size:7.5pt;font-family:'IBM Plex Sans Condensed';text-transform:uppercase;letter-spacing:.04em}
.ratio div{display:flex;align-items:center;padding:0 3mm;border:1px solid #E5E2DB}
.specimen p{margin:0}
.nutri{border-collapse:collapse;margin-top:12px;font-family:'IBM Plex Sans Condensed';font-weight:500;font-size:8pt;width:70mm;border:1.5px solid %(ink)s}
.nutri th{text-align:left;padding:1.5mm 2mm;border-bottom:1.5px solid %(ink)s;font-weight:500} .nutri td{padding:1mm 2mm;border-top:.5px solid #999} .nutri td+td{text-align:right;font-variant-numeric:tabular-nums}
.modes{display:flex;flex-direction:column;gap:3mm}
.mode-row{display:grid;grid-template-columns:16mm 16mm 1fr 44mm;gap:4mm;align-items:center;border-bottom:1px solid #ECEAE4;padding-bottom:3mm}
.mode-row .mt svg{width:16mm;height:16mm;display:block} .mode-row p{margin:0} .codes{color:%(graphite)s;font-size:7.5pt}
.mlks{display:grid;grid-template-columns:1fr 1fr;gap:5mm} .mlk{margin:0;background:%(paper)s;padding:6mm 7mm} .mlk.dark{background:%(carbon)s}
.grow-row{display:flex;gap:8mm;align-items:flex-start} .grow{margin:0;width:30mm} .grow svg{width:30mm;height:30mm;display:block}
.rules li{margin-bottom:2mm}
.mock{width:100%%;height:auto;display:block} .m-top{max-height:84mm;object-fit:cover;object-position:center} .m-row img{max-height:62mm;object-fit:contain;object-position:left top}
.mocks{grid-template-columns:1fr 1fr 1fr;align-items:start} .pair{display:grid;grid-template-columns:1fr 1fr;gap:3mm;align-items:start}
.page .mocks img{max-height:58mm;object-fit:contain;object-position:left top}
.files td:first-child{white-space:nowrap;font-family:'IBM Plex Sans Condensed';font-weight:500}
.tight{margin:0;padding-left:4mm} .tight li{margin-bottom:1mm}
code{font-family:'IBM Plex Sans Condensed';background:#EFEDE7;padding:0 1mm}
"""


def render_html():
    build()
    css = CSS % {"ink": C["Carbon"], "carbon": C["Carbon"], "paper": C["Paper"], "stone": C["Stone"], "silver": C["Silver"],
                 "tonic": C["Tonic"], "graphite": C["Graphite"]}
    foot_wm = svgwrap(WORD_W, H, wordmark(0, 0, WORD_W, "currentColor", "currentColor"), "MXDE")
    html = [f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>MXDE Brand Guidelines</title><style>'
            f'{FONT_CSS_LOCAL.replace("{F}", "../src/fonts")}{TEXT_CSS}{css}</style></head><body>']
    n = 0
    for section, title, body, dark, num in PAGES:
        n += 1
        head = (f'<div class="phead"><h2>{title}</h2><span class="sec">{section}</span></div>' if title else "")
        foot = (f'<div class="pfoot">{foot_wm}<span>MXDE brand guidelines · v1.0 · {n:02d}</span></div>' if num else "")
        html.append(f'<section class="page{" dark" if dark else ""}">{head}{body}{foot}</section>')
    html.append("</body></html>")
    out = os.path.join(ROOT, "guidelines", "mxde-brand-guidelines.html")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w") as f:
        f.write("".join(html))
    return out, n


if __name__ == "__main__":
    p, n = render_html()
    os.makedirs(os.path.join(ROOT, "build"), exist_ok=True)
    with open(os.path.join(ROOT, "build", "gl-jobs.json"), "w") as f:
        json.dump([{"in": "guidelines/mxde-brand-guidelines.html", "out": "guidelines/mxde-brand-guidelines.pdf",
                    "w": 1123, "h": 794, "pdf": {"preferCSSPageSize": True}}], f)
    print(p, n, "pages")
