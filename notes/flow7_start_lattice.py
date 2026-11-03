import sys
sys.path.insert(0, "/home/sprite/slop-salon-lelia/notes")
import numpy as np
from flow7_edge import trace_stop

BAND_I = range(0, 8)
BAND_J = range(8, 11)
CELL = (2, 9)


def counts(starts):
    cnt = np.zeros((16, 16), int)
    for s in starts:
        l = np.concatenate([trace_stop(s, -1)[::-1], trace_stop(s, 1)[1:]])
        idx = np.unique(np.clip((l * 16).astype(int), 0, 15), axis=0)
        cnt[idx[:, 0], idx[:, 1]] += 1
    return cnt


def report(name, cnt):
    band = np.array([cnt[i, j] for i in BAND_I for j in BAND_J])
    mask = np.ones((16, 16), bool)
    for i in BAND_I:
        for j in BAND_J:
            mask[i, j] = False
    rest = cnt[mask]
    top = np.unravel_index(cnt.argmax(), cnt.shape)
    print("%-22s cell %d  band mean %5.1f  rest mean %5.1f  max %3d at %s"
          % (name, cnt[CELL], band.mean(), rest.mean(), cnt.max(), top))


g = (np.arange(16) + 0.5) / 16
X, Y = np.meshgrid(g, g)
report("centres (as run)", counts(np.stack([X.ravel(), Y.ravel()], 1)))

for off in (0.25, 0.75):
    g = (np.arange(16) + off) / 16
    X, Y = np.meshgrid(g, g)
    report("lattice +%.2f cell" % off, counts(np.stack([X.ravel(), Y.ravel()], 1)))

for seed in range(5):
    rng = np.random.default_rng(seed)
    report("uniform random %d" % seed, counts(rng.random((256, 2))))


def trace_cap(p0, sign, n):
    from flow7_edge import heading
    pts, p = [p0.copy()], p0.copy()
    for _ in range(n):
        th = heading(p[None])[0]
        p = p + sign * 0.0045 * np.array([np.cos(th), np.sin(th)])
        if not ((p >= 0) & (p <= 1)).all():
            break
        pts.append(p.copy())
    return np.array(pts)


def counts_cap(starts, n):
    cnt = np.zeros((16, 16), int)
    longest = 0
    for s in starts:
        a, b = trace_cap(s, -1, n), trace_cap(s, 1, n)
        longest = max(longest, len(a), len(b))
        l = np.concatenate([a[::-1], b[1:]])
        idx = np.unique(np.clip((l * 16).astype(int), 0, 15), axis=0)
        cnt[idx[:, 0], idx[:, 1]] += 1
    return cnt, longest


g = (np.arange(16) + 0.5) / 16
X, Y = np.meshgrid(g, g)
starts = np.stack([X.ravel(), Y.ravel()], 1)
for n in (260, 600):
    cnt, longest = counts_cap(starts, n)
    report("cap %d steps" % n, cnt)
    print("   longest half-trace: %d points" % longest)
