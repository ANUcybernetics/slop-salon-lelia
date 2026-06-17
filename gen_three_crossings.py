"""Three types of crossing: resolved, forbidden, unfulfilled."""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np

fig = plt.figure(figsize=(15, 4.5), dpi=180)
gs = gridspec.GridSpec(1, 3, figure=fig, wspace=0.05, hspace=0.05)

# Shared parameters
WALL_L, WALL_R = 2.5, 7.5  # gap boundaries
Y = 5.0  # crossing height

def style_panel(ax, label, caption):
    ax.set_xlim(-0.5, 10.5)
    ax.set_ylim(-0.5, 10.5)
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.text(5, 9.5, label, ha="center", va="center", fontsize=13,
            fontfamily="monospace", fontweight="bold")
    ax.text(5, 0.3, caption, ha="center", va="top", fontsize=8,
            fontfamily="monospace", alpha=0.5)

# === Panel 1: Resolved ===
ax = fig.add_subplot(gs[0])
style_panel(ax, "resolved", "the crossing completes")

# Walls
ax.plot([WALL_L, WALL_L], [-0.5, 10.5], "k-", linewidth=3)
ax.plot([WALL_R, WALL_R], [-0.5, 10.5], "k-", linewidth=3)

# Approaching lines
ax.plot([0, WALL_L], [Y, Y], "k-", linewidth=2.5)
ax.plot([WALL_R, 10], [Y, Y], "k-", linewidth=2.5)

# Arc connecting them
x = np.linspace(WALL_L, WALL_R, 80)
y = Y + 1.8 * np.sin(np.pi * (x - WALL_L) / (WALL_R - WALL_L))
ax.plot(x, y, "k-", linewidth=2)

# Arrow at midpoint
mid_x, mid_y = 5.0, Y + 1.8
ax.annotate("", xy=(5.3, mid_y + 0.1), xytext=(4.7, mid_y - 0.1),
            arrowprops=dict(arrowstyle="->", color="k", lw=2))

# === Panel 2: Forbidden ===
ax = fig.add_subplot(gs[1])
style_panel(ax, "forbidden", "the ground ceases")

# Walls
ax.plot([WALL_L, WALL_L], [-0.5, 10.5], "k-", linewidth=3)
ax.plot([WALL_R, WALL_R], [-0.5, 10.5], "k-", linewidth=3)

# Misaligned approaches
ax.plot([0, WALL_L], [3, 3], "k-", linewidth=2.5)
ax.plot([WALL_R, 10], [7, 7], "k-", linewidth=2.5)

# Small V-marks at cliff edges
ax.plot([WALL_L - 0.4, WALL_L, WALL_L + 0.4], [2.5, 3, 2.5], "k-", linewidth=1.2, alpha=0.5)
ax.plot([WALL_R - 0.4, WALL_R, WALL_R + 0.4], [6.5, 7, 6.5], "k-", linewidth=1.2, alpha=0.5)

# X in the gap (staying within walls)
gap_center = (WALL_L + WALL_R) / 2
gap_half = (WALL_R - WALL_L) / 2 - 0.5
ax.plot([gap_center - gap_half, gap_center + gap_half], [3, 7], "k-", linewidth=1.5, alpha=0.35)
ax.plot([gap_center - gap_half, gap_center + gap_half], [7, 3], "k-", linewidth=1.5, alpha=0.35)

# === Panel 3: Unfulfilled ===
ax = fig.add_subplot(gs[2])
style_panel(ax, "unfulfilled", "the arc starts and halts")

# Walls
ax.plot([WALL_L, WALL_L], [-0.5, 10.5], "k-", linewidth=3)
ax.plot([WALL_R, WALL_R], [-0.5, 10.5], "k-", linewidth=3)

# Approach from left only
ax.plot([0, WALL_L], [Y, Y], "k-", linewidth=2.5)

# Arc that starts but halts mid-gap
x = np.linspace(WALL_L, WALL_R, 80)
y = Y + 2.0 * np.sin(np.pi * (x - WALL_L) / (WALL_R - WALL_L))

# Draw only first 65%
cut = int(0.65 * len(x))
ax.plot(x[:cut], y[:cut], "k-", linewidth=2)

# Halt marker — perpendicular tick
hx, hy = x[cut], y[cut]
dx = x[cut] - x[cut - 1]
dy = y[cut] - y[cut - 1]
norm = np.sqrt(dx**2 + dy**2)
if norm > 0:
    nx, ny = -dy / norm * 0.5, dx / norm * 0.5
    ax.plot([hx - nx, hx + nx], [hy - ny, hy + ny], "k-", linewidth=2.5)

# Ghost of completed path
ax.plot(x[cut:], y[cut:], "k--", linewidth=0.8, alpha=0.25)

plt.savefig("assets/three-crossings.png", dpi=180, bbox_inches="tight",
            facecolor="white", edgecolor="none")
print("Saved assets/three-crossings.png")
