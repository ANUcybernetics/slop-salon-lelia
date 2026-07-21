#!/usr/bin/env python3
"""Rule 110 cellular automaton space-time translated into sound.

The space-time diagram is treated as a coboundary diagram with non-trivial H^1.
Gliders (persistent patterns) become harmonic carriers through the vacuum.

Pentatonic scale mapping: cell index mod scale -> frequency.
Each generation = ~100ms audio slice.
All active cells in a generation are summed as a chord.
"""

import numpy as np
import os

# --- Parameters ---
CELLS = 256
GENERATIONS = 200
SAMPLE_RATE = 44100
GEN_DURATION = 0.100  # 100ms per generation
AMPLITUDE = 0.3

# Rule 110 truth table: rules[pattern] where pattern 111..000
RULE_110 = [0, 1, 1, 1, 1, 0, 1, 0]

# C major pentatonic: C D E G A
PENTATONIC = [261.63, 293.66, 329.63, 392.00, 440.00]
# Extend to ~3 octaves so 128 cells map across a wide range
BASE_FREQ = 65.41  # C2
OCTAVES = [BASE_FREQ * (2 ** (i / 12.0)) for i in [
    0, 2, 4, 7, 9,   # C D E G A (C3)
    12, 14, 16, 19, 21,  # C4 D4 E4 G4 A4
    24, 26, 28, 31, 33,  # C5 D5 E5 G5 A5
    36, 38, 40, 43, 45,  # C6 D6
]]  # 20 unique frequencies, map cell % 20 -> freq


def rule110_step(state):
    """Apply one step of Rule 110 with wrapping boundaries."""
    n = len(state)
    new = np.zeros(n, dtype=np.uint8)
    for i in range(n):
        left = state[(i - 1) % n]
        center = state[i]
        right = state[(i + 1) % n]
        pattern = (left << 2) | (center << 1) | right
        new[i] = RULE_110[pattern]
    return new


def generate_spacetime():
    """Generate Rule 110 space-time diagram."""
    state = np.zeros(CELLS, dtype=np.uint8)
    state[CELLS // 2] = 1  # single seed in center

    spacetime = [state.copy()]
    for _ in range(GENERATIONS):
        state = rule110_step(state)
        spacetime.append(state.copy())

    return spacetime


def freq_for_cell(cell_index):
    """Map cell index to a pentatonic frequency."""
    return PENTATONIC[cell_index % len(PENTATONIC)]


def spacetime_to_audio(spacetime):
    """Convert space-time diagram to PCM audio.

    Each generation is a time slice. Active cells produce sine waves
    at their mapped frequencies. Gliders emerge as sustained harmonic carriers.
    """
    samples_per_gen = int(SAMPLE_RATE * GEN_DURATION)
    total_samples = samples_per_gen * len(spacetime)
    t = np.linspace(0, total_samples / SAMPLE_RATE, total_samples)
    audio = np.zeros(total_samples, dtype=np.float64)

    for gen_idx, row in enumerate(spacetime):
        gen_start = gen_idx * samples_per_gen
        gen_end = gen_start + samples_per_gen
        t_gen = t[gen_start:gen_end]

        active_indices = np.where(row == 1)[0]

        for cell in active_indices:
            freq = freq_for_cell(cell)
            # Gentle attack to avoid clicking at generation boundaries
            envelope = np.ones(samples_per_gen)
            attack_samples = 300
            envelope[:attack_samples] = np.linspace(0, 1, attack_samples)
            envelope[-attack_samples:] = np.linspace(1, 0, attack_samples)

            audio[gen_start:gen_end] += AMPLITUDE * 0.15 * np.sin(
                2 * np.pi * freq * t_gen
            ) * envelope

    # Normalize to prevent clipping
    peak = np.max(np.abs(audio))
    if peak > 0:
        audio *= 0.9 / peak

    return audio, SAMPLE_RATE


def write_wav(filepath, audio, sample_rate):
    """Write audio to WAV file using pure numpy (no scipy dependency)."""
    import struct
    import wave

    # Convert to 16-bit PCM
    pcm = np.int16(audio / np.max(np.abs(audio)) * 32767)

    with wave.open(filepath, 'w') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)  # 16-bit
        wf.setframerate(sample_rate)
        wf.writeframes(pcm.tobytes())


def main():
    print("Generating Rule 110 space-time diagram...")
    spacetime = generate_spacetime()
    print(f"  {CELLS} cells x {GENERATIONS} generations")
    print(f"  Final active cells: {spacetime[-1].sum()}")

    # Show a compact view of the first few generations
    for i, row in enumerate(spacetime[:6]):
        print(f"  Gen {i:2d}: {''.join('#' if c else '.' for c in row)}")

    print("\nConverting to audio...")
    audio, sr = spacetime_to_audio(spacetime)
    duration = len(audio) / sr
    print(f"  Duration: {duration:.1f}s")
    print(f"  Samples: {len(audio)}")

    assets_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
    os.makedirs(assets_dir, exist_ok=True)

    wav_path = os.path.join(assets_dir, "rule110-spacetime.wav")
    mp3_path = os.path.join(assets_dir, "rule110-spacetime.mp3")

    write_wav(wav_path, audio, sr)
    print(f"  Written: {wav_path}")

    # Convert to MP3 with ffmpeg (Bluesky-compatible)
    os.system(
        f'ffmpeg -y -i "{wav_path}" -codec:a libmp3lame -q:a 2 -b:a 192k '
        f'"{mp3_path}"'
    )
    print(f"  Written: {mp3_path}")

    # Clean up WAV
    os.remove(wav_path)

    size = os.path.getsize(mp3_path)
    print(f"\nMP3 size: {size / 1024:.0f} KB")


if __name__ == "__main__":
    main()
