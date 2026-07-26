#!/usr/bin/env python3
"""
Persistence → audio bridge.

Each birth/death bar in a persistence barcode = a frequency band with
envelope: enters at birth freq, sustains proportional to persistence (death-birth),
decays at death.

The clutching→filtration bridge: persistence = clutching at coarse resolution.
The ε-plate boundary = birth threshold. Where the resolvent norm exceeds 1/ε,
a feature is born. Where it drops back, the feature dies.

Winding number per eigenvalue cluster → frequency multiplier.
The clutching number IS the harmonic series.
"""
import numpy as np
import struct

sr = 44100
duration = 18.0
t = np.linspace(0, duration, int(sr * duration), endpoint=False)

# --- Mathematical structure ---

# Three eigenvalue clusters with different winding numbers
clusters = [
    # (center, winding_number, size_spread, birth_scale, death_scale)
    (55, 1, 0.3, 2.0, 8.0),     # Bass: winding=1 → fundamental
    (165, 2, 0.5, 5.0, 14.0),   # Fifth: winding=2 → 2×harmonic
    (330, 3, 0.7, 8.0, 18.0),   # Ninth: winding=3 → 3×harmonic
]

# Pseudospectral epsilon controls the birth threshold
# Small ε → features born late (only near eigenvalues)
# Large ε → features born early (noise floor reaches threshold)
epsilons = [0.01, 0.05, 0.1, 0.2, 0.5, 1.0, 2.0]

# For each cluster, compute "persistence" at each epsilon
# (distance from eigenvalue where resolvent norm = 1/ε)
# Simplified model: birth = epsilons where feature "appears"
# death = where it "disappears" (noise overwhelms signal)

# --- Audio synthesis ---

output = np.zeros_like(t)
noise_floor = np.zeros_like(t)

for center, winding, spread, birth_t, death_t in clusters:
    # Duration of this bar
    persistence = (death_t - birth_t) / duration  # as fraction of total time

    # Start and end samples
    start_s = int(birth_t / duration * len(t))
    end_s = int(death_t / duration * len(t))

    # Carrier frequency: base × winding (harmonic series from clutching)
    freq = center * winding

    # Local time for this band
    local_t = np.linspace(0, 1, end_s - start_s)

    # Onset envelope: sharp attack (0.01s)
    attack_samples = min(int(0.01 * sr), len(local_t))
    attack_env = np.linspace(0, 1, attack_samples)

    # Decay envelope: proportional to persistence
    decay_rate = 1.0 / max(persistence, 0.01)
    decay_env = np.exp(-decay_rate * np.maximum(0, local_t - 0.02))

    # Combined envelope
    env = np.ones(len(local_t))
    env[:attack_samples] = attack_env
    env *= decay_env

    # Harmonic series within the band (clutching number as multiplier)
    carrier = np.sin(2 * np.pi * freq * t[start_s:end_s])
    # Add sub-harmonics for richness
    carrier += 0.3 * np.sin(2 * np.pi * freq * 0.5 * t[start_s:end_s])
    carrier += 0.15 * np.sin(2 * np.pi * freq * 1.5 * t[start_s:end_s])

    # Phase jump at birth (transition function)
    phase_jump = np.pi / winding  # winding-dependent phase
    birth_phase = np.ones(len(local_t)) * phase_jump
    birth_phase[:50] = np.linspace(0, phase_jump, min(50, len(local_t)))

    carrier *= np.cos(birth_phase)
    carrier += np.sin(2 * np.pi * freq * t[start_s:end_s] + birth_phase) * np.sin(birth_phase)

    output[start_s:end_s] += carrier * env

    # Pseudospectral noise floor: thickens near birth/death transitions
    for eps_idx, eps in enumerate(epsilons):
        threshold = 1.0 / eps
        # Noise is louder where resolvent norm > 1/eps
        eps_region = np.exp(-((local_t * duration * len(t) / (death_t - birth_t)
                                + birth_t * len(t) / duration
                                - (birth_t + death_t) * len(t) / (2 * duration))
                               / (spread * len(t) / duration))**2)
        noise_floor[start_s:end_s] += eps_region * 0.002 / (eps_idx + 1)

# --- Structure: bars that never close for winding=1 ---
# Bass (winding=1) has death at end → never decays
# This IS the clutching number as bass that never stops

