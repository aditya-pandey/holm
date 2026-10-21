# MODE — brand kit

Coffee concentrate in single-serve sachets. The mark is MO over DE, built in the grammar of Albert Hollenstein's
L'Echoppe monogram: every letter is a coffee (the m drips, the o is half poured, the D is a cup on its saucer,
the e is Hollenstein's e, left open). The range is the five modes: Wake, Active, Zen, Vital, Calm.
The mark never changes; modes are named on the pack with a ground, a line and a band in the mode's tint.

Start with `guidelines/MODE-Brand-Guidelines.pdf` (or the interactive `guidelines/mode-brand-guidelines.html`).

| Folder | What's inside |
| --- | --- |
| `logo/` | SVG, PDF, PNG (512/1024/2048): Carbon, Paper, Roast, black, white · `-small` cut · monogram · `-clearspace` |
| `icon/` | App icon (1024/512/192/180), `favicon.svg`, `favicon.ico` (16/32/48), profile pictures |
| `colour/` | `mode-palette.ase`, `.json`, `.css` |
| `packaging/sachet/` | Front and back for all five modes: SVG, print PDF with 2 mm bleed, PNG |
| `packaging/carton/` | Dielines with artwork for all five modes + a blank die |
| `packaging/mailer/`, `packaging/tumbler/` | Lid, inside lid, tumbler wrap |
| `packaging/renders/` | 3D renders, 1800 × 1200 |
| `digital/` | Instagram posts and story, e-commerce tile, website hero and header |
| `film/out/` | `MODE-brand-film-v2-1080p.mp4`: the 30 s film "From sketch to sachet" (1920 × 1080, 30 fps, H.264 + AAC) · v1 `MODE-brand-film-1080p.mp4` · both music tracks |
| `fonts/` | Instrument Sans, IBM Plex Mono (SIL Open Font License) |
| `src/` | The generators |

Placeholders to confirm before print: mode lines, tasting notes, caffeine and nutrition values, barcodes (GTIN),
the die (with the converter) and every Pantone/CMYK value (proof on the real stock).

## Rebuild

```
python3 src/build_logo.py      # logo, icons, colour files
python3 src/build_pack.py      # packaging flats, dielines, textures
node src/render3d.mjs          # 3D renders (needs NODE_PATH with playwright)
python3 src/build_digital.py   # social, e-commerce, web
python3 src/build_doc.py && node src/export_doc.mjs   # guidelines HTML + PDF
python3 film/v2/timeline.py && python3 film/v2/music.py && node film/shots3d.mjs && python3 film/v2/build.py && node film/v2/render.mjs   # film v2
```

The film's music is synthesised in `film/music.py` (120 BPM, no samples), so it is free to use anywhere.

Geometry lives in `src/mark.py`, colours and modes in `src/brand.py`: change them there and rebuild.
