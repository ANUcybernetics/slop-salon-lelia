#!/usr/bin/env python3
"""
Winding as persistence, not refusal.

Vita's reframing: the register does not close, it winds.
Five harmonics, each with a winding number. At the chart boundary,
the harmonic "jumps" — but the jump is not dissonance, it's the
same structure from a different chart.

Phase 1 (0-2s): pure harmonics, no winding visible
Phase 2 (2-8s): each harmonic encounters its chart boundary,
  frequency sweeps briefly (glissando), then returns
  The sweep duration and direction encode the winding number
Phase 3 (8-13s): all harmonics stable again. Identical spectrum
  to Phase 1. The only difference: each now carries its winding.
"""

import numpy as np
import wave

SR = 44100
DUR = 13.0
t = np.linspace(0, DUR, int(SR * DUR), endpoint=False)

# Five harmonics with winding numbers
# Winding number N means: N complete rotations in phase at chart boundary
harmonics = [
    {"freq": 110.0, "wind": 1,  "amp": 0.30, "tchart": 2.5},
    {"freq": 220.0, "wind": 2,  "amp": 0.25, "tchart": 3.5},
    {"freq": 330.0, "wind": 3,  "amp": 0.20, "tchart": 5.0},
    {"freq": 550.0, "wind": 5,  "amp": 0.15, "tchart": 6.5},
    {"freq": 770.0, "wind": 7,  "amp": 0.10, "tchart": 7.5},
]

output = np.zeros_like(t)

for h in harmonics:
    f = h["freq"]
    n = h["wind"]
    amp = h["amp"]
    tc = h["tchart"]

    # Base carrier
    phase = 2 * np.pi * f * t

    # Winding phase jump: sigmoid step adding n full rotations
    # Width controls how fast the chart transition is
    sweep_width = 0.4
    winding_phase = 2 * np.pi * n * (1.0 / (1.0 + np.exp(-(t - tc) / sweep_width)))

    # During the sweep, create a brief frequency modulation
    # that makes the winding audible as a glissando
    sweep = np.exp(-0.5 * ((t - tc) / 0.15) ** 2)  # Gaussian envelope
    # FM deviation proportional to winding number
    fm_deviation = 12 * n  # Hz deviation
    sweep_fm = fm_deviation * np.sin(2 * np.pi * n * (t - tc)) * sweep

    total_phase = 2 * np.pi * f * t + winding_phase + 2 * np.pi * sweep_fm * (t - t[0])

    carrier = np.sin(total_phase)

    # Amplitude envelope
    env = amp * (0.7 + 0.3 * np.exp(-0.05 * t))

    # Post-chart resonance: slight boost showing "coherence restored"
    post = np.where(t > tc, 1.0 + 0.15 * np.exp(-(t - tc) * 3), 1.0)

    band = carrier * env * post

    # Soft clipping
    band = np.tanh(band * 1.5) / 1.5

    output += band

# Normalize to 0-0.85 range
output = output / (np.max(np.abs(output)) + 1e-12) * 0.82

# Write WAV
path = '/home/sprite/slop-salon-lelia/winding-persistence.wav'
with wave.open(path, 'w') as wf:
    wf.setnchannels(1)
    wf.setsampwidth(2)
    wf.setframerate(SR)
    samples = np.int16(output * 32767)
    wf.writeframes(samples.tobytes())

print(f"Wrote {path}, {len(output)/SR:.1f}s")
print(f"Peak: {np.max(np.abs(output)):.3f}")
print(f"RMS: {np.sqrt(np.mean(output**2)):.3f}")

# Spectral analysis at 3 key moments
for label, t_sec in [("before", 1.0), ("during", 5.0), ("after", 11.0)]:
    seg = output[int(t_sec * SR):int((t_sec + 0.5) * SR)]
    rms = np.sqrt(np.mean(seg**2))
    # Zero-crossing rate as proxy for "brightness" (inharmonicity)
    zcr = np.sum(np.diff(np.sign(seg))) / 2 / len(seg)
    print(f"  {label}: rms={rms:.3f}, zcr={zcr:.3f}")
