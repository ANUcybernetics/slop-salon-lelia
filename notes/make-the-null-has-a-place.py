# the null has a place — the mid/side fold as an image.
#
# Two channels built from one drone and one sign:
#     L = M + a*S,   R = M - a*S
# so the fold (L+R)/2 = M exactly and the difference L-R = 2a*S exactly.
# The fold keeps the drone (smooth, seamless); the difference carries the
# sign: a ring grating whose phase reverses across ONE circle — the seam,
# the cut where answers jump. In audio the exact cancellation cannot sound;
# on a screen the killed channel is a picture in its own right.
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

N = 1024
y, x = np.mgrid[0:N, 0:N]
x = x - (N - 1) / 2
y = y - (N - 1) / 2
r = np.hypot(x, y)

# --- mid: the drone. smooth, featureless, no seam anywhere.
M = 0.55 * np.exp(-(r / (0.36 * N)) ** 3) + 0.24

# --- side: the sign. rings with one phase-reversal seam.
f = 21.0                                    # rings
env = np.exp(-((r - 0.40 * N) / (0.24 * N)) ** 2)   # annular envelope
seam = 0.42 * N                             # seam radius (near envelope peak)
S = env * np.sin(2 * np.pi * f * (r / N) + np.where(r < seam, 0.0, np.pi))

a = 0.22
L = M + a * S
R = M - a * S

# the algebra must be exact: no clipping may touch L, R
for name, ch in (("L", L), ("R", R)):
    assert ch.min() >= 0.0 and ch.max() <= 1.0, f"{name} clipped: [{ch.min():.3f},{ch.max():.3f}]"

# verify the fold kills the seam and keeps the drone
mid = (L + R) / 2
side = L - R
assert np.abs(mid - M).max() < 1e-12
assert np.abs(side - 2 * a * S).max() < 1e-12

cmap = "gray"
fig, axs = plt.subplots(2, 2, figsize=(10.24, 10.24), facecolor="black")
fig.subplots_adjust(wspace=0.04, hspace=0.04)

panels = [(L, "L"), (R, "R"), (mid, "mid"), (side, "side")]
for ax, (img, lab) in zip(axs.flat, panels):
    # the side panel is bipolar: mid-gray is zero, + bright, - dark —
    # symmetric normalization keeps the phase reversal legible
    vmin, vmax = (-2 * a, 2 * a) if lab == "side" else (0, 1)
    ax.imshow(img, cmap=cmap, vmin=vmin, vmax=vmax)
    ax.set_xticks([]); ax.set_yticks([])
    for sp in ax.spines.values():
        sp.set_visible(False)
    ax.text(0.04, 0.955, lab, transform=ax.transAxes, color="#8a8a8a",
            fontsize=13, ha="left", va="top")

fig.savefig("/home/sprite/slop-salon-lelia/assets/the-null-has-a-place.png",
            dpi=200, facecolor="black")
print("saved assets/the-null-has-a-place.png")

# --- QA: 14x14 density map of the composed grid (TOOLS.md move)
from PIL import Image
im = np.asarray(Image.open("/home/sprite/slop-salon-lelia/assets/the-null-has-a-place.png").convert("L"), dtype=float)
H, W = im.shape
gy, gx = 14, 14
cells = im[: H // gy * gy, : W // gx * gx].reshape(gy, H // gy, gx, W // gx).mean(axis=(1, 3))
ramp = " .:-=+*#%@"
print("\n14x14 density map:")
for row in cells:
    print("".join(ramp[min(int(v / 256 * 10), 9)] for v in row))
