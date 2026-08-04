#!/usr/bin/env python3
"""Cover: three walks of twelve fifths on the pitch circle.

left   — pure: the walk steps a just fifth each time and lands a comma
         short of closing. the gap is the seam.
center — tempered: the walk lands exactly on its start. closed.
right  — irrational: the walk unwrapped — it never comes home, a line
         rising without return. the universal cover.

Black field, amber lines, the register's mineral palette.
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BLACK = "#0a0a0a"
AMBER = "#e8a33d"
DIM = "#8a6a3a"
PALE = "#f5d9a0"

fig, axes = plt.subplots(1, 3, figsize=(15, 5.2),
                         subplot_kw=dict(aspect="equal"))
fig.patch.set_facecolor(BLACK)


def draw_circle(ax):
    th = np.linspace(0, 2 * np.pi, 400)
    ax.plot(np.cos(th), np.sin(th), color=DIM, lw=1.4)
    ax.plot(1.0, 0.0, marker="o", color=PALE, ms=7)  # the start / home


def walk_points(step_log2, n):
    ang = np.cumsum([0] + [step_log2 % 1.0] * n) % 1.0
    return ang * 2 * np.pi


# ---- left: pure ----------------------------------------------------------
ax = axes[0]
draw_circle(ax)
log2_3 = np.log2(3.0)              # 1.58496...  the just fifth
ang = walk_points(log2_3, 12)      # 12 steps, folded mod octave
pts = np.exp(1j * ang)
ax.plot(pts.real, pts.imag, color=AMBER, lw=1.0, alpha=0.45)
ax.scatter(pts.real[:-1], pts.imag[:-1], color=AMBER, s=26, zorder=3)
# final point lands just past home — the seam
ax.scatter(pts.real[-1], pts.imag[-1], color=PALE, s=60, zorder=4)
# the comma gap: arc from the home point to the final point
gap0 = 0.0
gap1 = ang[-1]
g = np.linspace(gap0, gap1, 60)
ax.plot(np.cos(g), np.sin(g), color=PALE, lw=2.2, zorder=5)
ax.annotate("the comma", xy=(np.cos((gap0 + gap1) / 2) * 1.14,
                             np.sin((gap0 + gap1) / 2) * 1.14),
            color=PALE, fontsize=10, ha="center")
ax.set_title("pure — a delta\none lump at the seam", color=PALE, fontsize=12)

# ---- center: tempered ----------------------------------------------------
ax = axes[1]
draw_circle(ax)
temp_log2 = 7.0 / 12.0             # the equal-tempered fifth
ang = walk_points(temp_log2, 12)
pts = np.exp(1j * ang)
ax.plot(pts.real, pts.imag, color=AMBER, lw=1.0, alpha=0.45)
ax.scatter(pts.real, pts.imag, color=AMBER, s=26, zorder=3)
# lands exactly on home — closed ring, hair spread through every step
ax.scatter(pts.real[-1], pts.imag[-1], color=PALE, s=60, zorder=4)
# faint inner ring of hairs — the distributed comma
hair_r = 0.82
hair_th = np.linspace(0, 2 * np.pi, 48)
ax.scatter(hair_r * np.cos(hair_th), hair_r * np.sin(hair_th),
           color=AMBER, s=3, alpha=0.7, zorder=2)
ax.set_title("tempered — a density\na hair into every fifth", color=PALE, fontsize=12)

# ---- right: irrational ---------------------------------------------------
ax = axes[2]
# unwrapped: the universal cover. steps climb, never returning to a phase.
log2_step = 7.0 / 12.0 + 2.0 ** 0.5 / 1000.0
k = np.arange(0, 30)
phase = k * log2_step            # unwrapped — no mod 1
x = k
y = phase * 2 * np.pi / 8.0
ax.plot(x, y, color=AMBER, lw=1.4)
ax.scatter(x, y, color=AMBER, s=22, zorder=3)
# the home line the walk never crosses back to
ax.axhline(0, color=DIM, lw=1.0, ls="--")
# a gap arrow showing the walk is past where 7 octaves would be
ax.annotate("", xy=(12, y[12]), xytext=(12, 7 * 2 * np.pi / 8.0),
            arrowprops=dict(arrowstyle="->", color=PALE, lw=1.6))
ax.text(12.4, (y[12] + 7 * 2 * np.pi / 8.0) / 2, "the comma",
        color=PALE, fontsize=10, rotation=90, va="center")
ax.set_ylim(-0.8, 16)
ax.set_xlim(-1, 30)
ax.set_title("irrational — no loop\nmonodromy undefined", color=PALE, fontsize=12)

for ax in axes:
    ax.set_facecolor(BLACK)
    ax.set_xticks([])
    ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)

plt.tight_layout(pad=1.2)
plt.savefig("./assets/comma-walks-cover.png", dpi=140, facecolor=BLACK)
print("wrote assets/comma-walks-cover.png")
