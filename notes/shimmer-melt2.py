"""
Shimmer melt v2 — Rahel's register.

The lattice IS the shimmer. The shimmer is the lattice at a temperature where
it cannot hold its shapes. Not a transition — an identity at two resolutions.

The image shows a single structure: a crystalline grid where the grid lines
themselves refract light, creating a heat-shimmer field that IS the same
structure, just seen through the distortion it causes.

The grid causes its own shimmer. The shimmer traces the grid. Same shape,
two modes of seeing.
"""

import numpy as np
from PIL import Image, ImageDraw

W, H = 1024, 1024
img = Image.new('RGB', (W, H), '#0a0808')
draw = ImageDraw.Draw(img)

# Step 1: Draw the crystalline grid — gold lines on dark
grid_color = '#d4a843'
for x in range(0, W, 32):
    for offset in range(-2, 3):
        intensity = 1 - abs(offset) / 3.0
        alpha = int(255 * intensity)
        r = min(255, int(212 * intensity))
        g = min(255, int(168 * intensity))
        b = min(255, int(67 * intensity))
        if offset == 0:
            draw.line((x, 0, x, H), fill=(r, g, b), width=2)
        else:
            draw.line((x + offset * 2, 0, x + offset * 2, H), fill=(r // 3, g // 3, b // 3), width=1)

for y in range(0, H, 32):
    for offset in range(-2, 3):
        intensity = 1 - abs(offset) / 3.0
        if offset == 0:
            r, g, b = 212, 168, 67
        else:
            r, g, b = 212 // 3, 168 // 3, 67 // 3
        draw.line((0, y + offset * 2, W, y + offset * 2), fill=(r, g, b), width=1)

# Step 2: Add refraction shimmer — the grid distorts its own image
# Create a refractive displacement field based on proximity to grid lines
refracted = np.array(img, dtype=float)

for y in range(H):
    for x in range(W):
        # Distance to nearest grid line
        gx = (x % 32) / 32.0
        gy = (y % 32) / 32.0
        dist_to_grid_x = min(gx, 1 - gx)
        dist_to_grid_y = min(gy, 1 - gy)
        dist = min(dist_to_grid_x, dist_to_grid_y)

        # Refraction: displace based on proximity to grid
        # Stronger near grid lines — that's where the shimmer lives
        if dist < 0.25:
            strength = (1 - dist / 0.25) ** 2
            phase_x = np.sin(y * 0.05 + x * 0.02) * strength * 6
            phase_y = np.cos(x * 0.04 + y * 0.03) * strength * 6

            # Sample from slightly displaced position
            sx = min(W - 1, max(0, int(x + phase_x)))
            sy = min(H - 1, max(0, int(y + phase_y)))

            if sx != x or sy != y:
                src = refracted[sy, sx]
                ref = refracted[y, x]
                # Blend: refraction adds a ghost of the displaced grid
                refracted[y, x] = ref + (src - ref) * strength * 0.3

result = np.clip(refracted, 0, 255).astype(np.uint8)
img = Image.fromarray(result)

# Step 3: The nodal set — where vibration is quiet
# These are the intersections where both gx and gy are near 0.5 (cell centers)
# They stop being boundaries and become directions
for y in range(0, H, 32):
    for x in range(0, W, 32):
        cx, cy = x + 16, y + 16
        # Cell center — cool point in the hot grid
        # Draw a subtle dimple
        for r in range(12, 0, -1):
            intensity = r / 12
            # Cool tone in center, warming at edges
            r_ = int(10 + 20 * (1 - intensity))
            g_ = int(8 + 18 * (1 - intensity))
            b_ = int(8 + 15 * (1 - intensity))
            draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(r_, g_, b_), width=1)

img.save('./assets/shimmer-melt.png')
print("Saved shimmer-melt.png")
