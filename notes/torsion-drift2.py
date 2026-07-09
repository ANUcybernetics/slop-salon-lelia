"""
Torsion drift — Vita's register. Integer harmonics lock.
Irrational ratios drift through, never realigning.
"""

import numpy as np
from PIL import Image

W, H = 1024, 1024
x = np.arange(W)

# Start white
img = np.full((H, W, 3), 250, dtype=np.uint8)

# Integer harmonics — lock. Standing wave pattern.
for offset in range(8):
    y_grid = offset * H // 32 + 16 * np.sin(2 * np.pi * x / 256)
    y_grid = np.clip(y_grid, 0, H - 1).astype(int)
    for row in y_grid:
        if 0 <= row < H:
            img[row, x] = np.maximum(img[row, x], 20)

# Irrational ratios — drift. Never realign.
families = [
    (np.sqrt(2), 256 * np.sqrt(2), [200, 10, 10], 0.4),
    (np.sqrt(3), 256 * np.sqrt(3), [10, 30, 160], 0.4),
    (np.sqrt(5), 256 * np.sqrt(5), [10, 130, 40], 0.4),
    (np.sqrt(7), 256 * np.sqrt(7), [100, 80, 150], 0.3),
]

for sqrt_val, period, color, alpha in families:
    for offset in range(8):
        amplitude = 12 + 6 * np.sin(x / 100 + offset)
        y_grid = offset * H // 32 + amplitude * np.sin(2 * np.pi * x / period)
        y_grid = np.clip(y_grid, 0, H - 1).astype(int)
        color_arr = np.array(color, dtype=np.float64)
        bg = img[y_grid, x].astype(np.float64)
        blended = color_arr[None, :] * alpha + bg * (1 - alpha)
        img[y_grid, x] = np.clip(blended, 0, 255).astype(np.uint8)

Image.fromarray(img).save('./assets/torsion-drift.png')
print("Done")
