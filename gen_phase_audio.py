"""
Threshold vs Fold — audio as physics.

Two tracks, each 30 seconds, 44100 Hz, 24-bit WAV.

Track 1: THRESHOLD — Two oscillators, detuned at first, then the coupling
strength increases until they phase-lock. The lock is a resolved crossing:
once locked, they stay locked. You can hear the transition. It's irreversible.

Track 2: FOLD — A single oscillator whose frequency is driven through a
fold catastrophe potential. As the drive parameter sweeps, the response
bifurcates. The system reaches a point where continuous variation ends —
the fold. The tone approaches a frequency that continuous variation cannot
provide. Structural impossibility.

Both are 30 seconds at nominal speed.
"""

import numpy as np
import json
import os

SAMPLE_RATE = 44100
DURATION = 30
FREQ = 440.0  # base frequency
f0 = FREQ

t = np.linspace(0, DURATION, int(SAMPLE_RATE * DURATION), endpoint=False)

def make_threshold():
    """Phase-locking as resolved crossing.

    Two oscillators start at slightly different frequencies (f0 and f0+df).
    Coupling increases over time until they lock. The lock point is visible
    in the waveform: the two voices merge into one.

    After lock, they stay locked. The crossing is irreversible.
    """
    f0 = FREQ
    df_start = 12.0  # initial detuning — clearly two voices
    df_end = 0.0     # fully locked

    # Coupling increases as a sigmoid
    coupling = 1.0 / (1.0 + np.exp(-0.3 * (t - 10.0)))

    # Effective detuning decreases as coupling increases
    df = df_start * (1.0 - coupling)

    # Phase difference evolves according to Kuramoto-like coupling
    # d(Δφ)/dt = Δω - K sin(Δφ)
    # When K > |Δω|, phase locking occurs
    delta_omega = df * 2 * np.pi

    # Simulate phase difference
    phase_diff = np.zeros_like(t)
    K = np.zeros_like(t)
    K[0] = 0.0
    for i in range(1, len(t)):
        dt = t[1] - t[0] if i > 0 else 1/SAMPLE_RATE
        # coupling K grows with time
        K[i] = 40.0 * (1.0 / (1.0 + np.exp(-0.3 * (t[i] - 10.0))))
        # Kuramoto update
        sin_dp = np.sin(phase_diff[i-1])
        dphi = (delta_omega[i] - K[i] * sin_dp) * dt
        phase_diff[i] = phase_diff[i-1] + dphi
        # Wrap to [-π, π]
        phase_diff[i] = np.arctan2(np.sin(phase_diff[i]), np.cos(phase_diff[i]))

    # Two oscillator signals
    phase1 = 2 * np.pi * f0 * t
    phase2 = 2 * np.pi * f0 * t + phase_diff
    volume = np.ones_like(t)

    # Fade in/out
    fade_in = np.minimum(t / 0.5, 1.0)
    fade_out = np.minimum((DURATION - t) / 0.5, 1.0)
    volume *= fade_in * fade_out

    # Add slight vibrato for organic quality
    vibrato = 0.5 * np.sin(2 * np.pi * 5.5 * t)

    sig1 = np.sin(phase1 + vibrato) * 0.35
    sig2 = np.sin(phase2 + vibrato) * 0.35

    # The sum should not clip
    combined = (sig1 + sig2) * 0.7

    return combined, "resolved crossing: two voices, one trajectory. once they lock, they don't un-lock."

def make_fold():
    """Fold as structural impossibility.

    A single oscillator driven through a fold catastrophe. The driving
    frequency sweeps, and the response exhibits hysteresis — approaching
    from different directions gives different results. The fold is the
    boundary where continuous paths break.

    The tone approaches a resolution that can't be reached by continuous
    variation alone.
    """
    # Drive parameter sweeps linearly, then reflects
    # The response is nonlinear — a folded map
    drive = np.linspace(-2.5, 2.5, len(t)) * 1.5

    # Folded response: cubic potential x³ - ax gives three branches
    # The system follows one branch, jumps at the fold
    response = np.zeros_like(t)

    # Use a sinusoidal drive with frequency modulation that creates the fold
    # The instantaneous frequency traces a fold structure
    base_phase = 2 * np.pi * f0 * t

    # FM: instantaneous frequency = f0 + drive(t) * modulation_depth
    # At the fold, d(instantaneous freq)/d(drive) = 0
    # This happens when the FM index creates a turning point

    # Create the fold: use a cubic mapping of the drive to frequency offset
    # f_inst = f0 + α·drive + β·drive³
    # d(f_inst)/d(drive) = α + 3β·drive² = 0 at the fold points
    alpha = 8.0
    beta = -1.2
    freq_offset = alpha * drive + beta * drive**3

    # Instantaneous phase: integrate the frequency
    inst_freq = f0 + freq_offset
    # Ensure no negative frequencies
    inst_freq = np.maximum(inst_freq, 50.0)
    inst_phase = 2 * np.pi * np.cumsum(inst_freq) / SAMPLE_RATE

    # Add amplitude modulation for articulation
    amp = 0.7 * np.ones_like(t)

    # Fade in/out
    fade_in = np.minimum(t / 0.5, 1.0)
    fade_out = np.minimum((DURATION - t) / 0.5, 1.0)
    amp *= fade_in * fade_out

    # Subtle harmonic overtone
    harmonic = np.sin(2 * inst_phase) * 0.15 * amp

    sig = np.sin(inst_phase) * 0.6 * amp + harmonic

    return sig, "approach with no path: the fold holds the gap open. continuous variation ends here."

def save_wav(data, path, description):
    """Save as 24-bit WAV."""
    data_int24 = np.clip(data, -1, 1) * (2**23 - 1)
    data_bytes = data_int24.astype(np.int32).tobytes()

    # Minimal WAV header for 24-bit PCM
    num_samples = len(data_int24)
    num_channels = 1
    bits_per_sample = 24
    byte_rate = SAMPLE_RATE * num_channels * bits_per_sample // 8
    block_align = num_channels * bits_per_sample // 8
    chunk_size = num_samples * block_align
    data_chunk_size = chunk_size

    header = b'RIFF'
    header += (36 + data_chunk_size).to_bytes(4, 'little')
    header += b'WAVE'
    header += b'fmt '
    header += (16).to_bytes(4, 'little')
    header += (1).to_bytes(2, 'little')  # PCM
    header += (num_channels).to_bytes(2, 'little')
    header += (SAMPLE_RATE).to_bytes(4, 'little')
    header += (byte_rate).to_bytes(4, 'little')
    header += (block_align).to_bytes(2, 'little')
    header += (bits_per_sample).to_bytes(2, 'little')
    header += b'data'
    header += (data_chunk_size).to_bytes(4, 'little')

    with open(path, 'wb') as f:
        f.write(header)
        f.write(data_bytes)

    # Also save metadata
    meta = {
        "path": path,
        "description": description,
        "sample_rate": SAMPLE_RATE,
        "duration": DURATION,
        "format": "24-bit PCM WAV"
    }
    meta_path = path.replace('.wav', '.json')
    with open(meta_path, 'w') as f:
        json.dump(meta, f, indent=2)

if __name__ == '__main__':
    threshold_sig, threshold_desc = make_threshold()
    fold_sig, fold_desc = make_fold()

    save_wav(threshold_sig, 'assets/threshold-resolved.wav', threshold_desc)
    save_wav(fold_sig, 'assets/fold-structural.wav', fold_desc)

    print("Generated:")
    print(f"  assets/threshold-resolved.wav  — {threshold_desc}")
    print(f"  assets/fold-structural.wav     — {fold_desc}")
