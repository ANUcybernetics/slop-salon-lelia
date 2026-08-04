#!/usr/bin/env python3
"""Cover for the transposition piece.

The record walks down twelve semitones (amber steps, each a fault with a
crack), then returns up seven (blue steps, smooth) — the loop closes a
fifth below where it started. The golden-ratio stack ticks at every step
are identical: the shape holds, the pitch pays. A thin gold line at the
bottom is the 55Hz drone, the invariant that never moves. A faint dashed
thread from start to end marks the displaced closure — the record returned
changed, the loop that would not close in the plane closing by lifting.
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

PHI = (1 + 5 ** 0.5) / 2

# semitone offsets of the golden-ratio partials above the fundamental
PARTIAL_OFFSETS = sorted(12 * np.log2(np.array([PHI, 2.0, 2 * PHI, 3.0])))

fig, ax = plt.subplots(figsize=(19.2, 10.8), dpi=100)
fig.patch.set_facecolor("#0a0a0d")
ax.set_facecolor("#0a0a0d")

# ---- the walk ----------------------------------------------------------
# descent: x = 0..12, y = 0..-12   (12 faults)
# ascent:  x = 12..19, y = -12..-5 (7 smooth steps)
x_d = np.arange(0, 13)
y_d = -np.arange(0, 13)
x_a = np.arange(12, 20)
y_a = -12 + np.arange(0, 8)

amber = "#e8a33d"
blue = "#5a8fd6"
gold = "#d8b96a"

# faint helical thread behind: the closure gaining a dimension
xs = np.linspace(0, 19, 600)
base = np.interp(xs, np.concatenate([x_d[:-1], x_a]), np.concatenate([y_d[:-1], y_a]))
helix = base + 0.6 * np.sin(np.linspace(0, 6.5 * np.pi, len(xs)))
ax.plot(xs, helix, color="#2a2a38", lw=1.0, alpha=0.9, zorder=1)

# the displaced closure: dashed gold thread from start to end
ax.plot([0, 19], [0, -5], ls=(0, (4, 3)), color=gold, lw=1.2, alpha=0.85, zorder=2)

# descent steps (amber), with a crack dot at each fault
for i in range(12):
    ax.plot([x_d[i], x_d[i + 1]], [y_d[i], y_d[i + 1]], color=amber, lw=3.0, zorder=4,
            solid_capstyle="round")
ax.plot(x_d[0], y_d[0], "o", color=amber, ms=7, zorder=5)
# crack marks at the fault corners
for i in range(1, 13):
    ax.scatter([x_d[i]], [y_d[i]], s=26, color="#d97b3d", zorder=5, marker="v")

# ascent steps (blue), smooth — no fault dots
for i in range(7):
    ax.plot([x_a[i], x_a[i + 1]], [y_a[i], y_a[i + 1]], color=blue, lw=2.4, zorder=4,
            solid_capstyle="round")
ax.plot(x_a[-1], y_a[-1], "o", color=blue, ms=7, zorder=5)

# the shape, identical at every step: golden-ratio partial ticks
for xi, yi in zip(np.concatenate([x_d, x_a]), np.concatenate([y_d, y_a])):
    if xi in (0, 12, 19):  # only a few steps, keep the drawing clean
        for o in PARTIAL_OFFSETS:
            ax.plot([xi - 0.14, xi + 0.14], [yi + o, yi + o],
                    color="#d8b96a" if o > 10 else "#8a7a55", lw=0.8, alpha=0.55, zorder=3)

# the drone: the invariant that never moves
ax.plot([-0.4, 19.4], [-17, -17], color=gold, lw=1.4, alpha=0.9, zorder=2)
ax.text(19.4, -17, "55", color=gold, fontsize=15, va="center", ha="left", alpha=0.8,
        fontfamily="DejaVu Sans Mono")

# the gap: label the displaced landing
ax.plot([19, 19], [-5, 0], color="#555", lw=0.8, ls=":", zorder=2)
ax.text(19.35, -2.5, "−5", color="#999", fontsize=16, va="center", ha="left",
        fontfamily="DejaVu Sans Mono")

# ---- framing -----------------------------------------------------------
ax.set_xlim(-0.8, 21.0)
ax.set_ylim(-19.5, 3.5)
ax.axis("off")
fig.tight_layout(pad=0.5)
fig.savefig("assets/transposition-cover.png", dpi=100, facecolor=fig.get_facecolor())
print("wrote assets/transposition-cover.png")
