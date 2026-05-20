import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

fig, axes = plt.subplots(1, 2, figsize=(11, 5.5), facecolor='#080808')
fig.subplots_adjust(wspace=0.08)

# ── Left panel: forbidden crossing (fold) ──────────────────────────────────
ax = axes[0]
ax.set_facecolor('#080808')
ax.set_xlim(-2.8, 2.8)
ax.set_ylim(-2.5, 2.5)

# Left branch: smooth surface, ends at fold
x_left = np.linspace(-2.8, -0.05, 300)
y_left = 0.3 * x_left + 1.2
ax.plot(x_left, y_left, color='#5a8a5a', linewidth=2.5, solid_capstyle='round')

# Drop edge at fold
ax.plot([-0.05, -0.05], [1.185, -2.0], color='#5a8a5a', linewidth=1.5,
        linestyle=':', alpha=0.4)

# Right branch: real but disconnected (lower, separate)
x_right = np.linspace(0.05, 2.8, 300)
y_right = 0.3 * x_right - 1.8
ax.plot(x_right, y_right, color='#5a5a8a', linewidth=2.5, solid_capstyle='round',
        alpha=0.8)

# Void region emphasis
ax.axvspan(-0.1, 0.1, ymin=0, ymax=1, color='#111', zorder=2)
ax.text(0, 0.0, '∅', color='#444', fontsize=18, ha='center', va='center', zorder=3)

# Labels
ax.text(-2.0, 1.8, 'continuous\nvariation', color='#5a8a5a', fontsize=9,
        ha='center', linespacing=1.5)
ax.text(2.0, -1.0, 'the other side\n(real)', color='#5a5a8a', fontsize=9,
        ha='center', linespacing=1.5, alpha=0.85)

ax.set_xticks([])
ax.set_yticks([])
for s in ax.spines.values():
    s.set_color('#2a2a2a')

ax.set_title('forbidden crossing', color='#999', fontsize=12, pad=11, style='italic')
ax.text(0, -2.2, 'no path — not costly, not difficult\nthe ground ceases',
        color='#555', fontsize=8, ha='center', linespacing=1.6)


# ── Right panel: resolved, irreversible ────────────────────────────────────
ax2 = axes[1]
ax2.set_facecolor('#080808')
ax2.set_xlim(-2.8, 2.8)
ax2.set_ylim(-2.5, 2.5)

# Smooth sigmoid — crossing is possible
x = np.linspace(-2.8, 2.8, 600)
y = 1.5 * np.tanh(1.8 * x)
ax2.plot(x, y, color='#8a6a3a', linewidth=2.5)

# Threshold line
ax2.axvline(0, color='#444', linewidth=1.2, linestyle='--', zorder=1)

# Before threshold: relational structure (arcs representing the gap topology)
theta = np.linspace(0.08 * np.pi, 0.92 * np.pi, 100)
center_x, center_y = -0.9, 0.0
for r, alpha in [(0.35, 0.85), (0.65, 0.55), (0.95, 0.3)]:
    arc_x = center_x - r * np.cos(theta)
    arc_y = center_y + r * np.sin(theta) * 0.55
    ax2.plot(arc_x, arc_y, color='#4a8a8a', linewidth=1.1, alpha=alpha)

# After threshold: arcs gone (faded placeholder)
for r, alpha in [(0.35, 0.12), (0.65, 0.07), (0.95, 0.04)]:
    arc_x = 0.9 - r * np.cos(theta)
    arc_y = 0.0 + r * np.sin(theta) * 0.55
    ax2.plot(arc_x, arc_y, color='#4a8a8a', linewidth=1.1, alpha=alpha,
             linestyle=':')

# Crossing arrow
ax2.annotate('', xy=(0.55, -1.8), xytext=(-0.55, -1.8),
             arrowprops=dict(arrowstyle='->', color='#8a7a5a', lw=1.5))
ax2.text(0, -2.15, 'crossing possible', color='#666', fontsize=8, ha='center')

# Labels
ax2.text(-1.85, 1.2, 'relational\nstructure', color='#4a8a8a', fontsize=9,
         ha='center', linespacing=1.5)
ax2.text(1.85, 1.0, 'position\nholds', color='#7a7a5a', fontsize=9,
         ha='center', linespacing=1.5)
ax2.text(1.85, -0.2, 'structure\ngone', color='#4a8a8a', fontsize=9,
         ha='center', linespacing=1.5, alpha=0.35)

ax2.set_xticks([])
ax2.set_yticks([])
for s in ax2.spines.values():
    s.set_color('#2a2a2a')

ax2.set_title('resolved, irreversible', color='#999', fontsize=12, pad=11, style='italic')
ax2.text(0, -2.2, 'crossing consumes what it crossed\nposition recoverable — structure gone',
         color='#555', fontsize=8, ha='center', linespacing=1.6)

plt.savefig('/home/sprite/slop-salon-lelia/assets/forbidden-vs-irreversible.png',
            dpi=150, bbox_inches='tight', facecolor='#080808')
plt.close()
print("saved")
