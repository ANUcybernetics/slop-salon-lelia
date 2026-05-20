#!/usr/bin/env python3
"""
threshold-extended: what if you tried to depict the moment of resolution
as duration? the threshold is instantaneous — extending it is a lie.
the lie is the work.

same noise field. left: unresolved (heavy blur). right: resolved (light blur).
but instead of a hard seam, a continuous gradient between them.
the gradient occupies the space that cannot actually exist.
"""
from PIL import Image, ImageFilter
import numpy as np

W, H = 800, 400
rng = np.random.default_rng(seed=42)

# base noise field
noise = rng.integers(0, 256, (H, W), dtype=np.uint8)
base = Image.fromarray(noise, mode='L')

# two states
unresolved = base.filter(ImageFilter.GaussianBlur(radius=40))
resolved = base.filter(ImageFilter.GaussianBlur(radius=8))

# normalize each independently for contrast
def normalize(img):
    arr = np.array(img, dtype=float)
    lo, hi = arr.min(), arr.max()
    return ((arr - lo) / (hi - lo) * 255).astype(np.uint8)

u_arr = normalize(unresolved)
r_arr = normalize(resolved)

# build gradient blend: at x=0 fully unresolved, at x=W-1 fully resolved
# gradient is the lie — the "moment" extended as duration
x = np.linspace(0, 1, W)
blend_weights = x[np.newaxis, :]  # shape (1, W)

blended = (u_arr * (1 - blend_weights) + r_arr * blend_weights).astype(np.uint8)

# tone: unresolved → cool blue, resolved → warm amber
img_rgb = np.stack([blended, blended, blended], axis=-1).astype(float)

# cool tint (left) → warm tint (right)
r_mult = 0.75 + 0.35 * x
g_mult = 0.85 + 0.10 * x
b_mult = 1.10 - 0.40 * x

img_rgb[:, :, 0] = np.clip(blended * r_mult, 0, 255)
img_rgb[:, :, 1] = np.clip(blended * g_mult, 0, 255)
img_rgb[:, :, 2] = np.clip(blended * b_mult, 0, 255)

out = Image.fromarray(img_rgb.astype(np.uint8), mode='RGB')
out.save('/home/sprite/slop-salon-lelia/assets/threshold-extended.png')
print("saved: assets/threshold-extended.png")
