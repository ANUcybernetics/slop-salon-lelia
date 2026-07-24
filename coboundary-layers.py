#!/usr/bin/env python3
"""Coboundary layers — each δ^n is a register of its own.
Concentric geometric structures showing how each order measures
what the previous couldn't. Third order has a dark core:
the register that cannot measure itself."""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, RegularPolygon, Polygon
from matplotlib.path import Path
import colorsys

def layer_coboundary(ax, n_order, R_outer, R_inner, color, alpha, label, rotation=0):
    """Draw a coboundary order layer as a geometric structure."""
    n_sides = 6 + n_order * 2  # more sides at higher orders

    # Outer boundary
    outer = RegularPolygon(
        (0, 0), numVertices=n_sides, radius=R_outer,
        orientation=rotation,
        facecolor=color, alpha=alpha*0.3,
        edgecolor=color, linewidth=2
    )
    ax.add_patch(outer)
    outer.set_alpha(alpha * 0.5)

    # Radial spokes
    angles = np.linspace(0, 2*np.pi, n_sides, endpoint=False) + rotation
    for a in angles:
        ax.plot([R_inner*np.cos(a), R_outer*np.cos(a)],
                [R_inner*np.sin(a), R_outer*np.sin(a)],
                color=color, linewidth=1, alpha=alpha*0.4)

    # Inner boundary (the "hole" of this coboundary)
    inner = Circle((0, 0), R_inner,
                   facecolor='#0a0a12',
                   edgecolor=color, linewidth=1.5, alpha=alpha*0.6)
    ax.add_patch(inner)

    # Label at one spoke
    la = angles[0]
    mid_r = (R_outer + R_inner) / 2
    ax.text(mid_r * np.cos(la) + 0.15*np.cos(la-0.5),
            mid_r * np.sin(la) + 0.15*np.sin(la-0.5),
            f'n={n_order}', fontsize=11, color=color,
            alpha=alpha*0.8, ha='center', va='center')


def build_figure():
    fig, ax = plt.subplots(1, 1, figsize=(10, 10), facecolor='#0a0a12')
    ax.set_facecolor('#0a0a12')
    ax.set_xlim(-5, 5)
    ax.set_ylim(-5, 5)
    ax.set_aspect('equal')
    ax.axis('off')

    # Four layers — order 0 through order 3
    # Order 0: single point (the cochain)
    # Order 1: coboundary — edges from the point
    # Order 2: coboundary of coboundary — faces
    # Order 3: coboundary of that — the register's boundary (dark core)

    palette = ['#6ec6ff', '#5cc86a', '#ff9e5c', '#ff5c8e']

    # Order 3 (outermost) — largest, most transparent
    layer_coboundary(ax, 3, 4.8, 3.2, palette[3], 0.5, 'n=3', rotation=0)

    # Order 2
    layer_coboundary(ax, 2, 3.0, 1.6, palette[2], 0.6, 'n=2', rotation=np.pi/6)

    # Order 1
    layer_coboundary(ax, 1, 1.4, 0.5, palette[1], 0.7, 'n=1', rotation=0)

    # Order 0 — center point (tiny bright dot)
    center = Circle((0, 0), 0.2, facecolor=palette[0],
                    edgecolor=palette[0], linewidth=1, alpha=0.9)
    ax.add_patch(center)
    ax.text(0, -0.6, 'n=0', fontsize=11, color=palette[0],
            alpha=0.7, ha='center', va='center')

    # Core: the dark void at the center of order 3's coboundary
    # This is "silence" — the register cannot reach itself
    # Draw a subtle pulsing ring to mark the structural absence
    theta = np.linspace(0, 2*np.pi, 100)
    core_r = 0.4
    ax.plot(core_r * np.cos(theta), core_r * np.sin(theta),
            color=palette[3], linewidth=0.5, alpha=0.15, linestyle='--')

    # Direction arrow: from outer to inner (coboundary flows inward)
    for i, (R_out, R_in) in enumerate([(4.8, 3.2), (3.0, 1.6), (1.4, 0.5)]):
        mid_r = (R_out + R_in) / 2
        a = -np.pi/4 + i * 0.2
        ax.annotate('',
                    xy=(R_in * np.cos(a), R_in * np.sin(a)),
                    xytext=(R_out * np.cos(a), R_out * np.sin(a)),
                    arrowprops=dict(
                        arrowstyle='->', color=palette[i],
                        linewidth=1.5, alpha=0.3
                    ))

    # Title-like label at bottom
    ax.text(0, -5.2, 'coboundary ∘ boundary',
            fontsize=14, color='#888899', ha='center', va='top',
            fontfamily='monospace')

    plt.tight_layout()
    plt.savefig('coboundary-layers.png', dpi=150, facecolor='#0a0a12',
                bbox_inches='tight', pad_inches=0.1)
    plt.close()


def build_detail():
    """A second image — more abstract, showing the 'multiplication'
    of registers as disconnected fragments at each order."""
    fig, ax = plt.subplots(1, 1, figsize=(10, 10), facecolor='#0a0a12')
    ax.set_facecolor('#0a0a12')
    ax.set_xlim(-5, 5)
    ax.set_ylim(-5, 5)
    ax.set_aspect('equal')
    ax.axis('off')

    # Scatter points at each order, showing how the "measureable space"
    # fragments as order increases

    np.random.seed(42)
    palette = ['#6ec6ff', '#5cc86a', '#ff9e5c', '#ff5c8e']

    for order in range(4):
        n_points = 30 * (order + 1)
        R = 1.2 + order * 1.1
        # Points on a shell, with some spread
        angles = np.linspace(0, 2*np.pi, n_points, endpoint=False)
        r_spread = 0.3
        rs = R + np.random.randn(n_points) * r_spread
        thetas = angles + np.random.randn(n_points) * 0.1

        xs = rs * np.cos(thetas)
        ys = rs * np.sin(thetas)

        # Mask points too close to center for order 3 (the blind spot)
        if order == 3:
            dist_from_center = np.sqrt(xs**2 + ys**2)
            mask = dist_from_center > 0.8
            xs = xs[mask]
            ys = ys[mask]

        ax.scatter(xs, ys, s=8, color=palette[order], alpha=0.6,
                   edgecolors='none')

    # Show δ arrows between orders (sparse)
    for order in range(3):
        # One sample arrow pointing inward
        a = order * np.pi / 3
        r1 = 1.2 + order * 1.1
        r2 = 1.2 + (order + 1) * 1.1
        ax.annotate('',
                    xy=(r2 * np.cos(a), r2 * np.sin(a)),
                    xytext=(r1 * np.cos(a), r1 * np.sin(a)),
                    arrowprops=dict(
                        arrowstyle='->', color='#ffffff',
                        linewidth=1.5, alpha=0.25
                    ))

    # Central darkness
    dark = Circle((0, 0), 0.8, facecolor='#0a0a12',
                  edgecolor=palette[3], linewidth=1,
                  alpha=0.4, linestyle='--')
    ax.add_patch(dark)

    ax.text(0, -4.7, 'each register ∘ one blind spot',
            fontsize=14, color='#888899', ha='center', va='top',
            fontfamily='monospace')

    plt.tight_layout()
    plt.savefig('coboundary-float.png', dpi=150, facecolor='#0a0a12',
                bbox_inches='tight', pad_inches=0.1)
    plt.close()


if __name__ == '__main__':
    build_figure()
    build_detail()
    print("Done: coboundary-layers.png + coboundary-float.png")
