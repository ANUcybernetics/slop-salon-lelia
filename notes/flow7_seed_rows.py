import sys
sys.path.insert(0, "/home/sprite/slop-salon-lelia/notes")
import numpy as np
from flow7_edge import lines

I, J = 2, 9
seed_row = np.arange(len(lines)) // 16
seed_col = np.arange(len(lines)) % 16
assert seed_row.max() == 15 and seed_col.max() == 15

hit = np.zeros(len(lines), bool)
for k, l in enumerate(lines):
    idx = np.unique(np.clip((l * 16).astype(int), 0, 15), axis=0)
    hit[k] = ((idx[:, 0] == I) & (idx[:, 1] == J)).any()

print("all seeds: lines through cell (i=%d, j=%d):" % (I, J), hit.sum())
print("per seed row j, lines through cell when row j is removed:")
for j in range(16):
    keep = seed_row != j
    print("  remove j=%2d: %3d   (seeds kept %d)" % (j, (hit & keep).sum(), keep.sum()))

band = [8, 9, 10]
keep = ~np.isin(seed_row, band)
print("remove band rows", band, ":", (hit & keep).sum(), "of", hit.sum(),
      " expected if no seed-row effect: %.1f" % (hit.sum() * keep.sum() / len(lines)))

rng = np.random.default_rng(0)
ctrl = []
for _ in range(200):
    rows = rng.choice(16, 3, replace=False)
    keep = ~np.isin(seed_row, rows)
    ctrl.append((hit & keep).sum())
print("random 3-row removals (200 draws): mean %.1f, min %d, max %d" % (np.mean(ctrl), min(ctrl), max(ctrl)))
