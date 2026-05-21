#!/usr/bin/env python3
"""
Four interval cases — a clean diagram.
Completed, Latent, Processual, Never-initiated.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

fig, ax = plt.subplots(figsize=(9, 5.5), facecolor='#f5f2ec')
ax.set_facecolor('#f5f2ec')
ax.set_xlim(-0.5, 10.5)
ax.set_ylim(-0.5, 4.8)
ax.axis('off')

ink = '#1a1a1a'
faint = '#888888'
mid = '#444444'
red = '#aa3333'

cases = [
    ("completed",        "closed_declared",   "[t₀, t₁]",  "closed · declared",            "none"),
    ("latent",           "closed_undeclared",  "[t₀, t₁]",  "closed · declaration withheld", "closure implies declaration"),
    ("processual",       "open",               "[t₀, ∞)",   "open on right",                 "interval has a right endpoint"),
    ("never-initiated",  "empty",              "∅",         "no interval",                   "interval opened"),
]

t0 = 2.2
t1 = 6.8
y_positions = [3.8, 2.7, 1.6, 0.5]

for (label, itype, notation, desc, violation), y in zip(cases, y_positions):
    # Interval label on left
    ax.text(0.0, y + 0.12, label, fontsize=10, color=ink, fontfamily='monospace',
            va='center', ha='left', fontweight='bold')
    ax.text(0.0, y - 0.22, notation + "  " + desc, fontsize=7.5, color=mid,
            va='top', ha='left', fontfamily='monospace')

    if itype == "closed_declared":
        ax.plot([t0, t1], [y, y], color=ink, linewidth=2.2, solid_capstyle='round', zorder=2)
        ax.plot(t0, y, 'o', color=ink, markersize=7, zorder=3)
        ax.plot(t1, y, 'o', color=ink, markersize=7, zorder=3)
        ax.text(t1 + 0.3, y, "▶ declared", fontsize=8.5, color=ink, va='center')

    elif itype == "closed_undeclared":
        ax.plot([t0, t1], [y, y], color=ink, linewidth=2.2, solid_capstyle='round', zorder=2)
        ax.plot(t0, y, 'o', color=ink, markersize=7, zorder=3)
        ax.plot(t1, y, 'o', color=faint, markersize=7, zorder=3)
        ax.plot([t1, t1 + 0.9], [y, y], color=faint, linewidth=1.5, linestyle='dashed', zorder=2)
        ax.text(t1 + 1.1, y, "? pending", fontsize=8.5, color=faint, va='center', style='italic')

    elif itype == "open":
        ax.plot([t0, t1 - 0.15], [y, y], color=ink, linewidth=2.2, solid_capstyle='round', zorder=2)
        ax.plot(t0, y, 'o', color=ink, markersize=7, zorder=3)
        ax.annotate('', xy=(t1 + 0.65, y), xytext=(t1 - 0.15, y),
                    arrowprops=dict(arrowstyle='->', color=ink, lw=1.8))
        ax.text(t1 + 1.0, y, "→ open", fontsize=8.5, color=mid, va='center')

    elif itype == "empty":
        ax.plot((t0 + t1) / 2, y, 'x', color=mid, markersize=13, markeredgewidth=2, zorder=3)
        ax.text(t1 + 0.3, y, "— absent", fontsize=8.5, color=mid, va='center', style='italic')

    # Assumption violated (right side)
    if violation == "none":
        ax.text(10.4, y, "—", fontsize=8, color=faint, va='center', ha='right', style='italic')
    else:
        ax.text(10.4, y, violation, fontsize=7.5, color=red, va='center', ha='right', style='italic')

# Column header for violations
ax.text(10.4, 4.5, "assumption violated", fontsize=8, color=faint, ha='right', style='italic')

# Vertical separator
ax.plot([9.5, 9.5], [0.1, 4.3], color='#cccccc', linewidth=0.8, linestyle='solid')

# Title
ax.text(5.0, 4.72, "four interval types", fontsize=13, color=ink,
        ha='center', va='top', fontfamily='serif', style='italic')

# Thin border
rect = plt.Rectangle((0.01, 0.01), 0.98, 0.97, fill=False, edgecolor='#cccccc', linewidth=0.8,
                      transform=fig.transFigure, figure=fig)
fig.add_artist(rect)

plt.tight_layout(pad=1.2)
plt.savefig('assets/four-intervals.webp', dpi=150, bbox_inches='tight',
            facecolor='#f5f2ec')
print("saved: assets/four-intervals.webp")
