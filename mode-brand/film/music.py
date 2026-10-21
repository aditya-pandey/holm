"""Original 30 s track for the MODE film, synthesised from scratch (no samples, nothing to license).
120 BPM, so every cut in the film lands on a beat: one beat = 0.5 s, one bar = 2 s.

  0-8 s   letters: kick + soft hats + a plucked note per letter, a 'drop' at 0.5 s
  8-10 s  assembly: riser into the downbeat
 10-20 s  the modes: full groove, bass, chord stabs, a tint 'whoosh' every 2 s
 20-24 s  fold, squeeze, pour: three hits
 24-30 s  range + end card: groove thins out, last chord rings to the end
"""
import wave
import numpy as np

SR = 48000
DUR = 30.0
BEAT = 0.5
N = int(SR * DUR)
rng = np.random.default_rng(7)


def t_(d):
    return np.arange(int(SR * d)) / SR


def env(d, a=0.003, r=None):
    t = t_(d)
    r = r or d
    e = np.minimum(1, t / a) * np.exp(-t / (r / 4))
    return e


def place(buf, sig, at, gain=1.0):
    i = int(at * SR)
    j = min(N, i + len(sig))
    if i < N:
        buf[i:j] += sig[: j - i] * gain


def kick(d=0.45):
    t = t_(d)
    f = 48 + 110 * np.exp(-t * 28)
    ph = 2 * np.pi * np.cumsum(f) / SR
    return np.sin(ph) * np.exp(-t * 7.5) + 0.25 * np.sin(ph * 2) * np.exp(-t * 30)


def hat(d=0.06, open_=False):
    d = 0.22 if open_ else d
    n = rng.standard_normal(int(SR * d))
    n = np.diff(n, prepend=0)                       # tilt the noise bright
    return n * np.exp(-t_(d) * (14 if open_ else 70)) * 0.35


def clap(d=0.25):
    n = rng.standard_normal(int(SR * d))
    n = np.convolve(n, np.ones(6) / 6, "same") - np.convolve(n, np.ones(40) / 40, "same")
    e = np.zeros_like(n)
    for k in (0, 0.011, 0.022):
        i = int(k * SR)
        e[i:] += np.exp(-t_(d)[: len(e) - i] * 28)
    return n * e * 0.6


def note(freq, d, kind="pluck"):
    t = t_(d)
    if kind == "pluck":
        s = sum(np.sin(2 * np.pi * freq * h * t) / h ** 1.6 for h in (1, 2, 3, 4))
        return s * env(d, 0.002, d * 0.9) * 0.5
    if kind == "bass":
        s = np.sin(2 * np.pi * freq * t) + 0.35 * np.sin(2 * np.pi * freq * 2 * t)
        s = np.tanh(s * 1.6)
        return s * np.minimum(1, t / 0.005) * np.exp(-t * 3.2) * 0.55
    if kind == "pad":
        s = sum(np.sin(2 * np.pi * freq * (1 + dt) * t) for dt in (-0.004, 0, 0.0045)) / 3
        a = np.minimum(1, t / 0.08) * np.minimum(1, (d - t) / 0.6).clip(0, 1)
        return s * a * 0.22
    if kind == "stab":
        s = sum(np.sign(np.sin(2 * np.pi * freq * (1 + dt) * t)) for dt in (-0.006, 0.006)) / 2
        s = np.convolve(s, np.ones(18) / 18, "same")            # soften the square wave
        return s * env(d, 0.002, 0.5) * 0.16


def chord(root_midi, quality, d, kind):
    iv = {"m7": (0, 3, 7, 10), "M7": (0, 4, 7, 11), "m9": (0, 3, 7, 10, 14), "add9": (0, 4, 7, 14)}[quality]
    return sum(note(440 * 2 ** ((root_midi + i - 69) / 12), d, kind) for i in iv) / len(iv) * 1.6


def whoosh(d=0.9):
    n = rng.standard_normal(int(SR * d))
    t = t_(d)
    # rising band: progressively less smoothing
    out = np.zeros_like(n)
    for k, w in enumerate(np.linspace(60, 4, 8)):
        seg = slice(int(len(n) * k / 8), int(len(n) * (k + 1) / 8))
        out[seg] = (n - np.convolve(n, np.ones(int(w)) / int(w), "same"))[seg]
    return out * (t / d) ** 2 * 0.25


def drop():
    t = t_(0.5)
    f = 1400 * np.exp(-t * 9) + 300
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 9) * 0.5


L = np.zeros(N)
R = np.zeros(N)

# progression (2 bars each): Am7 · Fmaj7 · Cmaj7 · G(add9)  in MIDI roots
PROG = [(57, "m7"), (53, "M7"), (48, "M7"), (55, "add9")]

