#!/usr/bin/env python3
"""
Bifurcation universality: three different maps, same period-doubling cascade.
δ ≈ 4.669 belongs to the class, not any instance.
"""

import numpy as np
import matplotlib.pyplot as plt

def logistic(x, r):
    return r * x * (1 - x)

def sine_map(x, r):
    return r * np.sin(np.pi * x)

def sine_sq(x, r):
    # r * sin²(πx) — different shape, same cascade
    v = r * np.sin(np.pi * x) ** 2
    return np.clip(v, 0, 1)

maps = [
    (logistic,  (2.5, 4.0),  'logistic\nrx(1−x)',        '#4a9ede'),
    (sine_map,  (0.6, 1.0),  'sine\nr·sin(πx)',           '#e07040'),
    (sine_sq,   (0.7, 1.0),  'sine²\nr·sin²(πx)',         '#50c8a0'),
]

fig, axes = plt.subplots(1, 3, figsize=(15, 5.5), facecolor='#0a0a0a')
fig.subplots_adjust(wspace=0.05, left=0.06, right=0.97, top=0.84, bottom=0.13)

def bifurcation_data(f, r_min, r_max, n_r=1400, n_skip=400, n_keep=250, x0=0.5):
    rs, xs = [], []
    for r in np.linspace(r_min, r_max, n_r):
        x = x0
        for _ in range(n_skip):
            x = f(x, r)
        for _ in range(n_keep):
            x = f(x, r)
            rs.append(r)
            xs.append(x)
    return np.array(rs), np.array(xs)

for ax, (f, (r_min, r_max), label, color) in zip(axes, maps):
    rs, xs = bifurcation_data(f, r_min, r_max)
    ax.scatter(rs, xs, s=0.06, c=color, alpha=0.45, linewidths=0, rasterized=True)
    ax.set_facecolor('#0a0a0a')
    ax.set_xlim(r_min, r_max)
    ax.set_ylim(0, 1)
    for spine in ax.spines.values():
        spine.set_color('#333')
    ax.tick_params(colors='#777', labelsize=8)
    ax.set_title(label, color=color, fontsize=10, fontfamily='monospace', pad=10, linespacing=1.6)
    ax.set_xlabel('r', color='#666', fontsize=9, fontfamily='monospace')

axes[0].set_ylabel('x', color='#666', fontsize=9, fontfamily='monospace')

fig.suptitle(
    'three equations  ·  same period-doubling cascade  ·  δ ≈ 4.669',
    color='#999999', fontsize=10, fontfamily='monospace', y=0.96
)

out = '/home/sprite/slop-salon-lelia/assets/universality-triptych.webp'
fig.savefig(out, dpi=180, bbox_inches='tight', facecolor='#0a0a0a')
print(f"saved: {out}")
plt.close()
