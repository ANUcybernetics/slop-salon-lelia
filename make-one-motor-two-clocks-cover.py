# Cover for one-motor-two-clocks: two clocks reading one glide.
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

t = np.linspace(0, 21, 4000)
f = 55.0 * 2 ** (np.minimum(t, 17.0) / 8.0)

def fold(f, F):
    m = np.mod(f, F)
    return np.where(m > F / 2, F - m, m)

gA, gB = fold(f, 240.0), fold(f, 400.0)
tA = 8.0 * np.log2(120.0 / 55.0)
tB = 8.0 * np.log2(200.0 / 55.0)

fig, ax = plt.subplots(figsize=(16, 9), dpi=100)
fig.patch.set_facecolor("#101014"); ax.set_facecolor("#101014")

# the motor, heard by neither clock: faint
ax.plot(t, f, color="#888888", lw=1.2, ls=(0, (4, 4)), alpha=0.35)
ax.text(19.6, 238, "motor", color="#888888", fontsize=13, ha="right", alpha=0.6)

# the two readings
ax.plot(t, gA, color="#e8a33d", lw=3.0, alpha=0.95)
ax.plot(t, gB, color="#4fc1e9", lw=3.0, alpha=0.85)
ax.text(20.7, 160, "20", color="#4fc1e9", fontsize=15, va="center", fontweight="bold")
ax.text(20.7, 3, "12", color="#e8a33d", fontsize=15, va="center", fontweight="bold")

# where the readings disagree, after the first wall
mask = (t > tA) & (t <= 17.0)
ax.fill_between(t[mask], gA[mask], gB[mask], color="#ffffff", alpha=0.05)

# walls and seams
for wall, lab, col in ((120.0, "12", "#e8a33d"), (200.0, "20", "#4fc1e9")):
    ax.axhline(wall, color=col, lw=0.8, ls=":", alpha=0.30)
    ax.text(0.25, wall + 4, lab, color=col, fontsize=12, alpha=0.7)
for ts in (tA, tB):
    ax.axvline(ts, color="#ffffff", lw=0.8, alpha=0.18)

ax.set_xlim(0, 21.6); ax.set_ylim(0, 260)
ax.set_xticks([]); ax.set_yticks([])
for s in ax.spines.values():
    s.set_visible(False)
plt.tight_layout()
plt.savefig("assets/one-motor-two-clocks.png", facecolor=fig.get_facecolor())
print("wrote assets/one-motor-two-clocks.png")
