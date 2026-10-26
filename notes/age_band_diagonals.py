import sys
from collections import Counter

import numpy as np

SEED = int(sys.argv[1]) if len(sys.argv) > 1 else 341
K = int(sys.argv[2]) if len(sys.argv) > 2 else 33
BANDS = [int(v) for v in sys.argv[3].split(",")] if len(sys.argv) > 3 else [33, 39, 45, 51, 57, 81, 195]
W, H, START, CEIL, RULE, SHIFT = 1024, 1024, 256, 254, 54, 1
TABLE = np.array([(RULE >> i) & 1 for i in range(8)], np.uint8)
RNG = np.random.default_rng(0)


def run():
    g = np.zeros((H, W), np.uint8)
    g[0, SEED] = 1
    age = np.zeros((H, W), np.int32)
    last = np.zeros(W, np.int32)
    zero = np.zeros(W, np.uint8)
    for t in range(1, H):
        p1 = g[t - 1]
        idx = (np.roll(p1, 1) << 2) | (p1 << 1) | np.roll(p1, -1)
        new = TABLE[idx] ^ (g[t - 2] if t >= 2 else zero) ^ np.roll(p1, SHIFT)
        g[t] = new
        last = np.where(new != p1, t, last)
        age[t] = t - last
    return age


age = run()
mask = (age >= K) & (age <= CEIL)
mask[:START] = False
rows, xs = np.nonzero(mask)
ends = [(int(r), int(x)) for r, x in zip(rows, xs) if r < H - 1 and not mask[r + 1, x]]
er = np.array([e[0] for e in ends])
ex = np.array([e[1] for e in ends])
ea = np.array([int(age[r, x]) for r, x in ends])
print("seed %d, K %d: ends %d" % (SEED, K, len(ends)))


def diag_best(r, x):
    best = (0, None, None)
    for s in range(-3, 4):
        top = Counter(((x - s * r) % W).tolist()).most_common(1)[0]
        if top[1] > best[0]:
            best = (top[1], s, top[0])
    return best


print("age  ends  best(count, slope, x-s*row mod W)  null mean, 95th")
for a in BANDS:
    sel = ea == a
    n = int(sel.sum())
    if n == 0:
        print("%3d  %4d  -" % (a, n))
        continue
    r, x = er[sel], ex[sel]
    cnt, s, off = diag_best(r, x)
    null = [diag_best(RNG.permutation(r), x)[0] for _ in range(200)]
    print("%3d  %4d  %3d, s=%d, offset %4d        %.1f, %d" % (a, n, cnt, s, off, np.mean(null), np.percentile(null, 95)))
