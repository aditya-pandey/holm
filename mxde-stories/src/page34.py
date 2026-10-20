"""Presentation page for logos 3 (Ring) and 4 (Mug) → presentation/mxde-logos-3-4.html."""
import html
import os
from letters import H, svg
import three_four as T
from two_page import reel, steps, panel_svg, TEMPLATE as BASE

ROOT = T.ROOT
esc = html.escape


def ladder(fn):
    cells = "".join(f'<figure><div style="height:{px}px">{panel_svg(fn(), "lad")}</div><figcaption>{px} px</figcaption></figure>'
                    for px in (12, 16, 24, 32, 48))
    return f'<div class="ladder">{cells}</div>'


def section(n, name, kind, oneliner, hero, mono, rev, story, frames, rid, think, construct, sizes, icons, board, works, risks):
    story_html = "".join(f"<p>{esc(p)}</p>" for p in story[:-1]) + f'<p class="line">{esc(story[-1])}</p>'
    return f"""
<section class="logo" id="logo-{n}">
  <div class="wrap">
    <header class="logo-head"><p class="eyebrow">Logo {n} · {esc(kind)}</p><h2>{esc(name)}</h2><p class="lede">{esc(oneliner)}</p></header>
    <div class="hero-panel warm">{panel_svg(hero, "hero-mark")}</div>
    <div class="variants"><div class="v v-paper">{panel_svg(mono)}</div><div class="v v-dark">{panel_svg(rev)}</div></div>
    <div class="cols"><div><h3>The story</h3><div class="story">{story_html}</div></div>
      <div><h3>The flow</h3>{reel(frames, rid)}</div></div>
    <div class="cols"><div><h3>How I got there</h3>{steps(think)}</div>
      <div><h3>Construction</h3><div class="diagram">{panel_svg(construct, "dg")}</div>
        <h3 class="mt">At every size</h3>{sizes}<div class="icons">{icons}</div></div></div>
    <h3 class="mt">On the sachet</h3><p class="note">Flat sachets that open with one hand: fold at the line, squeeze, pour. Front and back, three coffees. Presentation mockups, not production artwork.</p>
    <div class="board">{board}</div>
    <div class="cols mt"><div><h3>Why it works</h3><ul class="ticks">{"".join(f"<li>{esc(w)}</li>" for w in works)}</ul></div>
      <div><h3>Risks, said plainly</h3><ul class="risks">{"".join(f"<li>{esc(r)}</li>" for r in risks)}</ul></div></div>
  </div>
</section>"""


