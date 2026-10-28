import colorsys
import sys

import numpy as np
from PIL import Image

RULE = int(sys.argv[1])
SEEDS = [tuple(int(x) for x in s.split("+")) for s in sys.argv[2].split(",")]
OUT = sys.argv[3]
DEPTH = 2
W, H = 1024, 1024

table = np.array([(RULE >> i) & 1 for i in range(8)], np.uint8)
zero = np.zeros(W, np.uint8)
tiles = []

for seed in SEEDS:
    g = np.zeros((H, W), np.uint8)
    for s in seed:
        g[0, s] = 1
    age = np.zeros((H, W), np.int32)
    last = np.zeros(W, np.int32)
    for t in range(1, H):
        p1 = g[t - 1]
        l, c, r = np.roll(p1, 1), p1, np.roll(p1, -1)
        new = table[(l << 2) | (c << 1) | r]
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
    img = (np.clip(pal[band] * bright[..., None], 0, 1) * 255).astype(np.uint8)
    dead_late = ~alive[256:]
    still = int((dead_late & (age[256:] >= 31) & (age[256:] < 255)).sum())
    print(seed, "bands", nb, "alive", round(float(alive.mean()), 3), "still past 256 excl 255+:", still)
    tiles.append(Image.fromarray(img, "RGB").resize((512, 512), Image.NEAREST))

mosaic = Image.new("RGB", (512 * len(tiles) + 8 * (len(tiles) - 1), 512), (0, 0, 0))
for i, t in enumerate(tiles):
    mosaic.paste(t, (i * 520, 0))
mosaic.save(OUT)
print(OUT)
