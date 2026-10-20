# MXDE — logo exploration, round 2

Each logo starts from a different idea, carried in the drawing itself rather than in a choice of typeface.

| # | Logo | Starts from | Idea |
|---|---|---|---|
| 1 | **Crossfade** | what MXDE does | Every smooth switch is drawn as a crossfade, and a crossfade is an X. The X's two strokes taper with their "volume": the state you leave fades to grey, the state you enter arrives in the mode colour. |
| 2 | **Notch** | the object | The sachet's tear notch moves to the centre of the top seal and is cut deep, so the pack's silhouette becomes a solid M. The packaging is the logo. |

Logos 3–5 follow after feedback on these two.

- `presentation/mxde-logos-1-2.html` — story, six-frame flow, reasoning, construction, size tests, mode system and 2D mockups for both logos.
- `logos/01-crossfade/`, `logos/02-notch/` — SVG masters (colour, mono, reversed, white, symbols, mode lockups, Notch small-size cut).
- `src/letters.py` — parametric letter geometry; `src/crossfade.py`, `src/notch.py` — the two marks; `src/two_marks.py`, `src/two_mocks.py`, `src/two_page.py` — frames, mockups and the page.

Rebuild: `python3 src/two_marks.py && python3 src/two_page.py` (needs shapely, fonttools).
