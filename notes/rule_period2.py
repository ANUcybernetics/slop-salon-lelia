import sys

import numpy as np

RULE = int(sys.argv[1]) if len(sys.argv) > 1 else 22
SEEDS = [341, 682]
W, H = 1024, 1024
table = np.array([(RULE >> i) & 1 for i in range(8)], np.uint8)

g = np.zeros((H, W), np.uint8)
for s in SEEDS:
    g[0, s] = 1
for t in range(1, H):
    p1 = g[t - 1]
    new = table[(np.roll(p1, 1) << 2) | (p1 << 1) | np.roll(p1, -1)]
    if t >= 2:
        new = new ^ g[t - 2]
    g[t] = new

for lo, hi in [(256, 512), (512, 768), (768, 1024)]:
    seg = g[lo:hi]
    print(f"rule {RULE} rows {lo}-{hi}: g[t]==g[t-2] {(seg[2:] == seg[:-2]).mean():.3f}, "
          f"g[t]==g[t-1] {(seg[1:] == seg[:-1]).mean():.3f}, alive {seg.mean():.3f}")
last = g[-1]
rep = [t for t in range(H - 512, H - 1) if (g[t] == last).all()]
print("exact repeats of last row in last 512 rows:", rep[:5])
