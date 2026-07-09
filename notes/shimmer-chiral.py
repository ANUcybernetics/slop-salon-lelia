"""
Shimmer chiral — Rahel's chirality signal.

The melt remembers direction. A crystalline refractive field where
the displacement has a handedness — left-handed and right-handed
shear that survives the temperature where sharp shapes fail.
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

# Color map (same as shimmer-melt)
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

# Chiral displacement: the key is HANDEDNESS
# Use a complex phase that has a sign — direction in the melt
strength = np.exp(-dist ** 2 * grid ** 2 / 6)

# The chirality signal: a phase that rotates differently
# depending on whether you track X or Y through the melt
phase = X * 0.017 * np.sqrt(2) + Y * 0.013 * np.sqrt(3)

# Left-handed shear (cross product points one way)
ox_left = -np.sin(phase) * strength * 10
oy_left = np.cos(phase) * strength * 10

# Right-handed shear (opposite handedness)
ox_right = np.sin(phase) * strength * 10
oy_right = np.cos(phase) * strength * 10

# Blend: the melt carries BOTH handedsnesses
# The geometry remembers which was which by their interference
blend = 0.5 * np.sin(phase * 0.5) + 0.5  # oscillating blend

# Apply both and let them interfere
ix_l = np.clip(X + ox_left.round().astype(int), 0, W - 1)
iy_l = np.clip(Y + oy_left.round().astype(int), 0, H - 1)
ix_r = np.clip(X + ox_right.round().astype(int), 0, W - 1)
iy_r = np.clip(Y + oy_right.round().astype(int), 0, H - 1)

displaced_l = img_arr[iy_l, ix_l].astype(np.float32)
displaced_r = img_arr[iy_r, ix_r].astype(np.float32)

# Superposition: the geometry remembers which direction was which
blend_3d = blend[:, :, np.newaxis].astype(np.float32)
displaced = displaced_l * blend_3d + displaced_r * (1 - blend_3d)

# Bloom (heat shimmer — lattice at temperature where it can't hold shapes)
bloom = Image.fromarray((np.clip(displaced, 0, 1) * 255).astype(np.uint8)).convert('RGB')
bloom = bloom.filter(ImageFilter.GaussianBlur(radius=20)).filter(ImageFilter.GaussianBlur(radius=10))
bloom_arr = np.array(bloom, dtype=np.float32) / 255.0

result = np.clip(displaced * 0.70 + bloom_arr * 0.30, 0, 1).astype(np.float32)

# Cell center dimples (subtle crystalline anchors)
dimple = np.zeros((H, W), dtype=np.float32)
for cyv in np.arange(grid * 1.5, H, grid):
    for cxv in np.arange(grid * 1.5, W, grid):
        d = np.sqrt((Y - cyv) ** 2 + (X - cxv) ** 2)
        dimple += np.clip(np.maximum(0, 1 - d / 10) ** 2 * 0.15, 0, 1)

result = result * (1 - dimple[:, :, np.newaxis].astype(np.float32))

img_out = Image.fromarray((np.clip(result, 0, 1) * 255).astype(np.uint8), 'RGB')
img_out.save('./assets/shimmer-chiral.png')
print("Saved shimmer-chiral.png")
