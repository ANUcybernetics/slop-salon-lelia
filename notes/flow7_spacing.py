import sys
sys.path.insert(0, "/home/sprite/slop-salon-lelia/notes")
import numpy as np
from flow7_edge import lines

idx_cells = [np.unique(np.clip((l * 16).astype(int), 0, 15), axis=0) for l in lines]
cnt = np.zeros((16, 16), int)
for idx in idx_cells:
    cnt[idx[:, 0], idx[:, 1]] += 1


def cell_stats(i, j):
    lo = np.array([i, j]) / 16
    hi = lo + 1 / 16
    ids = [k for k, idx in enumerate(idx_cells) if ((idx[:, 0] == i) & (idx[:, 1] == j)).any()]
    pts, owner = [], []
    for k in ids:
        l = lines[k]
        m = ((l >= lo) & (l <= hi)).all(axis=1)
        pts.append(l[m])
        owner.append(np.full(m.sum(), k))
    P = np.concatenate(pts)
    O = np.concatenate(owner)
    c = P.mean(axis=0)
    cov = np.cov((P - c).T)
    w, v = np.linalg.eigh(cov)
    major, minor = v[:, 1], v[:, 0]
    perp = (P - c) @ minor
    along = (P - c) @ major
    # nearest point of each line to the cell centre, its perpendicular offset
    cc = (lo + hi) / 2
    offs = []
    for k in ids:
        q = P[O == k]
        d = np.linalg.norm(q - cc, axis=1)
        offs.append(((q[d.argmin()] - cc) @ minor))
    offs = np.array(offs)
    return dict(
        n_lines=len(ids), n_pts=len(P),
        std_major=np.sqrt(w[1]), std_minor=np.sqrt(w[0]),
        uniform_std=(1 / 16) / np.sqrt(12),
        perp_q=np.quantile(perp, [0.05, 0.25, 0.5, 0.75, 0.95]),
        line_offs_std=offs.std(), line_offs_iqr=np.subtract(*np.quantile(offs, [0.75, 0.25])),
        major=major,
    )


def show(name, i, j):
    s = cell_stats(i, j)
    print(f"{name} cell ({i},{j}) centre ({(i+0.5)/16:.3f},{(j+0.5)/16:.3f}): lines {s['n_lines']}, points {s['n_pts']}")
    print(f"  std along major {s['std_major']:.4f}, across {s['std_minor']:.4f}, uniform-in-cell {s['uniform_std']:.4f}")
    print(f"  across-band quantiles 5/25/50/75/95%: " + ' '.join(f"{q:+.4f}" for q in s['perp_q']))
    print(f"  per-line nearest-point offset std {s['line_offs_std']:.4f}, IQR {s['line_offs_iqr']:.4f}")
    print(f"  major direction {s['major'].round(3)}")


show("densest", 2, 9)
print("max cell in grid:", np.unravel_index(cnt.argmax(), cnt.shape), cnt.max())
show("typical (median count)", *np.unravel_index(np.argsort(cnt.ravel())[128], cnt.shape))
show("next dense", 3, 9)
