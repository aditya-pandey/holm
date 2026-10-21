"""Original track for 'From sketch to sachet' (film v2). 128 BPM, 16 bars = 30 s, synthesised from scratch.
Reads timeline.json so every pencil stroke, compass sweep and ink flood has its own sound, on its own frame.

  bars 1-4   tension: muffled pulse, pencil and compass, a hit on each card (one radius / cut / hairline)
  bars 5-8   the letters: the groove arrives, rolling bass, an ink 'whoomp' on every flood
  bar 9      the words: a stab per word, snare roll and riser
  bar 10     colour-way cuts: rising stabs on the eighths, a breath before the drop
  bars 11-15 the product: the drop, full groove, arpeggio
  bar 16     the logo: the groove falls away, the last chord rings
"""
import json
import os
import wave
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
TL = json.load(open(os.path.join(HERE, "timeline.json")))
SR = 48000
DUR = 30.0
BEAT = 60 / 128
BAR = 4 * BEAT
N = int(SR * DUR)
rng = np.random.default_rng(21)
b = lambda bar, beat=0.0: (bar - 1) * BAR + beat * BEAT
L = np.zeros(N)
Rc = np.zeros(N)


def t_(d):
    return np.arange(int(SR * d)) / SR


def place(sig, at, gain=1.0, pan=0.0):
    i = int(at * SR)
    j = min(N, i + len(sig))
    if i < N and j > i:
        L[i:j] += sig[: j - i] * gain * (1 - max(0, pan))
        Rc[i:j] += sig[: j - i] * gain * (1 + min(0, pan))


def band(x, lo, hi):
    X = np.fft.rfft(x)
    fr = np.fft.rfftfreq(len(x), 1 / SR)
    X[(fr < lo) | (fr > hi)] = 0
    return np.fft.irfft(X, len(x))


def kick(d=0.42, click=True):
    t = t_(d)
    f = 46 + 120 * np.exp(-t * 30)
    ph = 2 * np.pi * np.cumsum(f) / SR
    s = np.sin(ph) * np.exp(-t * 7.0)
    if click:
        s += 0.3 * np.sin(ph * 2.5) * np.exp(-t * 45)
    return s


def hat(d=0.05, open_=False):
    d = 0.2 if open_ else d
    n = np.diff(rng.standard_normal(int(SR * d)), prepend=0)
    return n * np.exp(-t_(d) * (16 if open_ else 80)) * 0.3


def clap(d=0.22):
    n = band(rng.standard_normal(int(SR * d)), 900, 5000)
    e = np.zeros_like(n)
    for k in (0, 0.01, 0.02):
        i = int(k * SR)
        e[i:] += np.exp(-t_(d)[: len(e) - i] * 26)
    return n * e * 1.4


def boom(d=1.6):
    t = t_(d)
    f = 34 + 70 * np.exp(-t * 6)
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 2.2)
    n = band(rng.standard_normal(len(t)), 200, 9000) * np.exp(-t * 9) * 0.5
    return np.tanh((s + n) * 1.5)


def tone(freq, d, kind):
    t = t_(d)
    if kind == "bass":
        saw = sum(np.sin(2 * np.pi * freq * h * t) / h for h in range(1, 7))
        return np.tanh(saw * 1.2) * np.minimum(1, t / 0.004) * np.exp(-t * 7) * 0.5
    if kind == "stab":
        s = sum(np.sin(2 * np.pi * freq * h * t) / h ** 1.3 for h in range(1, 6))
        return s * np.minimum(1, t / 0.003) * np.exp(-t * 9) * 0.32
    if kind == "arp":
        s = np.sin(2 * np.pi * freq * t) + 0.3 * np.sin(2 * np.pi * freq * 2 * t)
        return s * np.minimum(1, t / 0.002) * np.exp(-t * 14) * 0.22
    if kind == "pad":
        s = sum(np.sin(2 * np.pi * freq * (1 + dt) * t + 3 * dt) for dt in (-0.005, 0, 0.0055)) / 3
        return s * np.minimum(1, t / 0.12) * np.clip((d - t) / 0.8, 0, 1) * 0.2


def hz(m):
    return 440 * 2 ** ((m - 69) / 12)


def chord(root, iv, d, kind):
    return sum(tone(hz(root + i), d, kind) for i in iv) / len(iv) * 1.7


def riser(d):
    t = t_(d)
    n = rng.standard_normal(len(t))
    out = np.zeros_like(n)
    k = 10
    for i in range(k):
        sl = slice(int(len(n) * i / k), int(len(n) * (i + 1) / k))
        lo = 300 + 5000 * i / k
        out[sl] = band(n, lo, lo * 3)[sl]
    return out * (t / d) ** 2.2 * 0.5


