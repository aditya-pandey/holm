#!/usr/bin/env bash
# Rebuild every MXDE asset from source. Needs python3 (shapely, fonttools, pillow), node + playwright, poppler-utils.
set -euo pipefail
cd "$(dirname "$0")/.."
export NODE_PATH="${NODE_PATH:-$(npm root -g)}"

python3 src/palette.py > /dev/null          # colour/mxde-palette.json + .ase
python3 src/concepts.py                     # concepts/ — the three routes and the weight study
python3 src/build.py                        # logo/, icons/, modes/ SVG masters + render jobs
node src/render.mjs build/jobs.json         # PNG + PDF
python3 src/finish.py                       # favicon.ico, manifest, EPS
python3 src/render_mockups.py               # mockups/ pages
node src/render.mjs build/mockup-jobs.json  # mockups/ PNG
python3 src/guidelines.py                   # guidelines/ HTML
node src/render.mjs build/gl-jobs.json      # guidelines/ PDF
python3 src/presentation.py                 # presentation/ HTML
