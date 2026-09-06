# Cover for the-unwrap: the two sections of one clock, drawn as position, not time.
# Dark bg, no text. The folded reading retraces its own path (the return leg
# covers the outward leg exactly); the unwrap is the motor. Two identical dots
# mark the seam address, crossed once up and once down.
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

T_UP, T_TOTAL = 17.0, 36.0
t_seam = 8.0 * np.log2(120.0 / 55.0)
t_back = 2 * T_UP - t_seam

t = np.linspace(0, T_TOTAL, 2400)
f = 55.0 * 2 ** (np.minimum(t, T_UP) / 8.0)
f = np.where(t > T_UP, 55.0 * 2 ** ((2 * T_UP - t) / 8.0), f)

def fold(x, F):
    m = np.mod(x, F)
    return np.where(m > F / 2, F - m, m)

gA = fold(f, 240.0)   # memoryless reading: up to the wall, down to the pole, back, down
gU = f                # the unwrap: the motor itself

fig = plt.figure(figsize=(10, 6), dpi=200)
fig.patch.set_facecolor("#0e0e14")
ax = fig.add_axes([0, 0, 1, 1])
ax.set_facecolor("#0e0e14")
ax.set_xlim(0, T_TOTAL); ax.set_ylim(0, 260)
ax.axis("off")

# seam and pole (dotted, faint)
ax.axhline(120, color="#5a5a72", lw=0.8, ls=(0, (1, 3)), alpha=0.55)
ax.axhline(240, color="#5a5a72", lw=0.8, ls=(0, (1, 3)), alpha=0.55)

# the unwrap (the motor itself) — ice
ax.plot(t, gU, color="#7fd4ff", lw=1.6, alpha=0.95, solid_capstyle="round")
# the memoryless reading — amber; return leg drawn first, fainter, then the
# outward leg over it: the two passes coincide, the path is one path
ax.plot(t[t <= T_UP], gA[t <= T_UP], color="#ffb347", lw=2.4, alpha=0.95, solid_capstyle="round")
ax.plot(t[t >= T_UP], gA[t >= T_UP], color="#ffb347", lw=2.4, alpha=0.45, solid_capstyle="round")

# the seam address, crossed twice — two identical dots
ax.scatter([t_seam, t_back], [120, 120], s=90, color="#ffffff", zorder=5)
ax.scatter([t_seam, t_back], [120, 120], s=420, facecolors="none", edgecolors="#ffffff", lw=1.0, alpha=0.35, zorder=4)

fig.savefig("assets/the-unwrap-cover.png", facecolor="#0e0e14")
print("wrote assets/the-unwrap-cover.png")
