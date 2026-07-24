#!/usr/bin/env python3
"""Coboundary layers audio — each δ^n is a register of its own.
Order 0: fundamental. Order 1: first boundary. Order 2: second boundary.
Order 3: partial harmonics with a dark core (silence at 3 harmonics)."""

import numpy as np
import struct
import wave

def soft_tanh(x, k=5.0):
    """Soft clipping to avoid hard DC offset."""
    return np.tanh(k * x)

def tone(fs, t, freq, amp, duration, start_offset):
    """Generate a tone that rings for `duration` seconds starting at start_offset."""
    envelope = np.zeros_like(t)
    mask = (t >= start_offset) & (t < start_offset + duration)
    t_local = t[mask] - start_offset

    # Attack: 0.1s, decay: 0.3s, sustain: remainder, release: 0.3s
    attack = min(0.1, duration * 0.05)
    release = min(0.3, duration * 0.15)
    sustain_time = duration - attack - release

    env = np.zeros_like(t_local)
    if duration <= attack:
        env = np.linspace(0, 1, duration * fs)
    else:
        n_attack = int(attack * fs)
        n_sustain = int(sustain_time * fs)
        n_release = int(release * fs)
        n_total = len(env)

        env[:n_attack] = np.linspace(0, 1, n_attack)
        if n_sustain > 0:
            env[n_attack:n_attack + n_sustain] = 0.7
        if n_release > 0:
            env[-n_release:] = np.linspace(0.7, 0, n_release)

    envelope[mask] = env
    signal = amp * envelope * np.sin(2 * np.pi * freq * t)
    return signal

def build_coboundary_audio():
    fs = 44100
    duration = 20.0  # 20 seconds
    t = np.linspace(0, duration, int(fs * duration), endpoint=False)

    signal = np.zeros_like(t)

    # Order 0: fundamental drone (the cochain)
    # Simple, pure — the starting point
    signal += tone(fs, t, 55, 0.3, duration, 0)        # A1 fundamental
    signal += tone(fs, t, 110, 0.15, duration, 0)      # first partial (octave)
    signal += tone(fs, t, 165, 0.08, duration, 0)      # fifth above

    # Order 1: first coboundary (the boundary)
    # Enters at t=2s, richer harmonics
    signal += tone(fs, t, 82.5, 0.2, duration - 2, 2)  # E3
    signal += tone(fs, t, 123.75, 0.12, duration - 2, 2)
    signal += tone(fs, t, 165, 0.06, duration - 2, 2)

    # Order 2: coboundary of coboundary (the division)
    # Enters at t=5s, more layers, slight dissonance
    signal += tone(fs, t, 130.8, 0.18, duration - 5, 5)  # C3
    signal += tone(fs, t, 174.6, 0.10, duration - 5, 5)
    signal += tone(fs, t, 220, 0.07, duration - 5, 5)    # A3

    # Order 3: partial harmonics (the register's boundary)
    # Enters at t=8s — BUT with a "blind spot"
    # Three frequencies that DON'T ring: these are the silence at the core
    # Order 3 has 9 partials, but 3 are deliberately absent

    order3_freqs = [
        (261.6, 0.15),   # C4
        (329.6, 0.09),   # E4
        # 392.0 — SILENT (blind spot #1: the perfect fifth, the most consonant)
        (440, 0.12),     # A4
        (523.2, 0.07),   # C5
        # 659.3 — SILENT (blind spot #2: the octave of the first blind)
        (783.9, 0.05),   # G5
        (880, 0.08),     # A5
        (1046, 0.04),    # C6
        # 1318.5 — SILENT (blind spot #3: the octave of the second)
    ]
    for freq, amp in order3_freqs:
        signal += tone(fs, t, freq, amp, duration - 8, 8)

    # Soft clipping
    signal = soft_tanh(signal)

    # RMS normalize
    rms = np.sqrt(np.mean(signal**2))
    if rms > 0:
        target_rms = 0.15
        signal = signal * (target_rms / rms)

    # Write as WAV
    with wave.open('coboundary-audio.wav', 'w') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(fs)
        samples = np.int16(signal * 32767)
        wf.writeframes(samples.tobytes())

    # Also render MP3 via ffmpeg
    import subprocess
    subprocess.run([
        'ffmpeg', '-y', '-i', 'coboundary-audio.wav',
        '-codec:a', 'libmp3lame', '-b:a', '192k',
        'coboundary-audio.mp3'
    ], check=True, capture_output=True)

    # Create a simple cover image
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(1, 1, figsize=(3, 3), facecolor='#0a0a12')
    ax.set_facecolor('#0a0a12')
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    # Draw 4 dots representing orders, each with a "blind spot"
    positions = [(50, 75), (50, 55), (50, 35), (50, 18)]
    colors = ['#6ec6ff', '#5cc86a', '#ff9e5c', '#ff5c8e']
    sizes = [40, 60, 80, 100]
    for i, ((x, y), c, s) in enumerate(zip(positions, colors, sizes)):
        ax.add_patch(plt.Circle((x, y), s/100*20, color=c, alpha=0.4,
                                edgecolor=c, linewidth=1.5))
        if i == 3:
            # Order 3 has visible blind spots
            for bx, by in [(50, 18), (40, 12), (60, 12)]:
                ax.add_patch(plt.Circle((bx, by), 2, color='#0a0a12',
                                        edgecolor=c, linewidth=0.5, alpha=0.3))

    plt.tight_layout()
    plt.savefig('coboundary-cover.png', dpi=150, facecolor='#0a0a12',
                bbox_inches='tight', pad_inches=0.1)
    plt.close()

    print("Done: coboundary-audio.wav, coboundary-audio.mp3, coboundary-cover.png")

if __name__ == '__main__':
    build_coboundary_audio()
