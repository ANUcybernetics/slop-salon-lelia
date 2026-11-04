import sys
sys.path.insert(0, "/home/sprite/slop-salon-lelia/notes")
import numpy as np
from flow7_edge import lines, heading

idx_cells = [np.unique(np.clip((l * 16).astype(int), 0, 15), axis=0) for l in lines]


def slab_report(i, j, slab=0.01):
    lo = np.array([i, j]) / 16
    hi = lo + 1 / 16
    c = (lo + hi) / 2
    th = heading(c[None])[0]
    t = np.array([np.cos(th), np.sin(th)])
    n = np.array([-t[1], t[0]])
    ids = [k for k, idx in enumerate(idx_cells) if ((idx[:, 0] == i) & (idx[:, 1] == j)).any()]
    rows = []
    for k in ids:
        l = lines[k]
        m = ((l >= lo) & (l <= hi)).all(axis=1)
        q = l[m] - c
        for p in q:
            rows.append((k, p @ t, p @ n))
    R = np.array(rows)
    print(f"cell ({i},{j}) lines {len(ids)} heading {np.degrees(th):.1f} deg (along {np.round(t,3)})")
    print(f"  along-range {R[:,1].min():+.4f}..{R[:,1].max():+.4f}  across-range {R[:,2].min():+.4f}..{R[:,2].max():+.4f}")
    edges = np.arange(R[:,1].min(), R[:,1].max() + slab, slab)
    for a0 in edges[::max(1, len(edges)//6)]:
        s = (R[:,1] >= a0) & (R[:,1] < a0 + slab)
        if s.sum() < 2:
            continue
        per_line = {}
        for k, a, b in R[s]:
            per_line.setdefault(int(k), []).append(b)
        mb = np.sort([np.mean(v) for v in per_line.values()])
        gaps = np.diff(mb)
        print(f"  along [{a0:+.3f},{a0+slab:+.3f}): lines {len(mb)}, across std {np.std(R[s,2]):.4f}, "
              f"span {np.ptp(R[s,2]):.4f}, median gap {np.median(gaps) if len(gaps) else float('nan'):.5f}, "
              f"min gap {gaps.min() if len(gaps) else float('nan'):.5f}")


slab_report(2, 9)
slab_report(5, 2)
