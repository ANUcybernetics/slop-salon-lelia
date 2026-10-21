import sys
import numpy as np

SEED = int(sys.argv[1])
W = H = 1024
DEPTH, SHIFT = 2, 1
zero = np.zeros(W, np.uint8)

def run(rule):
    table = np.array([(rule >> i) & 1 for i in range(8)], np.uint8)
    g = np.zeros((H, W), np.uint8)
    g[0, SEED] = 1
    age = np.zeros((H, W), np.int32)
    last = np.zeros(W, np.int32)
    for t in range(1, H):
        p1 = g[t - 1]
        new = table[(np.roll(p1, 1) << 2) | (p1 << 1) | np.roll(p1, -1)]
        for k in range(2, DEPTH + 1):
            new = new ^ (g[t - k] if t >= k else zero)
        new = new ^ np.roll(p1, SHIFT)
        g[t] = new
        last = np.where(new != p1, t, last)
        age[t] = t - last
    m = (g[256:] == 0) & (age[256:] >= 31) & (age[256:] < 255)
    cols = np.unique(np.flatnonzero(m.any(axis=0)))
    odd = int(((cols - SEED) % 2 == 1).sum())
    return cols.size, odd

for rule in range(256):
    n, odd = run(rule)
    if n:
        print(f"rule={rule} cols={n} odd_offset={odd}")
