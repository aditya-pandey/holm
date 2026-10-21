"""Paper and film-grain textures for the film (numpy only)."""
import os
import numpy as np
from PIL import Image, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
rng = np.random.default_rng(3)


def blur_noise(h, w, scale):
    small = rng.standard_normal((max(2, h // scale), max(2, w // scale))).astype(np.float32)
    im = Image.fromarray(((small - small.min()) / (np.ptp(small) + 1e-6) * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC)
    return np.asarray(im, np.float32) / 255 - 0.5


def paper(w=2600, h=2000):
    base = np.array([241, 238, 231], np.float32)
    v = 0.06 * blur_noise(h, w, 220) + 0.035 * blur_noise(h, w, 40) + 0.02 * blur_noise(h, w, 6)
    fine = rng.standard_normal((h, w)).astype(np.float32) * 0.018
    lum = 1 + v + fine
    img = np.clip(base[None, None, :] * lum[..., None], 0, 255).astype(np.uint8)
    im = Image.fromarray(img)
    # fibres: short, faint strokes
    from PIL import ImageDraw
    d = ImageDraw.Draw(im, "RGBA")
    for _ in range(2600):
        x, y = rng.uniform(0, w), rng.uniform(0, h)
        a = rng.uniform(0, np.pi)
        L = rng.uniform(6, 28)
        c = int(rng.uniform(150, 215))
        d.line([(x, y), (x + np.cos(a) * L, y + np.sin(a) * L)], fill=(c, c - 4, c - 10, int(rng.uniform(10, 28))), width=1)
    im = im.filter(ImageFilter.GaussianBlur(0.6))
    im.save(os.path.join(HERE, "paper.jpg"), quality=90)


def grain(n=8, w=960, h=540):
    for i in range(n):
        g = rng.standard_normal((h, w)).astype(np.float32)
        a = np.clip(np.abs(g) * 22, 0, 60).astype(np.uint8)
        val = np.where(g > 0, 255, 0).astype(np.uint8)
        Image.fromarray(np.dstack([val, val, val, a]), "RGBA").save(os.path.join(HERE, f"grain{i}.png"))


paper()
grain()
print("ok")
