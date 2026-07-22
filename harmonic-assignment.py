#!/usr/bin/env python3
"""Harmonic assignment — visualizing the dual field of a DLA cluster."""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.ndimage import convolve, distance_transform_edt

def build_dla(size=128, n_particles=3000, seed=42):
    """DLA with boundary mask — launches at fixed distance, walks inward."""
    np.random.seed(seed)
    cx = cy = size // 2

    # Use distance transform to guide walkers inward (cheaper than pure BM)
    cluster = np.zeros((size, size), dtype=bool)
    cluster[cx, cy] = True

    def update_boundary():
        k = np.ones((3,3), dtype=np.float64)
        near = convolve(cluster.astype(float), k, mode='constant') > 0
        return near & ~cluster

    boundary = update_boundary()

    for i in range(n_particles):
        # Launch from circle at distance = max radius * 0.8
        max_r = max(int(np.sqrt((cx**2 + cy**2))) * 0.7, 15)
        angle = np.random.uniform(0, 2*np.pi)
        x, y = int(cx + max_r * np.cos(angle)), int(cy + max_r * np.sin(angle))
        x = max(0, min(size-1, x))
        y = max(0, min(size-1, y))

        stuck = False
        for step in range(size * size):
            if boundary[y, x]:
                cluster[y, x] = True
                boundary = update_boundary()
                stuck = True
                break

            # Biased random walk: slight pull toward center to prevent escapes
            dx = np.random.randint(-1, 2)
            dy = np.random.randint(-1, 2)
            # Add small inward drift
            dx += int(0.3 * np.sign(cx - x))
            dy += int(0.3 * np.sign(cy - y))
            x = max(1, min(size-2, x + int(dx)))
            y = max(1, min(size-2, y + int(dy)))

            # If got too close to center, check boundary
            r = np.sqrt((x-cx)**2 + (y-cy)**2)
            if r < 3 and boundary[y, x]:
                cluster[y, x] = True
                boundary = update_boundary()
                stuck = True
                break

        if i % 1000 == 0:
            print(f"  particle {i}: stuck={stuck}, cluster={cluster.sum()}")
            if boundary.sum() == 0:
                break

    return cluster

def compute_measures(cluster, size):
    """Harmonic measure via potential theory."""
    cx = cy = size // 2
    k = np.ones((3,3), dtype=np.float64)
    near = convolve(cluster.astype(float), k, mode='constant') > 0
    boundary = near & ~cluster
    exposure = convolve(boundary.astype(float), k, mode='constant')
    dist = distance_transform_edt(cluster == 0)
    dist_b = np.where(boundary, dist, 0)
    return exposure * np.exp(-dist_b / 5.0), boundary

def render(cluster, measure, boundary):
    size = cluster.shape[0]
    cx = cy = size // 2
    extent = [-size/2, size/2, -size/2, size/2]

    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    axes[0].imshow(cluster.T, cmap='magma_r', origin='lower', extent=extent)
    axes[0].set_title('DLA Cluster')
    axes[0].set_aspect('equal')
    axes[0].axis('off')

    m = np.log1p(measure)
    im = axes[1].imshow(m.T, cmap='inferno', origin='lower', extent=extent)
    axes[1].set_title('Harmonic Measure on Boundary')
    axes[1].set_aspect('equal')
    axes[1].axis('off')
    plt.colorbar(im, ax=axes[1], fraction=0.046, pad=0.04)

    # Polar analysis
    ys, xs = np.where(cluster)
    radii = np.sqrt((xs - cx)**2 + (ys - cy)**2)
    angles = np.arctan2(ys - cy, xs - cx)

    n_bins = 32
    bins = np.linspace(-np.pi, np.pi, n_bins + 1)
    max_r = np.zeros(n_bins)
    avg_m = np.zeros(n_bins)
    cnt = np.zeros(n_bins)

    for i in range(len(xs)):
        b = int(np.digitize(angles[i], bins)) - 1
        if b < 0:
            b = n_bins - 1
        if b < n_bins:
            if radii[i] > max_r[b]:
                max_r[b] = radii[i]
            avg_m[b] += measure[ys[i], xs[i]]
            cnt[b] += 1

    avg_m[cnt > 0] /= cnt[cnt > 0]

    sc = axes[2].scatter(max_r, avg_m, c=cnt, cmap='viridis', s=50, alpha=0.8)
    if len(max_r) > 5:
        z = np.polyfit(max_r, avg_m, 3)
        p = np.poly1d(z)
        axes[2].plot(np.linspace(0, max_r.max()+1, 50),
                      p(np.linspace(0, max_r.max()+1, 50)),
                      'r--', alpha=0.5)

    axes[2].set_xlabel('Max radial extent')
    axes[2].set_ylabel('Mean harmonic measure')
    axes[2].set_title('Measure vs. tip extent')
    fig.colorbar(sc, ax=axes[2], fraction=0.046, pad=0.04)

    fig.suptitle('Harmonic Assignment', fontsize=14, fontweight='bold', y=1.02)
    fig.tight_layout()
    fig.savefig('harmonic-assignment.png', dpi=150, bbox_inches='tight',
                facecolor='black')
    plt.close(fig)

if __name__ == '__main__':
    print("Building DLA...")
    cluster = build_dla(size=128, n_particles=3000)
    print(f"  Cluster: {cluster.sum()} cells")
    print("Computing harmonic measure...")
    measure, boundary = compute_measures(cluster, 128)
    print("Rendering...")
    render(cluster, measure, boundary)
    print("Done.")
