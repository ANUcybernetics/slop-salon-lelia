import sys

import numpy as np

RULE = int(sys.argv[1]) if len(sys.argv) > 1 else 42
SEEDS = [341, 682]
W, H = 1024, 1024
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

print(f"rule {RULE}, seeds {SEEDS}")
for lo, hi in [(256, 512), (512, 768), (768, 1024)]:
    rows = range(lo, hi)
    still = np.zeros((hi - lo, W), bool)
    changing = np.zeros((hi - lo, W), bool)
    p2 = np.zeros((hi - lo, W), bool)
    for i, t in enumerate(rows):
        still[i] = (age[t] >= 31) & (age[t] < 255)
        changing[i] = g[t] != g[t - 1]
        p2[i] = g[t] == g[t - 2]
    alive_all = g[lo:hi].mean()
    n_still = still.sum()
    n_chg = changing.sum()
    p2_all = p2.mean()
    p2_chg = (p2 & changing).sum() / max(n_chg, 1)
    print(f"rows {lo}-{hi}: all-cell period-2 {p2_all:.3f} | still cells {n_still} "
          f"(period-2 by construction) | changing cells {n_chg}, period-2 among them {p2_chg:.3f} "
          f"| alive {alive_all:.3f}")

still_mid = np.zeros(W, bool)
for t in range(512, 513):
    still_mid = (age[t] >= 31) & (age[t] < 255)
drifted = (g[512:1024][:, still_mid] != g[512][still_mid]).any(axis=0)
print(f"cells still at row 512 (age 31-254): {int(still_mid.sum())}; "
      f"changed again by row 1023: {int(drifted.sum())}")

for lo, hi in [(256, 512), (512, 768), (768, 1024)]:
    seg = g[lo:hi]
    dead = (seg == 0).mean()
    print(f"rows {lo}-{hi}: dead share {dead:.3f}")
