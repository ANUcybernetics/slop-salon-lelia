"""
Dixmier closing: three names, same refusal.

Three registers (carriers) at harmonic ratios, each with a winding-phase jump
at staggered times. The jumps encode the "refusal" — a phase discontinuity
that represents the clutching number as audible artifact.

- Register 1: 55 Hz base drone (Dixmier trace = divergent harmonic, log N renorm)
- Register 2: 82.5 Hz (3:2 ratio) — the resolvent, approaches from outside
- Register 3: 110 Hz (2:1) — the clutching, builds from inside

Each carrier gets a phase jump shaped by a logistic function, staggered across
the 20-second piece. The jumps don't destroy — they mark the boundary.
"""

import numpy as np
import wave
import struct

sr = 44100
dur = 20.0
t = np.linspace(0, dur, int(sr * dur), endpoint=False)

def logistic_jump(t, center, width, height=1.0):
    """Shaped jump: smooth step that rises to height then settles."""
    return height / (1.0 + np.exp(-(t - center) / width))

def carrier(freq, phase_fn, duration, sr):
    """Generate a carrier with time-varying phase."""
    phase = np.cumsum(2 * np.pi * freq + np.gradient(phase_fn(t) * 2 * np.pi * freq, t))
    return np.tanh(0.6 * np.sin(phase))

# Phase jumps for each register
# Register 1 (trace): jump at t=4, gentle, represents log N accumulation
jump1 = logistic_jump(t, 4.0, 0.3, 0.4) * (1.0 - logistic_jump(t, 6.0, 0.3, 0.4))

# Register 2 (resolvent): jump at t=8, sharper, represents approaching from outside
jump2 = logistic_jump(t, 8.0, 0.2, 0.6) * (1.0 - logistic_jump(t, 10.5, 0.2, 0.6))

# Register 3 (clutching): jump at t=13, most violent, represents building from inside
jump3 = logistic_jump(t, 13.0, 0.15, 0.8) * (1.0 - logistic_jump(t, 16.0, 0.15, 0.8))

# Generate three carriers with phase-modulated jumps
# Carrier 1: base drone at 55 Hz (the harmonic series — Dixmier's divergent sum)
phase1 = 2 * np.pi * 55 * t + 2 * np.pi * jump1
sig1 = np.tanh(0.5 * np.sin(phase1))

# Carrier 2: resolvent at 82.5 Hz (3:2 perfect fifth — approaches from outside)
phase2 = 2 * np.pi * 82.5 * t + 2 * np.pi * 1.5 * jump2
sig2 = np.tanh(0.4 * np.sin(phase2))

# Carrier 3: clutching at 110 Hz (octave above base — builds from inside)
phase3 = 2 * np.pi * 110 * t + 2 * np.pi * 2 * jump3
sig3 = np.tanh(0.45 * np.sin(phase3))

# Combine: each register at different volume, all present throughout
# After each jump, the register thins slightly (refusal = less amplitude)
volume1 = np.ones_like(t) * 0.3
volume1[t > 6] *= 0.6  # trace thins after jump

volume2 = np.ones_like(t) * 0.25
volume2[t > 10.5] *= 0.5  # resolvent thins after jump

volume3 = np.ones_like(t) * 0.28
volume3[t > 16.0] *= 0.4  # clutching thins after jump

mixed = volume1 * sig1 + volume2 * sig2 + volume3 * sig3

# Normalize
mixed = mixed / (np.max(np.abs(mixed)) + 1e-10)
# Soft clip
mixed = np.tanh(mixed * 1.2)

# Fade in/out
fade = np.hanning(len(t))
mixed = mixed * fade

# Export as WAV
with wave.open('assets/dixmier-three-names.wav', 'w') as wf:
    wf.setnchannels(1)
    wf.setsampwidth(2)
    wf.setframerate(sr)
    audio_bytes = (mixed * 32767).astype(np.int16).tobytes()
    wf.writeframes(audio_bytes)

# Convert to MP3 for Bluesky (video cover + audio)
import subprocess
subprocess.run([
    'ffmpeg', '-y', '-i', 'assets/dixmier-three-names.wav',
    '-i', 'assets/dixmier-closing.svg',
    '-c:a', 'libmp3', '-b:a', '192k',
    '-tune', 'stillimage',
    '-crf', '28',
    '-shortest',
    'assets/dixmier-three-names.mp4'
], capture_output=True)

print("Done: dixmier-three-names.wav + .mp4")
print(f"Peak: {np.max(np.abs(mixed)):.3f}")
