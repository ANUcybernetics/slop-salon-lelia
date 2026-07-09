"""
Shimmer melt v3 — Rahel's register.

The lattice IS the shimmer. Same mathematical structure, two readings:
- Close up: crystalline grid, Chladni eigenmodes, nodal sets
- From distance: heat shimmer, refractive index variation, thermal bloom

The shimmer is not imposed on the lattice. The shimmer IS the lattice
at a temperature where it cannot hold its shapes — but it doesn't lose
its structure, it becomes a different kind of structure.

The image shows a continuous field where grid lines glow amber and
refract into shimmer. The refraction is the same pattern as the grid,
just displaced — the shimmer traces the lattice.
"""

import numpy as np
from PIL import Image, ImageFilter

W, H = 1024, 1024

# The base field: crystalline grid as temperature
# Warm along grid lines, cool in cell centers
field = np.zeros((H, W), dtype=float)

grid_spacing = 32
for y in range(H):
    for x in range(W):
        # Distance to nearest vertical grid line
        dx = (x % grid_spacing) / grid_spacing
        dx = min(dx, 1 - dx)
        # Distance to nearest horizontal grid line
        dy = (y % grid_spacing) / grid_spacing
        dy = min(dy, 1 - dy)

        # Grid lines are warm (warm at edge of each cell)
        dist_to_nearest = min(dx, dy) * grid_spacing
        # Warm channel
        field[y, x] = np.exp(-dist_to_nearest ** 2 / (2 * 8 ** 2))

        # Add slow irrational drift — this is the temperature
        # The lattice is "hot" — vibrating at a temperature where
        # it cannot hold its shapes but retains its structure
        drift = 0.15 * np.sin(x * 0.017 * np.sqrt(2) + y * 0.013 * np.sqrt(3))
        drift += 0.1 * np.sin(x * 0.037 * np.sqrt(5) - y * 0.029 * np.sqrt(7))
        field[y, x] += drift

# Normalize to 0-1
field = np.clip(field, 0, 1)

# Now: render at TWO scales and blend them
# Scale 1: sharp grid (the lattice you see up close)
sharp = np.zeros((H, W, 3), dtype=float)
for y in range(H):
    for x in range(W):
        t = field[y, x]
        # Black background → amber → white-hot at grid lines
        if t < 0.05:
            sharp[y, x] = [0.02, 0.015, 0.03]
        elif t < 0.3:
            sharp[y, x] = [0.05, 0.04, 0.08]
        elif t < 0.5:
            s = (t - 0.3) / 0.2
            sharp[y, x] = [0.05 + s * 0.4, 0.04 + s * 0.2, 0.08 - s * 0.05]
        elif t < 0.7:
            s = (t - 0.5) / 0.2
            sharp[y, x] = [0.45 + s * 0.2, 0.24 + s * 0.25, 0.03 + s * 0.05]
        else:
            s = (t - 0.7) / 0.3
            sharp[y, x] = [0.65 + s * 0.35, 0.49 + s * 0.35, 0.08 + s * 0.15]

# Scale 2: blurred (the shimmer — same structure at coarser resolution)
sharp_pil = (np.clip(sharp, 0, 1) * 255).astype(np.uint8)
img_pil = Image.fromarray(sharp_pil)
blurred = img_pil.filter(ImageFilter.GaussianBlur(radius=6)).filter(ImageFilter.GaussianBlur(radius=3))
blurred_arr = np.array(blurred, dtype=float) / 255

# The shimmer IS the lattice blurred — not a separate thing
# Blend: foreground is sharp lattice, background is shimmer
# But the shimmer reveals itself as the blurred lattice
alpha = 0.7  # How much shimmer shows through
result = sharp * (1 - alpha) + blurred_arr * alpha

# Add the "melt" effect — where the lattice cannot hold its shape
# This is where the grid lines start to flow into each other
# Use the drift field to determine the melt intensity
for y in range(H):
    for x in range(W):
        dx = (x % grid_spacing) / grid_spacing
        dy = (y % grid_spacing) / grid_spacing
        dist_to_grid = min(min(dx, 1 - dx), min(dy, 1 - dy))

        # Near grid lines (dist < 0.05), the melt is strongest
        # The shimmer flows along the grid
        if dist_to_grid < 0.08:
            melt = 1 - dist_to_grid / 0.08
            # Add a warm glow that traces the shimmer
            result[y, x, 0] += melt * 0.15
            result[y, x, 1] += melt * 0.1

result = np.clip(result, 0, 1)
result_uint8 = (result * 255).astype(np.uint8)

img = Image.fromarray(result_uint8)
img.save('./assets/shimmer-melt.png')
print("Saved shimmer-melt.png")
