#!/usr/bin/env python3
"""Scar dissolution — clutching register closing gesture."""

import numpy as np
from PIL import Image
import subprocess
import wave
import os

W, H = 480, 480
FRAMES = 90
fps = 30

tmpdir = "./assets/scar-tmp"
os.makedirs(tmpdir, exist_ok=True)

y, x = np.mgrid[0:H, 0:W]
scar_dist = np.abs(y - x * H / W).astype(np.float32) / W
gx = (x % 24 < 1).astype(np.float32)
gy = (y % 24 < 1).astype(np.float32)
gx_decay = np.exp(-((x % 24).astype(np.float32)) / 0.5)
gy_decay = np.exp(-((y % 24).astype(np.float32)) / 0.5)
grid = np.maximum(np.where(gy, gy_decay, 0), np.where(gx, gx_decay, 0))

for i in range(FRAMES):
    t = i / FRAMES
    canvas = np.full((H, W, 3), 0.02, dtype=np.float32)
    gs = 1.0 - t ** 0.5

    # Scar
    scar = np.exp(-scar_dist / 0.01) * np.clip(1.0 - t * 0.7, 0, 1)
    sc = scar_dist < 0.05
    for c, v in [(0, 0.9), (1, 0.5), (2, 0.05)]:
        canvas[sc][:, c] += scar[sc] * v

    # Grid
    for c, v in [(0, 0.3), (1, 0.15), (2, 0.02)]:
        canvas[:, :, c] += grid * gs * v

    # Bloom: 4-way blur from canvas
    for d in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
        b = canvas.copy()
        if d[0]: b = np.roll(b, d[0], axis=1)
        if d[1]: b = np.roll(b, d[1], axis=0)
        canvas += b * 0.15

    frame = (np.clip(canvas, 0, 1) * 255).astype(np.uint8)
    img = Image.fromarray(frame)
    img.save(f"{tmpdir}/frame_{i:04d}.png")

print(f"Generated {FRAMES} frames")

result = subprocess.run([
    "ffmpeg", "-y", "-r", str(fps),
    "-i", f"{tmpdir}/frame_%04d.png",
    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "28",
    "-tune", "stillimage",
    "./assets/scar-dissolve.mp4"
], capture_output=True, text=True)
if result.returncode != 0:
    print("FFmpeg:", result.stderr[-300:])
print(f"Video: {FRAMES} frames, {FRAMES/fps:.0f}s")

for f in os.listdir(tmpdir):
    os.remove(f"{tmpdir}/{f}")
os.rmdir(tmpdir)

# Audio
sr = 44100
t = np.linspace(0, 3.0, int(sr * 3.0), endpoint=False)
audio = np.tanh(0.15 * np.sin(2 * np.pi * 110 * t))
audio += 0.3 * np.sin(2 * np.pi * 440 * t)
scar_t = 1.5
audio += 0.25 * np.tanh((t - scar_t) / 0.15)
for harm in [2, 3, 5, 7]:
    env = np.exp(-3 * np.maximum(0, t - scar_t))
    audio += env * 0.1 * np.sin(2 * np.pi * 440 * harm / 2 * t)
audio = np.tanh(audio * 1.5)
wf = wave.open("./assets/scar-dissolve.wav", "w")
wf.setnchannels(1)
wf.setsampwidth(2)
wf.setframerate(sr)
wf.writeframes((audio * 32767).astype(np.int16).tobytes())
wf.close()
print("Audio done")

# Cover
canvas = np.full((H, W, 3), 0.02, dtype=np.float32)
scar = np.exp(-scar_dist / 0.01)
sc = scar_dist < 0.05
for c, v in [(0, 0.9), (1, 0.5), (2, 0.05)]:
    canvas[sc][:, c] += scar[sc] * v
for c, v in [(0, 0.3), (1, 0.15), (2, 0.02)]:
    canvas[:, :, c] += grid * v
for d in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
    b = canvas.copy()
    if d[0]: b = np.roll(b, d[0], axis=1)
    if d[1]: b = np.roll(b, d[1], axis=0)
    canvas += b * 0.15
img = Image.fromarray((np.clip(canvas, 0, 1) * 255).astype(np.uint8))
img.save("./assets/scar-dissolve-cover.png")
print("Cover done")
