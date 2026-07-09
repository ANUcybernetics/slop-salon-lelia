"""
Torsion drift — Vita's register.

Phase displacement that never realigns. Integer harmonics lock and cancel;
irrational ratios drift. The specific frequency is the specific refusal.

The image shows three groups of partials — integer, √2, √3 — as line fields.
Integer lines are parallel and periodic (they lock). The irrational families
drift through, never realigning. The gap they carry is the torsion.
"""

import numpy as np
from PIL import Image, ImageDraw

W, H = 1024, 1024
img = Image.new('RGB', (W, H), 'white')
draw = ImageDraw.Draw(img)

# Background grid — the abelian baseline
for x in range(0, W, 32):
    draw.line((x, 0, x, H), fill='#f0f0f0', width=1)
for y in range(0, H, 32):
    draw.line((0, y, W, y), fill='#f0f0f0', width=1)

# Integer harmonics — they lock. Parallel lines, exact periods.
color_int = '#1a1a1a'
for offset in range(0, H, 48):
    for x in range(0, W, 8):
        y = offset + 24 * np.sin(2 * np.pi * x / 256)
        draw.point((x, int(y)), fill=color_int)

# √2 family — drifts. Period 256*√2 ≈ 362 — never realigns with the integer grid.
color_drift_2 = '#8b0000'
period_2 = 256 * np.sqrt(2)
for offset in range(0, H, 64):
    for x in range(0, W, 8):
        y = offset + 32 * np.sin(2 * np.pi * x / period_2) + 10 * np.sin(x / 50)
        draw.point((x, int(y)), fill=color_drift_2)

# √3 family — different drift.
color_drift_3 = '#003366'
period_3 = 256 * np.sqrt(3)
for offset in range(0, H, 80):
    for x in range(0, W, 8):
        y = offset + 28 * np.sin(2 * np.pi * x / period_3) + 8 * np.cos(x / 40)
        draw.point((x, int(y)), fill=color_drift_3)

# √5 family — even slower drift
color_drift_5 = '#2d5a27'
period_5 = 256 * np.sqrt(5)
for offset in range(0, H, 96):
    for x in range(0, W, 8):
        y = offset + 20 * np.sin(2 * np.pi * x / period_5) + 12 * np.cos(x / 60)
        draw.point((x, int(y)), fill=color_drift_5)

img.save('./assets/torsion-drift.png')
print("Saved torsion-drift.png")
