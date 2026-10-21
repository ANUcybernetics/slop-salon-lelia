import sys
import numpy as np

SEEDS = [int(x) for x in sys.argv[1].split(",")]
RULE = int(sys.argv[2]) if len(sys.argv) > 2 else 54
DEPTH, SHIFT = 2, 1
W = H = 1024

table = np.array([(RULE >> i) & 1 for i in range(8)], np.uint8)
g = np.zeros((H, W), np.uint8)
for s in SEEDS:
    g[0, s] = 1
age = np.zeros((H, W), np.int32)
last = np.zeros(W, np.int32)
zero = np.zeros(W, np.uint8)
for t in range(1, H):
    p1 = g[t - 1]
    l, c, r = np.roll(p1, 1), p1, np.roll(p1, -1)
    new = table[(l << 2) | (c << 1) | r]
    for k in range(2, DEPTH + 1):
        new = new ^ (g[t - k] if t >= k else zero)
    if SHIFT:
        new = new ^ np.roll(p1, SHIFT)
    g[t] = new
    last = np.where(new != p1, t, last)
    age[t] = t - last

def still(row):
    return (g[row] == 0) & (age[row] >= 31) & (age[row] < 255)

hits = sum(int(still(r).sum()) for r in range(256, H))
cols = set()
for r in range(256, H):
    cols.update(np.flatnonzero(still(r)).tolist())
u = np.array(sorted(cols))
print(f"seeds={SEEDS} hits={hits} distinct={u.size} odd={int((u%2==1).sum())} even={int((u%2==0).sum())}")
print("  row900 still:", np.flatnonzero(still(900)).tolist())
