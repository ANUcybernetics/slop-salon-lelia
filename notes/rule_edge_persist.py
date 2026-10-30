import sys

import numpy as np

RULE = int(sys.argv[1]) if len(sys.argv) > 1 else 234
NEAR = int(sys.argv[2]) if len(sys.argv) > 2 else 3
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


def report(label, sel_fn):
    n = m2 = m4 = m24 = pat = 0
    for t in range(LO, H):
        still = (age[t] >= 31) & (age[t] < 255)
        changed = g[t] != g[t - 1]
        sel = sel_fn(still, changed, t)
        n += sel.sum()
        p2 = g[t] == g[t - 2]
        p4 = g[t] == g[t - 4]
        m2 += (sel & p2).sum()
        m4 += (sel & p4).sum()
        m24 += (sel & p2 & p4).sum()
        pat += (sel & p2 & (g[t - 1] == g[t - 3])).sum()
    print(
        f"{label}: changes {n}, t-2 {m2 / max(n, 1):.3f}, "
        f"t-4 {m4 / max(n, 1):.3f}, t-2 and t-4 {m24 / max(n, 1):.3f}, "
        f"period-2 over 4 rows {pat / max(n, 1):.3f}"
    )


print(f"rule {RULE}, seeds {SEEDS}, rows {LO}-{H}, edge within {NEAR} col, far no still within {FAR}")
report("edge", lambda still, changed, t: changed & near(still, NEAR))
report("far ", lambda still, changed, t: changed & ~near(still, FAR))

run = np.zeros((H, W), np.int32)
for t in range(2, H):
    run[t] = np.where(g[t] == g[t - 2], run[t - 1] + 1, 0)
for label, mask_fn in [
    ("edge", lambda still, changed: changed & near(still, NEAR)),
    ("far ", lambda still, changed: changed & ~near(still, FAR)),
]:
    n = long8 = long32 = 0
    for t in range(LO, H):
        still = (age[t] >= 31) & (age[t] < 255)
        sel = mask_fn(still, g[t] != g[t - 1])
        n += sel.sum()
        long8 += (sel & (run[t] >= 8)).sum()
        long32 += (sel & (run[t] >= 32)).sum()
    print(f"{label} run length: changes in a period-2 run of 8+ rows {long8 / max(n, 1):.3f}, 32+ rows {long32 / max(n, 1):.3f}")
