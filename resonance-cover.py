#!/usr/bin/env python3
"""Cover for resonance-standing: standing wave as mineral strata.

Two frequencies locked in the gap ratio — shown as interference pattern
between two sine waves. The beat pattern IS the standing wave.

Black background, amber and deep blue sine waves, their interference
showing the mineral structure of the gap.
"""

import numpy as np
from PIL import Image, ImageDraw, ImageFont

width, height = 1200, 600
bg_color = (8, 8, 14)

img = Image.new('RGB', (width, height), bg_color)
draw = ImageDraw.Draw(img)

# Draw two sine waves and their interference
# Wave 1: 60Hz (amber) — boundary
# Wave 2: 28.2Hz (deep blue) — gap partial
# Interference: the standing wave pattern

cx = width // 2
cy = height // 2

# Scale: show ~3 cycles of the beat envelope
# Beat frequency = |60 - 28.2| = 31.8 Hz
# Envelope frequency = beat/2 = 15.9 Hz
f1 = 60.0
f2 = 28.2

# Draw as horizontal bands with vertical oscillation
y_center = cy

# Draw interference pattern
points_upper = []
points_lower = []
for x in range(width):
    t = x / width * 8 * np.pi  # 4 cycles
    # Standing wave: sum of two frequencies creates beat pattern
    val = (0.5 * np.sin(f1 * t / 20) + 0.5 * np.sin(f2 * t / 20))
    y = int(y_center + val * 180)
    points_upper.append((x, max(0, y - 2)))
    points_lower.append((x, min(height, y + 2)))

# Draw interference as filled region
if points_upper and points_lower:
    # Build polygon points: upper left to right, then lower right to left
    poly = points_upper + points_lower[::-1]
    draw.polygon(poly, fill=(180, 120, 40, 100))

# Draw the envelope — the standing wave amplitude
envelope_points = []
for x in range(width):
    t = x / width * 8 * np.pi
    # Envelope = |sum of amplitudes|
    env = abs(np.sin((f1 - f2) * t / 40))
    y = int(y_center + env * 200)
    envelope_points.append((x, max(0, y)))

# Draw amplitude peaks as small dots
for x in range(0, width, 3):
    t = x / width * 8 * np.pi
    env = abs(np.sin((f1 - f2) * t / 40))
    y = int(y_center + env * 200)
    if env > 0.3:
        r = int(1 + env * 2)
        draw.ellipse([x - r, y - r, x + r, y + r], fill=(220, 160, 50))

# Draw the two component frequencies as thin lines
# Wave 1 (60Hz) — amber
pts1 = []
for x in range(0, width, 2):
    t = x / width * 8 * np.pi
    y = int(y_center + np.sin(f1 * t / 20) * 120)
    pts1.append((x, y))
if len(pts1) > 2:
    draw.line(pts1, fill=(200, 140, 50), width=1)

# Wave 2 (28.2Hz) — deep blue
pts2 = []
for x in range(0, width, 2):
    t = x / width * 8 * np.pi
    y = int(y_center + np.sin(f2 * t / 20) * 120)
    pts2.append((x, y))
if len(pts2) > 2:
    draw.line(pts2, fill=(40, 80, 160), width=1)

# Horizontal axis line
draw.line([(0, cy), (width, cy)], fill=(60, 60, 80), width=1)

# Label the gap
font_size = 18
try:
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
except:
    font = ImageFont.load_default()

# Draw "f₁ = 60" and "f₂ = 28.2" and "beat = 31.8"
text_color = (180, 150, 100)
draw.text((30, 30), "f₁ = 60", fill=text_color, font=font)
draw.text((30, 55), "f₂ = 28.2", fill=(80, 120, 180), font=font)
draw.text((30, 80), "|f₁ - f₂| = 31.8  →  standing wave", fill=(200, 180, 120), font=font)
draw.text((30, 105), "gap = 0.47  —  the obstruction carrying through time", fill=(160, 140, 100), font=font)

img.save("assets/resonance-cover.png")
print(f"Wrote resonance-cover.png ({width}x{height})")
