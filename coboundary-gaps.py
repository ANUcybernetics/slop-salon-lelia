#!/usr/bin/env python3
"""Coboundary gaps: the operator d maps 0-cochains to 1-cochains.
Its kernel is the constants. Its image is the exact forms.
H¹ = ker(d₁)/im(d₀) — the gaps that the coboundary cannot fill.

Harmonic structure:
- Kernel drone (55Hz): what the coboundary cannot see through
- Image harmonics: exact forms entering at coboundary times
- Gaps: silence at frequencies that are NOT in the image
"""

import numpy as np
import wave
import struct

# --- Audio synthesis ---
sr = 44100
duration = 12  # seconds — short, structural

t = np.linspace(0, duration, int(sr * duration), endpoint=False)

# Kernel drone — 55Hz, constant under d
# This is what the coboundary sees as zero, but we hear it as the constant background
kernel_drone = 0.12 * np.sin(2 * np.pi * 55 * t)
# Sub-octave for body
kernel_drone += 0.08 * np.sin(2 * np.pi * 27.5 * t)

# Image: coboundary applied to discrete 0-cochain values
# Imagine a simplicial complex: 5 vertices, edges between them
# 0-cochains: values on vertices (5 values)
# 1-cochains: values on edges (9 edges for a 5-vertex graph)
# Coboundary matrix d: 9x5, d[f](u,v) = f(v) - f(u)

np.random.seed(42)
f0 = np.array([0.3, -0.2, 0.8, -0.5, 0.1])  # 0-cochain values

# Build coboundary matrix for a path graph + one cycle
# Edges: (0,1), (1,2), (2,3), (3,4) = path, plus (0,4) = closing edge
edges = [(0,1), (1,2), (2,3), (3,4), (0,4)]
d_matrix = np.zeros((len(edges), len(f0)))
for i, (u, v) in enumerate(edges):
    d_matrix[i, v] = 1
    d_matrix[i, u] = -1

# Apply coboundary
image = d_matrix @ f0  # 1-cochain values on edges

# Map image values to harmonic frequencies
# Each edge's coboundary value determines amplitude of a harmonic
fundamental = 110  # A3
gaps = [3/2, 5/4, 7/6, 9/8]  # frequencies NOT in the image (harmonic gaps)

# Image harmonics — exact forms ring clearly
image_harmonics = np.zeros_like(t)
for i, amp in enumerate(image):
    freq = fundamental * (1 + i * 0.15)
    envelope = np.clip(1 - np.exp(-30 * t)) * np.clip(np.exp(-2 * (t - i * 0.8) * (t - i * 0.8) / 0.5))
    image_harmonics += amp * 0.06 * np.sin(2 * np.pi * freq * t) * envelope

# Gap tones — the frequencies the coboundary CANNOT produce
# These enter as partial silences, heard only by contrast
gap_tones = np.zeros_like(t)
for i, gap_freq in enumerate(gaps):
    freq = fundamental * gap_freq
    # These are heard in the negative: they shape the envelope
    gap_envelope = 0.02 * np.sin(2 * np.pi * freq * t)
    gap_tones += gap_envelope * np.exp(-((t - 3 - i*1.5)**2) / 0.3)

# Composite
signal = kernel_drone + image_harmonics + gap_tones

# Soft clip
signal = np.tanh(signal * 1.5) / np.tanh(1.5)

# Normalize
signal = signal / (np.max(np.abs(signal)) + 1e-10) * 0.9

# Write WAV
wav_path = './assets/coboundary-gaps.wav'
with wave.open(wav_path, 'w') as wf:
    wf.setnchannels(1)
    wf.setsampwidth(2)
    wf.setframerate(sr)
    for sample in signal:
        wf.writeframes(struct.pack('<h', int(sample * 32767)))

print(f"Audio written: {wav_path}")

# --- Cover visualization ---
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))

# Left: coboundary matrix visualization
ax1.imshow(d_matrix, cmap='RdBu_r', vmin=-1, vmax=1, aspect='auto')
ax1.set_title('Coboundary operator d: C⁰ → C¹', fontsize=10, pad=10)
ax1.set_xlabel('Vertices (0-cochains)')
ax1.set_ylabel('Edges (1-cochains)')
ax1.set_xticks(range(5))
ax1.set_yticks(range(5))
ax1.text(2, -1.5, 'image: exact forms  |  kernel: constants', ha='center', fontsize=8)

# Right: spectral view — what the coboundary produces vs what it cannot
freqs = np.fft.rfft(signal)
freq_bins = np.fft.rfftfreq(len(signal), 1/sr)
mag = np.abs(freqs) / len(signal)

# Show only audible range
visible = freq_bins < 800
ax2.plot(freq_bins[visible], mag[visible], 'w-', linewidth=0.5)
ax2.set_title('Spectrum: kernel (55Hz) + image harmonics + gaps', fontsize=10, pad=10)
ax2.set_xlabel('Frequency (Hz)')
ax2.set_ylabel('Amplitude')
ax2.set_xlim(0, 600)
ax2.axvline(55, color='r', alpha=0.5, label='kernel drone')
ax2.axvline(55*3/2, color='b', alpha=0.3, ls='--', label='gap (not in image)')
ax2.legend(fontsize=7, loc='upper right')
ax2.set_facecolor('black')
ax1.set_facecolor('black')
fig.patch.set_facecolor('black')

plt.tight_layout(pad=1)
plt.savefig('./assets/coboundary-gaps-cover.png', dpi=150, bbox_inches='tight',
            facecolor=fig.get_facecolor(), edgecolor='none')
plt.close()
print(f"Cover written: ./assets/coboundary-gaps-cover.png")
