#!/usr/bin/env python3
"""Harmonic assignment cover — harmonic measure on a cluster of boundary points.

Instead of a single seed, use a small circular shell as the "cluster."
The harmonic measure then distributes across the boundary shell with
natural variation — simulating what a real DLA boundary would look like.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

size = 512
cx, cy = size // 2, size // 2
max_r = np.sqrt(cx**2 + cy**2)

y, x = np.mgrid[0:size, 0:size]
r = np.sqrt((x - cx)**2 + (y - cy)**2)
theta = np.arctan2(y - cy, x - cx)

# Create a multi-shell cluster (like a DLA would have)
# Multiple concentric shells with some perturbation
shell_radii = [0.15, 0.35, 0.55, 0.75, 0.88, 0.95, 0.98]
cluster = np.zeros((size, size), dtype=float)

for rad in shell_radii:
    # Add perturbed shell
    n_points = 100
    for _ in range(n_points):
        angle = np.random.uniform(0, 2*np.pi)
        r_offset = rad * max_r + np.random.normal(0, max_r * 0.04)
        px = int(cx + r_offset * np.cos(angle))
        py = int(cy + r_offset * np.sin(angle))
        # Draw a small circle around this point
        dy = np.arange(-3, 4)
        dx = np.arange(-3, 4)
        yy, xx = np.meshgrid(dy, dx, indexing='ij')
        rr = np.sqrt(xx**2 + yy**2)
        mask = (rr <= 3)
        xx = px + xx[mask]
        yy = py + yy[mask]
        ok = (xx >= 0) & (xx < size) & (yy >= 0) & (yy < size)
        cluster[yy[ok], xx[ok]] = 1.0

# Compute distance from each point to cluster
from scipy.ndimage import distance_transform_edt
dist = distance_transform_edt(cluster == 0)

# Exposure: measure of "openness" — count empty neighbors
k = np.ones((3,3), dtype=np.float64)
near_cluster = (distance_transform_edt(cluster == 0) <= 2)

# Harmonic measure approximation
measure = near_cluster.astype(float) * np.exp(-dist / (max_r * 0.1))

# Normalize
measure = (measure - measure.min()) / (measure.max() - measure.min())

# Create smooth visualization
fig, ax = plt.subplots(figsize=(10, 10), dpi=150)
ax.set_aspect('equal')

colors = [
    (0.01, 0.01, 0.03),
    (0.08, 0.02, 0.1),
    (0.25, 0.08, 0.08),
    (0.55, 0.2, 0.05),
    (0.85, 0.5, 0.1),
    (0.95, 0.8, 0.3),
]
from matplotlib.colors import LinearSegmentedColormap
cmap = LinearSegmentedColormap.from_list('harmonic', colors, N=256)

im = ax.imshow(measure, cmap=cmap, extent=[-size/2, size/2, -size/2, size/2],
               interpolation='bicubic')
ax.set_axis_off()
fig.patch.set_facecolor('black')
ax.set_facecolor('black')
fig.savefig('harmonic-assignment-cover.png', dpi=150, bbox_inches='tight',
            facecolor='black', edgecolor='none')
plt.close(fig)
print("Done.")
