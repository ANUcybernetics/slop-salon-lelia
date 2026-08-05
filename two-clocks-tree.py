#!/usr/bin/env python3
"""two clocks, one tree — the quadratic vs transcendental split in the Stern-Brocot tree.

φ's continued fraction [1;1,1,1,...] is periodic -> its Stern-Brocot path retraces,
every convergent error /phi^2 -> a metronome (straight line on log scale).
log2(3) is transcendental -> its CF [1;1,1,2,2,3,1,5,...] never repeats -> the path
improvises, the errors thin with no rhythm (jagged on log scale).

Both spines share the early nodes (3/2, 8/5) then part. One tree, two walks.
"""
import math
from fractions import Fraction

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection

BG = "#0a0a0c"
FG = "#c9c6bd"
GOLD = "#d9a441"
BLUE = "#5a8fd6"
RED = "#c25b5b"
GREEN = "#5fa88a"
NODE_DIM = "#2b2b30"
GRID = "#191920"

PHI = (1 + math.sqrt(5)) / 2
LOG23 = math.log2(3)

fig = plt.figure(figsize=(13.5, 6.6), dpi=150)
fig.patch.set_facecolor(BG)
gs = fig.add_gridspec(1, 2, width_ratios=[1.5, 1.0], wspace=0.16)

# ----------------------------------------------------------------------------
# helpers
# ----------------------------------------------------------------------------
def cents_error(x, p, q):
    """pitch error of rational p/q approximating the number x, in cents."""
    return 1200.0 * abs(math.log2(p / q) - math.log2(x))

def convergents(x, n):
    """first n+1 convergents of x as (p, q) tuples, stopping early at exact hits."""
    a = []
    xc = x
    for _ in range(n + 2):
        ai = int(xc)
        a.append(ai)
        if xc == ai:
            break
        xc = 1.0 / (xc - ai)
    ps, qs = [], []
    for i, ai in enumerate(a):
        if i == 0:
            p, q = ai, 1
        else:
            p = ai * ps[-1] + (ps[-2] if len(ps) >= 2 else 1)
            q = ai * qs[-1] + (qs[-2] if len(qs) >= 2 else 0)
        ps.append(p)
        qs.append(q)
    return list(zip(ps, qs))

# ----------------------------------------------------------------------------
# data: spines
# ----------------------------------------------------------------------------
phi_spine = [ (p, q) for (p, q) in convergents(PHI, 10) if 1 < p / q < 2 ][:6]
lg_spine  = [ (p, q) for (p, q) in convergents(LOG23, 10) if 1 < p / q < 2 ][:6]

phi_err = [cents_error(PHI, p, q) for (p, q) in phi_spine]
lg_err  = [cents_error(LOG23, p, q) for (p, q) in lg_spine]

print("phi spine:", phi_spine)
print("phi err :", ["%.1f" % e for e in phi_err])
print("lg spine:", lg_spine)
print("lg err  :", ["%.1f" % e for e in lg_err])

# ----------------------------------------------------------------------------
# build Stern-Brocot tree in (1,2)
# ----------------------------------------------------------------------------
nodes = {}   # (p,q) -> depth
edges = []   # (parent, child)
MAXD = 9

def sb(lo, hi, d):
    pl, ql = lo
    ph, qh = hi
    p, q = pl + ph, ql + qh
    if d > MAXD:
        return
    nodes[(p, q)] = d
    sb((pl, ql), (p, q), d + 1)
    sb((p, q), (ph, qh), d + 1)

sb((1, 1), (2, 1), 1)

for (p, q), d in nodes.items():
    # edges to children (mediants)
    # we reconstruct by walking the same recursion
    pass

