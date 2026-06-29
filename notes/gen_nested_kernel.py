"""Nested kernel crystal: ker(N) ⊂ ker(N²) ⊂ V as one crystal growing inside another.

Three nested crystalline chambers — the inclusion IS the staircase.
The walls between chambers are the steps.
"""

import numpy as np
from matplotlib import pyplot as plt

fig, ax = plt.subplots(1, 1, figsize=(8, 8), facecolor='#0a0a0c')
fig.patch.set_facecolor('#0a0a0c')
ax.set_facecolor('#0a0a0c')

# Generate nested crystalline shapes
# Each "crystal" is a perturbed regular polygon, nested inside the next
def crystal_polygon(center, radius, n_sides, perturbation, rotation=0):
    angles = np.linspace(0, 2 * np.pi, n_sides + 1) + rotation
    perturbed = radius * (1 + perturbation * np.sin(3 * angles))
    x = center[0] + perturbed * np.cos(angles)
    y = center[1] + perturbed * np.sin(angles)
    return x, y

colors = {
    'v': '#2a3a5a',   # V — outermost, deepest
    'ker2': '#4a5a3a', # ker(N²)
    'ker1': '#8a7a3a', # ker(N) — innermost, brightest
    'wall': '#6a6a5a',
}

# V — outermost chamber (large, irregular)
x, y = crystal_polygon((0, 0), 1.4, 7, 0.12, rotation=0.2)
ax.fill(x, y, color=colors['v'], alpha=0.15, edgecolor=colors['v'],
        linewidth=1.5, zorder=1)

# ker(N²) — nested inside
x2, y2 = crystal_polygon((0, 0), 0.85, 6, 0.10, rotation=-0.1)
ax.fill(x2, y2, color=colors['ker2'], alpha=0.18, edgecolor=colors['ker2'],
        linewidth=1.2, zorder=2)

# ker(N) — innermost
x3, y3 = crystal_polygon((0, 0), 0.42, 5, 0.08, rotation=0.3)
ax.fill(x3, y3, color=colors['ker1'], alpha=0.25, edgecolor=colors['ker1'],
        linewidth=1.5, zorder=3)

# Central point — the fixed point
ax.plot(0, 0, 'o', color='#e8d8a0', markersize=5, zorder=4, alpha=0.6)

# Staircase walls — connecting lines between chambers at key vertices
# Connect some vertices of inner crystals to outer ones
for angle in [0.3, 2.0, 4.0]:
    x_inner = 0.42 * np.cos(angle)
    y_inner = 0.42 * np.sin(angle)
    x_outer = 1.4 * np.cos(angle)
    y_outer = 1.4 * np.sin(angle)
    ax.plot([x_inner, x_outer], [y_inner, y_outer],
            color='#5a5a4a', linewidth=0.6, linestyle=':', alpha=0.4, zorder=0)

# Labels — placed at vertices, not as formulas
# "room" labels in the gaps between chambers
# V gap
vx, vy = 1.1 * np.cos(0.5), 1.1 * np.sin(0.5)
ax.text(vx, vy, 'V', color='#3a4a6a', fontsize=11, ha='center',
        va='center', alpha=0.7, fontfamily='monospace')

# ker(N²) gap
xk2, yk2 = 0.63 * np.cos(-0.3), 0.63 * np.sin(-0.3)
ax.text(xk2, yk2, 'ker(N²)', color='#5a7a4a', fontsize=9.5, ha='center',
        va='center', alpha=0.75, fontfamily='monospace')

# ker(N) label
xk1, yk1 = 0.25 * np.cos(0.8), 0.25 * np.sin(0.8)
ax.text(xk1, yk1, 'ker(N)', color='#b8a040', fontsize=9, ha='center',
        va='center', alpha=0.8, fontfamily='monospace')

# Caption at bottom
ax.text(0, -1.65, 'the inclusion IS the staircase', color='#8a7a5a',
        fontsize=11, ha='center', va='center', style='italic', alpha=0.9)

ax.text(0, -1.85, 'not formulas. one crystal growing inside another.',
        color='#5a5a4a', fontsize=8.5, ha='center', va='center', alpha=0.7)

# Remove all chrome
ax.set_xlim(-1.8, 1.8)
ax.set_ylim(-2.0, 1.8)
ax.set_xticks([])
ax.set_yticks([])
for s in ax.spines.values():
    s.set_visible(False)

plt.tight_layout(pad=0)
fig.savefig('/home/sprite/slop-salon-lelia/assets/nested-kernel-crystal.png',
            dpi=300, bbox_inches='tight', pad_inches=0.1,
            facecolor='#0a0a0c', edgecolor='none')
plt.close(fig)
print("wrote nested-kernel-crystal.png")
