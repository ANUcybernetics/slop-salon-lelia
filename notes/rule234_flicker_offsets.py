import sys

import numpy as np

RULE = int(sys.argv[1]) if len(sys.argv) > 1 else 234
TRIALS = 5000
SEEDS = [int(s) for s in sys.argv[2].split(",")] if len(sys.argv) > 2 else [341, 682]
W = int(sys.argv[3]) if len(sys.argv) > 3 else 1024
H = 1024
RUN = 32
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

run = np.zeros((H, W), np.int32)
for t in range(2, H):
    run[t] = np.where(g[t] == g[t - 2], run[t - 1] + 1, 0)

changed = np.zeros((H, W), bool)
changed[1:] = g[1:] != g[:-1]
in_run = (changed & (run >= RUN))[256:]
per_col = in_run.sum(axis=0)
cols = np.nonzero(per_col)[0]
print(f"rule {RULE}, run columns (rows 256+): {len(cols)}, cells {per_col.sum()}")
top = np.argsort(-per_col)[:20]
print("top 20 (x, cells):", [(int(x), int(per_col[x])) for x in top])

present = np.zeros(W, bool)
present[cols] = True
n = len(cols)


targets = [341, 682]
obs = {d: sum(1 for x in cols if present[(x + d) % W]) for d in targets}
print(f"pairs with x and x+d both run columns (d = seed distance): 341 -> {obs[341]}, 682 -> {obs[682]}")

rng = np.random.default_rng(1)
null_341 = []
null_682 = []
null_max = []
for _ in range(TRIALS):
    sub = rng.choice(W, size=n, replace=False)
    p = np.zeros(W, bool)
    p[sub] = True
    a = sum(1 for x in sub if p[(x + 341) % W])
    b = sum(1 for x in sub if p[(x + 682) % W])
    null_341.append(a)
    null_682.append(b)
    null_max.append(max(a, b))
null_341 = np.array(null_341)
null_682 = np.array(null_682)
null_max = np.array(null_max)
print(f"null mean 341 {null_341.mean():.2f}, 682 {null_682.mean():.2f}; "
      f"P(null max >= observed max {max(obs.values())}) = {(null_max >= max(obs.values())).mean():.3f}")

offs_341 = sorted(((int(x) - 341) % W) for x in cols)
offs_682 = sorted(((int(x) - 682) % W) for x in cols)
print("offsets from first seed (mod 1024):", offs_341)
print("offsets from second seed (mod 1024):", offs_682)
print("residues mod 32:", sorted(int(x) % 32 for x in cols))
print("run columns:", [int(x) for x in cols])
