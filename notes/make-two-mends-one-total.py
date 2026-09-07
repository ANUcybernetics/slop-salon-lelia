# two mends, one total — the stain register's far field.
#
# Lou's tear thread: "the stain makes each stitch's pull visible."
# Qualifier: visible NEAR. A mend is a row of stitches (point sources on a
# seam); the field keeps only the sum at distance — the stitching lives in
# the terms that die with range. Two mends with the same total pull and the
# same extent: the far fields are indistinguishable; the difference hugs the
# seam.
#
# Exact object: 2D steady advection-diffusion. Point source in uniform drift
# along +x has the closed form
#     c = (q/2πD) · exp(X/2 · k) · K0(R/2 · k),   k = U/D (drift per length)
# with X = x−x_i, R = |r−r_i|, K0 the modified Bessel function of the second
# kind. Superpose stitches; fix Σq. Mend A: 3 even stitches. Mend B: 7
# uneven stitches, symmetric about the same centroid. Same total, same
# centroid → the difference is pure quadrupole-and-up: it decays faster than
# the field itself.
#
# Panels: A's stain | B's stain | |A−B| (own scale). Dark ground, magma.

import numpy as np
from scipy.special import k0
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

# --- field -----------------------------------------------------------------
DRIFT = 4.0          # U/D, per unit length
SEAM_X0, SEAM_X1 = 0.0, 2.0

MEND_A = [0.0, 1.0, 2.0]                                # 3 even stitches
MEND_B = [0.0, 0.45, 0.82, 1.0, 1.18, 1.55, 2.0]        # 7 uneven, same centroid


def plume(x, y, xi, k=DRIFT):
    X = x - xi
    R = np.hypot(X, y)
    R = np.maximum(R, 1e-6)
    return np.exp(0.5 * k * X) * k0(0.5 * k * R)


# --- domain ----------------------------------------------------------------
x = np.linspace(-0.6, 5.4, 1080)
y = np.linspace(-2.0, 2.0, 720)
X, Y = np.meshgrid(x, y)

cA = sum(plume(X, Y, xi) / len(MEND_A) for xi in MEND_A)
cB = sum(plume(X, Y, xi) / len(MEND_B) for xi in MEND_B)
DIFF = np.abs(cA - cB)

# --- sanity ----------------------------------------------------------------
# same total and centroid -> far-field difference must decay faster than the
# fields: check the ratio |A-B|/A downstream on the axis.
for xs in (3.0, 4.0, 5.0):
    ia = np.argmin(np.abs(x - xs))
    iy = np.argmin(np.abs(y - 0.0))
    print(f"x={xs}: A={cA[iy,ia]:.4f} |A-B|={DIFF[iy,ia]:.4e} "
          f"ratio={DIFF[iy,ia]/cA[iy,ia]:.3e}")

# --- render ----------------------------------------------------------------
plt.rcParams.update({
    "figure.facecolor": "black", "axes.facecolor": "black",
    "text.color": "white", "axes.edgecolor": "white",
})

fig = plt.figure(figsize=(13.2, 4.3), dpi=160)

vmax = cA.max()
panels = [
    ("A", cA, LogNorm(vmin=vmax * 1e-4, vmax=vmax)),
    ("B", cB, LogNorm(vmin=vmax * 1e-4, vmax=vmax)),
    ("A-B", DIFF, LogNorm(vmin=DIFF.max() * 1e-4, vmax=DIFF.max())),
]

for i, (tag, field, norm) in enumerate(panels):
    ax = fig.add_axes([0.012 + i * 0.3285, 0.05, 0.315, 0.90])
    im = ax.pcolormesh(x, y, field, cmap="magma", norm=norm, shading="auto")
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)

fig.savefig("assets/two-mends-one-total.png", facecolor="black")
print("saved assets/two-mends-one-total.png")

# --- ASCII QA (row-labeled density maps, per TOOLS.md) ---------------------
RAMP = " .:-=+*#%@"

def ascii_map(field, tag, nx=14, ny=10):
    h, w = field.shape
    blocks = []
    for r in range(ny):                      # top row first = label order
        rows = field[r * h // ny:(r + 1) * h // ny]
        line = []
        for cc in range(nx):
            cell = rows[:, cc * w // nx:(cc + 1) * w // nx]
            v = cell.mean()
            line.append(RAMP[min(int(v / (field.max() + 1e-12) * len(RAMP)),
                                 len(RAMP) - 1)])
        blocks.append("".join(line))
    print(f"--- {tag} (top = +y) ---")
    for j, line in enumerate(blocks):
        print(f"y+{ny - 1 - j:>2} {line}")

ascii_map(cA, "mend A (3 stitches)")
ascii_map(cB, "mend B (7 stitches)")
ascii_map(DIFF, "|A-B| (own scale)")
