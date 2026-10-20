"""Post-render steps: favicon.ico, web manifest, <head> snippet, EPS masters."""
import glob
import json
import os
import subprocess
from PIL import Image
from palette import colour

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
icons = os.path.join(ROOT, "icons")

# favicon.ico — each size rendered on its own, not downscaled from one bitmap
frames = [Image.open(os.path.join(icons, f"favicon-{s}.png")).convert("RGBA") for s in (48, 32, 16)]
frames[0].save(os.path.join(icons, "favicon.ico"), sizes=[(48, 48), (32, 32), (16, 16)], append_images=frames[1:])

manifest = {
    "name": "MXDE", "short_name": "MXDE",
    "icons": [{"src": "/favicon-192.png", "sizes": "192x192", "type": "image/png"},
              {"src": "/app-icon-carbon-512.png", "sizes": "512x512", "type": "image/png"}],
    "theme_color": colour("Carbon"), "background_color": colour("Paper"), "display": "standalone",
}
with open(os.path.join(icons, "site.webmanifest"), "w") as f:
    json.dump(manifest, f, indent=2)
with open(os.path.join(icons, "head-snippet.html"), "w") as f:
    f.write('<link rel="icon" href="/favicon.ico" sizes="48x48">\n'
            '<link rel="icon" href="/favicon.svg" type="image/svg+xml">\n'
            '<link rel="apple-touch-icon" href="/apple-touch-icon-180.png">\n'
            '<link rel="manifest" href="/site.webmanifest">\n'
            f'<meta name="theme-color" content="{colour("Carbon")}">\n')

# EPS from the vector PDFs
n = 0
for pdf in glob.glob(os.path.join(ROOT, "logo", "pdf", "*.pdf")) + glob.glob(os.path.join(ROOT, "modes", "pdf", "*.pdf")):
    eps = pdf.replace(os.sep + "pdf" + os.sep, os.sep + "eps" + os.sep).replace(".pdf", ".eps")
    os.makedirs(os.path.dirname(eps), exist_ok=True)
    subprocess.run(["pdftocairo", "-eps", pdf, eps], check=True)
    n += 1
print(f"favicon.ico, manifest, head snippet, {n} EPS files")
