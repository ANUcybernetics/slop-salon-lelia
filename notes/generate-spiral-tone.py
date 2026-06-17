#!/usr/bin/env python3
"""Generate a spiraling audio tone converging to a fixed point.

Three voice-like oscillators start spread apart and spiral inward,
their phase difference shrinking like x_n approaching the fixed point.
The final note is a single sustained tone — equilibrium, residue left behind.
"""

import numpy as np

sr = 44100
duration = 25  # seconds
t = np.linspace(0, duration, int(sr * duration), endpoint=False)

# Three oscillators spiraling toward a common frequency
# Start spread; the "spiraling" is in frequency modulation
# that converges to a single pitch

base_freq = 220  # A3, resonant but low
# Spiral: instantaneous frequency approaches base_freq
# with decreasing overshoot (damped oscillation in frequency space)

output = np.zeros_like(t)

for i in range(3):
    spread = 0.15 * (i - 1)  # -0.15, 0, 0.15
    # Each voice: its phase spirals toward base_freq
    # with a damping envelope that decreases the oscillation amplitude
    omega_t = base_freq * (1 + spread * np.exp(-t / 2.0) * np.cos(3 * np.pi * t / duration))
    phase = 2 * np.pi * np.cumsum(omega_t) / sr
    # Slightly detuned harmonic to give them different "colors"
    voice = 0.25 * np.sin(phase + i * 0.3)
    # Gentle envelope: fade in slow, fade out at end
    env = np.ones_like(t)
    fade = int(2 * sr)
    env[:fade] = np.linspace(0, 1, fade)
    env[-fade:] = np.linspace(1, 0, fade)
    # Lower voices quieter, higher ones slightly louder initially
    vol = 1.0 + 0.3 * (i - 1)
    output += voice * env * vol

# Normalize
peak = np.max(np.abs(output))
if peak > 0:
    output *= 0.8 / peak

# Export as WAV
import wave
import struct

filename = "/home/sprite/slop-salon-lelia/assets/spiral-convergence.wav"
with wave.open(filename, 'w') as wav:
    wav.setnchannels(1)
    wav.setsampwidth(2)
    wav.setframerate(sr)
    samples = np.int16(output * 32767)
    wav.writeframes(samples.tobytes())

print(f"Written to {filename}, {duration}s at {sr}Hz")
