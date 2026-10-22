import numpy as np

K = np.array([(0.005, 1.195), (-1.819, -3.967), (-1.969, -2.482), (0.422, -3.722)])
PH = np.array([4.874, 0.033, 1.904, 3.170])
AM = np.array([0.613, 0.911, 0.639, 0.777])


def heading(p):
    return 2 * (np.sin(p @ K.T + PH) * AM).sum(axis=1)


def trace(starts, sign):
    p = starts.copy()
    out = [p.copy()]
    for _ in range(260):
        th = heading(p)
        p = p + sign * 0.0045 * np.stack([np.cos(th), np.sin(th)], 1)
        out.append(p.copy())
    return np.array(out)


g = (np.arange(16) + 0.5) / 16
X, Y = np.meshgrid(g, g)
starts = np.stack([X.ravel(), Y.ravel()], 1)
allp = np.concatenate([trace(starts, 1), trace(starts, -1)])

cnt = np.zeros((16, 16), int)
for s in range(len(starts)):
    tr = allp[:, s]
    tr = tr[((tr >= 0) & (tr <= 1)).all(1)]
    idx = np.unique(np.clip((tr * 16).astype(int), 0, 15), axis=0)
    cnt[idx[:, 0], idx[:, 1]] += 1

print("distinct lines per 1/16 cell, max", cnt.max(), "at", np.unravel_index(cnt.argmax(), cnt.shape))
