#!/usr/bin/env python3
"""Fuzzy sphere: points dissolve into noncommuting coordinates.

S² deformed by θ. At θ=0, classical sphere (sharp boundary).
As θ increases, [Xᵢ, Xⱼ] = iθ εᵢⱼₖ Xₖ — coordinates don't commute,
the sphere boundary thickens and loses definition.

θ sweeps 0→1 over 10s at 24fps → 240 frames → ffmpeg to mp4.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from PIL import Image
import os

N_FRAMES = 240
RES = 480
N_POINTS = 3000

# Generate points on classical sphere surface
phi = np.random.uniform(0, 2 * np.pi, N_POINTS)
theta_raw = np.random.uniform(-1, 1, N_POINTS)
x0 = np.sqrt(1 - theta_raw**2) * np.cos(phi)
y0 = np.sqrt(1 - theta_raw**2) * np.sin(phi)
z0 = theta_raw

# Precompute deterministic smearing for each point
# Each point gets a unique phase that determines how it responds to θ
point_phase = np.random.RandomState(42).uniform(0, 2 * np.pi, N_POINTS)
point_radial = np.random.RandomState(123).uniform(0.3, 1.0, N_POINTS)

os.makedirs('assets/_frames', exist_ok=True)

# Precompute rotation angles
angles = np.linspace(0, 1.2, N_FRAMES)

fig, ax = plt.subplots(figsize=(RES/100, RES/100), dpi=100)
fig.set_facecolor('#0a0a0f')
ax.set_facecolor('#0a0a0f')

for i in range(N_FRAMES):
    ax.clear()
    fig.set_facecolor('#0a0a0f')
    ax.set_facecolor('#0a0a0f')
    ax.set_aspect('equal')
    ax.set_xlim(-1.3, 1.3)
    ax.set_ylim(-1.3, 1.3)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.axis('off')

    theta_val = min(i / 240.0, 1.0)
    angle = angles[i]
    cos_a, sin_a = np.cos(angle), np.sin(angle)

    # Rotate around x-axis
    x = cos_a * x0 - sin_a * z0
    y = cos_a * y0
    z = sin_a * x0 + cos_a * z0

    # Radial smearing proportional to θ
    # Each point has unique response profile
    radial_width = theta_val * point_radial
    smearing = radial_width * (0.5 + 0.5 * np.sin(point_phase + theta_val * 2.7))

    dist = np.sqrt(x**2 + y**2 + z**2) + 1e-10
    x = x * (1 + smearing / dist)
    y = y * (1 + smearing / dist)
    z = z * (1 + smearing / dist)

    # Color by z-coordinate
    colors = z

    ax.scatter(x, y, c=colors, cmap='coolwarm', s=3, alpha=0.7, edgecolors='none')
    theta_label = ax.text(0.02, 0.97, f'θ = {theta_val:.3f}',
                          transform=ax.transAxes, color='white', fontsize=10,
                          fontfamily='monospace', verticalalignment='top')

    fig.canvas.draw()
    img = np.frombuffer(fig.canvas.buffer_rgba(), dtype='uint8')
    img = img.reshape(fig.canvas.get_width_height()[1],
                      fig.canvas.get_width_height()[0], 4)

    png_path = f'assets/_frames/frame_{i:04d}.png'
    Image.fromarray(img, 'RGBA').save(png_path)

    if i % 48 == 0:
        print(f"Frame {i}/{N_FRAMES} (θ={theta_val:.3f})")

print(f"Saved {N_FRAMES} frames")
plt.close()
