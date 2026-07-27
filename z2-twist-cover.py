#!/usr/bin/env python3
"""Z₂ twist cover: two interlocking circles, same path, opposite orientation.

The clutching is the same loop with opposite direction.
Forward = →, backward = ←. Same circle, different reading.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Arc
import matplotlib.patches as mpatches

fig, ax = plt.subplots(1, 1, figsize=(8, 8), facecolor='#000')
ax.tick_params(colors='#fff', labelcolor='#fff')
ax.set_facecolor('#000')
ax.set_xlim(-1.5, 1.5)
ax.set_ylim(-1.5, 1.5)
ax.set_aspect('equal')
ax.axis('off')

# Two circles — same radius, same center, opposite orientation
radius = 0.9
center = (0, 0)

# Forward circle (clockwise, warm amber)
theta_fwd = np.linspace(0, 2*np.pi, 200)
x_fwd = center[0] + radius * np.cos(theta_fwd)
y_fwd = center[1] + radius * np.sin(theta_fwd)
ax.plot(x_fwd, y_fwd, color='#d4851a', linewidth=3, alpha=0.9)

# Backward circle (counter-clockwise, cool blue)
theta_bwd = np.linspace(0, 2*np.pi, 200)
x_bwd = center[0] + radius * np.cos(-theta_bwd)
y_bwd = center[1] + radius * np.sin(-theta_bwd)
ax.plot(x_bwd, y_bwd, color='#4a7fff', linewidth=3, alpha=0.9)

# Arrowheads to show direction
# Forward: right side, pointing down
ax.annotate('', xy=(radius, -0.3), xytext=(radius, -0.1),
            arrowprops=dict(arrowstyle='->', color='#d4851a', lw=4))

# Backward: left side, pointing up
ax.annotate('', xy=(-radius, 0.3), xytext=(-radius, 0.1),
            arrowprops=dict(arrowstyle='->', color='#4a7fff', lw=4))

# Center point
ax.plot(0, 0, 'o', color='#fff', markersize=4)

# Small label: g and g⁻¹ on the overlap region
ax.text(0.2, 1.1, r'$g$', fontsize=20, color='#d4851a', ha='center')
ax.text(0.2, 1.25, r'$g^{-1}$', fontsize=20, color='#4a7fff', ha='center')

# Z₂ label
ax.text(0, -1.35, r'$\mathbb{Z}_2$', fontsize=24, color='#fff',
        ha='center', fontweight='bold')

plt.tight_layout()
plt.savefig('./assets/z2-twist-cover.png', dpi=150, bbox_inches='tight',
            facecolor='#000', edgecolor='none')
print("Wrote z2-twist-cover.png")
