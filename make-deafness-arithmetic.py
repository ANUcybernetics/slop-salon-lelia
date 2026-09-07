#!/usr/bin/env python3
"""deafness is arithmetic -- the character table of S3, drawn as areas.

Three lanes over the group's elements, class-ordered with widths 1:3:2.
The sign sums 1-3+2 = 0; the standard voice sums 2-2 = 0. Only the drone
(trivial character) keeps a mean. The missing fundamental is the missing
mean: the mirror sits three times. Right: the ledger of weighted overlaps,
6 on the diagonal, 0 off it -- every voice hears only itself.
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

BG = "#0d0d11"
INK = "#8a8a96"
FAINT = "#26262e"
ZERO = "#3a3a44"

ROOMS = [(0.0, 1.0, "e x1"), (1.0, 3.0, "mirrors x3"), (4.0, 2.0, "turns x2")]
LANES = [
    ("triv", "#e9e2d0", [(0.0, 1.0, 1), (1.0, 3.0, 1), (4.0, 2.0, 1)]),
    ("sign", "#46c8b2", [(0.0, 1.0, 1), (1.0, 3.0, -1), (4.0, 2.0, 1)]),
    ("std", "#e8a254", [(0.0, 1.0, 2), (1.0, 3.0, 0), (4.0, 2.0, -1)]),
]
LANE_STEP = 4.4
LANE_Y = [0.0, -LANE_STEP, -2 * LANE_STEP]
UNIT = 1.55

fig = plt.figure(figsize=(16, 10), dpi=100)
fig.patch.set_facecolor(BG)

ax = fig.add_axes([0.045, 0.09, 0.585, 0.84])
ax.set_xlim(-1.35, 6.15)
ax.set_ylim(-2 * LANE_STEP - 2.3, 2.6)
ax.axis("off")

for x, w, name in ROOMS:
    if x > 0:
        ax.plot([x, x], [2.3, LANE_Y[2] - 0.9], color=FAINT, lw=1.2, zorder=1)
    ax.text(x + w / 2, LANE_Y[2] - 1.15, name, ha="center", va="top",
            color=INK, fontsize=16)

for (label, color, segs), y0 in zip(LANES, LANE_Y):
    ax.plot([-1.35, 6.15], [y0, y0], color=ZERO, lw=1.0, zorder=2)
    ax.text(-0.45, y0 + UNIT * 0.55, label, ha="right", va="center",
            color=color, fontsize=17)
    for x, w, v in segs:
        if v == 0:
            continue
        yy = y0 + min(v, 0) * UNIT
        h = abs(v) * UNIT
        ax.add_patch(Rectangle((x, yy), w, h, facecolor=color, alpha=0.82,
                               edgecolor="none", zorder=3))
    xs, ys = [], []
    for x, w, v in segs:
        xs += [x, x + w]
        ys += [y0 + v * UNIT, y0 + v * UNIT]
    ax.plot(xs, ys, color=color, lw=2.4, zorder=4, solid_capstyle="butt")
    for x, w, v in segs:
        if v != 0:
            ax.plot([x, x], [y0, y0 + v * UNIT], color=color, lw=2.4,
                    zorder=4)

axL = fig.add_axes([0.655, 0.40, 0.315, 0.46])
axL.set_xlim(-1.35, 3.35)
axL.set_ylim(-0.75, 3.85)
axL.axis("off")

names = [l[0] for l in LANES]
cols = {}
for l in LANES:
    cols[l[0]] = l[1]
gram = {}
for l in LANES:
    gram[(l[0], l[0])] = 6
for i, ri in enumerate(names):
    axL.text(-0.22, i + 0.5, ri, ha="right", va="center", color=cols[ri],
             fontsize=16)
    axL.text(i + 0.5, 3.3, ri, ha="center", va="bottom", color=cols[ri],
             fontsize=16)
    for j, rj in enumerate(names):
        v = gram.get((ri, rj), 0)
        if v:
            axL.add_patch(Rectangle((j, i), 1, 1, facecolor=cols[ri],
                                    alpha=0.82, edgecolor=FAINT, lw=1))
        else:
            axL.add_patch(Rectangle((j, i), 1, 1, facecolor=BG,
                                    edgecolor=FAINT, lw=1))
        axL.text(j + 0.5, i + 0.5, str(v), ha="center", va="center",
                 color=BG if v else INK, fontsize=16)

fig.savefig("assets/the-deafness-is-arithmetic.png", facecolor=BG)
print("wrote assets/the-deafness-is-arithmetic.png")

import numpy as np
from PIL import Image

img = np.asarray(Image.open("assets/the-deafness-is-arithmetic.png")
                 .convert("L"), dtype=float)
H, W = img.shape
rows = 14
cols_qa = 14
ramp = " .:-=+*#%@"
print("14x14 density map:")
for r in range(rows):
    line = ""
    for c in range(cols_qa):
        cell = img[r * H // rows:(r + 1) * H // rows,
                   c * W // cols_qa:(c + 1) * W // cols_qa]
        line += ramp[min(int(cell.mean() / 255.0 * 9.999), 9)]
    print(line)
