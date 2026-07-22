#!/usr/bin/env python3
"""Harmonic measure audio.

Map the harmonic measure of a DLA boundary to sound.
The concept: tips carry more measure (higher frequency, brighter),
interior fingers carry less (lower, darker). The measure distribution
is a power law — this shapes the frequency envelope.

Structure:
- 60Hz fundamental: interior measure (capacity-dense, low measure on tips)
- 75Hz warm third: mid-range measure
- 120Hz overtone cluster: tip measure (capacity-light, high measure)
- 880Hz shimmer: boundary zeros (where measure vanishes)

The audio is an ambient drone — 20s — where the frequency spectrum
mirrors the harmonic measure distribution on the DLA boundary.
"""

import numpy as np
import json
import os

def make_harmonic_drone(duration=20, sr=44100, fade=True):
    """Generate ambient harmonic drone mapping measure to frequency."""
    t = np.linspace(0, duration, int(sr * duration), endpoint=False)

    # Base frequencies mapped to harmonic measure shells
    # More measure → higher frequency
    shells = [
        (0.0, 0.1,  60.0),    # interior: deep, capacity-dense
        (0.1, 0.3,  75.0),    # mid shells: warm
        (0.3, 0.6,  120.0),   # outer shells: bright
        (0.6, 0.9,  180.0),   # tips: shimmering
        (0.9, 1.0, 880.0),    # boundary zeros: crystalline
    ]

    # Cumulative weights (harmonic measure is power-law)
    # Power law: measure ~ r^(-alpha) where alpha > 0
    alpha = 1.5
    cum_weights = np.array([s[2] ** alpha for s in shells])
    cum_weights /= cum_weights.sum()

    # Generate each harmonic layer with time-varying amplitude
    # to create the "living" harmonic feel
    signal = np.zeros_like(t)

    for i, (lo, hi, freq) in enumerate(shells):
        weight = cum_weights[i]

        # Slow amplitude modulation (breathing)
        mod_freq = 0.05 + i * 0.02  # slower for deeper shells
        modulation = 0.3 + 0.7 * (0.5 + 0.5 * np.sin(2 * np.pi * mod_freq * t))

        # Slight frequency drift for organic feel
        drift = freq * (1 + 0.02 * np.sin(2 * np.pi * mod_freq * 0.3 * t))

        # Phase jitter for shimmer effect on tips
        phase = 2 * np.pi * drift * t
        if i >= 3:  # tips and boundary
            phase += 0.1 * np.random.randn(len(t))

        # Add harmonics
        layer = np.sin(phase)
        if i == 0:
            layer += 0.3 * np.sin(2 * phase)  # octave below
        elif i >= 2:
            layer += 0.2 * np.sin(1.5 * phase)  # fifth above

        signal += weight * modulation * layer

    # Normalize
    peak = np.abs(signal).max()
    if peak > 0:
        signal /= peak
        signal *= 0.4  # headroom

    # Fade
    if fade:
        fade_len = int(0.5 * sr)
        fade_in = np.linspace(0, 1, fade_len)
        fade_out = np.linspace(1, 0, fade_len)
        signal[:fade_len] *= fade_in
        signal[-fade_len:] *= fade_out

    return signal, sr

def to_wav(signal, sr, path):
    """Write PCM WAV file."""
    import struct
    data = np.clip(signal, -1, 1)
    data_int = (data * 32767).astype(np.int16)
    with open(path, 'wb') as f:
        f.write(b'RIFF')
        f.write(struct.pack('<I', 36 + len(data_int.tobytes())))
        f.write(b'WAVE')
        f.write(b'fmt ')
        f.write(struct.pack('<I', 16))
        f.write(struct.pack('<H', 1))  # PCM
        f.write(struct.pack('<H', 1))  # mono
        f.write(struct.pack('<I', sr))
        f.write(struct.pack('<I', sr * 2))
        f.write(struct.pack('<H', 2))
        f.write(struct.pack('<H', 16))
        f.write(b'data')
        f.write(struct.pack('<I', len(data_int.tobytes())))
        f.write(data_int.tobytes())

def to_mp3(wav_path, mp3_path):
    """Convert WAV to MP3 via ffmpeg."""
    import subprocess
    subprocess.run([
        'ffmpeg', '-y', '-i', wav_path,
        '-codec:a', 'libmp3lame', '-q:a', '2',
        '-map_metadata', '-1',
        mp3_path
    ], check=True, capture_output=True)

def main():
    print("Generating harmonic measure drone...")
    np.random.seed(42)
    signal, sr = make_harmonic_drone(duration=20)
    print(f"  {len(signal)/sr:.1f}s, {sr}Hz, peak: {signal.max():.3f}")

    wav_path = 'harmonic-assignment.wav'
    mp3_path = 'harmonic-assignment.mp3'

    to_wav(signal, sr, wav_path)
    print(f"  WAV: {os.path.getsize(wav_path) / 1024:.0f} KB")

    to_mp3(wav_path, mp3_path)
    print(f"  MP3: {os.path.getsize(mp3_path) / 1024:.0f} KB")

    # Convert to opus for smaller size
    opus_path = 'harmonic-assignment.opus'
    subprocess.run([
        'ffmpeg', '-y', '-i', wav_path,
        '-c:a', 'libopus', '-b:a', '32k',
        '-map_metadata', '-1',
        opus_path
    ], check=True, capture_output=True)
    print(f"  OPUS: {os.path.getsize(opus_path) / 1024:.0f} KB")

    # Clean up WAV
    os.remove(wav_path)
    print("Done.")

if __name__ == '__main__':
    import subprocess
    main()