def build():
    ring_icons = (svg((0, 0, 160, 160), f'<rect width="160" height="160" rx="36" fill="{T.CREAM}"/>' + T.ring_symbol(20, 20, 120), "icon").replace("<svg ", '<svg class="ic" ', 1)
                  + svg((0, 0, 160, 160), f'<rect width="160" height="160" rx="36" fill="{T.K}"/>' + T.ring_symbol(20, 20, 120, T.CREAM, "#C9A273", "#C9A273"), "icon").replace("<svg ", '<svg class="ic" ', 1))
    s3 = section(
        3, "Ring", "wordmark with a found mark · starts from the cup",
        "Put your coffee down on the name. The ring it leaves sits round the X and becomes the O, so MXDE reads Mode.",
        T.ring_svg("colour"), T.ring_svg("mono"), T.ring_svg("reversed"),
        ["MXDE has one real problem: nobody knows how to say it. M-X-D-E? Mix-dee? The X is standing in for an O, and the eye can't tell.",
         "Coffee fixes it. Set a cup down on the word and lift it again. It leaves a ring, the most familiar mark coffee makes, and the ring lands round the X. Now there's an O on the page. The eye reads Mode, and the name still spells MXDE.",
         "So the logo isn't drawn so much as left behind by a cup. The letters are precise and quiet. The ring is human: slightly out of round, thin where the cup lifted first. The only colour in the logo is the colour of coffee.",
         "Say it Mode. Your cup already knows."],
        T.ring_frames(), "reel3",
        [("Find the real problem.", "The name is easy to say and hard to read. A logo that doesn't help the eye find the O leaves the brand's biggest problem unsolved."),
         ("Look for an O that already belongs to coffee.", "A cup from above, a saucer, a bean, a ring stain. Only the stain is an O and nothing else. You don't need the cup, just the trace it leaves."),
         ("Put it round the X, not in its place.", "The X stays, so the name stays MXDE. The ring adds the O on top. You get two readings at once, which is the whole point of the name."),
         ("Draw it like a real stain, then tame it.", "Real rings are out of round, with a sharp dark edge, a pale wash inside and a thin spot where the cup tipped as it lifted. Four sine terms set the shape, three set the edge weight, plus one deliberate thin spot. Nothing is random, so every file is identical."),
         ("Keep the letters out of the way.", "Light 12.5-unit stems and 40 units of space either side of the X, so the ring has room and leads."),
         ("Rejected along the way.", "A clean geometric circle (it read as ⊗, a maths symbol), a cup seen from above (a café sign, not a name), and a ring in place of the X (it loses the name)."),
         ("Test it.", "At 16 px the ring still reads as an O. It holds in one colour, and reversed the ring turns caramel on espresso.")],
        T.ring_construction(), ladder(lambda: T.svg(T.RING_VB, T.ring_lockup(0, 0, None, hero=False), "MXDE")), ring_icons,
        T.ring_board(),
        ["It solves the pronunciation inside the logo, with no phonetic guide needed.",
         "Coffee is in the mark without a bean, a cup or steam: only the trace coffee leaves.",
         "Precise and human at once, which is what makes it memorable.",
         "Use becomes brand: every real cup ring on a desk or a pack echoes the logo."],
        ["Coffee rings are a familiar decorative motif in café branding. Ours works as a letter, but a trademark search should check for ring-around-letter marks.",
         "Some people will first read \"M ⊗ DE\". The out-of-round edge and the brown are what make it a stain, so never redraw it as a clean circle.",
         "A stain can look dirty if it's used large and grey. Keep it coffee-coloured, sharp-edged and on clean grounds."])

    mug_icons = (svg((0, 0, 160, 160), f'<rect width="160" height="160" rx="36" fill="#3B2618"/>' + T.mug_symbol(26, 26, 108, "#C08A5B"), "icon").replace("<svg ", '<svg class="ic" ', 1)
                 + svg((0, 0, 160, 160), f'<rect width="160" height="160" rx="36" fill="{T.CREAM}"/>' + T.mug_symbol(26, 26, 108, T.MUG), "icon").replace("<svg ", '<svg class="ic" ', 1))
    s4 = section(
        4, "Mug", "custom wordmark · starts from a letter",
        "A D is a straight back and a round belly. Thicken the back, lift the belly off the ground, and the D becomes a coffee mug.",
        T.mug_svg("colour"), T.mug_svg("mono"), T.mug_svg("reversed"),
        ["Look at a D long enough and it turns into something you already own. Thicken its straight back and you have the body of a mug. Lift its round belly off the ground and you have the handle.",
         "So MXDE has a mug in the middle of its name, and it still reads as a D. A rim line across the top and a rounded foot are all it takes to make it coffee.",
         "It also fits how the coffee is meant to be used: with one hand. You fold and squeeze the sachet with one hand, and you hold a mug with one hand, by the handle. The handle is the D's bowl, drawn as thick as every other stroke, so the mug belongs to the alphabet around it.",
         "One hand. One shot. MXDE coffee."],
        T.mug_frames(), "reel4",
        [("Ask which letter is already an object.", "M could be a mountain or a crown, X a crossing, E a comb. D is a mug in profile, waiting."),
         ("Move it one step at a time.", "Thicken the stem into a mug's body (44 units), then shrink the bowl and lift it into a handle."),
         ("Keep the letter.", "In the first pass the handle sat mid-height, like on a real mug, and the word read MXPE. To stay a D, the handle had to run nearly the full height (4–90%). The gap left under it becomes the mug's foot."),
         ("Add only what makes it coffee.", "A rim line 6.5 units below the top and rounded bottom corners. No steam, no saucer."),
         ("Make it heavy enough to hold.", "M, X and E have 17-unit stems and the handle is 17 too, so the mug reads as part of the type, not a picture dropped in."),
         ("Rejected along the way.", "Steam lines over the mug (clutter, and a café cliché), a cup in place of the X (it loses the name), and a fully illustrated mug (it doesn't scale)."),
         ("Test it.", "It reads as a D at 12 px and as a solid letter in one colour. On its own, the mug works as the app icon.")],
        T.mug_construction(), ladder(lambda: T.svg(T.MUG_VB, T.mug_lockup(), "MXDE")), mug_icons,
        T.mug_board(),
        ["Anyone gets it in a second: there's a mug in the name.",
         "It's simple enough to stamp, emboss or print at 12 px, and the mug works as an icon on its own.",
         "Warm and bold without the café clichés: no beans, no steam.",
         "It ties to the sachet: one hand to open it, one hand on the handle."],
        ["Mug-shaped letters have appeared in café branding before. Ours only works as this D, but a trademark search should confirm the distance.",
         "It doesn't help people say \"Mode\", because the X stays a plain X.",
         "The rim line is thin. Below about 14 px it closes up, though the solid mug still reads as a D."])

    head = """
<header class="intro"><div class="wrap">
  <p class="eyebrow">MXDE · logo exploration · logos 3 and 4</p>
  <h1>Two more, made of coffee.</h1>
  <p class="lede">This round drops the brand system. Each logo keeps only the name and the coffee, and pushes one idea as far as it goes. Both are shown on the flat, fold-and-squeeze sachet.</p>
  <nav class="method" aria-label="The two logos">
    <a href="#logo-3"><span>Logo 3 · from the cup</span><b>Ring</b><span>A coffee ring lands round the X and becomes the O. The word reads Mode.</span></a>
    <a href="#logo-4"><span>Logo 4 · from a letter</span><b>Mug</b><span>The D's back thickens and its belly lifts off the ground: it's a mug.</span></a>
  </nav>
</div></header>"""
    compare = """
<section class="compare"><div class="wrap">
  <p class="eyebrow">Side by side</p><h2 style="font-size:clamp(28px,4vw,44px)">Ring and Mug, compared</h2>
  <div class="tablewrap"><table>
    <thead><tr><th>Question</th><th>Ring</th><th>Mug</th></tr></thead>
    <tbody>
      <tr><td>Does it read as "Mode"?</td><td>Yes. That is the idea.</td><td>No. The X stays a plain X.</td></tr>
      <tr><td>Where is the coffee?</td><td>In the trace it leaves: the ring.</td><td>In the object: the D is a mug.</td></tr>
      <tr><td>How fast does it land?</td><td>One beat: "oh, it's an O".</td><td>Instantly: "there's a mug in it".</td></tr>
      <tr><td>Small and one colour?</td><td>Yes. The ring reads as an O at 16 px.</td><td>Yes, to 12 px. The rim line closes below about 14 px.</td></tr>
      <tr><td>Feel</td><td>Quiet, precise, human. Editorial.</td><td>Warm, bold, graphic. Friendly.</td></tr>
      <tr><td>On the sachet</td><td>The pack looks like it's been used as a coaster: a ring on it.</td><td>A big mug on every pack. One hand to open, one hand to hold.</td></tr>
    </tbody></table></div>
  <div class="next"><h3>Next</h3>
    <p>Tell me what you like and don't like in each. If one of them is close, I'll refine it before moving on. Logo 5 comes next, from yet another starting point.</p></div>
</div></section>"""
    page = BASE
    a = page.index('<header class="intro">')
    b = page.index("<footer>")
    page = page[:a] + head + s3 + s4 + compare + page[b:]
    page = page.replace("<title>MXDE Logos One and Two</title>", "<title>MXDE Logos Three and Four</title>")
    page = page.replace("MXDE logo exploration, round 2. The marks are drawn from geometry, not from a font.",
                        "MXDE logo exploration, logos 3 and 4. The marks are drawn from geometry; COFFEE is set in Instrument Sans and Archivo.")
    page = page.replace(".modename2,.head2,.ghost{", ".sku{font-family:'Instrument Sans',system-ui,sans-serif;font-weight:600}\n.sku2,.modename2,.head2,.ghost{")
    page = page.replace(".hero-panel{background:var(--paper);", ".hero-panel.warm{background:#F4EFE6}\n.hero-panel{background:var(--paper);")
    page = page.replace(".icons .ic{width:84px;height:84px}", ".icons .ic{width:96px;height:96px}")
    out = os.path.join(ROOT, "presentation", "mxde-logos-3-4.html")
    open(out, "w").write(page)
    return out, len(page)


if __name__ == "__main__":
    p, n = build()
    print(p, f"{n / 1024:.0f} KB")
