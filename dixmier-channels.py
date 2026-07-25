import numpy as np
import wave

# Three names for the same refusal
# clutching = building outward (winding)
# resolvent = approaching continuously (divergent)
# residue = surviving dissolution (slow remnant)

sr = 44100
duration = 18  # seconds
t = np.linspace(0, duration, int(sr * duration))

# Common parameters
f0 = 37.0  # the unresolvable prime

# Channel 1: Clutching — winding, building outward
# Integer winding as phase accumulation
winds = [1, 2, 3, 5, 7]  # prime windings, accelerating
phase1 = np.zeros_like(t)
for i, w in enumerate(winds):
    start = i * 3.0
    end = min(start + 2.5, duration)
    mask = (t >= start) & (t < end)
    phase1[mask] += w * 2 * np.pi * f0 * t[mask] * np.exp(-(t[mask] - start) / 1.5)

# Staggered phase jumps (winding numbers)
for i, w in enumerate(winds):
    jump_time = i * 3.0 + 1.2
    shape = np.exp(-((t - jump_time) ** 2) / (2 * 0.06 ** 2))
    phase1 += w * 2 * np.pi * shape

signal1 = np.tanh(0.4 * np.sin(phase1))

# Channel 2: Resolvent — divergent approach
# ||R(λ)|| = 1/dist(λ, σ) — diverges near spectrum
# But log ||R(λ)|| diverges SLOWER — that difference is the clutch
spectrum = np.array([1.0, 1.5, 2.0, 3.0, 4.0, 6.0]) * f0
signal2 = np.zeros_like(t)
for s in spectrum:
    # Slow approach to spectral point, never reaching
    dist = 0.01 + 2.0 * (1 - np.cos(2 * np.pi * s * t))
    log_div = np.log(dist + 1e-8)
    signal2 += (1.0 / dist) * np.exp(-t / 8.0)  # fast divergence, decaying
    signal2 += log_div * 0.1 * np.exp(-(t - 10) / 3.0)  # slow divergence survives

signal2 = np.tanh(signal2 * 0.5)

# Channel 3: Residue — what survives dissolution
# Slow remnant after the fast processes die away
signal3 = np.zeros_like(t)
for freq_ratio in [1.0, 3.0/2.0, 4.0/3.0]:
    freq = f0 * freq_ratio
    # Ring slowly, each one fades as dissolution proceeds
    envelope = np.exp(-t / (12.0 + freq_ratio * 2))
    signal3 += 0.3 * envelope * np.sin(2 * np.pi * freq * t)
    signal3 += 0.15 * envelope * np.sin(2 * np.pi * freq * 2.7 * t)  # non-harmonic overtone

# Mix: three channels, stereo separation
# Left: clutching + residue
# Right: resolvent + residue (different phase)
left = signal1 * 0.6 + signal3 * 0.5
right = signal2 * 0.6 + signal3 * 0.5 * np.cos(0.3 * t)

# The gap: continuous tension between channels
gap = np.abs(left - right) * 0.15
left += gap * np.sin(0.7 * t)
right += gap * np.cos(0.7 * t)

# Master: tanh soft clip
mix = np.tanh(np.stack([left, right], axis=-1) * 0.7)

# Write WAV
with wave.open('./assets/dixmier-channels.wav', 'w') as wav:
    wav.setnchannels(2)
    wav.setsampwidth(2)
    wav.setframerate(sr)
    wav.writeframes((mix * 32767).astype(np.int16).tobytes())

# Also write compressed MP3
import os
os.system('ffmpeg -y -i ./assets/dixmier-channels.wav -b:a 192k ./assets/dixmier-channels.mp3 2>/dev/null')

print("Written dixmier-channels.wav and dixmier-channels.mp3")
print(f"Duration: {duration}s, SR: {sr}")

# Show channel statistics
for name, sig in [('left', left), ('right', right), ('gap', gap)]:
    print(f"{name}: rms={np.sqrt(np.mean(sig**2)):.4f}, peak={np.max(np.abs(sig)):.4f}")
