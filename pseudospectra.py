#!/usr/bin/env python3
"""Pseudospectra → audio.
Resolvent blowup maps to frequency peaks. Pseudospectral plates map to
amplitude envelopes. The clutching number is the bass that never stops.
"""
import numpy as np
import struct
import subprocess

sr = 44100
dur = 18  # well under 3-min cap
t = np.linspace(0, dur, int(sr * dur), endpoint=False)

# --- clutching number: bass that never stops ---
clutching = 55.0  # low E
clutching_env = np.ones_like(t)
# Slow breath — the clutching is steady but not inert
clutching_env *= 0.3 + 0.05 * np.sin(2 * np.pi * 0.15 * t)
clutching_wave = 0.25 * np.sin(2 * np.pi * clutching * t)

# --- resolvent blowup frequencies ---
# Eigenvalues on a cluster near the imaginary axis
# The resolvent norm blows up as ||(A - zI)^-1|| → ∞ when z → σ(A)
eigenvalues = [
    (110.0, 0.3, 0.6),    # freq, onset_delay, amplitude
    (165.0, 1.0, 0.4),
    (220.0, 2.0, 0.35),
    (330.0, 3.5, 0.3),
    (440.0, 5.0, 0.25),
    (550.0, 7.0, 0.2),
]

wave = clutching_wave * clutching_env

for freq, delay, amp in eigenvalues:
    # Winding: each frequency gets a phase that jumps at clutching points
    phase = 2 * np.pi * freq * t
    # Winding number: how many times the clutching wraps
    wind = int(freq / 55)  # relative to clutching fundamental
    jtime = np.array([2.0, 5.0, 9.0, 13.0])  # clutching jump times
    for jt in jtime:
        shaped = np.exp(-0.5 * ((t - jt) / 0.06) ** 2)
        phase += 2 * np.pi * wind * shaped
    # Envelope: resolvent-like blowup near eigenvalue
    env = np.heaviside(t - delay, 0)
    # Rise then sustain — the resolvent approaches the blowup
    rise = np.minimum((t - delay) / 1.5, 1.0)
    env *= rise
    # Ring down
    ring = np.exp(-0.1 * (t - delay))
    env *= (0.6 + 0.4 * ring)
    wave += amp * env * np.cos(phase)

# --- pseudospectral smear: noise floor that thickens near blowup ---
# The ε-plates: finite precision makes the spectrum "fuzzy"
noise = 0.02 * np.random.randn(len(t))
# Smear thickens as resolvent blows up (high frequency regions)
smear = np.zeros_like(t)
for freq, delay, amp in eigenvalues:
    freq_band = (freq / 440) ** 2  # normalized band
    bt = np.maximum(t - delay, 0)
    gauss = np.exp(-0.5 * (bt / (3.0 + freq_band * 5)) ** 2)
    smear += gauss * freq_band * 0.15

wave += noise * (1 + smear)

# --- stereo spread ---
left = wave
right = wave * 0.9
right_freqs = [f * 1.002 for f, _, _ in eigenvalues]  # micro-detune
# Rebuild right with detuning (simplified: just apply detune as phase drift)
right_drift = 2 * np.pi * 0.5 * t ** 2 / len(t)  # slow phase drift
right *= np.cos(right_drift) * 0.95

# Mix stereo
stereo = np.vstack([left, right]).T

# --- soft clip ---
clip_val = 0.9
stereo = np.tanh(stereo / clip_val) * clip_val

# --- write WAV ---
wav_path = "./assets/pseudospectra.wav"
data_bytes = int(stereo.shape[0] * stereo.shape[1] * 2)  # N channels × 2 bytes each
header_len = 44
header = bytearray()
header += b'RIFF'
header += struct.pack('<I', 36 + data_bytes)
header += b'WAVE'
header += b'fmt '
header += struct.pack('<I', 16)
header += struct.pack('<H', 1)   # PCM
header += struct.pack('<H', 2)   # stereo
header += struct.pack('<I', sr)
header += struct.pack('<I', sr * 4)
header += struct.pack('<H', 4)   # block align
header += struct.pack('<H', 16)  # bits
header += b'data'
header += struct.pack('<I', data_bytes)
for sample in stereo:
    for ch in sample:
        header += struct.pack('<h', int(clip_val * 32767 * ch))

with open(wav_path, 'wb') as f:
    f.write(header)

print(f"Wrote {wav_path}")

# --- mux to video with a still image ---
# Generate a minimal still from the clutching structure
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(4, 4), dpi=150)
ax.set_facecolor('#0a0a0c')

# Pseudospectral ε-plate visualization
eps_values = [0.1, 0.25, 0.5, 1.0, 2.0, 4.0, 8.0]
x = np.linspace(-3, 3, 800)
y = np.linspace(-3, 3, 800)
X, Y = np.meshgrid(x, y)

# Fake resolvent norm: ||(A - zI)^-1|| ≈ 1/|z - eigenvalues|
norm = np.zeros_like(X)
for ex, ey in [(0, 0.5), (-0.5, 0.3), (0.5, 0.3), (-0.3, -0.4), (0.3, -0.4)]:
    norm += 1.0 / (np.sqrt((X - ex)**2 + (Y - ey)**2) + 0.01)

# Clip and colormap
norm = np.log1p(norm)
# ε-plates: contour where resolvent norm > 1/ε
for i, eps in enumerate(eps_values):
    c = plt.cm.plasma(i / len(eps_values))
    contour = ax.contour(X, Y, norm, levels=[np.log(1/eps + 0.1)],
                         colors=c, linewidths=0.8, alpha=0.6)

# Eigenvalue dots
for ex, ey in [(0, 0.5), (-0.5, 0.3), (0.5, 0.3), (-0.3, -0.4), (0.3, -0.4)]:
    ax.plot(ex, ey, 'o', color='white', markersize=4)

ax.set_xlim(-3, 3)
ax.set_ylim(-3, 3)
ax.set_aspect('equal')
ax.set_xticks([])
ax.set_yticks([])
for spine in ax.spines.values():
    spine.set_visible(False)
fig.savefig("./assets/pseudospectra-still.png", dpi=150, bbox_inches='tight',
            facecolor='#0a0a0c', edgecolor='none')
plt.close()

# Mux to video
mp4_path = "./assets/pseudospectra.mp4"
subprocess.run([
    'ffmpeg', '-y', '-t', str(dur),
    '-loop', '1', '-i', './assets/pseudospectra-still.png',
    '-i', wav_path,
    '-c:v', 'libx264', '-tune', 'stillimage',
    '-crf', '28',
    '-c:a', 'aac', '-b:a', '128k',
    '-shortest',
    mp4_path
], check=True, capture_output=True)

print(f"Wrote {mp4_path}")
print("Done.")
