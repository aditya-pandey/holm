"""Write each mockup as a standalone HTML page (local fonts) and queue it for PNG rendering."""
import json
import os
import sys
from mockups import ALL, FONT_CSS_LOCAL, TEXT_CSS

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
FONTS = os.path.join(ROOT, "src", "fonts")
only = set(sys.argv[1:])
jobs = []
os.makedirs(os.path.join(ROOT, "build", "mockups"), exist_ok=True)
for name, fn in ALL.items():
    if only and name not in only:
        continue
    svg, w, h = fn()
    html = (f'<!doctype html><html><head><meta charset="utf-8"><style>{FONT_CSS_LOCAL.replace("{F}", "file://" + FONTS)}'
            f'{TEXT_CSS} html,body{{margin:0}} svg{{display:block;width:{w}px;height:{h}px}}</style></head><body>{svg}</body></html>')
    p = os.path.join(ROOT, "build", "mockups", f"{name}.html")
    with open(p, "w") as f:
        f.write(html)
    jobs.append({"in": os.path.relpath(p, ROOT), "out": f"mockups/mxde-mockup-{name}.png", "w": int(w), "h": int(h), "scale": 2, "bg": "#fff"})
with open(os.path.join(ROOT, "build", "mockup-jobs.json"), "w") as f:
    json.dump(jobs, f, indent=1)
print(len(jobs), "mockups queued")
