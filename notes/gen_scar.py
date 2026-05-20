#!/usr/bin/env python3
"""
Inversion of the diptych: the seam is the subject.
The scar — the trace of crossing — rendered as the most resolved part.
Sides fade to uniformity. Center is where the event was.
"""
import numpy as np
from PIL import Image
import math

rng = np.random.default_rng(42)

W, H = 900, 500

def fbm(seed, scale, octaves=6):
    rng2 = np.random.default_rng(seed)
    result = np.zeros((H, W))
    amp = 1.0
    freq = 1.0
    for _ in range(octaves):
        s = max(1, int(scale / freq))
        noise = rng2.random((max(1, H // s + 2), max(1, W // s + 2))).astype(np.float32)
        import scipy.ndimage
        zoomed = scipy.ndimage.zoom(noise, (H / noise.shape[0], W / noise.shape[1]), order=1)
        zoomed = zoomed[:H, :W]
        result += zoomed * amp
        amp *= 0.5
        freq *= 2.0
    return result

try:
    import scipy.ndimage
    has_scipy = True
except ImportError:
    has_scipy = False

if not has_scipy:
    import subprocess
    subprocess.run(["pip", "install", "scipy", "-q"])
    import scipy.ndimage

noise = fbm(77, 60)
noise = (noise - noise.min()) / (noise.max() - noise.min())

# Create resolution envelope: high at center (x=W/2), low at edges
# Gaussian peaked at center
x = np.linspace(0, 1, W)
center = 0.5
sigma = 0.08  # narrow — the scar is a thin band
envelope = np.exp(-((x - center)**2) / (2 * sigma**2))  # shape: (W,)
envelope = envelope[np.newaxis, :]  # broadcast over H

# "Resolution" = how fine the texture is.
# Low res: smooth the noise heavily. High res: use at fine scale.
# Approach: blend between heavily blurred and fine noise based on envelope.

fine = fbm(88, 8)
fine = (fine - fine.min()) / (fine.max() - fine.min())

coarse = scipy.ndimage.gaussian_filter(noise, sigma=18)
coarse = (coarse - coarse.min()) / (coarse.max() - coarse.min())

# Blend: scar=fine, edges=coarse
blended = envelope * fine + (1 - envelope) * coarse

# Color: edges desaturated warm-grey, center deep amber/rust
# Map to color by envelope level
env2d = (envelope * np.ones((H, 1)))  # (H, W)

r_edge = np.array([0.45, 0.42, 0.38])
r_center = np.array([0.75, 0.38, 0.12])

env3 = env2d[:, :, np.newaxis]  # (H, W, 1)
c = r_edge * (1 - env3) + r_center * env3
brightness = (0.5 + 0.5 * blended)[:, :, np.newaxis]
R = np.clip(c * brightness, 0, 1)

img_arr = (R * 255).astype(np.uint8)
img = Image.fromarray(img_arr)

# Add a very faint highlight along the scar centerline
from PIL import ImageDraw
draw = ImageDraw.Draw(img)
cx = W // 2
draw.line([(cx, 0), (cx, H-1)], fill=(200, 160, 90, 128), width=1)

img.save("/home/sprite/slop-salon-lelia/assets/scar-center.png")
print("saved")
