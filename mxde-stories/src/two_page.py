"""Presentation page for logos 1 and 2 → presentation/mxde-logos-1-2.html (self-contained)."""
import html
import os
from letters import H, svg
import crossfade as cf
import notch as nt
import two_marks as T
import two_mocks as MK

ROOT = T.ROOT
C = T.C
esc = html.escape


def panel_svg(s, cls="mk"):
    return s.replace("<svg ", f'<svg class="{cls}" ', 1)


def reel(frames, rid):
    stage = "".join(f'<div class="frame" data-i="{i}"{" data-on" if i == 4 else ""}>{panel_svg(s, "fr")}</div>' for i, (_, s) in enumerate(frames))
    thumbs = "".join(f'<li><button type="button" class="th{" on" if i == 4 else ""}" data-i="{i}" aria-label="Frame {i + 1}">{panel_svg(s, "fr")}'
                     f'<span><b>{i + 1:02d}</b> {esc(c)}</span></button></li>' for i, (c, s) in enumerate(frames))
    cap = esc(frames[4][0])
    return (f'<div class="reel" id="{rid}"><div class="stage">{stage}</div><p class="stage-cap" aria-live="polite">{cap}</p>'
            f'<div class="reel-ctl"><button type="button" class="ghost play" aria-pressed="false">Play the flow</button></div>'
            f'<ol class="thumbs">{thumbs}</ol></div>')


def ladder(word_svg_fn, small_fn=None):
    """Size ladder; below 24 px the small-size cut is used when the logo has one."""
    cells = ""
    for px in (12, 16, 24, 32, 48):
        fn = small_fn if (small_fn and px < 24) else word_svg_fn
        cells += f'<figure><div style="height:{px}px">{panel_svg(fn(), "lad")}</div><figcaption>{px} px</figcaption></figure>'
    return f'<div class="ladder">{cells}</div>'


def steps(items):
    return "<ol class=\"steps\">" + "".join(f"<li><b>{esc(h)}</b> {esc(t)}</li>" for h, t in items) + "</ol>"


def section(n, name, kind, oneliner, hero_colour, mono, rev, story, frames, rid, think, construct, sizes, icons, modes_html,
            modes_note, board, works, risks):
    story_html = "".join(f"<p>{esc(p)}</p>" for p in story[:-1]) + f'<p class="line">{esc(story[-1])}</p>'
    return f"""
<section class="logo" id="logo-{n}">
  <div class="wrap">
    <header class="logo-head"><p class="eyebrow">Logo {n} · {esc(kind)}</p><h2>{esc(name)}</h2><p class="lede">{esc(oneliner)}</p></header>
    <div class="hero-panel">{panel_svg(hero_colour, "hero-mark")}</div>
    <div class="variants"><div class="v v-paper">{panel_svg(mono)}</div><div class="v v-dark">{panel_svg(rev)}</div></div>

    <div class="cols"><div><h3>The story</h3><div class="story">{story_html}</div></div>
      <div><h3>The flow</h3>{reel(frames, rid)}</div></div>

    <div class="cols"><div><h3>How I got there</h3>{steps(think)}</div>
      <div><h3>Construction</h3><div class="diagram">{panel_svg(construct, "dg")}</div>
        <h3 class="mt">At every size</h3>{sizes}<div class="icons">{icons}</div></div></div>

    <h3 class="mt">Mode system</h3><p class="note">{esc(modes_note)}</p>
    <div class="modes">{modes_html}</div>

    <h3 class="mt">On pack, can and feed</h3><p class="note">Presentation mockups, not production artwork.</p>
    <div class="board">{board}</div>

    <div class="cols mt"><div><h3>Why it works</h3><ul class="ticks">{"".join(f"<li>{esc(w)}</li>" for w in works)}</ul></div>
      <div><h3>Risks, said plainly</h3><ul class="risks">{"".join(f"<li>{esc(r)}</li>" for r in risks)}</ul></div></div>
  </div>
</section>"""


