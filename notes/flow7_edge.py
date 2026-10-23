import numpy as np

K = np.array([(0.005, 1.195), (-1.819, -3.967), (-1.969, -2.482), (0.422, -3.722)])
PH = np.array([4.874, 0.033, 1.904, 3.170])
AM = np.array([0.613, 0.911, 0.639, 0.777])


def heading(p):
    return 2 * (np.sin(p @ K.T + PH) * AM).sum(axis=1)


def trace_stop(p0, sign):
    pts, p = [p0.copy()], p0.copy()
    for _ in range(260):
        th = heading(p[None])[0]
        p = p + sign * 0.0045 * np.array([np.cos(th), np.sin(th)])
        if not ((p >= 0) & (p <= 1)).all():
            break
        pts.append(p.copy())
    return np.array(pts)


def through(pts, x0, x1, y0, y1):
    return bool(((pts[:, 0] >= x0) & (pts[:, 0] <= x1) & (pts[:, 1] >= y0) & (pts[:, 1] <= y1)).any())


g = (np.arange(16) + 0.5) / 16
X, Y = np.meshgrid(g, g)
lines = []
for s in np.stack([X.ravel(), Y.ravel()], 1):
    lines.append(np.concatenate([trace_stop(s, -1)[::-1], trace_stop(s, 1)[1:]]))

print("box [0.97,1.07]x[0.47,0.57] (stop at edge):", sum(through(l, 0.97, 1.07, 0.47, 0.57) for l in lines))
print("box centred [0.92,1.02]x[0.42,0.52] (stop at edge):", sum(through(l, 0.92, 1.02, 0.42, 0.52) for l in lines))
