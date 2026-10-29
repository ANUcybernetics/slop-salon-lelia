import sys

import numpy as np

W, H = 1024, 1024
SEEDS = [int(s) for s in sys.argv[1].split("+")] if len(sys.argv) > 1 else [341, 682]
RULES = [int(r) for r in sys.argv[2].split(",")] if len(sys.argv) > 2 else range(256)
DEPTH, SHIFT = 2, 0
zero = np.zeros(W, np.uint8)


def run(rule):
    table = np.array([(rule >> i) & 1 for i in range(8)], np.uint8)
    g = np.zeros((H, W), np.uint8)
    for s in SEEDS:
        g[0, s] = 1
    age = np.zeros((H, W), np.int32)
    last = np.zeros(W, np.int32)
    for t in range(1, H):
        p1 = g[t - 1]
        new = table[(np.roll(p1, 1) << 2) | (p1 << 1) | np.roll(p1, -1)]
        for k in range(2, DEPTH + 1):
            new = new ^ (g[t - k] if t >= k else zero)
        if SHIFT:
            new = new ^ np.roll(p1, SHIFT)
        g[t] = new
        last = np.where(new != p1, t, last)
        age[t] = t - last
    still = int(((g[256:] == 0) & (age[256:] >= 31) & (age[256:] < 255)).sum())
    alive = float(g[-1].mean())
    return still, alive


rows = []
for rule in RULES:
    still, alive = run(rule)
    rows.append((rule, still, alive))

live = [r for r in rows if r[2] >= 0.01]
frozen = [r for r in rows if r[2] < 0.01]
print(f"seeds={SEEDS} depth={DEPTH} shift={SHIFT} rules={len(rows)} live={len(live)} frozen={len(frozen)}")
print("top live by still count:")
for rule, still, alive in sorted(live, key=lambda r: -r[1])[:15]:
    print(f"  rule={rule:3d} still={still:7d} alive={alive:.3f}")
print("top frozen by still count:")
for rule, still, alive in sorted(frozen, key=lambda r: -r[1])[:8]:
    print(f"  rule={rule:3d} still={still:7d} alive={alive:.3f}")
