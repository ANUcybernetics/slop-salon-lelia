import sys

import numpy as np
from PIL import Image

OUT = sys.argv[1] if len(sys.argv) > 1 else "assets/rule54_still_cells.png"
W, H = 1024, 1024
START, K, CEIL = 256, 31, 254
RULE = 54


def still_cells(shift):
    table = np.array([(RULE >> i) & 1 for i in range(8)], np.uint8)
    g = np.zeros((H, W), np.uint8)
    g[0, W // 3] = 1
    g[0, 2 * W // 3] = 1
    age = np.zeros((H, W), np.int32)
    last = np.zeros(W, np.int32)
    zero = np.zeros(W, np.uint8)
    for t in range(1, H):
        p1 = g[t - 1]
        idx = (np.roll(p1, 1) << 2) | (p1 << 1) | np.roll(p1, -1)
        new = table[idx] ^ (g[t - 2] if t >= 2 else zero)
        if shift:
            new = new ^ np.roll(p1, shift)
        g[t] = new
        last = np.where(new != p1, t, last)
        age[t] = t - last
    return (age[START:] >= K) & (age[START:] <= CEIL)


panels = []
for s in (0, 1):
    m = still_cells(s)
    print("shift", s, "still cells", int(m.sum()))
    panels.append(m)

gap = np.zeros((H - START, 16), bool)
both = np.concatenate([panels[0], gap, panels[1]], axis=1)
img = np.zeros(both.shape + (3,), np.uint8)
img[both] = (255, 60, 60)
Image.fromarray(img, "RGB").save(OUT)
print(OUT, img.shape)
