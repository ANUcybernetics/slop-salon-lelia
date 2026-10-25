import sys
from collections import Counter

import numpy as np

W = int(sys.argv[3]) if len(sys.argv) > 3 else 1024
H = 1024
START = int(sys.argv[4]) if len(sys.argv) > 4 else 256
K = int(sys.argv[5]) if len(sys.argv) > 5 else 31
CEIL = 254
RULE = 54
SEEDS = tuple(int(v) for v in sys.argv[1].split(",")) if len(sys.argv) > 1 else (W // 3, 2 * W // 3)
RNG = np.random.default_rng(0)


def still_mask(shift=1):
    table = np.array([(RULE >> i) & 1 for i in range(8)], np.uint8)
    g = np.zeros((H, W), np.uint8)
    for s in SEEDS:
        g[0, s] = 1
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


m = still_mask(int(sys.argv[2]) if len(sys.argv) > 2 else 1)
rows, xs = np.nonzero(m)
rows = rows + START
print("still cells", len(rows), "distinct x", len(set(xs.tolist())))

# an end: still at row t, not still at (t+1, x); last row has no successor, so skip it
last_row = H - 1
ends = [(r, x) for r, x in zip(rows, xs) if r < last_row and not m[r - START + 1, x]]
print("column ends (rows %d-1022):" % START, len(ends))
er = np.array([e[0] for e in ends])
ex = np.array([e[1] for e in ends])

row_counts = Counter(er.tolist())
print("most ends on one row:", row_counts.most_common(5))
print("rows with any end:", len(row_counts))


def diag_max(r, x, slopes=range(-3, 4)):
    best = (0, None)
    for s in slopes:
        d = Counter((x - s * r).tolist())
        top = d.most_common(1)[0]
        if top[1] > best[0]:
            best = (top[1], (s, top[0]))
    return best


print("best diagonal x - s*row (count, (s, offset)):", diag_max(er, ex))

# null: shuffle end rows against x, keep the same multiset of ends per x
null_row_max, null_diag_max = [], []
for _ in range(200):
    shuffled = RNG.permutation(er)
    null_row_max.append(Counter(shuffled.tolist()).most_common(1)[0][1])
    null_diag_max.append(diag_max(shuffled, ex)[0])
print("null max ends per row: mean %.1f, 95th %d" % (np.mean(null_row_max), np.percentile(null_row_max, 95)))
print("null max diagonal count: mean %.1f, 95th %d" % (np.mean(null_diag_max), np.percentile(null_diag_max, 95)))