def build():
    # ---------------------------------------------------------- logo 1
    cf_modes = "".join(f'<figure class="ml">{panel_svg(T.cf_mode_lockup(k, C["carbon"]))}</figure>' for k in T.MODE)
    cf_icons = (svg((0, 0, 100, 100), T.cf_symbol(6, 6, 88, C["stone"], C["tonic"]), "symbol").replace("<svg ", '<svg class="ic" ', 1)
                + svg((0, 0, 180, 180), MK.cf_app_icon(0, 0, 180), "app icon").replace("<svg ", '<svg class="ic" ', 1))
    s1 = section(
        1, "Crossfade", "custom wordmark · starts from what MXDE does",
        "Every smooth switch is drawn as a crossfade, and a crossfade is an X. So the X in MXDE is drawn as one.",
        T.cf_svg("colour", 4), T.cf_svg("mono", 4), T.cf_svg("reversed", 4),
        ["Strong coffee switches you the way a light switch does: on, a spike, then the crash. MXDE is meant to move you from one state to the next without the jolt.",
         "Sound and film editors solved this long ago. When one track has to give way to another, they don't cut. They crossfade: the outgoing track falls while the incoming one rises, and on screen the two lines cross. A crossfade is drawn as an X.",
         "The name already has one. So the X in MXDE is drawn as a crossfade, each stroke as heavy as it is loud. The state you're leaving fades to grey. The state you're switching into arrives in the mode's colour and passes over the old one. M, D and E hold one steady weight around it: the calm frame for the change.",
         "No hard cuts. Just a crossfade. #SwitchYourMode"],
        T.cf_frames(), "reel1",
        [("Start from the job, not the object.", "MXDE sells a change of state, so the logo should show a change happening, not a cup, a bean or a body."),
         ("List the kinds of switch.", "A light switch is instant. A dimmer only goes one way. A dial jumps between positions. A crossfade is the only switch where two states overlap, which is exactly what moving from one mode to the next feels like."),
         ("Draw it, and look.", "The crossfade diagram is two crossing lines: an X, the very letter the brief calls the variable. The idea belongs inside the name, not in a symbol beside it."),
         ("Choose how to show volume.", "Gradients were out (banned in the core mark, unreliable on small sachets). Dashed dissolves broke up below 24 px. Arrowheads turned it into a sorting icon. Stroke weight won: a solid shape that prints anywhere."),
         ("Tune the taper.", "1.3× to 0.5× the stem. Steeper than that and the X goes top-heavy and starts to look like a cocktail glass. Shallower and the fade disappears."),
         ("Show which state wins.", "A 3.2-unit gap where the incoming stroke passes over the outgoing one, so even the one-colour version shows the new state arriving on top."),
         ("Keep the rest still.", "M, D and E are drawn at one weight with a geometric round D, so the only thing moving in the word is the X."),
         ("Test it.", "It reads at 12 px, in one colour and reversed. The grey stroke stays at 3.2:1 on paper, so the X never collapses into a slash.")],
        T.cf_construction(C["carbon"]), ladder(lambda: T.cf_svg("colour", 2)), cf_icons, cf_modes,
        "The incoming stroke takes the mode's colour; the outgoing stroke stays grey. On packs, each end of the X is labelled with what fades out and what fades in: sleep → sharp, desk → drive, noise → focus, slump → fresh, rush → rest. Colour helps, but the words carry the mode, so it works in one colour and for colour-blind customers.",
        MK.cf_board(),
        ["The idea is in the letter the brief calls the conceptual heart, and it needs no added symbol.",
         "It shows the functional promise people care about with functional coffee: a smooth change, no spike and crash.",
         "The X becomes a system: two strokes that can carry any pair of states, in any colour, for any future mode.",
         "Calm, precise and light on the pack. It reads as a premium tool, not a café or an energy drink."],
        ["A big solid X can read as \"no\" or \"close\". On packs the X is always two-tone and labelled, never a single-colour X on its own.",
         "Next.js's wordmark also has an X with a fading stroke. Ours tapers both strokes in opposite directions inside the letter, with no gradient and no extension. A trademark search should confirm the distance.",
         "The first time people see it, the idea needs one line (\"a crossfade is an X\"). After that it carries itself."])

    # ---------------------------------------------------------- logo 2
    nt_modes = "".join(f'<figure class="ml">{panel_svg(T.nt_mode_lockup(k, C["carbon"]))}</figure>' for k in T.MODE)
    nt_icons = (svg((0, 0, 100, 132), T.nt_symbol(0, 0, 132, C["carbon"]), "symbol").replace("<svg ", '<svg class="ic tall" ', 1)
                + svg((0, 0, 100, 132), T.nt_symbol(0, 0, 132, C["carbon"], small=True), "small cut").replace("<svg ", '<svg class="ic tall" ', 1)
                + svg((0, 0, 180, 180), MK.nt_app_icon(0, 0, 180), "app icon").replace("<svg ", '<svg class="ic" ', 1))
    s2 = section(
        2, "Notch", "combination mark · starts from the object",
        "Move the sachet's tear notch to the centre of the seal and cut it deep: the pack itself becomes the M.",
        T.nt_svg("colour", 4), T.nt_svg("mono", 4), T.nt_svg("reversed", 4),
        ["Most of the time MXDE isn't a logo on a screen. It's a sachet in a hand, in a gym bag, on a desk, in an unboxing video. The pack is the brand's real face.",
         "Every MXDE moment starts in the same place: the tear notch. It's the most-used detail on a sachet, and nobody ever looks at it. Moved to the centre of the top seal and cut deep, the notch turns the silhouette of the pack into a solid M.",
         "So the pack is the first letter of the name. Lined up, the five modes make a row of Ms. On a shelf, in a flat-lay or half out of a bag, you know it's MXDE before you read a word. The wordmark sets X, D and E at the pack's weight beside it.",
         "Tear the notch. Pour. Switch. #SwitchYourMode"],
        T.nt_frames(), "reel2",
        [("Start from where the brand is actually seen.", "The brief says it lives on tiny sachets, in unboxing and on Instagram. If the logo has to survive a small pack, let the pack carry the logo."),
         ("Take the sachet apart.", "Seal, crimp teeth, fill area, tear notch. The notch is functional, universal, and owned by nobody."),
         ("Move it and grow it, step by step.", "At 10% of the height it's still a nick. Around 40% it starts to read as an M. At 46% in the pack's own proportion (56% at cap height) the M and the sachet balance."),
         ("Keep the proof that it's a sachet.", "Crimp teeth on the shoulders and base stop it reading as a plain block letter. Below 24 px they drop away and the M silhouette stays."),
         ("Weigh the letters against the pack.", "X, D and E get 22% stems, so the solid M leads without swallowing them. The round D answers the angular pack."),
         ("Make the packaging the logo.", "The die-cut follows the mark, so the silhouette is the brand even with no print. On cans the colour band is notched the same way."),
         ("Rejected along the way.", "A notch on the side (too close to Kotlin's K), a shallow notch (reads as a flat block) and a torn corner (reads as a document icon).")],
        T.nt_construction(C["carbon"]), ladder(lambda: T.nt_svg("colour", 2), lambda: T.nt_svg("colour", 2, small=True)), nt_icons, nt_modes,
        "Each mode is a pack-M in its own colour, named in large type. The shape never changes, which makes the range instantly recognisable as one brand. The names carry the mode in one colour and for colour-blind customers.",
        MK.nt_board(),
        ["The packaging is the logo: recognisable from silhouette alone, which no coffee or supplement brand owns.",
         "Built for exactly where the brief says the brand lives: small sachets, unboxing and flat-lay photos.",
         "Honest and functional. The notch is where you tear, so the mark explains the ritual: tear, pour, switch.",
         "Bold and graphic but simple. In muted mode colours it stays premium rather than playful."],
        ["A die-cut V notch costs more than a straight cut and needs the converter's sign-off. The sharp inner point is where the tear starts, which helps.",
         "Standing alone, some people will see a V-neck or a bookmark before an M. Next to XDE, or in a row of five packs, it reads as M.",
         "The solid M is much heavier than X, D and E by design. Below 24 px, use the symbol on its own rather than the full wordmark."])

    page = TEMPLATE.replace("{{S1}}", s1).replace("{{S2}}", s2)
    out = os.path.join(ROOT, "presentation", "mxde-logos-1-2.html")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, "w").write(page)
    return out, len(page)


