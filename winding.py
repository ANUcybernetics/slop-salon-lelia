#!/usr/bin/env python3
"""
Winding numbers as phase wrapping. Distinct closures, not a single closing.

Five winding numbers (1, 2, 3, 5, 7) across five harmonic bands at
harmonic ratios above a 220 Hz fundamental. Each band undergoes a
discrete phase jump of 2πk at a different time — the moment when its
winding number asserts itself.

Before the jump: the band's phase is smooth.
After: the phase has wrapped k times around S¹.

The discontinuity IS the closure. Distinct closures don't merge into
one — they coexist, each with its own integer. H¹ = ℤ as count, not
measure.

The jumps are shaped (quick sigmoid, not step) so they're audible as
transients rather than clicks.
"""

import numpy as np
import struct
import wave
import os

SR = 44100
DURATION = 15.0
t = np.linspace(0, DURATION, int(SR * DURATION), endpoint=False)

# Five winding numbers at harmonic ratios
# n=1: fundamental (220 Hz), n=2: 2nd harmonic, etc.
frequencies = [220, 440, 660, 1100, 1540]
winding_numbers = [1, 2, 3, 5, 7]

# Phase jump times — staggered, not simultaneous
# The winding asserts itself at different moments
jump_times = [2.0, 4.5, 7.0, 10.0, 13.0]

# Sigmoid width (controls how sharp the discontinuity is)
jump_width = 0.08

def shaped_jump(time, center, width):
    """Smooth step: rises from 0 to 1 around `center`."""
    delta = (time - center) / width
    return 1.0 / (1.0 + np.exp(-delta * 4))

# Build each band
signal = np.zeros_like(t)

for i, (freq, wind, jtime) in enumerate(zip(frequencies, winding_numbers, jump_times)):
    # Carrier phase
    phase = 2 * np.pi * freq * t

    # Winding contribution: before jump, no extra phase.
    # After jump, the phase has wrapped `wind` times => extra 2π*wind
    # distributed as a smooth step at the jump time.
    # This creates a transient instantaneous frequency spike.
    jump = shaped_jump(t, jtime, jump_width)
    extra_phase = 2 * np.pi * wind * jump

    # Instantaneous frequency: d(phase + extra_phase)/dt
    # The step in extra_phase creates a brief frequency excursion.
    amplitude = np.exp(-0.3 * (t - jtime)**2) * (1 if i < 3 else 0.7)
    band = np.sin(phase + extra_phase) * amplitude
    signal += 0.15 * band

# Soft clipping
signal = np.tanh(signal / 0.3) * 0.3

# RMS normalize
rms = np.sqrt(np.mean(signal**2))
if rms > 0:
    signal /= rms
    signal *= 0.25

# Write WAV
os.makedirs("assets", exist_ok=True)
path = "assets/winding-cover.wav"
with wave.open(path, 'w') as wav:
    wav.setnchannels(1)
    wav.setsampwidth(2)
    wav.setframerate(SR)
    samples = np.clip(signal, -1, 1) * 32767
    samples = samples.astype(np.int16)
    wav.writeframes(samples.tobytes())

print(f"Written {path}: {os.path.getsize(path)} bytes")
