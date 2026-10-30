import sys

import numpy as np
from PIL import Image

RULE = int(sys.argv[1]) if len(sys.argv) > 1 else 234
OUT = sys.argv[2] if len(sys.argv) > 2 else "assets/rule_234_flicker.png"
NEAR = 3
RUN = 32
SEEDS = [341, 682]
W, H = 1024, 1024
FAR = 16
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

run = np.zeros((H, W), np.int32)
for t in range(2, H):
    run[t] = np.where(g[t] == g[t - 2], run[t - 1] + 1, 0)


def near(mask, d):
    out = np.zeros_like(mask)
    for k in range(-d, d + 1):
        out |= np.roll(mask, k, axis=-1)
    return out


img = np.zeros((H, W, 3), np.uint8)
img[:] = (18, 18, 22)
still = (age >= 31) & (age < 255)
img[still] = (70, 74, 84)
changed = np.zeros((H, W), bool)
changed[1:] = g[1:] != g[:-1]
in_run = changed & (run >= RUN)
other = changed & ~in_run
img[other] = (200, 196, 180)
img[in_run] = (240, 150, 60)
Image.fromarray(img).save(OUT)

edge_mask = np.zeros((H, W), bool)
for t in range(256, H):
    edge_mask[t] = near(still[t], NEAR)
print(f"rule {RULE}, seeds {SEEDS}, ring {W}, rows 0-{H - 1}")
print(f"changing cells in period-2 run of {RUN}+ rows: {in_run[256:].sum()} of {changed[256:].sum()} (rows 256+)")
print(f"edge cells (within {NEAR} of still) in run: {(in_run & edge_mask)[256:].sum()} of {(changed & edge_mask)[256:].sum()}")
print(f"wrote {OUT}")
