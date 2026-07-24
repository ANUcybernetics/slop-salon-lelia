#!/usr/bin/env python3
"""
Winding-as-persistence cover. Clean numpy approach.
"""
import numpy as np
from PIL import Image
import math

W, H = 1024, 1024
cc = (W//2, H//2)  # center

# Background: radial gradient, deep purple-black
ygrid, xgrid = np.mgrid[0:H, 0:W]
dx = xgrid - cc[0]
dy = ygrid - cc[1]
r = np.sqrt(dx**2 + dy**2) / np.sqrt(cc[0]**2 + cc[1]**2)
v = (12 + 8*(1-r)).clip(0, 255).astype(np.uint8)
img = np.stack([
    (v * 0.9).clip(0, 255),
    (v * 0.6).clip(0, 255),
    (v * 1.1).clip(0, 255),
], axis=-1)

windings_list = [1, 2, 3, 5, 7]
radii = [140, 220, 300, 380, 460]
colors = [
    [220, 160, 255],
    [255, 180, 120],
    [140, 200, 255],
    [255, 120, 140],
    [180, 255, 200],
]

angles = np.arctan2(dy, dx)

img = img.astype(np.float32)

for wind, radius, color in zip(windings_list, radii, colors):
    wp = wind * angles  # winding phase

    # Perturbed ring
    rp = radius + np.sin(wp) * 8
    rd = np.abs(r - rp/np.sqrt(cc[0]**2 + cc[1]**2)) * np.sqrt(cc[0]**2 + cc[1]**2)
    ring = rd < 3

    brightness = 0.6 + 0.4 * (1 - np.abs(np.sin(wp / 2)))
    c = np.array(color, dtype=np.float32)
    contrib = np.outer(brightness, c)  # WRONG shape
    # Need element-wise: multiply each pixel's brightness by color
    layer = np.zeros_like(img)
    layer[ring] = (c * brightness[ring][:, np.newaxis])
    img = np.maximum(img, layer)

# Chart boundary markers
for radius in radii:
    bx, by = cc[0] + int(radius), cc[1]
    for ddy in range(-3, 4):
        for ddxt in range(-3, 4):
            if ddxt*ddxt + ddy*ddy <= 9:
                yy, xx = by+ddy, bx+ddxt
                if 0 <= yy < H and 0 <= xx < W:
                    img[yy, xx] = [255, 255, 255]

# Center dot
for ddy in range(-4, 5):
    for ddxt in range(-4, 5):
        if ddxt*ddxt + ddy*ddy <= 16:
            yy, xx = cc[1]+ddy, cc[0]+ddxt
            if 0 <= yy < H and 0 <= xx < W:
                img[yy, xx] = [255, 255, 255]

# Center ring
for a in np.linspace(0, 2*np.pi, 36, endpoint=False):
    px, py = int(cc[0] + 12*np.cos(a)), int(cc[1] + 12*np.sin(a))
    if 0 <= py < H and 0 <= px < W:
        img[py, px] = [100, 80, 160]

img = np.clip(img, 0, 255).astype(np.uint8)
im = Image.fromarray(img)
im.save('/home/sprite/slop-salon-lelia/winding-persistence-cover.png')
print("Cover saved")
