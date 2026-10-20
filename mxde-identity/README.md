# MXDE — logo and brand identity

MXDE is pronounced **Mode**. The X takes the place of the O and stands for the variable: whichever mode you switch into.

**The idea:** the O becomes a square *slot* with the X cut into it. The slot keeps the O's place and weight, so the word reads "Mode". The cut spells MXDE. Each product mode is the same square, cut differently:

| Mode | Cut | Idea | Tint |
|---|---|---|---|
| WAKE | ▲ | The X stands up: a rising peak | `#2771BE` |
| ACTIVE | ▶ | The X points forward: momentum | `#0B8457` |
| ZEN | ‖‖ upright | Aligned, focused mind | `#4F758B` |
| VITAL | + | The X turned upright: replenish | `#557F22` |
| CALM | ≡ laid down | A body at rest | `#8C6A4E` |

Status: **proposal pending sign-off**. Items marked *to confirm* in the guidelines are working assumptions from the brief.

## What's here

| Folder | Contents |
|---|---|
| `presentation/` | The story page: the reel, three routes, construction, mode system, colour, type and mockups. A single self-contained HTML file. |
| `guidelines/` | `mxde-brand-guidelines.pdf` (18 pages, A4 landscape) and its HTML source |
| `concepts/` | The three routes (A Crossover, B Slot ✔, C Shift), the plain reference build and the 10/14/18/22 weight study |
| `logo/svg · pdf · eps · png` | Wordmark and tagline lockup in fullcolour, carbon, black, white, tonic and silver. Monogram in carbon, white, tonic and black. |
| `icons/` | `favicon.svg`, `favicon.ico` (16/32/48), PNG 16–192, apple-touch 180, app icons 512, profile picture 1080, `site.webmanifest`, `head-snippet.html` |
| `modes/svg · pdf · eps · png` | Five mode lockups in four colourways each. Five mode tiles in three colourways each. |
| `colour/` | `mxde-palette.json` (HEX, RGB, CMYK, Pantone, WCAG results) and `mxde-palette.ase` (Adobe swatch exchange) |
| `mockups/` | Sachets ×5, thumbnail test, carton, e-commerce tile, web hero, header and favicon, Instagram post, story and profile, tumbler (PNG @2×) |
| `src/` | Everything above is generated from here |

## Rebuilding

```bash
pip install shapely fonttools pillow     # plus node with playwright, and poppler-utils (pdftocairo)
./src/make.sh
```

The wordmark geometry lives in `src/geom.py`: stem 18, cut 11.2, 60° M, 45° chamfered D, on a cap height of 100. The colours live in `src/palette.py`. Change a value and rerun. Every master, lockup, icon, mockup and both documents update together. Don't hand-edit outlined files.

## Notes

- Fonts: Archivo and IBM Plex Sans, both under the SIL Open Font License (files in `src/fonts/`). They're free for print, web and packaging. The wordmark is drawn from straight lines and uses no font.
- `.ai` files aren't included. The PDF masters open directly in Illustrator and can be saved as `.ai` from there.
- Pantone references are the nearest matches and CMYK values are starting points. Approve both against a physical guide and a press proof.
- No trademark search has been run on the name or the slot mark.