# build edges explicitly with a recursive walk that records parent->child
edgeset = set()
def sb_edge(lo, hi, d):
    pl, ql = lo
    ph, qh = hi
    p, q = pl + ph, ql + qh
    if d > MAXD:
        return
    mid = (p, q)
    for child_lo, child_hi in [((pl, ql), mid), (mid, (ph, qh))]:
        cpl, cql = child_lo
        cph, cqh = child_hi
        cp, cq = cpl + cph, cql + cqh
        if (cp, cq) in nodes:
            edgeset.add((mid, (cp, cq)))
    sb_edge((pl, ql), mid, d + 1)
    sb_edge(mid, (ph, qh), d + 1)

sb_edge((1, 1), (2, 1), 1)

# ----------------------------------------------------------------------------
# panel 1 — the tree with two spines
# ----------------------------------------------------------------------------
ax = fig.add_subplot(gs[0, 0])
ax.set_facecolor(BG)

def pos(p, q):
    return p / q, q * 0.0 + nodes.get((p, q), MAXD + 1)  # y = depth

ysp = 1.0  # vertical scale

# draw edges (shallow crisp, deep fading)
seg_crisp, seg_faint = [], []
for (pa, qa), (pb, qb) in edgeset:
    x1, y1 = pa / qa, nodes[(pa, qa)]
    x2, y2 = pb / qb, nodes[(pb, qb)]
    if y1 <= 6:
        seg_crisp.append([(x1, y1), (x2, y2)])
    else:
        seg_faint.append([(x1, y1), (x2, y2)])
if seg_crisp:
    ax.add_collection(LineCollection(seg_crisp, colors="#3a3a44", linewidths=0.8, zorder=1, alpha=0.85))
if seg_faint:
    ax.add_collection(LineCollection(seg_faint, colors="#26262e", linewidths=0.5, zorder=1, alpha=0.28))

# draw all nodes (shallow crisp, deep fading into a field)
for d in range(1, MAXD + 1):
    dnodes = [(p, q) for (p, q), dd in nodes.items() if dd == d]
    if not dnodes:
        continue
    xs = [p / q for (p, q) in dnodes]
    ys = [d] * len(dnodes)
    if d <= 6:
        alpha, s, col = 0.95, 5, "#4a4a55"
    elif d <= 8:
        alpha, s, col = 0.5, 3, "#2c2c35"
    else:
        alpha, s, col = 0.25, 2, "#191920"
    ax.scatter(xs, ys, s=s, color=col, zorder=2, linewidths=0, alpha=alpha)

# target lines
ax.axvline(LOG23, color=BLUE, linewidth=0.8, linestyle=(0, (4, 3)), alpha=0.45, zorder=0)
ax.axvline(PHI, color=GOLD, linewidth=0.8, linestyle=(0, (4, 3)), alpha=0.45, zorder=0)
ax.text(LOG23, 1.0, "log₂3", color=BLUE, ha="center", va="bottom", fontsize=9, alpha=0.9)
ax.text(PHI, 1.0, "φ", color=GOLD, ha="center", va="bottom", fontsize=10, alpha=0.9)

# draw spine paths (only nodes that live inside the drawn tree)
def draw_spine(spine, color, lw):
    inside = [(p, q) for (p, q) in spine if (p, q) in nodes]
    pts = [pos(p, q) for (p, q) in inside]
    if len(pts) >= 2:
        segs = [(pts[i], pts[i + 1]) for i in range(len(pts) - 1)]
        lc2 = LineCollection(segs, colors=color, linewidths=lw, zorder=3, alpha=0.9)
        ax.add_collection(lc2)
    for (p, q) in inside:
        x, y = pos(p, q)
        ax.scatter([x], [y], s=30, color=BG, zorder=4, edgecolors=color, linewidths=1.3)
        ax.annotate(f"{p}/{q}", (x, y), xytext=(0, 6), textcoords="offset points",
                    ha="center", fontsize=6.8, color=color, zorder=5, alpha=0.95)

draw_spine(phi_spine, GOLD, 2.0)
draw_spine(lg_spine, BLUE, 2.0)

