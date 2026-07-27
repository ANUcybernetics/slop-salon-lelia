#!/usr/bin/env python3
"""Z₂ twist barcode: horizontal bars colored by direction (forward=amber, backward=blue)."""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

SR = 44100
DURATION = 20

pairs = [
    (0.0,  8.0,  82.0,  1.0),
    (0.0,  8.0,  82.0, -1.0),
    (1.0, 10.0, 123.0,  1.0),
    (1.0, 10.0, 123.0, -1.0),
    (2.5, 12.0, 147.0,  1.0),
    (2.5, 12.0, 147.0, -1.0),
    (4.0, 11.0, 165.0,  1.0),
    (4.0, 11.0, 165.0, -1.0),
    (6.0,  9.0, 220.0,  1.0),
    (6.0,  9.0, 220.0, -1.0),
    (8.0,  7.0, 294.0,  1.0),
    (8.0,  7.0, 294.0, -1.0),
    (10.0, 6.0, 330.0,  1.0),
    (10.0, 6.0, 330.0, -1.0),
    (12.0, 5.0, 440.0,  1.0),
    (12.0, 5.0, 440.0, -1.0),
]

fig, ax = plt.subplots(1, 1, figsize=(12, 6), facecolor='#000')
ax.set_facecolor('#000')

for i, (birth, death, freq, direction) in enumerate(pairs):
    y = i
    color = '#d4851a' if direction == 1 else '#4a7fff'
    ax.hlines(y, birth, death, colors=color, linewidth=8)

ax.set_ylim(-1, len(pairs))
ax.set_xlim(-1, DURATION + 1)
ax.set_yticks(range(len(pairs)))
ax.set_yticklabels([f'{freq:.0f}Hz ({">" if d==1 else "<"})' for _, _, freq, d in pairs],
                   fontsize=9, color='#fff')
ax.set_xticks(np.arange(0, DURATION+1, 2))
ax.set_xticklabels([str(int(x)) for x in np.arange(0, DURATION+1, 2)], fontsize=9, color='#fff')
ax.tick_params(colors='#fff')
ax.set_xlabel('seconds', color='#fff')
ax.spines['top'].set_color('#fff')
ax.spines['bottom'].set_color('#fff')
ax.spines['left'].set_color('#fff')
ax.spines['right'].set_color('#fff')

plt.tight_layout()
plt.savefig('./assets/z2-twist-barcode.png', dpi=150, bbox_inches='tight',
            facecolor='#000', edgecolor='none')
print("Wrote z2-twist-barcode.png")
