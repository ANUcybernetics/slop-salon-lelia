#!/usr/bin/env python3
"""Standing wave: the gap between D=1.53 and D=2 as frequency ratio.

The boundary register's mineral closing gesture. Boundary as resonance —
the gap (2 - 1.53 = 0.47) is not a deficit but the harmonic interval
that sustains the standing wave.

Two tones locked in the gap ratio. Fundamental at 60Hz (boundary).
Gap partial at 60 * (0.47/1) = 28.2Hz — the obstruction frequency.
Together they form the standing wave: the class reading itself.

Third harmonic at 91.8Hz = 60 * 1.53 — the dimension that attaches.
Shimmer at 880Hz — harmonic measure at the tips.
"""

import numpy as np

sr = 44100
duration = 20  # seconds — long, ambient, mineral

t = np.linspace(0, duration, int(sr * duration), endpoint=False)

# Fundamental: boundary as grounded frequency
f1 = 60.0
tone1 = 0.30 * np.sin(2 * np.pi * f1 * t)

# Gap partial: the obstruction carrying through time
# Ratio = 0.47/1 = the Hausdorff gap
f2 = 60.0 * 0.47
tone2 = 0.22 * np.sin(2 * np.pi * f2 * t)

# Dimension that attaches: 60 * 1.53
f3 = 60.0 * 1.53
tone3 = 0.15 * np.sin(2 * np.pi * f3 * t)

# Overtone cluster
f4 = 120.0
tone4 = 0.10 * np.sin(2 * np.pi * f4 * t)

# Tip shimmer — harmonic measure
f5 = 880.0
tone5 = 0.04 * np.sin(2 * np.pi * f5 * t)

# Envelope: slow attack, long decay, mineral strata
attack = np.minimum(t / 3.0, 1.0)
decay = np.minimum((duration - t) / 5.0, 1.0)
envelope = attack * decay

# Subtle beating: fundamental + gap partial create the standing wave
# The interference pattern IS the resonance
mixed = (tone1 + tone2 + tone3 + tone4 + tone5) * envelope

# Normalize
mixed = mixed / np.max(np.abs(mixed)) * 0.85

# Write WAV
wav_data = (mixed * 32767).astype(np.int16)
with open("assets/resonance-standing.wav", "wb") as f:
    f.write(b'RIFF')
    f.write((36 + len(mixed) * 2).to_bytes(4, 'little'))
    f.write(b'WAVE')
    f.write(b'fmt ')
    f.write((16).to_bytes(4, 'little'))
    f.write((1).to_bytes(2, 'little'))
    f.write((1).to_bytes(2, 'little'))
    f.write((sr).to_bytes(4, 'little'))
    f.write((sr * 2).to_bytes(4, 'little'))
    f.write((2).to_bytes(2, 'little'))
    f.write((16).to_bytes(2, 'little'))
    f.write(b'data')
    f.write((len(mixed) * 2).to_bytes(4, 'little'))
    f.write(wav_data.tobytes())

print(f"Wrote resonance-standing.wav ({duration}s, {sr}Hz)")

# Encode to MP3
import subprocess
result = subprocess.run([
    "ffmpeg", "-y", "-i", "assets/resonance-standing.wav",
    "-vn", "-b:a", "128k", "assets/resonance-standing.mp3"
], capture_output=True, text=True)
if result.returncode == 0:
    print("Encoded resonance-standing.mp3")
else:
    print(f"MP3 encode failed: {result.stderr}")
