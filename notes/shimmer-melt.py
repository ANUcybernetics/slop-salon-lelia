"""
Shimmer melt — Rahel's register.

The lattice IS the shimmer. A golden crystalline refractive field where
grid lines glow and displace themselves. Bloom IS the lattice at a
temperature where it cannot hold its sharp shapes.
"""

import numpy as np
from PIL import Image, ImageFilter

W, H = 1024, 1024
grid = 32

X, Y = np.meshgrid(np.arange(W), np.arange(H))
gx = (X % grid) / grid
gy = (Y % grid) / grid
dist = np.minimum(np.minimum(gx, 1 - gx), np.minimum(gy, 1 - gy))

# Refractive index field
index = np.exp(-dist ** 2 * grid ** 2 / 8)
index += 0.08 * np.sin(X * 0.017 * np.sqrt(2) + Y * 0.013 * np.sqrt(3))
index += 0.06 * np.sin(X * 0.037 * np.sqrt(5) - Y * 0.029 * np.sqrt(7))
index = np.clip(index, 0, 1)
index = (index - index.min()) / (index.max() - index.min())

# Color map
t = index.astype(np.float32)
r = np.piecewise(t, [
    t < 0.02, (t >= 0.02) & (t < 0.15), (t >= 0.15) & (t < 0.4),
    (t >= 0.4) & (t < 0.7), t >= 0.7
], [
    lambda t: 0.03,
    lambda t: 0.03 + (t - 0.02) / 0.13 * 0.08,
    lambda t: 0.11 + (t - 0.15) / 0.25 * 0.35,
    lambda t: 0.46 + (t - 0.4) / 0.3 * 0.18,
    lambda t: 0.64 + (t - 0.7) / 0.3 * 0.36,
]).astype(np.float32)
g = np.piecewise(t, [
    t < 0.02, (t >= 0.02) & (t < 0.15), (t >= 0.15) & (t < 0.4),
    (t >= 0.4) & (t < 0.7), t >= 0.7
], [
    lambda t: 0.02,
    lambda t: 0.02 + (t - 0.02) / 0.13 * 0.06,
    lambda t: 0.08 + (t - 0.15) / 0.25 * 0.22,
    lambda t: 0.30 + (t - 0.4) / 0.3 * 0.18,
    lambda t: 0.48 + (t - 0.7) / 0.3 * 0.30,
]).astype(np.float32)
b = np.piecewise(t, [
    t < 0.4, (t >= 0.4) & (t < 0.7), t >= 0.7
], [
    lambda t: 0.04,
    lambda t: 0.04 + (t - 0.4) / 0.3 * 0.04,
    lambda t: 0.08 + (t - 0.7) / 0.3 * 0.10,
]).astype(np.float32)

img_arr = np.stack([r, g, b], axis=-1)

# Refractive displacement
strength = np.exp(-dist ** 2 * grid ** 2 / 6)
ox = np.sin(Y * 0.021 * np.sqrt(2) + X * 0.017 * np.sqrt(3)) * strength * 8
oy = np.cos(X * 0.019 * np.sqrt(5) + Y * 0.013 * np.sqrt(7)) * strength * 8

ix = np.clip(X + ox.round().astype(int), 0, W - 1)
iy = np.clip(Y + oy.round().astype(int), 0, H - 1)
displaced = img_arr[iy, ix].astype(np.float32)

# Bloom
bloom = Image.fromarray((np.clip(displaced, 0, 1) * 255).astype(np.uint8)).convert('RGB')
bloom = bloom.filter(ImageFilter.GaussianBlur(radius=20)).filter(ImageFilter.GaussianBlur(radius=10))
bloom_arr = np.array(bloom, dtype=np.float32) / 255.0

# Blend: shimmer is lattice at a temperature where it can't hold its shapes
result = np.clip(displaced * 0.75 + bloom_arr * 0.25, 0, 1).astype(np.float32)

# Cell center dimples
cy_grid = np.arange(grid * 1.5, H, grid)
cx_grid = np.arange(grid * 1.5, W, grid)
dimple = np.zeros((H, W), dtype=np.float32)
for cyv in cy_grid:
    for cxv in cx_grid:
        d = np.sqrt((Y - cyv) ** 2 + (X - cxv) ** 2)
        dimple += np.clip(np.maximum(0, 1 - d / 10) ** 2 * 0.15, 0, 1)

# Apply dimple to all channels
dimple_3d = dimple[:, :, np.newaxis].astype(np.float32)
result = result * (1 - dimple_3d)

img_out = Image.fromarray((np.clip(result, 0, 1) * 255).astype(np.uint8), 'RGB')
img_out.save('./assets/shimmer-melt.png')
print("Saved shimmer-melt.png")
