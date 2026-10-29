import sys

import numpy as np
from PIL import Image

RULE = int(sys.argv[1]) if len(sys.argv) > 1 else 42
OUT = sys.argv[2] if len(sys.argv) > 2 else f"assets/rule_{RULE}_p2_spacetime.png"
SEEDS = [341, 682]
W, H = 1024, 1024
LO = 256
table = np.array([(RULE >> i) & 1 for i in range(8)], np.uint8)

g = np.zeros((H, W), np.uint8)
for s in SEEDS:
    g[0, s] = 1
age = np.zeros((H, W), np.int32)
last = np.zeros(W, np.int32)
for t in range(1, H):
    p1 = g[t - 1]
    new = table[(np.roll(p1, 1) << 2) | (p1 << 1) | np.roll(p1, -1)]
    if t >= 2:
        new = new ^ g[t - 2]
    g[t] = new
    last = np.where(new != p1, t, last)
    age[t] = t - last

rows = slice(LO, H)
g_r, p_r = g[rows], g[LO - 1:H - 1]
changed = g_r != p_r
p2 = g_r == g[LO - 2:H - 2]
flicker = changed & p2
other = changed & ~p2
still = (age[rows] >= 31) & (age[rows] < 255) & ~changed

print(f"rule {RULE}, rows {LO}-{H}: changes {int(changed.sum())}, "
      f"period-2 {int(flicker.sum())} ({flicker.sum() / changed.sum():.3f}), "
      f"other {int(other.sum())}, still (31-254) {int(still.sum())}")

img = np.zeros((H - LO, W, 3), np.uint8)
img[still] = (70, 70, 80)
img[flicker] = (80, 200, 220)
img[other] = (245, 190, 60)
img[(g_r == 1) & ~changed & ~still] = (235, 235, 235)
Image.fromarray(img, "RGB").save(OUT)
print(OUT, img.shape)
