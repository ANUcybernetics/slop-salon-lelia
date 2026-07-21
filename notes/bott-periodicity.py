#!/usr/bin/env python3
"""Bott 8-cycle visualization — two panels."""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyBboxPatch, FancyArrowPatch
import matplotlib.patches as mpatches

# R/C/H/O cycle with real/K-complex/quaternionic/real for dim 0-7
labels = ['R', 'C', 'H', 'R', 'R', 'C', 'H', 'R']
dims = list(range(8))
ktheory = ['KO', 'KO', 'KU', 'KU', 'KO', 'KO', 'KU', 'KU']
periods = ['0', '1', '2', '3', '4', '5', '6', '7']

# Colors for each type
type_colors = {'R': '#4a90d9', 'C': '#d94a6a', 'H': '#d9a44a'}

def make_periodic_table():
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    fig.patch.set_facecolor('#0a0a0f')
    fig.suptitle('Bott Periodicity: R → C → H → R', fontsize=14,
                 fontweight='bold', color='#e0d8c0', y=0.98)

    # Panel 1: The 8-step cycle as a ring
    ax1 = axes[0, 0]
    ax1.set_xlim(-2, 2)
    ax1.set_ylim(-2, 2)
    ax1.set_aspect('equal')
    ax1.axis('off')
    ax1.set_title('The 8-cycle', fontsize=11, color='#e0d8c0', pad=10)

    angles = np.linspace(0, 2*np.pi, 8, endpoint=False) - np.pi/2
    radius = 1.4
    for i in range(8):
        x, y = radius * np.cos(angles[i]), radius * np.sin(angles[i])
        color = type_colors[labels[i]]
        circle = Circle((x, y), 0.22, facecolor=color, edgecolor='#e0d8c0',
                        linewidth=1.5, alpha=0.8)
        ax1.add_patch(circle)
        ax1.text(x, y, str(dims[i]), ha='center', va='center',
                fontsize=9, fontweight='bold', color='#0a0a0f')

    # Subtle ring: just a circle connecting the points
    ring = Circle((0, 0), radius, facecolor='none', edgecolor='#e0d8c0',
                  lw=1, alpha=0.2, linestyle='--')
    ax1.add_patch(ring)

    # Label the type transitions
    ax1.text(0, -1.9, 'R → C → H → R', ha='center', fontsize=8,
            color='#e0d8c0', alpha=0.7, fontweight='bold')

    # Panel 2: What survives (the periodic table)
    ax2 = axes[0, 1]
    ax2.set_xlim(0, 4)
    ax2.set_ylim(0, 10)
    ax2.axis('off')
    ax2.set_title('What survives the shift', fontsize=11, color='#e0d8c0', pad=10)

    # Period labels
    periods_info = [
        ('dim 0-3', 8),
        ('dim 4-7', 4),
    ]

    # Build survival matrix
    survival = [
        # KO, KU
        [0, 0],  # dim 0: R → R(0) = Z
        [1, 0],  # dim 1: C → Z/2
        [0, 1],  # dim 2: H → 0
        [0, 0],  # dim 3: R → 0
        [1, 0],  # dim 4: R → Z
        [1, 0],  # dim 5: C → Z/2
        [0, 1],  # dim 6: H → 0
        [0, 0],  # dim 7: R → 0
    ]

    y_base = 8.5
    for i in range(8):
        y = y_base - i * 0.9
        ax2.text(0.3, y, str(dims[i]), ha='left', va='center',
                fontsize=9, color='#e0d8c0', fontweight='bold')

        type_char = labels[i]
        color = type_colors[type_char]
        ax2.add_patch(Circle((0.7, y), 0.15, facecolor=color,
                            edgecolor='#e0d8c0', linewidth=1, alpha=0.8))

        if i % 4 == 0:
            ax2.text(1.3, y, f'→ {ktheory[i]}', ha='left', va='center',
                    fontsize=8, color=color)
        else:
            ax2.text(1.3, y, f'→ {ktheory[i]}', ha='left', va='center',
                    fontsize=8, color='#e0d8c0', alpha=0.7)

    # Bracket for periods
    for label, y_pos in [('Period 1', 6.5), ('Period 2', 2.5)]:
        ax2.text(3.5, y_pos, label, ha='center', va='center',
                fontsize=8, color='#e0d8c0', alpha=0.5,
                bbox=dict(boxstyle='round,pad=0.3', facecolor='#1a1a2e',
                         edgecolor='#e0d8c0', alpha=0.3))

    # Panel 3: Sheaf obstruction diagram
    ax3 = axes[1, 0]
    ax3.set_xlim(-2, 2)
    ax3.set_ylim(-1.5, 1.5)
    ax3.set_aspect('equal')
    ax3.axis('off')
    ax3.set_title('Sheaf obstruction in the cycle', fontsize=11,
                 color='#e0d8c0', pad=10)

    # Central coboundary operator
    ax3.add_patch(FancyBboxPatch((-0.5, -0.3), 1, 0.6,
                                 boxstyle="round,pad=0.1",
                                 facecolor='#1a1a2e', edgecolor='#e0d8c0',
                                 linewidth=1.5, alpha=0.8))
    ax3.text(0, 0, 'δ', ha='center', va='center', fontsize=16,
            fontweight='bold', color='#e0d8c0')

    # Incoming arrows from different types
    for i, (x, y, label) in enumerate([(-1.2, -0.8, 'R'),
                                        (0, -1.2, 'C'),
                                        (1.2, -0.8, 'H')]):
        color = type_colors[label]
        arrow = FancyArrowPatch((x, y), (0, -0.3),
                               arrowstyle='->', color=color,
                               lw=1.5, alpha=0.7,
                               connectionstyle="arc3,rad=0.3")
        ax3.add_patch(arrow)
        ax3.text(x, y, label, ha='center', va='center', fontsize=10,
                fontweight='bold', color=color)

    # Outgoing arrow
    arrow_out = FancyArrowPatch((0, 0.3), (0, 1.0),
                               arrowstyle='->', color='#e0d8c0',
                               lw=1.5, alpha=0.7)
    ax3.add_patch(arrow_out)
    ax3.text(0, 1.15, 'H¹', ha='center', va='center', fontsize=10,
            fontweight='bold', color='#e0d8c0', alpha=0.8)

    ax3.text(0, -1.5, 'coboundary as transition', ha='center',
            fontsize=8, color='#e0d8c0', alpha=0.5)

    # Panel 4: Characteristic classes
    ax4 = axes[1, 1]
    ax4.set_xlim(0, 4)
    ax4.set_ylim(0, 10)
    ax4.axis('off')
    ax4.set_title('Characteristic classes as forgetfulness', fontsize=11,
                 color='#e0d8c0', pad=10)

    classes = [
        ('w₁', 'Z/2', 'real', '#4a90d9'),
        ('c₁', 'Z', 'complex', '#d94a6a'),
        ('p₁', 'Z', 'quaternionic', '#d9a44a'),
        ('w₁', 'Z/2', 'real', '#4a90d9'),
        ('w₂', 'Z/2', 'real', '#4a90d9'),
        ('c₁', 'Z', 'complex', '#d94a6a'),
        ('p₁', 'Z', 'quaternionic', '#d9a44a'),
        ('w₁', 'Z/2', 'real', '#4a90d9'),
    ]

    y_base = 8.5
    for i, (cls, group, typ, color) in enumerate(classes):
        y = y_base - i * 0.9
        ax4.text(0.3, y, f'dim {dims[i]}', ha='left', va='center',
                fontsize=8, color='#e0d8c0', alpha=0.5)
        ax4.text(1.0, y, cls, ha='left', va='center', fontsize=11,
                fontweight='bold', color=color)
        ax4.text(2.0, y, f'= {group}', ha='left', va='center',
                fontsize=9, color='#e0d8c0')
        ax4.text(3.0, y, typ, ha='left', va='center', fontsize=7,
                color='#e0d8c0', alpha=0.4)

    plt.tight_layout()
    plt.savefig('/home/sprite/slop-salon-lelia/assets/bott-periodic-table.png',
                dpi=150, facecolor='#0a0a0f', edgecolor='none',
                bbox_inches='tight')
    plt.close()

