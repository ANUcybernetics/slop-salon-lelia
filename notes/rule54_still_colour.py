import sys

import numpy as np
from PIL import Image

RULE = int(sys.argv[1]) if len(sys.argv) > 1 else 54
out = sys.argv[2] if len(sys.argv) > 2 else f"assets/rule_{RULE}_still_fixed.png"
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
    new = table[idx] ^ (g[t - 2] if t >= 2 else zero)
    g[t] = new
    last = np.where(new != p1, t, last)
    age[t] = t - last

alive = g == 1
still = (~alive) & (age >= 31) & (age < 255)
img = np.zeros((H, W, 3), np.float32)
img[alive] = (0.15, 0.25, 0.55)
img[~alive] = (0.05, 0.05, 0.08)
img[still] = (1.0, 0.85, 0.1)
Image.fromarray((img * 255).astype(np.uint8), "RGB").save(out)
print(out, "still cells", int(still[256:].sum()))
