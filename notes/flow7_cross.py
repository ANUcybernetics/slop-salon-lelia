import sys
sys.path.insert(0, "/home/sprite/slop-salon-lelia/notes")
import numpy as np
from flow7_edge import lines, heading


def crossings(i, j, half=0.3):
    c = (np.array([i, j]) + 0.5) / 16
    th = heading(c[None])[0]
    t = np.array([np.cos(th), np.sin(th)])
    n = np.array([-t[1], t[0]])
    out = []
    for k, l in enumerate(lines):
        r = l - c
        a = r @ t
        b = r @ n
        s = np.where(np.sign(a[:-1]) != np.sign(a[1:]))[0]
        for q in s:
            f = a[q] / (a[q] - a[q + 1])
            bb = b[q] + f * (b[q + 1] - b[q])
            if abs(bb) < half:
                out.append((k, bb))
    return np.array(out), c, th


def profile(name, i, j):
    C, c, th = crossings(i, j)
    b = np.sort(C[:, 1])
    print(f"{name} cell ({i},{j}) centre ({c[0]:.3f},{c[1]:.3f}) heading {np.degrees(th):.1f} deg")
    print(f"  distinct lines crossing the centre normal within +-0.3: {len(np.unique(C[:,0]))}")
    for w in (0.03, 0.0625, 0.125, 0.25):
        print(f"    crossings within +-{w/2:.4f}: {(np.abs(b) < w/2).sum()}")
    gaps = np.diff(b)
    print(f"  across-coordinate range of all crossings: {b.min():+.4f}..{b.max():+.4f}")
    print(f"  median gap {np.median(gaps):.5f}, 90th pct gap {np.quantile(gaps,0.9):.5f}, max gap {gaps.max():.5f}")
    hist, edges = np.histogram(b, bins=np.arange(-0.3, 0.3 + 0.025, 0.025))
    print("  histogram (bin 0.025 from -0.3):", hist.tolist())


profile("densest", 2, 9)
profile("typical", 5, 2)