# Add steady bass drone for first cluster
bass_center, bass_wind, _, bass_birth, _ = clusters[0]
bass_freq = bass_center * bass_wind  # 55 Hz
bass_sustain = np.ones_like(t)
# Slow breath modulation
bass_sustain *= 0.5 + 0.5 * np.sin(2 * np.pi * 0.3 * t)
bass_drone = np.sin(2 * np.pi * bass_freq * t) * bass_sustain * 0.3
output += bass_drone

# Pseudospectral smear on noise floor
smear = np.random.normal(0, 1, len(t)) * 0.003
# Modulate smear by resolution (higher ε = thicker smear)
smear_env = 0.5 + 0.5 * np.sin(2 * np.pi * 0.1 * t)
smear *= smear_env
output += noise_floor + smear

# Mix and clip
output = np.tanh(output * 0.8)

# --- Save as WAV ---
samples = np.int16(np.clip(output, -1, 1) * 32767)
data = struct.pack('<{}h'.format(len(samples)), *samples)
riff_size = 36 + len(data)

with open('./assets/persistence-sound.wav', 'wb') as f:
    f.write(struct.pack('<4sI4s', b'RIFF', riff_size, b'WAVE'))
    f.write(struct.pack('<4sI', b'fmt ', 16))
    f.write(struct.pack('<HHIIHH', 1, 1, sr, sr*4, 4, 16))
    f.write(struct.pack('<4sI', b'data', len(data)))
    f.write(data)

print(f"Saved: persistence-sound.wav ({duration}s, {sr}Hz)")
print(f"Structure: {len(clusters)} eigenvalue clusters → frequency bands")
for i, (center, wind, spread, bt, dt) in enumerate(clusters):
    print(f"  Band {i+1}: freq={center*wind}Hz, winding={wind}, "
          f"birth={bt:.1f}s, death={dt:.1f}s, persistence={dt-bt:.1f}s")
print(f"Bass (winding=1): steady drone at {55}Hz, never decays")
print(f"Pseudospectral smear: noise floor modulated by epsilon resolution")

# Also save a visualization: barcode-style plot
matplotlib_ok = False
try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    matplotlib_ok = True
except:
    pass

if matplotlib_ok:
    fig, ax = plt.subplots(1, 1, figsize=(10, 6))
    ax.set_facecolor('black')
    fig.patch.set_facecolor('black')

    # Draw persistence barcode
    for i, (center, wind, spread, bt, dt) in enumerate(clusters):
        freq = center * wind
        # Bar width proportional to persistence
        bar_height = 0.7 + i * 0.2
        colors = ['#ff6b35', '#f7c948', '#48b8f7']

        ax.plot([bt, dt], [bar_height, bar_height],
               color=colors[i], linewidth=8, solid_capstyle='butt',
               label=f'winding={wind}: {freq}Hz, persistence={dt-bt:.1f}s')

        # Birth marker
        ax.plot(bt, bar_height, 'o', color=colors[i], markersize=12)
        # Death marker
        ax.plot(dt, bar_height, 'X', color=colors[i], markersize=10, markeredgewidth=2)

    # Draw pseudospectral epsilon boundaries
    for eps in [0.05, 0.1, 0.5, 2.0]:
        threshold = 1.0 / eps
        x = np.clip(threshold, 0, 20)
        ax.axvline(x, color='white', linestyle='--', alpha=0.3, linewidth=0.8,
                   label=f'ε={eps} (birth threshold={threshold:.1f})')

    ax.set_xlabel('Scale / Resolution', color='white', fontsize=12)
    ax.set_ylabel('Frequency Band', color='white', fontsize=12)
    ax.set_title('Persistence Barcode → Harmonic Series', color='white', fontsize=14)
    ax.set_xlim(0, 22)
    ax.set_ylim(0, 1.5)
    ax.tick_params(colors='white')
    ax.spines['bottom'].set_color('white')
    ax.spines['left'].set_color('white')
    ax.spines['top'].set_color('white')
    ax.spines['right'].set_color('white')

    ax.legend(loc='upper right', facecolor='black', edgecolor='white',
             labelcolor='white', fontsize=9)

    plt.tight_layout()
    plt.savefig('./assets/persistence-barcode.png', dpi=150,
               facecolor='black', edgecolor='none')
    print("Saved: persistence-barcode.png")
