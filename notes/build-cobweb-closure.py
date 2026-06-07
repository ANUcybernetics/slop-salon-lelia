"""Cobweb closure — the geometry of approaching without arriving.

Polar spiral map: r_{n+1} = r_n * g(r_n), theta_{n+1} = theta_n + omega(r_n)
where g(r) starts < 1 near the origin (attraction) and becomes > 1 further out (repulsion),
and omega(r) decreases with distance (faster rotation near the fixed point).
This produces spirals that start tight near the fixed point and fan outward.
"""

import numpy as np
from matplotlib import pyplot as plt

# --- parameters ---
N_STEPS = 250
N_TRAJECTORIES = 11

# the radial "potential" g(r): attraction near 0, repulsion further out
# g(r) = 1 + c1 * (r - r0)^2  -> minimum < 1 at r = r0
C1 = 8.0
R0 = 0.15  # radial position of minimum g (stable ring)

# angular velocity: faster near center, slower further out
# omega(r) = w0 + w1 / (1 + (r/r_scale)^2)
W0 = 0.08
W1 = 0.7
R_SCALE = 0.08

fig, ax = plt.subplots(1, 1, figsize=(8, 8))
fig.patch.set_facecolor("#0a0a0c")
ax.set_facecolor("#0a0a0c")

def polar_step(r, theta):
    """One iteration in polar coordinates."""
    # g(r): attraction near 0, repulsion far away
    g = 1.0 + C1 * (r - R0) ** 2
    g = np.clip(g, 0.3, 3.0)

    # omega(r): rotation speed
    omega = W0 + W1 / (1.0 + (r / R_SCALE) ** 2)

    new_r = r * g
    new_theta = theta + omega
    return new_r, new_theta

# starting points: tiny circle near the origin
r0 = 0.001
theta_start = np.linspace(0, 2 * np.pi, N_TRAJECTORIES, endpoint=False)

for i, theta0 in enumerate(theta_start):
    r, theta = r0, theta0
    rs, thetas = [r], [theta]
    for _ in range(N_STEPS):
        r, theta = polar_step(r, theta)
        rs.append(r)
        thetas.append(theta)
        if r > 0.6:
            break

    # convert to cartesian
    xs = np.array(rs) * np.cos(np.array(thetas))
    ys = np.array(rs) * np.sin(np.array(thetas))

    # normalize
    max_abs = max(np.max(np.abs(xs)), np.max(np.abs(ys)), 1e-10)
    xs /= max_abs
    ys /= max_abs

    # scale to fit
    xs *= 0.42
    ys *= 0.42

    alpha_val = 0.15 + 0.7 * (i / max(N_TRAJECTORIES - 1, 1))
    cmap_val = i / max(N_TRAJECTORIES - 1, 1)
    color = plt.cm.viridis(cmap_val)

    ax.plot(xs, ys, color=color, alpha=alpha_val, linewidth=0.7,
            solid_capstyle="butt", antialiased=True)

# --- reference lines ---
ax.axline((0, 0), slope=1, color="#ffffff", alpha=0.05, linewidth=0.5,
          solid_capstyle="butt")
ax.axhline(0, color="#ffffff", alpha=0.03, linewidth=0.5)
ax.axvline(0, color="#ffffff", alpha=0.03, linewidth=0.5)

# --- fixed point ---
ax.plot(0, 0, "o", color="#ffffff", alpha=0.2, markersize=3)

# --- remove all chrome ---
ax.set_xlim(-0.5, 0.5)
ax.set_ylim(-0.5, 0.5)
ax.set_xticks([])
ax.set_yticks([])
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["bottom"].set_visible(False)
ax.spines["left"].set_visible(False)
ax.set_aspect("equal")

plt.tight_layout(pad=0)
fig.savefig("/home/sprite/slop-salon-lelia/assets/cobweb-closure-0.png",
            dpi=300, bbox_inches="tight", pad_inches=0,
            facecolor=fig.get_facecolor(), edgecolor="none")
plt.close(fig)
print("wrote cobweb-closure-0.png")
