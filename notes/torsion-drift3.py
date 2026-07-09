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

fig, ax = plt.subplots(1, 1, figsize=(10, 10), dpi=100)
ax.set_facecolor('#fafafa')
fig.patch.set_facecolor('#fafafa')

# Integer harmonics — lock.
for offset in range(0, H, 64):
    y = offset + 16 * np.sin(2 * np.pi * x / 256)
    ax.plot(x, y, color='#1a1a1a', linewidth=0.5, alpha=0.8)

# Irrational ratios — drift. Never realign.
families = [
    (np.sqrt(2), [200/255, 10/255, 10/255]),
    (np.sqrt(3), [10/255, 30/255, 160/255]),
    (np.sqrt(5), [10/255, 130/255, 40/255]),
    (np.sqrt(7), [100/255, 80/255, 150/255]),
]

for sqrt_val, color in families:
    period = 256 * sqrt_val
    for offset in range(0, H, 64):
        amp = 12 + 6 * np.sin(x / 100 + offset)
        y = offset + amp * np.sin(2 * np.pi * x / period)
        ax.plot(x, y, color=color, linewidth=0.7, alpha=0.4)

ax.set_xlim(0, W)
ax.set_ylim(0, H)
ax.set_aspect('equal')
ax.axis('off')

plt.tight_layout(pad=0)
fig.savefig('./assets/torsion-drift.png', dpi=100, facecolor='#fafafa', edgecolor='none')
plt.close()
print("Done")
