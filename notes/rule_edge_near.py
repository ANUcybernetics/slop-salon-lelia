import sys

import numpy as np

RULE = int(sys.argv[1]) if len(sys.argv) > 1 else 234
NEARS = [int(n) for n in sys.argv[2].split(",")] if len(sys.argv) > 2 else [1, 3, 6]
SEEDS = [341, 682]
W, H = 1024, 1024
FAR = 16
LO = 768
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


def near(mask, d):
    out = np.zeros_like(mask)
    for k in range(-d, d + 1):
        out |= np.roll(mask, k, axis=-1)
    return out


print(f"rule {RULE}, seeds {SEEDS}, rows {LO}-{H}, far = no still cell within {FAR} columns")
far_n = far_p2 = 0
for t in range(LO, H):
    still = (age[t] >= 31) & (age[t] < 255)
    changed = g[t] != g[t - 1]
    far = changed & ~near(still, FAR)
    far_n += far.sum()
    far_p2 += (far & (g[t] == g[t - 2])).sum()
print(f"far p2 {far_p2 / max(far_n, 1):.3f} ({far_n} changes)")
for d in NEARS:
    e_n = e_p2 = 0
    for t in range(LO, H):
        still = (age[t] >= 31) & (age[t] < 255)
        changed = g[t] != g[t - 1]
        edge = changed & near(still, d)
        e_n += edge.sum()
        e_p2 += (edge & (g[t] == g[t - 2])).sum()
    print(f"edge within {d} col: p2 {e_p2 / max(e_n, 1):.3f} ({e_n} changes)")
