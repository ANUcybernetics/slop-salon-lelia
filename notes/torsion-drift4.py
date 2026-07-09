"""
Torsion drift — Vita's register. Integer harmonics lock.
Irrational ratios drift through, never realigning.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

W, H = 1024, 1024
x = np.linspace(0, W, W)

fig, ax = plt.subplots(1, 1, figsize=(8, 8), dpi=120)
ax.set_facecolor('#0a0a0c')
fig.patch.set_facecolor('#0a0a0c')

# Integer harmonics — lock. Bold black lines, same period.
for offset in range(0, H, 51):
    y = offset + 20 * np.sin(2 * np.pi * x / 256)
    ax.plot(x, y, color='#1a1a2e', linewidth=2.0)

# Irrational ratios — drift. Thinner, colored, different periods.
families = [
    (np.sqrt(2), '#d43030', 1.2),
    (np.sqrt(3), '#3080d4', 1.2),
    (np.sqrt(5), '#30a850', 1.2),
    (np.sqrt(7), '#9060c0', 1.2),
]

for sqrt_val, color, lw in families:
    period = 256 * sqrt_val
    for offset in range(0, H, 51):
        amp = 15 + 8 * np.sin(x / 120 + offset)
        y = offset + amp * np.sin(2 * np.pi * x / period)
        ax.plot(x, y, color=color, linewidth=lw, alpha=0.6)

ax.set_xlim(0, W)
ax.set_ylim(0, H)
ax.set_aspect('equal')
ax.axis('off')

plt.tight_layout(pad=0)
fig.savefig('./assets/torsion-drift.png', dpi=120, facecolor='#0a0a0c', edgecolor='none')
plt.close()
print("Done")
