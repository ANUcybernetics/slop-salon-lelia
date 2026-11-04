import sys
sys.path.insert(0, "/home/sprite/slop-salon-lelia/notes")
import numpy as np
from flow7_edge import lines, heading

C = np.array([2.5, 9.5]) / 16
TH = heading(C[None])[0]
T = np.array([np.cos(TH), np.sin(TH)])
N = np.array([-T[1], T[0]])
AS = [-0.2, -0.1, 0.0, 0.1, 0.2]


def b_at(line, a0):
    r = line - C
    a = r @ T
    b = r @ N
    s = np.where(np.sign(a[:-1] - a0) != np.sign(a[1:] - a0))[0]
    if len(s) == 0:
        return None
    q = s[np.argmin(np.abs(a[s] - a0))]
    f = (a0 - a[q]) / (a[q + 1] - a[q])
    return b[q] + f * (b[q + 1] - b[q])


def group(lo, hi):
    out = {a0: [] for a0 in AS}
    n = 0
    for line in lines:
        r = line - C
        a = r @ T
        b = r @ N
        s = np.where(np.sign(a[:-1]) != np.sign(a[1:]))[0]
        hit = False
        for q in s:
            f = a[q] / (a[q] - a[q + 1])
            bb = b[q] + f * (b[q + 1] - b[q])
            if lo <= bb <= hi:
                hit = True
        if not hit:
            continue
        n += 1
        for a0 in AS:
            v = b_at(line, a0)
            if v is not None:
                out[a0].append(v)
    return n, out


for name, lo, hi in [("channel |b|<0.015", -0.015, 0.015),
                     ("control 0.03..0.06", 0.03, 0.06),
                     ("control -0.06..-0.03", -0.06, -0.03)]:
    n, out = group(lo, hi)
    print(f"{name}: {n} lines")
    for a0 in AS:
        v = np.array(out[a0])
        if len(v):
            print(f"  a={a0:+.1f}: n={len(v):3d} mean b {v.mean():+.4f} spread (std) {v.std():.4f}  "
                  f"abs-mean {np.abs(v).mean():.4f}")
