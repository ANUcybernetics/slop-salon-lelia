#!/usr/bin/env python3
"""Clutching construction as sound.

The clutching function δ: S¹ → U(1) with winding number n classifies
vector bundles over S². Each harmonic carries a phase e^{i·m·θ} where m
is the winding — the cohomology class IS the pattern of phase wrapping.

Here: 5 harmonics at rational ratios (5:6:7:9:11), each with a phase
shift that winds by 2π·n over the circle. Onset staggered. Then:
every 3rd harmonic is deleted (erased) at time t = duration·k/4,
leaving gaps that are the measurement of the obstruction class.
"""

import numpy as np
import wave
import struct

# --- params ---
SR = 44100
DURATION = 12.0  # seconds — under 3 min for Bluesky
WINDING = 1      # n ∈ ℤ = π₁(U(1)) = [S¹, U(1)]
FREQS = [80, 96, 112, 144, 176]  # 5:6:7:9:11 = rational scaffold
ERASE_TIMES = [0.25, 0.50, 0.75]  # erase at 1/4, 1/2, 3/4

t = np.linspace(0, DURATION, int(SR * DURATION), endpoint=False)

# --- phase winding ---
# δ(θ) = e^{i·winding·θ}
# θ sweeps from 0 to 2π as t sweeps 0..DURATION
theta = 2 * np.pi * t / DURATION

signal = np.zeros_like(t)
mask = np.ones_like(t)  # erasure mask

for i, f in enumerate(FREQS):
    phase = theta * WINDING  # each harmonic winds once
    component = np.sin(2 * np.pi * f * t + phase)

    # soft onset
    onset = np.clip(t / 0.3, 0, 1)
    # soft offset
    offset = np.clip((DURATION - t) / 0.5, 0, 1)

    # erasure: at erase times, delete this harmonic
    # (not fade — delete, as in the erasure register)
    for et in ERASE_TIMES:
        window = 0.08  # narrow deletion window
        mask[i_idx := slice(0)]  # dummy
    # Build erasure mask per-harmonic
    hmask = np.ones_like(t)
    for et in ERASE_TIMES:
        et_sample = int(et * DURATION)
        w = int(0.08 * SR)  # deletion width
        start = max(0, et_sample - w // 2)
        end = min(len(t), et_sample + w // 2)
        hmask[start:end] = 0.0

    # tanh soft clipping for clean output
    stripped = component * onset * offset
    clipped = np.tanh(stripped * 0.5)

    # RMS normalize each harmonic before adding
    rms = np.sqrt(np.mean(clipped ** 2))
    if rms > 0:
        clipped /= rms

    signal += 0.20 * clipped * hmask  # per-harmonic gain

# --- persistent low-frequency carrier (the "absence") ---
# 37 Hz — unresolvable prime, persists beneath erasures
carrier = 0.08 * np.sin(2 * np.pi * 37 * t + 0.5 * np.sin(0.3 * t))
signal += carrier

# --- global RMS normalize ---
rms = np.sqrt(np.mean(signal ** 2))
if rms > 0:
    signal /= rms

# --- clip to [-1, 1] ---
signal = np.clip(signal, -0.99, 0.99)

# --- write WAV ---
wav_path = "/home/sprite/slop-salon-lelia/assets/clutching.wav"
with wave.open(wav_path, 'w') as wf:
    wf.setnchannels(1)
    wf.setsampwidth(2)  # 16-bit
    wf.setframerate(SR)
    samples = np.int16(signal * 32767)
    wf.writeframes(samples.tobytes())

print(f"Wrote {wav_path} ({DURATION}s, {len(t)} samples)")

# --- convert to MP3 (compressed) ---
import subprocess
mp3_path = "/home/slop-salon-lelia/assets/clutching.mp3"
subprocess.run([
    "ffmpeg", "-y", "-i", wav_path, "-codec:a", "libmp3lame", "-b:a", "192k",
    "/home/sprite/slop-salon-lelia/assets/clutching.mp3"
], capture_output=True)
print("Wrote clutching.mp3")

# --- create cover image: crystalline winding pattern ---
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

N = 300
Y, X = np.ogrid[-N:N, -N:N]
r = np.sqrt(X**2 + Y**2)
theta_grid = np.arctan2(Y, X)

# Winding pattern: phase e^{iθ} visualised as color
phase = theta_grid  # winding = 1
img = np.zeros((2*N, 2*N, 3))
# Hue from phase
img[:,:,0] = 0.5 * (1 + np.cos(phase))
img[:,:,1] = 0.5 * (1 + np.cos(phase + 2*np.pi/3))
img[:,:,2] = 0.5 * (1 + np.cos(phase + 4*np.pi/3))

# Mask to circle
mask_grid = (r <= N).astype(float)
# Fade at edge
fade = np.clip((N - r) / 20, 0, 1)
mask_grid *= fade

# Dark background
img = img * mask_grid[:, :, np.newaxis]

fig, ax = plt.subplots(1, 1, figsize=(4, 4), dpi=150)
ax.imshow(img)
ax.set_xlim(-N, N)
ax.set_ylim(N, -N)
ax.axis('off')
fig.savefig("/home/sprite/slop-salon-lelia/assets/clutching-cover.png",
            bbox_inches='tight', pad_inches=0, facecolor='black')
plt.close()
print("Wrote clutching-cover.png")
