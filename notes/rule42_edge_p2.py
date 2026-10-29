import sys

import numpy as np

RULE = int(sys.argv[1]) if len(sys.argv) > 1 else 42
SEEDS = [341, 682]
W, H = 1024, 1024
NEAR = 3
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


def near(mask, d):
    out = np.zeros_like(mask)
    for k in range(-d, d + 1):
        out |= np.roll(mask, k, axis=-1)
    return out


print(f"rule {RULE}, seeds {SEEDS}, edge = changing within {NEAR} columns of a still cell (age 31-254), "
      f"far = no still cell within {FAR} columns")
print("block      edge changes  edge p2   far changes  far p2")
for lo in range(256, H, 64):
    hi = min(lo + 64, H)
    e_n = e_p2 = f_n = f_p2 = 0
    for t in range(lo, hi):
        still = (age[t] >= 31) & (age[t] < 255)
        changed = g[t] != g[t - 1]
        p2 = g[t] == g[t - 2]
        edge = changed & near(still, NEAR)
        far = changed & ~near(still, FAR)
        e_n += edge.sum()
        e_p2 += (edge & p2).sum()
        f_n += far.sum()
        f_p2 += (far & p2).sum()
    print(f"{lo:4d}-{hi:4d}  {e_n:12d}  {e_p2 / max(e_n, 1):7.3f}  {f_n:11d}  {f_p2 / max(f_n, 1):6.3f}")