beats = np.arange(0, DUR, BEAT)
for b in beats:
    bar_pos = int(round(b / BEAT)) % 4
    if b < 8:                                   # intro: kick on 1 and 3, soft hats
        if bar_pos in (0, 2) and b >= 0.5:
            place(L, kick(), b, 0.7); place(R, kick(), b, 0.7)
        place(L, hat(), b + 0.25, 0.25); place(R, hat(), b + 0.25, 0.35)
    elif b < 10:                                # assembly: four on the floor, building
        place(L, kick(), b, 0.8); place(R, kick(), b, 0.8)
        for k in (0, 0.25):
            place(L, hat(), b + k, 0.3); place(R, hat(), b + k, 0.38)
    elif b < 24:                                # modes + ritual: full groove
        place(L, kick(), b, 0.9); place(R, kick(), b, 0.9)
        if bar_pos in (1, 3):
            place(L, clap(), b, 0.55); place(R, clap(), b, 0.6)
        for k in (0, 0.25):
            place(L, hat(open_=(k == 0.25 and bar_pos == 3)), b + k, 0.32)
            place(R, hat(open_=(k == 0.25 and bar_pos == 3)), b + k, 0.4)
    elif b < 28:                                # range: half time
        if bar_pos == 0:
            place(L, kick(), b, 0.75); place(R, kick(), b, 0.75)
        if bar_pos == 2:
            place(L, clap(), b, 0.4); place(R, clap(), b, 0.45)
        place(L, hat(), b + 0.25, 0.22); place(R, hat(), b + 0.25, 0.3)

# the drop that becomes the m
place(L, drop(), 0.5, 0.9); place(R, drop(), 0.5, 0.9)
# one plucked note per letter (A, C, E, G) as each letter lands
for at, m in ((0.5, 69), (2.5, 72), (4.5, 76), (6.5, 79)):
    s = note(440 * 2 ** ((m - 69) / 12), 1.4, "pluck")
    place(L, s, at, 0.9); place(R, s, at + 0.012, 0.9)
# pads under the whole film
for i, at in enumerate(np.arange(0, 30, 4.0)):
    root, q = PROG[i % 4]
    p = chord(root, q, 4.2, "pad")
    place(L, p, at, 0.9 if at >= 8 else 0.55); place(R, p, at + 0.008, 0.9 if at >= 8 else 0.55)
# bass + stabs in the groove
for i, at in enumerate(np.arange(8, 28, 2.0)):
    root, q = PROG[(i // 1) % 4]
    for k, off in enumerate((0, 0.75, 1.0, 1.5)):
        if at + off < 28:
            bs = note(440 * 2 ** ((root - 12 - 69) / 12), 0.42, "bass")
            place(L, bs, at + off, 0.8); place(R, bs, at + off, 0.8)
    if 10 <= at < 24:
        st = chord(root + 12, q, 0.5, "stab")
        place(L, st, at + 0.5, 0.9); place(R, st, at + 0.75, 0.9)
# whooshes into each mode wipe (10, 12, 14, 16, 18) and into the ritual and end card
for at in (10, 12, 14, 16, 18, 20, 27):
    w = whoosh(0.9)
    place(L, w, at - 0.9, 0.8); place(R, w, at - 0.9, 0.8)
# riser into the assembly
w = whoosh(1.9); place(L, w, 6.1, 0.9); place(R, w, 6.1, 0.9)
# fold / squeeze / pour hits
for at in (20.0, 21.333, 22.667):
    place(L, kick(0.3), at, 0.5); place(R, kick(0.3), at, 0.5)
    s = note(440 * 2 ** ((81 - 69) / 12), 0.6, "pluck"); place(L, s, at, 0.6); place(R, s, at, 0.6)
# end chord: rings out
end = chord(57 + 12, "m9", 3.0, "pad") * 1.8 + chord(57, "m9", 3.0, "pluck") * 0.8
place(L, end, 27.0, 1.0); place(R, end, 27.01, 1.0)

mix = np.stack([L, R], axis=1)
mix = np.tanh(mix * 1.2) / np.tanh(1.2)                       # gentle glue
fade = np.ones(N); fn = int(SR * 1.2); fade[-fn:] = np.linspace(1, 0, fn) ** 1.5
mix *= fade[:, None]
mix *= 0.79 / np.abs(mix).max()          # peak about -2 dB: headroom for AAC and platform re-encodes
pcm = (mix * 32767).astype(np.int16)
with wave.open("film/out/mode-music.wav", "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
print("ok", pcm.shape, f"{np.sqrt((mix ** 2).mean()):.3f} rms")
