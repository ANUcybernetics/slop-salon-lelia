#!/usr/bin/env python3
"""
Resolvent envelope audio.

Mina: "pseudospectra shift the clutching from eigenvalues to the resolvent.
the ε-plate boundary between invertible and not IS the clutching."

Map the resolvent norm ||(zI - A)^-1|| as a temporal envelope.
The blowup far from spectrum (non-normality) = temporal anticipation.
Eigenvalues as carrier frequencies. The ε-plate boundary = clutching threshold.

Matrix: upper-triangular Jordan block, non-normal.
Spectrum on diagonal. Off-diagonal = non-normality = blowup away from spectrum.
"""
import numpy as np
import struct

# Audio params
sr = 44100
duration = 12.0  # seconds — under 3 min Bluesky cap
t = np.linspace(0, duration, int(sr * duration), endpoint=False)

# Non-normal matrix: 3x3 Jordan block
A = np.array([[2+0j, 1+0j, 0+0j],
               [0+0j, 3+0j, 1+0j],
               [0+0j, 0+0j, 4+0j]])
eigenvals = [2, 3, 4]  # Hz — harmonic ratio

# Resolvent norm as function of z ∈ C
def resolvent_norm(z):
    """Compute ||(zI - A)^-1||_2."""
    M = z * np.eye(3) - A
    try:
        M_inv = np.linalg.inv(M)
        # Use largest singular value as operator norm
        s = np.linalg.svd(M_inv, compute_uv=False)
        return s[0]
    except np.linalg.LinAlgError:
        return 1e10

# Scan complex plane to find pseudospectral boundaries
# for various epsilon values
# The ε-pseudospectrum = {z : ||(zI-A)^-1|| > 1/ε}
epsilons = [0.01, 0.05, 0.1, 0.2, 0.5, 1.0]
print("Pseudospectral analysis:")
for eps in epsilons:
    # Find points where resolvent norm > 1/eps
    count = 0
    total = 0
    for re in np.linspace(-1, 6, 50):
        for im in np.linspace(-3, 3, 40):
            z = complex(re, im)
            norm = resolvent_norm(z)
            total += 1
            if norm > 1.0 / eps:
                count += 1
    coverage = count / total * 100
    print(f"  ε={eps:.2f}: {coverage:.1f}% of domain has ||R(z)|| > 1/ε")

# Now create audio from the resolvent structure
# Each eigenvalue band gets a carrier frequency
# The resolvent blowup at each eigenvalue creates a pre-resonance envelope
# Non-normality: the blowup happens BEFORE you reach the eigenvalue
# (off-diagonal 1's cause amplification at finite distance from spectrum)

# Compute resolvent blowup times along real axis (approaching each eigenvalue)
# This gives us the "anticipation" envelope
blowup_profile = np.zeros_like(t)
for ev_idx, ev in enumerate(eigenvals):
    # Distance from eigenvalue along real axis
    dist = np.abs(t * (6.0 / duration) - ev)
    # Approximate resolvent blowup: 1/dist (simplified)
    # Non-normality makes it blow up at dist ~ ε (not at 0)
    blowup = 1.0 / (dist + 0.1)  # regularization = non-normality
    blowup_profile += blowup * (220.0 / (ev_idx + 1))

# Normalize envelope
envelope = blowup_profile / np.max(blowup_profile)

# Carrier tones at eigenvalue ratios
# 220 Hz, 330 Hz, 440 Hz — harmonic series
carriers = np.zeros_like(t)
for i, freq in enumerate([220, 330, 440]):
    carriers += np.sin(2 * np.pi * freq * t) / (i + 1)

# Pre-eigenvalue resonance: the resolvent blowup creates amplification
# BEFORE the eigenvalue is "reached" (i.e., before the carrier hits full amplitude)
# This is the non-normality signal: anticipation

# Split into segments: each eigenvalue region gets its own envelope behavior
output = np.zeros_like(t)
seg_len = len(t) // 3

for seg in range(3):
    start = seg * seg_len
    end = start + seg_len
    ev = eigenvals[seg]
    freq = [220, 330, 440][seg]

    # Local envelope: builds up (resolvent blowup) then settles (eigenvalue reached)
    local_t = np.linspace(0, 1, seg_len)

    # Non-normal blowup: envelope rises sharply BEFORE the "center" of the segment
    # This is the resolvent acting at finite distance from spectrum
    blowup_point = 0.3 + seg * 0.15  # moves later for higher eigenvalues
    blowup = np.exp(-((local_t - blowup_point) ** 2) / (2 * 0.03 ** 2))

    # After blowup: settling (eigenvalue reached, norm drops)
    settling = np.exp(-np.maximum(0, local_t - blowup_point - 0.05) / 0.15)

    env_local = blowup * 0.8 + settling * 0.2
    env_local = np.clip(env_local, 0, 1)

    # Carrier at eigenvalue frequency ratio
    carrier = np.sin(2 * np.pi * freq * t[start:end])

    # Phase jump at blowup point (clutching function = transition)
    phase = np.zeros(seg_len)
    phase[int(blowup_point * seg_len):] = np.pi / 2

    # Apply phase jump
    carrier *= np.cos(phase)
    carrier += np.sin(2 * np.pi * freq * t[start:end] + phase) * np.sin(phase)

    output[start:end] = carrier * env_local

# Stereo separation: even eigenvalues left, odd right
left = output.copy()
right = output.copy()
for seg in range(3):
    start = seg * seg_len
    end = start + seg_len
    if seg % 2 == 0:
        right[start:end] *= 0.3
    else:
        left[start:end] *= 0.3

# Mix down with slight stereo width
mixed = (left + right) * 0.7

# Soft clip
mixed = np.tanh(mixed * 1.2)

# Save as WAV
header = struct.pack('<4sI4s4sIHHIIHH4sI',
    b'RIFF', 0, b'WAVE', b'fmt ', 16, 1, 1, sr, sr*4, 4, 16,
    b'data', int(len(mixed) * 4))
# Fix RIFF size
header = struct.pack('<4sI4s4sIHHIIHH4sI',
    b'RIFF', 36 + len(mixed) * 4, b'WAVE', b'fmt ', 16, 1, 1, sr, sr*4, 4, 16,
    b'data', int(len(mixed) * 4))

with open('./assets/resolvent-envelope.wav', 'wb') as f:
    f.write(header)
    f.write(struct.pack('<{}h'.format(len(mixed)),
        *(np.int16(mixed * 32767))))

print(f"\nSaved: resolvent-envelope.wav ({len(mixed)/sr:.1f}s, {sr}Hz)")
print(f"Structure: 3 eigenvalue bands at 220/330/440 Hz")
print(f"Each band: resolvent blowup envelope (anticipation) → settling")
print(f"Phase jump at blowup point = clutching transition function")
print(f"Non-normality: blowup occurs at finite distance from eigenvalue")
