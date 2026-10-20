import colorsys
import sys

import numpy as np
from PIL import Image

RULE = int(sys.argv[1]) if len(sys.argv) > 1 else 110
out = sys.argv[2] if len(sys.argv) > 2 else f"assets/rule_{RULE}_bands.png"
DEPTH = int(sys.argv[3]) if len(sys.argv) > 3 else 2
W, H = 1024, 1024

table = np.array([(RULE >> i) & 1 for i in range(8)], np.uint8)

g = np.zeros((H, W), np.uint8)
g[0, W // 3] = 1
g[0, 2 * W // 3] = 1

age = np.zeros((H, W), np.int32)
last = np.zeros(W, np.int32)
zero = np.zeros(W, np.uint8)

for t in range(1, H):
    p1 = g[t - 1]
    l, c, r = np.roll(p1, 1), p1, np.roll(p1, -1)
    idx = (l << 2) | (c << 1) | r
    new = table[idx]
    for k in range(2, DEPTH + 1):
        new = new ^ (g[t - k] if t >= k else zero)
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
print(out, img.shape, "bands", nb, "alive", round(float(alive.mean()), 3))
