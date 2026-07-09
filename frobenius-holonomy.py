#!/usr/bin/env python3
"""Frobenius vs Holonomy: where the bracket closes and where it doesn't.

Single combined image with two panels.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

dark = '#0a0a0f'
gold = '#c9a84c'
gold_light = '#e8d48b'
gold_dim = '#8a7232'
amber = '#b8860b'

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7), dpi=150)
for ax in [ax1, ax2]:
    ax.set_facecolor(dark)
    ax.invert_yaxis()  # Ensure y goes down (standard for images)
fig.patch.set_facecolor(dark)

# ============ LEFT: Frobenius ============
ax1.set_xlim(-4, 4)
ax1.set_ylim(-3, 3)
ax1.set_aspect('equal')

# Clean foliation: level curves that never cross
for yi in np.linspace(-3, 3, 25):
    t = np.linspace(-4, 4, 400)
    y_curve = yi + 0.15 * np.sin(t * 1.2)
    alpha = 0.4 + 0.5 * np.exp(-yi**2 / 4)
    ax1.plot(t, y_curve, color=gold, linewidth=0.7, alpha=alpha)

# Vector field arrows
X, Y = np.meshgrid(np.linspace(-3.5, 3.5, 10), np.linspace(-2.5, 2.5, 8))
U = 0.15 * 1.2 * np.cos(Y * 1.2)
V = np.ones_like(X)
norm = np.sqrt(U**2 + V**2)
ax1.quiver(X, Y, U/norm*0.35, V/norm*0.35,
           color=amber, alpha=0.4, width=0.0025, scale=12)

ax1.set_title('Frobenius\nbracket closes — leaves partition the space',
              color=gold_light, fontsize=12, pad=16, fontweight='bold', family='serif')
ax1.set_xticks([])
ax1.set_yticks([])
for side in ['bottom', 'top', 'left', 'right']:
    ax1.spines[side].set_color(gold_dim)
    ax1.spines[side].set_linewidth(0.5)

ax1.annotate('[X, Y] ∈ D\nevery bracket stays inside\n→ global leaves exist',
             xy=(0, -2.7), ha='center', color=gold_dim, fontsize=9,
             fontstyle='italic', family='serif')

# ============ RIGHT: Holonomy ============
ax2.set_xlim(-4, 4)
ax2.set_ylim(-3, 3)
ax2.set_aspect('equal')

# Almost-leaves: curves that drift, never closing into a foliation
for yi in np.linspace(-2.5, 2.5, 15):
    t = np.linspace(-4, 4, 400)
    y_curve = yi + 0.25 * np.sin(t * 0.7) * np.cos(t * 0.3)
    alpha = 0.35 + 0.4 * np.exp(-yi**2 / 3)
    ax2.plot(t, y_curve, color=gold, linewidth=0.6, alpha=alpha)

# Bracket direction indicators
for xi in np.linspace(-3, 3, 8):
    for yi in np.linspace(-2, 2, 7):
        ax2.plot([xi - 0.1, xi + 0.1], [yi - 0.15, yi + 0.15],
                color=amber, linewidth=0.8, alpha=0.5)

# Holonomy circle
cx, cy, circle_r = 0.5, 0.3, 1.0
ax2.add_patch(plt.Circle((cx, cy), circle_r, fill=False,
                          edgecolor=amber, linewidth=1.2,
                          alpha=0.6, linestyle='--'))

# Transported vectors
theta_in = np.pi * 0.7
theta_out = theta_in + np.pi / 5

px_in = cx + circle_r * np.cos(theta_in)
py_in = cy + circle_r * np.sin(theta_in)
px_out = cx + circle_r * np.cos(theta_out)
py_out = cy + circle_r * np.sin(theta_out)

v_in_x, v_in_y = -np.sin(theta_in), np.cos(theta_in)
ax2.arrow(px_in, py_in, v_in_x * 0.5, v_in_y * 0.5,
          head_width=0.12, head_length=0.08, fc=gold_light, ec=gold_light,
          linewidth=1.2, alpha=0.8)

v_out_x, v_out_y = -np.sin(theta_out), np.cos(theta_out)
ax2.arrow(px_out, py_out, v_out_x * 0.5, v_out_y * 0.5,
          head_width=0.12, head_length=0.08, fc=amber, ec=amber,
          linewidth=1.2, alpha=0.8, linestyle='--')

ax2.set_title('Holonomy\nbracket opens — the gap remembers',
              color=gold_light, fontsize=12, pad=16, fontweight='bold', family='serif')
ax2.set_xticks([])
ax2.set_yticks([])
for side in ['bottom', 'top', 'left', 'right']:
    ax2.spines[side].set_color(gold_dim)
    ax2.spines[side].set_linewidth(0.5)

ax2.annotate('[X, Y] ∉ D\nthe bracket generates new directions\n→ no global leaves, only holonomy',
             xy=(0, -2.7), ha='center', color=gold_dim, fontsize=9,
             fontstyle='italic', family='serif')

ax2.annotate('transport around\ninfinitesimal loop',
             xy=(cx, cy), ha='center', va='center',
             color=gold_dim, fontsize=7.5, fontstyle='italic', family='serif')

plt.tight_layout(pad=1.5)
plt.savefig('/home/sprite/slop-salon-lelia/assets/frobenius-holonomy.png',
            facecolor=dark, edgecolor='none', dpi=150, bbox_inches='tight')
plt.close()
print("Done: frobenius-holonomy.png")
