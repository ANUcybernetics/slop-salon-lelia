import numpy as np

K = np.array([(0.005, 1.195), (-1.819, -3.967), (-1.969, -2.482), (0.422, -3.722)])
PH = np.array([4.874, 0.033, 1.904, 3.170])
AM = np.array([0.613, 0.911, 0.639, 0.777])


def heading(p):
    return 2 * (np.sin(p @ K.T + PH) * AM).sum(axis=1)


def heading_grad(p):
    c = np.cos(p @ K.T + PH) * AM
    return 2 * np.stack([(c * K[:, 0]).sum(axis=1), (c * K[:, 1]).sum(axis=1)], 1)


C = np.array([2.5, 9.5]) / 16
TH = heading(C[None])[0]
T = np.array([np.cos(TH), np.sin(TH)])
N = np.array([-T[1], T[0]])

A = np.arange(-0.3, 0.3001, 0.05)
B_CHAN = [-0.015, 0.0, 0.015]
B_NEIGH = [-0.05, 0.05]


def dtheta_db(a, b):
    p = C + a * T + b * N
    return heading_grad(p[None])[0] @ N


print("dtheta/db along the band (a), at channel and neighbour offsets b")
print("a      " + "  ".join(f"b={b:+.3f}" for b in B_CHAN + B_NEIGH))
rows = {}
for a in A:
    vals = [dtheta_db(a, b) for b in B_CHAN + B_NEIGH]
    rows[round(a, 3)] = vals
    print(f"{a:+.2f}  " + "  ".join(f"{v:+8.3f}" for v in vals))

chan = np.array([rows[k][:3] for k in rows])
neigh = np.array([rows[k][3:] for k in rows])
print()
print("mean |dtheta/db| in channel (b=-0.015..0.015):", round(np.abs(chan).mean(), 3))
print("mean |dtheta/db| at neighbours (b=+-0.05):    ", round(np.abs(neigh).mean(), 3))
print("mean dtheta/db at b=0 over band:              ", round(np.mean([rows[k][1] for k in rows]), 3))
print("sd of dtheta/db over band, channel b=0:       ", round(np.std([rows[k][1] for k in rows]), 3))

dth_chan = []
for a in A:
    p0 = C + a * T
    th = [heading(p0[None] + b * N[None])[0] for b in B_CHAN]
    dth_chan.append(th[2] - th[0])
print("theta(b=+0.015) - theta(b=-0.015) along band:", np.round(dth_chan, 4))
