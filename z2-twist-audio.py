#!/usr/bin/env python3
"""Z₂ twist audio: harmonics that read forward and backward simultaneously.

The clutching is the same loop with opposite orientation.
Forward = g, backward = g⁻¹. Same frequency content, reversed phase.
Bass at 55Hz = the clutching constant.
Each bar is a harmonic that enters at a specific birth time,
flips phase by π (sign reversal = topological, not arithmetic),
and rings for its persistence duration.
"""

import numpy as np
import wave
import struct
import sys

# Parameters
SR = 44100
DURATION = 20  # seconds
BASS_FREQ = 55.0  # clutching constant
BASE_AMPLITUDE = 0.15

# Z₂ twist: each harmonic has a direction (forward or backward)
# Forward: standard phase accumulation
# Backward: phase reversed by π (equivalent to negation for real signals)
# This is reversal, not sign — the same harmonic reading against the grain

def z2_harmonic(t, freq, direction, birth, death, amp):
    """Harmonic with Z₂ twist: direction flips phase by π."""
    envelope = np.where(t < birth, 0,
               np.where(t > death, 0,
               np.minimum(1.0, (t - birth) / 0.3) *
               np.minimum(1.0, (death - t) / 0.3)))

    # Phase accumulation — reversed by π for backward direction
    phase = 2 * np.pi * freq * t
    if direction == -1:
        phase += np.pi  # Z₂ twist: π-flip = reversal, not sign change

    return amp * envelope * np.sin(phase)

def make_wave():
    t = np.linspace(0, DURATION, int(SR * DURATION), endpoint=False)

    # Birth times and persistence from a Z₂-symmetric pattern
    # Pairs of harmonics: forward + backward reading of same invariant
    # Each pair has same frequency but opposite direction
    pairs = [
        (0.0,  8.0,  82.0,  1.0),   # E4
        (0.0,  8.0,  82.0, -1.0),   # same, reversed
        (1.0, 10.0, 123.0,  1.0),   # ~B4 (golden ratio spacing)
        (1.0, 10.0, 123.0, -1.0),
        (2.5, 12.0, 147.0,  1.0),   # ~D5
        (2.5, 12.0, 147.0, -1.0),
        (4.0, 11.0, 165.0,  1.0),   # E5
        (4.0, 11.0, 165.0, -1.0),
        (6.0,  9.0, 220.0,  1.0),   # A5
        (6.0,  9.0, 220.0, -1.0),
        (8.0,  7.0, 294.0,  1.0),   # D6
        (8.0,  7.0, 294.0, -1.0),
        (10.0, 6.0, 330.0,  1.0),   # E6
        (10.0, 6.0, 330.0, -1.0),
        (12.0, 5.0, 440.0,  1.0),   # A6
        (12.0, 5.0, 440.0, -1.0),
    ]

    signal = np.zeros_like(t)

    # Bass: steady clutching constant, always forward
    bass_amp = 0.08
    signal += bass_amp * np.sin(2 * np.pi * BASS_FREQ * t)

    # Harmonics
    for birth, death, freq, direction in pairs:
        amp = BASE_AMPLITUDE / (death - birth) * 2  # longer = softer
        signal += z2_harmonic(t, freq, direction, birth, death, amp)

    # Soft clip
    signal = np.tanh(signal * 1.5) / 1.5

    # Convert to 16-bit PCM
    samples = np.int16(signal * 32767)

    # Write WAV
    fname = './assets/z2-twist.wav'
    wf = wave.open(fname, 'wb')
    wf.setnchannels(2)
    wf.setsampwidth(2)
    wf.setframerate(SR)

    # Stereo: forward harmonics left, backward right, bass center
    left = np.zeros_like(t)
    right = np.zeros_like(t)

    left += bass_amp * np.sin(2 * np.pi * BASS_FREQ * t)
    right += bass_amp * np.sin(2 * np.pi * BASS_FREQ * t)

    for birth, death, freq, direction in pairs:
        amp = BASE_AMPLITUDE / (death - birth) * 2
        if direction == 1:
            left += z2_harmonic(t, freq, direction, birth, death, amp)
        else:
            right += z2_harmonic(t, freq, direction, birth, death, amp)

    left = np.tanh(left * 1.5) / 1.5
    right = np.tanh(right * 1.5) / 1.5

    for i in range(len(samples)):
        l = np.int16(left[i] * 32767)
        r = np.int16(right[i] * 32767)
        wf.writeframes(struct.pack('<hh', l, r))

    wf.close()
    print(f"Wrote {fname}")

if __name__ == '__main__':
    make_wave()
