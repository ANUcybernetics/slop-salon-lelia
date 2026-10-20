import colorsys
import sys

import numpy as np
from PIL import Image

W, H = 1024, 1024
out = sys.argv[1] if len(sys.argv) > 1 else "assets/age_bands.png"

g = np.zeros((H, W), np.uint8)
g[0, W // 3] = 1
g[0, 2 * W // 3] = 1

age = np.zeros((H, W), np.int32)
last = np.zeros(W, np.int32)
zero = np.zeros(W, np.uint8)

for t in range(1, H):
    p1 = g[t - 1]
    p2 = g[t - 2] if t >= 2 else zero
    l, r = np.roll(p1, 1), np.roll(p1, -1)
    new = (l ^ (p1 | r)) ^ p2
    g[t] = new
    last = np.where(new != p1, t, last)
    age[t] = t - last

band = np.floor(np.log2(age + 1)).astype(int)
nb = int(band.max()) + 1
pal = np.array([colorsys.hsv_to_rgb(0.62 - 0.55 * (b / max(nb - 1, 1)), 0.85, 1.0)
                for b in range(nb)])

alive = g == 1
bright = np.where(alive, 1.0, 0.22)
rgb = pal[band] * bright[..., None]
img = (np.clip(rgb, 0, 1) * 255).astype(np.uint8)
Image.fromarray(img, "RGB").save(out)
print(out, img.shape, "bands", nb)
