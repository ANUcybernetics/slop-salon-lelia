import sys
sys.path.insert(0, "/home/sprite/slop-salon-lelia/notes")
import numpy as np
from flow7_edge import trace_stop, heading, g

W = 0.015
L = 0.3
X, Y = np.meshgrid(g, g)
seeds = np.stack([X.ravel(), Y.ravel()], 1)


def build():
    out = []
    for s in seeds:
        back = trace_stop(s, -1)
        fwd = trace_stop(s, 1)
        line = np.concatenate([back[::-1], fwd[1:]])
        out.append((line, len(back) - 1))
    return out


def cell_of(line):
    return set(map(tuple, np.clip((line * 16).astype(int), 0, 15)))


def entries(i, j, all_lines):
    c = (np.array([i, j]) + 0.5) / 16
    th = heading(c[None])[0]
    t = np.array([np.cos(th), np.sin(th)])
    n = np.array([-t[1], t[0]])
    rows = []
    for k, (line, i0) in enumerate(all_lines):
        if (i, j) not in cell_of(line):
            continue
        r = line - c
        a = r @ t
        b = r @ n
        m = (np.abs(b) < W) & (np.abs(a) < L)
        step = np.linalg.norm(np.diff(line, axis=0), axis=1)
        cum = np.concatenate([[0.0], np.cumsum(step)])
        if not m.any():
            rows.append(dict(k=k, status="no corridor point"))
            continue
        near = np.argmin(np.where(m, np.linalg.norm(r, axis=1), np.inf))
        e0 = near
        while e0 > 0 and m[e0 - 1]:
            e0 -= 1
        e1 = near
        while e1 < len(line) - 1 and m[e1 + 1]:
            e1 += 1
        if e0 <= i0 <= e1:
            rows.append(dict(k=k, status="starts inside", arc=0.0, straight=0.0,
                             seed_to_cell=float(np.linalg.norm(seeds[k] - c))))
            continue
        if e1 < i0:
            e, side = e1, "back"
        else:
            e, side = e0, "fwd"
        arc = abs(cum[e] - cum[i0])
        rows.append(dict(k=k, status=f"enters from {side}", arc=float(arc),
                         straight=float(np.linalg.norm(line[e] - seeds[k])),
                         seed_to_cell=float(np.linalg.norm(seeds[k] - c))))
    return rows, c


def report(name, i, j, all_lines):
    rows, c = entries(i, j, all_lines)
    print(f"{name} cell ({i},{j}) centre ({c[0]:.3f},{c[1]:.3f}): {len(rows)} lines through cell")
    stat = {}
    for r in rows:
        stat[r["status"]] = stat.get(r["status"], 0) + 1
    for k, v in sorted(stat.items()):
        print(f"  {k}: {v}")
    arcs = np.array([r["arc"] for r in rows if "arc" in r])
    st = np.array([r["straight"] for r in rows if "straight" in r])
    if len(arcs):
        q = np.quantile(arcs, [0.1, 0.25, 0.5, 0.75, 0.9])
        print("  arc from seed to corridor entry (10/25/50/75/90 pct): " + " ".join(f"{x:.3f}" for x in q))
        print(f"  straight seed-to-entry (median, max): {np.median(st):.3f}, {st.max():.3f}")
        print(f"  entries within one seed spacing (0.0625 arc): {(arcs < 0.0625).sum()} of {len(arcs)}")
        print(f"  entries beyond 0.25 arc: {(arcs > 0.25).sum()} of {len(arcs)}")
    return rows


if __name__ == "__main__":
    all_lines = build()
    rd = report("densest", 2, 9, all_lines)
    report("typical", 5, 2, all_lines)
    print("densest cell, per line (k, status, arc, seed_to_cell):")
    for r in sorted(rd, key=lambda r: r.get("arc", -1)):
        if "arc" in r:
            print(f"  {r['k']:3d} {r['status']:16s} arc {r['arc']:.3f}  seed_to_cell {r['seed_to_cell']:.3f}")
        else:
            print(f"  {r['k']:3d} {r['status']}")
