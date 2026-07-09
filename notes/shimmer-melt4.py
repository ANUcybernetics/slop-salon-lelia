"""
Shimmer melt v4 — Rahel's register.

The shimmer IS the lattice. Not a grid with shimmer overlaid, but a golden
heat-shimmer field where the shimmer itself traces crystalline structure.

From a distance: refractive gold field, uniform warmth.
Close up: the shimmer's displacement is governed by a lattice.
The shimmer's texture IS the crystalline pattern.

The lattice at a temperature where it cannot hold its shapes — but it
doesn't become formless. It becomes a different kind of form.
"""

import numpy as np
from PIL import Image, ImageFilter, ImageDraw

W, H = 1024, 1024

# Start with a black field
field = np.zeros((H, W, 3), dtype=float)

# Generate shimmer noise — the golden refractive field
# Multiple frequency layers for organic shimmer
for scale in [64, 32, 16, 8, 4]:
    noise = np.random.randn(H // scale, W // scale, 3).astype(float)
    # Bicubic-ish upsample
    for sy in range(H // scale):
        for sx in range(W // scale):
            val = noise[sy, sx]
            for dy in range(scale):
                for dx in range(scale):
                    y, x = sy * scale + dy, sx * scale + dx
                    alpha = (1 - dy / scale) * (1 - dx / scale)
                    field[y, x] += val * alpha * 0.3

# Normalize noise per channel
for c in range(3):
    field[:, :, c] = (field[:, :, c] - field[:, :, c].min()) / (field[:, :, c].max() - field[:, :, c].min())

# Now: impose the lattice as a MODULATION of the shimmer
# The shimmer's brightness/displacement is organized by crystalline structure
grid_spacing = 32

for y in range(H):
    for x in range(W):
        # Crystalline displacement field
        dx = (x % grid_spacing) / grid_spacing
        dy = (y % grid_spacing) / grid_spacing
        dist_x = min(dx, 1 - dx)
        dist_y = min(dy, 1 - dy)
        dist = min(dist_x, dist_y)

        # Along grid lines: the shimmer is warmer/brighter
        # This is where the lattice reveals itself IN the shimmer
        grid_factor = np.exp(-dist * grid_spacing ** 2 / 2 / 16 ** 2)

        # The shimmer along grid lines is golden
        field[y, x, 0] = 0.7 + 0.3 * grid_factor  # R: warm
        field[y, x, 1] = 0.45 + 0.35 * grid_factor  # G: amber
        field[y, x, 2] = 0.05 + 0.1 * grid_factor  # B: minimal, warm light

        # Cell centers: dimmer, cooler — but still shimmering
        if dist > 0.1:
            cell_brightness = (1 - dist) * 0.15
            field[y, x, 0] = max(field[y, x, 0], cell_brightness)
            field[y, x, 1] = max(field[y, x, 1], cell_brightness * 0.7)

# Add "refractive" displacement — shimmer is refractive, not luminous
# Create displacement vectors that bend light
displacement = np.zeros((H, W, 2), dtype=float)
for y in range(H):
    for x in range(W):
        dx = (x % grid_spacing) / grid_spacing
        dy = (y % grid_spacing) / grid_spacing

        # Displacement is strongest near grid lines
        dist = min(min(dx, 1 - dx), min(dy, 1 - dy))
        strength = np.exp(-dist * grid_spacing ** 2 / 2 / 12 ** 2)

        # Phase varies slowly — this is what makes it shimmer, not just shine
        phase_x = np.sin(y * 0.021 * np.sqrt(2) + x * 0.013 * np.sqrt(3))
        phase_y = np.cos(x * 0.019 * np.sqrt(5) + y * 0.017 * np.sqrt(7))

        displacement[y, x] = [phase_x, phase_y] * strength * 4

# Apply refractive displacement
result = np.zeros_like(field)
for y in range(H):
    for x in range(W):
        sx = int(x + displacement[y, x, 0])
        sy = int(y + displacement[y, x, 1])
        sx = min(W - 1, max(0, sx))
        sy = min(H - 1, max(0, sy))
        result[y, x] = field[sy, sx]

# Add a soft bloom where the shimmer is hottest (near grid lines)
img_pil = Image.fromarray(np.clip(result, 0, 1) * 255).convert('RGB')

# Bloom pass
bloom = img_pil.filter(ImageFilter.GaussianBlur(radius=24)).filter(ImageFilter.GaussianBlur(radius=12))
# Blend sharp-ish shimmer with bloom
result_img = Image.blend(img_pil, bloom, 0.3)

result_img.save('./assets/shimmer-melt.png')
print("Saved shimmer-melt.png")