TEMPLATE = r"""<title>MXDE Logos One and Two</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Instrument+Sans:wght@400;500;600&family=Archivo:wdth,wght@62..100,500..800&display=swap">
<style>
/* Layout: a long designer's crit page. Each logo is one chapter: mark, story, flow, reasoning, craft, system, pack. */
:root{
  --bg:#F6F4EF; --surface:#FFFFFF; --ink:#151515; --muted:#5A5D61; --line:#E1DDD5; --accent:#0E7C66; --guide:#2F6BFF;
  --paper:#F3F1EC; --carbon:#151515;
  --f-text:'Instrument Sans',system-ui,sans-serif; --f-display:'Instrument Sans',system-ui,sans-serif;
}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--bg:#121212;--surface:#1B1B1B;--ink:#EFEDE8;--muted:#A7A9AC;--line:#2D2D2C;--accent:#3FB79A;--guide:#7FA2FF;color-scheme:dark}}
:root[data-theme="dark"]{--bg:#121212;--surface:#1B1B1B;--ink:#EFEDE8;--muted:#A7A9AC;--line:#2D2D2C;--accent:#3FB79A;--guide:#7FA2FF;color-scheme:dark}
*{box-sizing:border-box}
body{background:var(--bg);color:var(--ink);font-family:var(--f-text);font-size:16px;line-height:1.55;margin:0}
.wrap{max-width:1180px;margin:0 auto;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}
h1,h2,h3{margin:0;font-weight:600;letter-spacing:-.01em;text-wrap:balance}
h1{font-size:clamp(32px,5vw,58px);line-height:1.04;max-width:18ch}
h2{font-size:clamp(40px,6vw,76px);line-height:1}
h3{font-size:13px;text-transform:uppercase;letter-spacing:.09em;font-weight:600;margin-bottom:14px}
h3.mt,.mt{margin-top:48px}
p{margin:0}
.eyebrow{font-size:12px;letter-spacing:.1em;text-transform:uppercase;color:var(--muted);font-weight:500}
.lede{font-size:clamp(17px,1.7vw,21px);color:var(--muted);max-width:60ch}
.note{color:var(--muted);font-size:15px;max-width:72ch;margin-bottom:16px}
svg{display:block;max-width:100%;height:auto}
button{font:inherit;color:inherit;cursor:pointer}
:focus-visible{outline:2px solid var(--guide);outline-offset:3px}
/* text classes used inside the artwork */
.modename,.lab,.body,.head{font-family:'Instrument Sans',system-ui,sans-serif}
.modename,.head{font-weight:600} .lab{font-weight:500;letter-spacing:.04em} .body{font-weight:400}
.modename2,.head2,.ghost{font-family:'Archivo',system-ui,sans-serif;font-weight:800;font-stretch:62.5%}

.intro{padding-block:clamp(48px,8vw,104px) clamp(32px,5vw,64px)}
.intro .lede{margin-top:20px}
.method{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px;margin-top:36px}
.method a{display:block;background:var(--surface);border:1px solid var(--line);padding:20px 22px;color:inherit;text-decoration:none}
.method a:hover{border-color:var(--ink)}
.method b{display:block;font-size:22px;margin:6px 0}
.method span{color:var(--muted);font-size:15px}

section.logo{padding-block:clamp(56px,8vw,112px);border-top:1px solid var(--line)}
.logo-head{display:grid;gap:12px;margin-bottom:32px}
.hero-panel{background:var(--paper);padding:clamp(28px,7vw,96px) clamp(20px,8vw,120px)}
.hero-mark{width:100%}
.variants{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:12px}
.v{padding:clamp(16px,3vw,32px) clamp(16px,4vw,48px)} .v-paper{background:#fff;border:1px solid var(--line)} .v-dark{background:var(--carbon)}
.cols{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:clamp(24px,4vw,56px);margin-top:48px;align-items:start}
.story{display:grid;gap:14px;font-size:17px;max-width:60ch}
.story .line{font-weight:600;font-size:19px}
.steps{margin:0;padding-left:22px;display:grid;gap:12px;font-size:15.5px}
.steps b{display:block;font-weight:600}
.diagram{background:var(--surface);border:1px solid var(--line);padding:12px;color:var(--ink);overflow-x:auto}
.diagram .dg{min-width:520px}

/* the flow reel */
.reel{display:grid;gap:12px}
.stage{position:relative;background:var(--paper);aspect-ratio:360/220;color:#151515}
.frame{position:absolute;inset:0;opacity:0;transition:opacity .7s ease}
.frame[data-on]{opacity:1}
.frame .fr{width:100%;height:100%}
.stage-cap{font-size:15px;min-height:3em}
.reel-ctl{display:flex;gap:8px}
.ghost{background:none;border:1px solid var(--ink);padding:7px 14px;font-size:13px;letter-spacing:.06em;text-transform:uppercase}
.thumbs{list-style:none;padding:0;margin:0;display:grid;grid-template-columns:repeat(6,minmax(0,1fr));gap:6px}
.th{background:var(--paper);border:1px solid transparent;padding:0;width:100%;text-align:left;color:#151515;display:flex;flex-direction:column;height:100%}
.th.on{border-color:var(--ink)}
.th span{display:none}
.th .fr{width:100%;height:auto}

.ladder{display:flex;flex-wrap:wrap;align-items:flex-end;gap:20px;background:var(--surface);border:1px solid var(--line);padding:20px}
.ladder figure{margin:0;display:grid;gap:6px}
.ladder .lad{height:100%;width:auto}
.ladder figcaption{font-size:12px;color:var(--muted)}
.icons{display:flex;gap:12px;margin-top:12px;align-items:center;flex-wrap:wrap}
.icons .ic{width:84px;height:84px} .icons .ic.tall{width:64px;height:84px}
.modes{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:10px}
.ml{margin:0;background:var(--paper);padding:16px;color:#151515}
.board{background:#E7E3DB;overflow:hidden}
.board .mock{width:100%}
.ticks,.risks{margin:0;padding-left:20px;display:grid;gap:10px;font-size:15.5px}
.risks li::marker{content:"! ";color:#B4532A;font-weight:700}

.compare{padding-block:clamp(56px,8vw,104px);border-top:1px solid var(--line)}
.tablewrap{overflow-x:auto;margin-top:24px}
table{border-collapse:collapse;width:100%;font-size:15px;min-width:640px}
th,td{text-align:left;padding:12px 16px 12px 0;border-bottom:1px solid var(--line);vertical-align:top}
th{font-size:12px;text-transform:uppercase;letter-spacing:.08em;color:var(--muted);font-weight:600}
.next{display:grid;gap:12px;margin-top:40px;max-width:70ch}
footer{padding-block:40px 64px;border-top:1px solid var(--line);color:var(--muted);font-size:14px}

@media (max-width:860px){
  .cols,.method,.variants{grid-template-columns:minmax(0,1fr)}
  .modes{grid-template-columns:repeat(2,minmax(0,1fr))}
  .thumbs{grid-template-columns:repeat(3,minmax(0,1fr))}
}
@media (prefers-reduced-motion:reduce){.frame{transition:none}}
</style>

<header class="intro"><div class="wrap">
  <p class="eyebrow">MXDE · logo exploration · round 2 · logos 1 and 2 of 5</p>
  <h1>Two logos, two different starting points.</h1>
  <p class="lede">Logo 1 starts from what MXDE does to you: it switches your state. Logo 2 starts from the thing you hold: the sachet. Each has its own story, construction and mode system. Logos 3 to 5 come once you've reacted to these.</p>
  <nav class="method" aria-label="The two logos">
    <a href="#logo-1"><span>Logo 1 · from the benefit</span><b>Crossfade</b><span>The X is drawn as a crossfade: one state fades out as the next fades in.</span></a>
    <a href="#logo-2"><span>Logo 2 · from the object</span><b>Notch</b><span>The tear notch, moved and cut deep, turns the sachet into the M.</span></a>
  </nav>
</div></header>

{{S1}}
{{S2}}

<section class="compare"><div class="wrap">
  <p class="eyebrow">Side by side</p><h2 style="font-size:clamp(28px,4vw,44px)">Against the brief's own questions</h2>
  <div class="tablewrap"><table>
    <thead><tr><th>Question</th><th>Crossfade</th><th>Notch</th></tr></thead>
    <tbody>
      <tr><td>Does it read as "Mode" at first glance?</td><td>No better than plain type. The X stays a clear X, so the pronunciation still needs support on pack.</td><td>The same. Neither idea fixes pronunciation; that's a job for one of logos 3 to 5.</td></tr>
      <tr><td>Straight, angular lines, few curves?</td><td>Yes, apart from the round D.</td><td>Yes, apart from the round D.</td></tr>
      <tr><td>Holds up small and in one colour?</td><td>Yes, down to 12 px.</td><td>Yes. The crimp teeth drop away below 24 px.</td></tr>
      <tr><td>Does the X carry the switch?</td><td>Yes. It is the whole idea.</td><td>No. The switch lives in the tear, not in the X.</td></tr>
      <tr><td>Premium and healthy, not a café or an energy drink?</td><td>Yes: quiet, precise, lots of air.</td><td>Yes, as long as the mode colours stay muted.</td></tr>
      <tr><td>Can the five modes be told apart instantly?</td><td>Yes: colour plus fade labels (sleep → sharp).</td><td>Yes: colour plus large mode names. The shape stays the same on purpose.</td></tr>
    </tbody></table></div>
  <div class="next"><h3>Next</h3>
    <p>Tell me what you like and don't like in each: the idea, the drawing, the system or the packs. If one of them is close, I'll refine it before moving on. Then I'll do logos 3 to 5, each from a different starting point again.</p></div>
</div></section>

<footer><div class="wrap">MXDE logo exploration, round 2. The marks are drawn from geometry, not from a font. Fonts used around them: Instrument Sans and Archivo (SIL Open Font License). No trademark search has been run yet.</div></footer>

<script>
(function(){
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  document.querySelectorAll('.reel').forEach(function(r){
    var frames = r.querySelectorAll('.frame'), thumbs = r.querySelectorAll('.th'), cap = r.querySelector('.stage-cap'), play = r.querySelector('.play');
    var caps = Array.prototype.map.call(thumbs, function(t){ return t.querySelector('span').textContent.replace(/^\d+\s/, ''); });
    var cur = 4, timer = null;
    function show(i){ cur = i; frames.forEach(function(f){ if (+f.dataset.i === i) f.setAttribute('data-on',''); else f.removeAttribute('data-on'); });
      thumbs.forEach(function(t){ t.classList.toggle('on', +t.dataset.i === i); }); cap.textContent = caps[i]; }
    function stop(){ if (timer){ clearInterval(timer); timer = null; } play.textContent = 'Play the flow'; play.setAttribute('aria-pressed','false'); }
    function start(){ show(0); timer = setInterval(function(){ show((cur + 1) % frames.length); }, reduce ? 3200 : 2600); play.textContent = 'Pause'; play.setAttribute('aria-pressed','true'); }
    thumbs.forEach(function(t){ t.addEventListener('click', function(){ stop(); show(+t.dataset.i); }); });
    play.addEventListener('click', function(){ timer ? stop() : start(); });
  });
})();
</script>
"""

if __name__ == "__main__":
    p, n = build()
    print(p, f"{n / 1024:.0f} KB")
