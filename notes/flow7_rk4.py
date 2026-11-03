import sys
sys.path.insert(0, "/home/sprite/slop-salon-lelia/notes")
import numpy as np
from flow7_edge import heading

H = 0.0045
N = 260
CELL = (2, 9)
BAND_I = range(0, 8)
BAND_J = range(8, 11)


def direction(p):
    th = heading(p[None])[0]
    return np.array([np.cos(th), np.sin(th)])


def step_euler(p, h):
    return p + h * direction(p)


def step_rk4(p, h):
    k1 = direction(p)
    k2 = direction(p + 0.5 * h * k1)
    k3 = direction(p + 0.5 * h * k2)
    k4 = direction(p + h * k3)
    return p + (h / 6) * (k1 + 2 * k2 + 2 * k3 + k4)


def trace(p0, sign, stepper, h, n):
    pts, p = [p0.copy()], p0.copy()
    for _ in range(n):
        p = stepper(p, sign * h)
        if not ((p >= 0) & (p <= 1)).all():
            break
        pts.append(p.copy())
    return np.array(pts)


def counts(starts, stepper, h, n):
    cnt = np.zeros((16, 16), int)
    for s in starts:
        a, b = trace(s, -1, stepper, h, n), trace(s, 1, stepper, h, n)
        l = np.concatenate([a[::-1], b[1:]])
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
    print("%-28s cell %3d  band mean %5.1f  rest mean %5.1f  max %3d at %s"
          % (name, cnt[CELL], band.mean(), rest.mean(), cnt.max(), top))


g = (np.arange(16) + 0.5) / 16
X, Y = np.meshgrid(g, g)
starts = np.stack([X.ravel(), Y.ravel()], 1)

report("euler h=0.0045 (as run)", counts(starts, step_euler, H, N))
report("rk4 h=0.0045", counts(starts, step_rk4, H, N))
report("euler h=0.00045 (x10 steps)", counts(starts, step_euler, H / 10, N * 10))