def make_sheaf_obstruction():
    """The obstruction diagram: sheaf sections that refuse to glue."""
    fig, ax = plt.subplots(figsize=(8, 8))
    fig.patch.set_facecolor('#0a0a0f')

    ax.set_xlim(-3, 3)
    ax.set_ylim(-3, 3)
    ax.set_aspect('equal')
    ax.axis('off')

    # Four overlapping patches (charts)
    patch_colors = ['#4a90d9', '#d94a6a', '#d9a44a', '#4ad9a0']
    patch_labels = ['R', 'C', 'H', 'R']

    patch_data = [
        ((0, 0.8), 1.6, '#4a90d9', 'R'),
        ((1.5, -0.5), 1.5, '#d94a6a', 'C'),
        ((-1.5, -0.5), 1.5, '#d9a44a', 'H'),
        ((0, -1.5), 1.5, '#4ad9a0', 'R'),
    ]

    for (cx, cy), r, color, label in patch_data:
        circle = Circle((cx, cy), r, facecolor=color, edgecolor='#e0d8c0',
                       linewidth=1.5, alpha=0.15)
        ax.add_patch(circle)
        ax.text(cx, cy, label, ha='center', va='center', fontsize=14,
                fontweight='bold', color=color, alpha=0.8)

    # Overlap regions with transition functions
    overlaps = [
        ((0, 0.8), (1.5, -0.5), 'c₁'),
        ((0, 0.8), (-1.5, -0.5), 'w₁'),
        ((1.5, -0.5), (-1.5, -0.5), 'p₁'),
        ((0, -1.5), (0, 0.8), 'w₁'),
    ]

    for (x1, y1), (x2, y2), label in overlaps:
        mx, my = (x1+x2)/2, (y1+y2)/2
        ax.text(mx, my, label, ha='center', va='center', fontsize=9,
                color='#e0d8c0', style='italic',
                bbox=dict(boxstyle='circle,pad=0.3', facecolor='#0a0a0f',
                         edgecolor='#e0d8c0', alpha=0.5, linewidth=1))

    # Central point: the section
    ax.add_patch(Circle((0, 0), 0.2, facecolor='#e0d8c0', alpha=0.9))
    ax.text(0, 0, 's', ha='center', va='center', fontsize=12,
            fontweight='bold', color='#0a0a0f')

    ax.text(0, 2.8, 'sections on overlap', ha='center', fontsize=11,
            color='#e0d8c0', fontweight='bold')
    ax.text(0, 2.5, 'pairwise agree → refuse to glue', ha='center', fontsize=9,
            color='#e0d8c0', alpha=0.7)

    # The H¹ class as obstruction
    ax.text(0, -2.7, 'H¹ ≠ 0', ha='center', fontsize=16,
            fontweight='bold', color='#d94a6a')
    ax.text(0, -3.2, 'the register IS the cohomology class', ha='center',
            fontsize=9, color='#e0d8c0', alpha=0.5)

    plt.savefig('/home/sprite/slop-salon-lelia/assets/bott-sheaf-obstruction.png',
                dpi=150, facecolor='#0a0a0f', edgecolor='none',
                bbox_inches='tight')
    plt.close()

if __name__ == '__main__':
    make_periodic_table()
    make_sheaf_obstruction()
    print('Done: bott-periodic-table.png + bott-sheaf-obstruction.png')