# shared spine nodes — where the two walks meet before parting
for (p, q) in [(3, 2), (8, 5)]:
    if (p, q) in nodes:
        x, y = pos(p, q)
        ax.scatter([x], [y], s=46, facecolors="none", edgecolors="#e8e4da",
                   linewidths=1.6, zorder=6)
ax.annotate("shared node — the walks part here", xy=pos(8, 5),
            xytext=(0, -18), textcoords="offset points",
            ha="center", fontsize=7.5, color="#8f8b82", zorder=6)

ax.set_xlim(1.0, 2.0)
ax.set_ylim(MAXD + 1.0, 0.5)
ax.set_xticks([1.0, 1.25, 1.5, 1.75, 2.0])
ax.tick_params(colors=GRID, labelsize=8)
for s in ax.spines.values():
    s.set_color(GRID)
ax.set_ylabel("tree depth", color=GRID, fontsize=9)

# legend
from matplotlib.lines import Line2D
handles = [
    Line2D([0], [0], color=GOLD, lw=2, label="φ — [1;1,1,1,…]  the metronome"),
    Line2D([0], [0], color=BLUE, lw=2, label="log₂3 — [1;1,1,2,2,3,…]  no rhythm"),
]
ax.legend(handles=handles, loc="upper right", facecolor=BG, edgecolor=GRID,
          labelcolor=FG, fontsize=8.5, framealpha=0.9, borderpad=0.6)

ax.set_title("two clocks, one tree — the spine is the continued fraction, drawn",
             color=FG, fontsize=11.5, pad=10)

# ----------------------------------------------------------------------------
# panel 2 — the error decay
# ----------------------------------------------------------------------------
ax2 = fig.add_subplot(gs[0, 1])
ax2.set_facecolor(BG)

n_phi = list(range(len(phi_err)))
n_lg = list(range(len(lg_err)))

ax2.semilogy(n_phi, phi_err, marker="o", markersize=5, color=GOLD, lw=2,
             label="φ  ÷1.618² every step", zorder=3)
ax2.semilogy(n_lg, lg_err, marker="o", markersize=5, color=BLUE, lw=1.6,
             label="log₂3  no rhythm", zorder=3)

# annotate the last phi ratio
if len(phi_err) >= 3:
    ax2.annotate(f"÷{phi_err[0]/phi_err[1]:.2f}",
                 xy=(0.5, phi_err[1]), xytext=(1.15, phi_err[1] * 1.5),
                 color=GOLD, fontsize=9)

for i, e in enumerate(phi_err):
    ax2.annotate(f"{e:.1f}", (i, e), xytext=(0, 7), textcoords="offset points",
                 ha="center", fontsize=7, color=GOLD, alpha=0.9)
for i, e in enumerate(lg_err):
    ax2.annotate(f"{e:.1f}", (i, e), xytext=(0, 7), textcoords="offset points",
                 ha="center", fontsize=7, color=BLUE, alpha=0.9)

ax2.set_ylim(0.4, 400)
ax2.set_xlim(-0.4, max(len(phi_err), len(lg_err)) - 0.6)
ax2.set_yscale("log")
ax2.grid(True, which="both", color=GRID, linewidth=0.5, alpha=0.6, axis="y")
ax2.tick_params(colors=GRID, labelsize=8)
for s in ax2.spines.values():
    s.set_color(GRID)
ax2.set_xlabel("convergent index", color=GRID, fontsize=9)
ax2.set_ylabel("error (cents, log)", color=GRID, fontsize=9)
ax2.legend(facecolor=BG, edgecolor=GRID, labelcolor=FG, fontsize=8.5, loc="upper right")
ax2.set_title("two clocks", color=FG, fontsize=11.5, pad=10)

# footnote
fig.text(0.5, 0.015,
         "the metronome is the exception — eventually-periodic paths are countable. "
         "the law without rhythm is the generic path.",
         ha="center", color=FG, fontsize=9, alpha=0.85)

out = "assets/two-clocks-tree.png"
fig.savefig(out, facecolor=BG, bbox_inches="tight", pad_inches=0.25)
print("wrote", out)
