#!/usr/bin/env python3
"""Cover score for 'the bill of the seam': two rows, one common time axis.

L row: the 3-stitch mend's bill — all three clicks are the universal death-tail
(heights 1/3, 1/2, 1; waits 9,4,1 units).
R row: the 7-stitch mend — 4 dim preamble clicks, then the same bright tail.
The flat line between = the winding (conserved, no lifetime).

Same death, different ages: R's tail is L's row, displaced in time.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

U, TAIL_S = 0.30, 1.5
DUR = sum(m * m for m in range(1, 8)) * U + TAIL_S  # 43.5 s

def bill(n):
    ms = list(range(n, 0, -1))
    return np.cumsum([m * m * U for m in ms]), [1.0 / m for m in ms]

tL, aL = bill(3)
tR, aR = bill(7)

BG, DIM, BRIGHT, WIRE = "#0d0d12", "#3d4a63", "#f0a832", "#6a6a76"
ROW, H = 1.15, 0.9
fig, ax = plt.subplots(figsize=(12, 9), dpi=120)
fig.patch.set_facecolor(BG); ax.set_facecolor(BG)

ax.plot([0, DUR], [0, 0], color=WIRE, lw=1.2)  # the winding

for y, ts, amps, cols in [
        (+ROW, tL, aL, [BRIGHT] * 3),
        (-ROW, tR, aR, [DIM]*4 + [BRIGHT]*3)]:
    for t, a, c in zip(ts, amps, cols):
        ax.plot([t, t], [y, y + a * H], color=c, lw=1.8)
        ax.plot(t, y + a * H, "|", color=c, ms=9, mew=1.8)

ax.annotate("L", (0.012, ROW), xycoords=("axes fraction", "data"),
            color="#c8c8d0", fontsize=16, va="center", fontweight="bold")
ax.annotate("winding", (0.012, 0), xycoords=("axes fraction", "data"),
            color=WIRE, fontsize=12, va="center")
ax.annotate("R", (0.012, -ROW), xycoords=("axes fraction", "data"),
            color="#c8c8d0", fontsize=16, va="center", fontweight="bold")
ax.annotate("0 s", (0.012, -2.0), color="#7a7a84", fontsize=11)
ax.annotate("42 s", (0.962, -2.0), color="#7a7a84", fontsize=11)

ax.set_xlim(0, DUR); ax.set_ylim(-2.1, 2.35)
ax.axis("off")
plt.tight_layout()
plt.savefig("assets/the-bill-of-the-seam-cover.png", facecolor=BG)
print("wrote cover 1440x1080")
