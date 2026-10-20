"""Quick exploration sheet of the five marks (greyscale), for looking at them."""
import os
from logos import *

OUT = os.path.join(ROOT, "build", "explore")
os.makedirs(OUT, exist_ok=True)
K = "#151515"
rows = []


def put(name, box, body):
    p = os.path.join(OUT, name + ".svg")
    open(p, "w").write(svg(box, body, name))
    return p


# 1 say
s = say()
put("say", s["box"], P(s["layers"]["letters"], K) + P(s["layers"]["macron"], K))
s = say_lockup()
put("say-lockup", s["box"], "".join(P(d, K) for d in s["layers"].values()))
# 2 dial
for st in ["logo"] + MODES:
    s = dial(st)
    put(f"dial-{st}", s["box"], P(s["layers"]["knob"], K) + P(s["layers"]["letters"], K))
# 3 light
for st in ["logo"] + MODES:
    s = light(st)
    y0, y1 = s["horizon"]
    W = s["width"]
    body = (f'<defs><clipPath id="u"><rect x="-5" y="-5" width="{W + 10}" height="{y0 + 5}"/></clipPath>'
            f'<clipPath id="l"><rect x="-5" y="{y1}" width="{W + 10}" height="{CAP - y1 + 5}"/></clipPath></defs>'
            f'<path clip-path="url(#u)" fill="#8A8D90" d="{s["layers"]["letters"]}"/><path clip-path="url(#l)" fill="{K}" d="{s["layers"]["letters"]}"/>')
    put(f"light-{st}", s["box"], body)
# 4 tear
s = tear()
put("tear", s["box"], P(s["layers"]["letters"], K) + P(s["layers"]["slash"], K))
s = tear("WAKE")
put("tear-wake", s["box"], "".join(P(d, K) for d in s["layers"].values()))
# 5 shift
s = shift(progressive=True)
put("shift-progressive", s["box"], P(s["layers"]["letters"], K))
for st in MODES:
    s = shift(st)
    put(f"shift-{st}", s["box"], P(s["layers"]["letters"], K))
print("ok")
