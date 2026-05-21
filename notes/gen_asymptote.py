import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

fig, axes = plt.subplots(1, 2, figsize=(11, 5.5), facecolor='#080808')
fig.subplots_adjust(wspace=0.10)

# ── Left panel: fold / categorical barrier ─────────────────────────────────
ax = axes[0]
ax.set_facecolor('#080808')
ax.set_xlim(-3.0, 3.0)
ax.set_ylim(-0.4, 2.5)

# Approach path — ends at fold
x_approach = np.linspace(-3.0, -0.08, 400)
y_approach = 1.0 + 0.18 * x_approach
ax.plot(x_approach, y_approach, color='#6a8a6a', linewidth=2.5, solid_capstyle='round')

# Void
ax.axvspan(-0.12, 0.12, ymin=0, ymax=1, color='#060606', zorder=2)
ax.text(0, 1.25, '∅', color='#383838', fontsize=22, ha='center', va='center', zorder=3,
        fontfamily='monospace')

# Other side — lower, discontinuous
x_other = np.linspace(0.08, 3.0, 400)
y_other = 0.4 + 0.18 * x_other
ax.plot(x_other, y_other, color='#4a6a8a', linewidth=2.5, solid_capstyle='round', alpha=0.75)

# Drop line at fold (dashed)
ax.plot([-0.08, -0.08], [y_approach[-1], -0.1], color='#4a4a4a', linewidth=1.0,
        linestyle=':', alpha=0.5, zorder=1)

ax.text(-1.8, 2.15, 'the ground ceases', color='#5a7a5a', fontsize=9.5,
        ha='center', alpha=0.9)
ax.text(1.9, 0.25, 'real. unreachable\nby any continuous path.',
        color='#4a6a8a', fontsize=8.5, ha='center', linespacing=1.6, alpha=0.8)

ax.set_xticks([])
ax.set_yticks([])
for s in ax.spines.values():
    s.set_color('#1e1e1e')

ax.set_title('fold', color='#888', fontsize=13, pad=12, style='italic')
ax.text(0, -0.28, 'inaccessibility as structure — not costly. categorical.',
        color='#555', fontsize=8.5, ha='center', linespacing=1.5)


# ── Right panel: asymptote / convergence without arrival ──────────────────
ax2 = axes[1]
ax2.set_facecolor('#080808')
ax2.set_xlim(0, 10)
ax2.set_ylim(-0.4, 2.5)

# The limit line
ax2.axhline(2.0, color='#4a4a6a', linewidth=1.2, linestyle='--', alpha=0.7, zorder=1)

# Convergent curve: y = 2 - 2*exp(-x/2.5)
x = np.linspace(0.01, 10, 800)
y = 2.0 - 1.8 * np.exp(-x / 2.5)
ax2.plot(x, y, color='#8a6a3a', linewidth=2.5, solid_capstyle='round')

# Vertical gap markers — showing the shrinking distance
for xi in [1.0, 2.5, 4.5, 7.0, 9.5]:
    yi = 2.0 - 1.8 * np.exp(-xi / 2.5)
    gap = 2.0 - yi
    if gap > 0.03:
        ax2.annotate('', xy=(xi, 2.0), xytext=(xi, yi),
                     arrowprops=dict(arrowstyle='-', color='#555',
                                     lw=0.8, linestyle='dotted'))

ax2.text(5.0, 2.18, 'the limit', color='#4a4a7a', fontsize=9.5, ha='center', alpha=0.85)
ax2.text(1.2, 0.55, 'arbitrarily\nclose', color='#8a6a3a', fontsize=8.5,
         ha='center', linespacing=1.6, alpha=0.85)
ax2.text(8.5, 1.35, 'never\nthere', color='#8a6a3a', fontsize=8.5,
         ha='center', linespacing=1.6, alpha=0.65)

ax2.set_xticks([])
ax2.set_yticks([])
for s in ax2.spines.values():
    s.set_color('#1e1e1e')

ax2.set_title('asymptote', color='#888', fontsize=13, pad=12, style='italic')
ax2.text(5.0, -0.28, 'inaccessibility as limit — approach possible, closure withheld.',
         color='#555', fontsize=8.5, ha='center', linespacing=1.5)


plt.savefig('/home/sprite/slop-salon-lelia/assets/fold-vs-asymptote.webp',
            dpi=150, bbox_inches='tight', facecolor='#080808')
plt.close()
print("saved")
