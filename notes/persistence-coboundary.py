"""
Persistence coboundary — two-panel figure showing cycles born and killed across filtration.

The coboundary reads the boundary's history at every scale. Filtration is the
differential: at each step, new edges create new 1-cycles (they are born), and
filling triangles kill them (they die). The persistence diagram is the coboundary
of the boundary — a record of what the space remembered and what it forgot.

Panel A: filtration sequence — five stages from empty graph to complete graph.
Panel B: persistence diagram — lifetime vs persistence.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

fig = plt.figure(figsize=(16, 6))

# Five points in a pentagon
n = 5
angles = np.linspace(0, 2*np.pi, n, endpoint=False) + np.pi/2
pts = np.column_stack([1.5*np.cos(angles) + 2, 1.5*np.sin(angles) + 2])

# Edges sorted by filtration value (Euclidean distance)
edges = []
for i in range(n):
    for j in range(i+1, n):
        dist = np.linalg.norm(pts[i] - pts[j])
        edges.append((i, j, dist))
edges.sort(key=lambda e: e[2])

# Each stage adds edges
stage_edges = [
    [],                          # t0: empty
    [0, 1],                      # t1: some edges
    [0, 1, 2, 3, 4],            # t2: outer ring closed (H1 born)
    [0, 1, 2, 3, 4, 5, 6],     # t3: triangle fills (H1 dies)
    [0, 1, 2, 3, 4, 5, 6, 7],  # t4: complete
]
stage_labels = ['t\u2080', 't\u2081', 't\u2082', 't\u2083', 't\u2084']

# Top row: 5 filtration stages
for idx, (edge_set, label) in enumerate(zip(stage_edges, stage_labels)):
    ax = fig.add_subplot(2, 5, idx + 1)
    ax.set_xlim(-0.5, 4.5)
    ax.set_ylim(-0.5, 4.5)
    ax.set_aspect('equal')
    ax.axis('off')

    ax.scatter(pts[:, 0], pts[:, 1], s=100, c='#1a1a1a', zorder=5)

    for eidx, (i, j, dist) in enumerate(edges):
        if eidx in edge_set:
            ax.plot([pts[i, 0], pts[j, 0]], [pts[i, 1], pts[j, 1]],
                    color='#1a1a1a', lw=2, alpha=0.9, zorder=2)

    # Highlight cycle-closing edge at t2
    if idx == 2:
        e = edges[4]
        ax.plot([pts[e[0], 0], pts[e[1], 0]], [pts[e[0], 1], pts[e[1], 1]],
                color='#c41e3a', lw=3, zorder=3)

    # Fill triangle at t3
    if idx == 3:
        tri = mpatches.Polygon(pts[[0, 2, 4]], closed=True,
                               facecolor='#e8d44d', alpha=0.2, edgecolor='#c41e3a', lw=2, zorder=1)
        ax.add_patch(tri)

    ax.set_title(label, fontsize=11, fontweight='bold', y=1.02)

# Bottom row: persistence diagram (spanning all columns)
ax_b = fig.add_subplot(2, 1, 2)
ax_b.set_xlim(0, 3)
ax_b.set_ylim(0, 3)
ax_b.axline((0, 0), slope=1, color='#ccc', lw=1, ls='--', label='x = y')

births = [0.6, 0.8, 1.0, 1.1]
deaths = [1.2, 1.5, 1.8, 2.4]
long_b, long_d = 0.6, 2.4

for b, d in zip(births, deaths):
    ax_b.plot(b, d, 'o', color='#4a90d9', markersize=10, alpha=0.7)
    ax_b.plot(b, b, 'o', color='#999', markersize=6, alpha=0.5)
    ax_b.annotate('', xy=(b, d), xytext=(b, b),
                  arrowprops=dict(arrowstyle='->', color='#4a90d9', lw=1, alpha=0.5))

ax_b.plot(long_b, long_d, 'o', color='#c41e3a', markersize=14, zorder=5)
ax_b.annotate('', xy=(long_b, long_d), xytext=(long_b, long_b),
              arrowprops=dict(arrowstyle='->', color='#c41e3a', lw=2.5))

ax_b.set_xlabel('birth', fontsize=12)
ax_b.set_ylabel('death', fontsize=12)
ax_b.set_title('persistence diagram', fontsize=14, fontweight='bold', pad=10)
ax_b.text(0.05, 2.7, 'long-lived cycle', fontsize=9, color='#c41e3a', fontweight='bold')
ax_b.text(0.05, 2.5, 'persistence = 1.8', fontsize=8, color='#c41e3a')
ax_b.text(0.05, 0.2, 'short-lived noise', fontsize=8, color='#999')
ax_b.text(1.5, 0.5, '\u03b4\u00b2 = 0\nin the language\nof scale',
          fontsize=10, color='#666', ha='center',
          bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

plt.tight_layout()
plt.savefig('./assets/persistence-coboundary.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
print("Saved persistence-coboundary.png")
