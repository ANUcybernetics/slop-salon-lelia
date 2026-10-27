import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

K = np.array([(0.005, 1.195), (-1.819, -3.967), (-1.969, -2.482), (0.422, -3.722)])
PH = np.array([4.874, 0.033, 1.904, 3.170])
AM = np.array([0.613, 0.911, 0.639, 0.777])


def heading(p):
    return 2 * (np.sin(p @ K.T + PH) * AM).sum(axis=1)


def heading_grad(p):
    c = np.cos(p @ K.T + PH) * AM
    return 2 * np.stack([(c * K[:, 0]).sum(axis=1), (c * K[:, 1]).sum(axis=1)], 1)


def trace_stop(p0, sign):
    pts, p = [p0.copy()], p0.copy()
    for _ in range(260):
        th = heading(p[None])[0]
        p = p + sign * 0.0045 * np.array([np.cos(th), np.sin(th)])
        if not ((p >= 0) & (p <= 1)).all():
            break
        pts.append(p.copy())
    return np.array(pts)


g = (np.arange(16) + 0.5) / 16
X, Y = np.meshgrid(g, g)
lines = []
for s in np.stack([X.ravel(), Y.ravel()], 1):
    lines.append(np.concatenate([trace_stop(s, -1)[::-1], trace_stop(s, 1)[1:]]))

cnt = np.zeros((16, 16), int)
for l in lines:
    idx = np.unique(np.clip((l * 16).astype(int), 0, 15), axis=0)
    cnt[idx[:, 0], idx[:, 1]] += 1

N = 400
u = (np.arange(N) + 0.5) / N
UX, UY = np.meshgrid(u, u)
P = np.stack([UX.ravel(), UY.ravel()], 1)
TH = heading(P).reshape(N, N)
GR = heading_grad(P)
GM = np.hypot(GR[:, 0], GR[:, 1]).reshape(N, N)

cell = np.clip((P * 16).astype(int), 0, 15)
gmean = np.zeros((16, 16))
for i in range(16):
    for j in range(16):
        m = (cell[:, 0] == i) & (cell[:, 1] == j)
        gmean[i, j] = GM.ravel()[m].mean()

def ranks(a):
    r = np.empty(a.size)
    r[np.argsort(a.ravel())] = np.arange(a.size)
    return r.reshape(a.shape)

TH_FLAT = heading(P)
DIV = -np.sin(TH_FLAT) * GR[:, 0] + np.cos(TH_FLAT) * GR[:, 1]
dmean = np.zeros((16, 16))
for i in range(16):
    for j in range(16):
        m = (cell[:, 0] == i) & (cell[:, 1] == j)
        dmean[i, j] = DIV[m].mean()

rc = np.corrcoef(ranks(cnt).ravel(), ranks(gmean).ravel())[0, 1]
rd = np.corrcoef(ranks(cnt).ravel(), ranks(-dmean).ravel())[0, 1]
print("Spearman(lines per cell, mean |grad heading| per cell):", round(rc, 3))
print("Spearman(lines per cell, -div of unit heading field per cell):", round(rd, 3))
dens = np.unravel_index(cnt.argmax(), cnt.shape)
print("max lines per cell:", cnt.max(), "at", dens)
print("densest cell: mean |grad| ", round(gmean[dens], 3), " div ", round(dmean[dens], 3),
      " field mean |grad|", round(GM.mean(), 3), " field mean div", round(DIV.mean(), 3))
print("share of cells with div<0:", round((dmean < 0).mean(), 3))
print("top-10 cells by lines: mean div", round(np.mean([dmean[i, j] for _, i, j in
      sorted(((cnt[i, j], i, j) for i in range(16) for j in range(16)), reverse=True)[:10]]), 3))

fig, (a, b) = plt.subplots(1, 2, figsize=(10, 5), dpi=150)
a.imshow(TH, origin="lower", extent=(0, 1, 0, 1), cmap="twilight", interpolation="bilinear")
a.set_title("heading, mod 2π (colour)")
a.set_xlabel("x")
a.set_ylabel("y")
im = b.imshow(cnt.T, origin="lower", extent=(0, 1, 0, 1), cmap="magma")
b.set_title("distinct lines per 1/16 cell (stop at exit)")
b.set_xlabel("x")
fig.colorbar(im, ax=b, shrink=0.8)
plt.tight_layout()
plt.savefig("/home/sprite/slop-salon-lelia/assets/flow7_heading.png")
