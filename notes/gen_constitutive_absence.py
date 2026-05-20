"""
constitutive absence — image generator

Potential flow streamlines around a void at center.
The void is not drawn. Its existence is inferred from the curvature of the field.

This is the topological version: the hole that changes the fundamental group.
Everything curves around it. The emptiness is load-bearing.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

W, H = 2400, 2400
DPI = 300

fig, ax = plt.subplots(figsize=(W/DPI, H/DPI), dpi=DPI, facecolor='#0a0a0a')
ax.set_facecolor('#0a0a0a')

# Void radius (normalized coords)
R = 0.22

# Grid
res = 3000
x = np.linspace(-3, 3, res)
y = np.linspace(-3, 3, res)
X, Y = np.meshgrid(x, y)
r2 = X**2 + Y**2

# Potential flow stream function around a cylinder:
# psi = y * (1 - R^2 / r^2)
# Outside the cylinder only — inside is masked to NaN
r2_safe = np.where(r2 < R**2, np.inf, r2)
psi = Y * (1.0 - R**2 / r2_safe)

# Mask the interior
psi[r2 < R**2] = np.nan

# Contour levels — dense, thin lines
n_levels = 180
psi_max = 2.4
levels = np.linspace(-psi_max, psi_max, n_levels)

# Color: very slight blue-white gradient by distance from center
# Lines far from void are slightly cooler; lines close are slightly warmer
# But keep it subtle — this is not a color piece

# Draw contours
cs = ax.contour(
    X, Y, psi,
    levels=levels,
    colors='white',
    linewidths=0.28,
    alpha=0.85
)

# Frame
ax.set_xlim(-2.8, 2.8)
ax.set_ylim(-2.8, 2.8)
ax.set_aspect('equal')
ax.axis('off')

plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
plt.savefig(
    'assets/constitutive-absence.png',
    dpi=DPI,
    bbox_inches='tight',
    pad_inches=0,
    facecolor='#0a0a0a'
)
print("saved: assets/constitutive-absence.png")
