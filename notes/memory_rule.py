import sys

import numpy as np
from PIL import Image

W, H = 1024, 1024
out = sys.argv[1] if len(sys.argv) > 1 else "assets/memory_rule.png"

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

alive = g == 1
a = np.clip(age / 40.0, 0, 1)
r = np.where(alive, 0.95 - 0.2 * a, 0.02)
gr = np.where(alive, 0.55 - 0.45 * a, 0.02)
b = np.where(alive, 0.25 + 0.6 * a, 0.04)
img = np.stack([r, gr, b], axis=-1)
img = (np.clip(img, 0, 1) * 255).astype(np.uint8)
Image.fromarray(img, "RGB").save(out)
print(out, img.shape)