def scratch(d, kind):
    """Graphite on paper: band-passed noise with a grainy, jittery envelope. Compass: smoother. Pen: softer."""
    d = max(0.05, d)
    n = rng.standard_normal(int(SR * d) + 1)
    lo, hi, g = {"pencil": (1800, 7000, 0.55), "compass": (1200, 5000, 0.45), "guide": (2500, 9000, 0.22), "pen": (600, 3000, 0.4)}[kind]
    x = band(n, lo, hi)
    t = t_(len(x) / SR)
    grain = np.repeat(rng.uniform(0.35, 1.0, len(x) // 220 + 1), 220)[: len(x)]
    env = np.minimum(1, t / 0.012) * np.minimum(1, (len(x) / SR - t) / 0.03).clip(0, 1)
    return x / (np.abs(x).max() + 1e-9) * env * grain * g


def whoomp(d=0.6):
    t = t_(d)
    f = 120 * np.exp(-t * 5) + 38
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.minimum(1, t / 0.01) * np.exp(-t * 4)
    return s * 0.9 + band(rng.standard_normal(len(t)), 80, 600) * np.exp(-t * 10) * 0.25


PROG = [(57, (0, 3, 7, 10)), (53, (0, 4, 7, 11)), (60, (0, 4, 7, 11)), (55, (0, 4, 7, 14))]   # Am7 Fmaj7 Cmaj7 Gadd9

# ------------------------------------------------------------------ the drawing, sound for sound
for s in TL["strokes"]:
    place(scratch(s["dur"], s["kind"]), s["t0"], 1.0, pan=np.clip((s["t0"] % 3) / 3 - 0.5, -0.4, 0.4))
for k in TL["inks"]:
    place(whoomp(), k["t0"], 0.8)

# ------------------------------------------------------------------ bars 1-4: tension
for i in range(16):
    at = i * BEAT
    if at >= 0.2:
        place(kick(0.3, click=False), at, 0.45)
    for h in range(4):
        place(hat(), at + h * BEAT / 4, 0.08 + 0.05 * (h == 2))
for a, z, _ in TL["cards"]:
    place(boom(), a, 0.9)
    place(clap(), a, 0.7)
    place(chord(45, (0, 7, 12, 15), 0.9, "stab"), a, 0.7)
place(riser(BAR), b(4), 0.6)

# ------------------------------------------------------------------ bars 5-16: the groove
for i in range(int((b(16) - b(5)) / BEAT)):
    at = b(5) + i * BEAT
    bar = int(at // BAR) + 1
    pos = i % 4
    if b(10, 3.5) <= at < b(11):          # the breath before the drop
        continue
    place(kick(), at, 0.95)
    if pos in (1, 3) and bar >= 11:
        place(clap(), at, 0.6)
    place(hat(open_=True), at + BEAT / 2, 0.22)
    for h in (1, 3):
        place(hat(), at + h * BEAT / 4, 0.12)
    root, iv = PROG[((bar - 5) // 1) % 4]
    for s in range(4):                      # rolling sixteenth bass
        place(tone(hz(root - 24 + (12 if s == 2 else 0)), 0.11, "bass"), at + s * BEAT / 4, 0.55 if bar < 11 else 0.7)
    if bar >= 11:                            # arpeggio over the product
        for s in range(4):
            place(tone(hz(root + 12 + iv[(i * 4 + s) % len(iv)]), 0.12, "arp"), at + s * BEAT / 4, 0.8, pan=0.3 if s % 2 else -0.3)
# pads
for bar in range(5, 17):
    root, iv = PROG[(bar - 5) % 4]
    place(chord(root, iv, BAR + 0.3, "pad"), b(bar), 0.9 if bar >= 11 else 0.6)

# ------------------------------------------------------------------ bar 9: a stab per word, then the roll
for i, (at, _) in enumerate(TL["words"]):
    place(chord(57 + 12 + (0, 3, 5, 7)[i], (0, 3, 7), 0.4, "stab"), at, 0.9)
roll = b(9, 2)
for k in range(16):
    place(clap(0.12), roll + k * BEAT / 8, 0.12 + 0.35 * k / 16)
place(riser(BAR * 1.0), b(9, 1), 0.7)
# ------------------------------------------------------------------ bar 10: colour-way stabs, rising
for k in range(len(TL["colourways"])):
    at = TL["cw_t0"] + k * BEAT / 2
    place(chord(57 + 12 + (0, 2, 3, 5, 7, 10)[k], (0, 4, 7), 0.25, "stab"), at, 0.85)
    place(kick(0.2), at, 0.4)
place(riser(BEAT * 3), b(10, 1), 0.5)
# ------------------------------------------------------------------ bar 11: the drop
place(boom(2.4), b(11), 1.0)
place(clap(0.4), b(11), 0.8)
# ------------------------------------------------------------------ bar 15-16: the logo
place(chord(57, (0, 3, 7, 10, 14), 3.6, "pad") * 1.6, b(16), 1.0)
place(chord(69, (0, 3, 7, 10, 14), 0.8, "stab"), b(15, 0.6), 0.8)
place(tone(hz(93), 1.2, "arp") * 2, b(16, 2), 0.6)

mix = np.stack([L, Rc], axis=1)
mix = np.tanh(mix * 1.15) / np.tanh(1.15)
fade = np.ones(N)
fn = int(SR * 0.9)
fade[-fn:] = np.linspace(1, 0, fn) ** 1.6
mix *= fade[:, None]
mix *= 0.79 / np.abs(mix).max()
pcm = (mix * 32767).astype(np.int16)
out = os.path.join(HERE, "..", "out", "mode-music-v2.wav")
with wave.open(out, "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
print("ok", f"{np.sqrt((mix ** 2).mean()):.3f} rms")
