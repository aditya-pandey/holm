"""Sketch sheet: render rows of candidate geometries to one PNG for review."""
import json, subprocess, sys
from shapely.ops import unary_union
from shapely import affinity
from five_six import d_of

OUT = "/tmp/claude-0/-home-user-holm/94fcf371-5ac2-5efb-a06a-4d37b8b52066/scratchpad/echo"


def sheet(rows, name, row_h=240, wpx=1400, pad=40):
    """rows: list of (label, geometry). Each row scaled to fit row_h."""
    body = []
    y = pad
    for label, g in rows:
        b = g.bounds
        k = min((row_h - 50) / (b[3] - b[1]), (wpx - 2 * pad) / (b[2] - b[0]))
        gg = affinity.translate(g, -b[0], -b[1])
        body.append(f'<text x="{pad}" y="{y + 14}" font-family="sans-serif" font-size="14" fill="#888">{label}</text>')
        body.append(f'<path transform="translate({pad} {y + 30}) scale({k:.4f})" d="{d_of(gg)}" fill="#111"/>')
        y += row_h
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {wpx} {y + pad}">' + "".join(body) + "</svg>"
    p = f"{OUT}/{name}.svg"
    open(p, "w").write(svg)
    jobs = [{"in": p, "out": f"{OUT}/{name}.png", "w": wpx, "h": int(y + pad), "bg": "#fff"}]
    open(f"{OUT}/jobs.json", "w").write(json.dumps(jobs))
    subprocess.run(["node", "engine/render.mjs", f"{OUT}/jobs.json"], check=True,
                   env={"NODE_PATH": "/opt/node22/lib/node_modules", "PATH": "/usr/bin:/bin:/opt/node22/bin"})
    return f"{OUT}/{name}.png"


def flat(parts):
    gs = []
    for p in parts:
        for k in ("solid", "hair"):
            if p.get(k) is not None:
                gs.append(p[k])
    return unary_union(gs)
