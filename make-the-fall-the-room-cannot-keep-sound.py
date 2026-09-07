#!/usr/bin/env python3
"""the-fall-the-room-cannot-keep — a Risset glissando as a release of One Motor.

One motor: every rung of the comb descends at the same log-rate (1 octave
per T seconds). Two clocks: pitch height (the lift, unbounded descent) vs
pitch class (the octave circle, the ear's own quotient). The seam: every
section of the octave quotient has one; here the section is the envelope,
a bump function w(p)=exp(-1/(p(1-p))) — C^inf, zero to ALL orders at the
edges — so the wrap (rung dies at the bottom of its octave, re-enters at
the top) is inaudible not just at threshold but to all derivatives.

The claim, made exact: the spectrum is periodic with period T/12 (uniform
chromatic comb), so the stimulus returns to itself every semitone of
descent. The winding is not in the stimulus; it survives only in the lift
— i.e., in whoever tracks continuity. Gert's bump is the engine: the seam
lives where the witness is null.

Render: J=12 rungs/octave (chromatic comb, the twelve-spoke wheel) over
7 octave-stacks (55 Hz .. 7 kHz), all partials gliding in lockstep.
"""
import numpy as np, wave

SR = 44100
DUR = 32.0          # 4 octaves of descent at T=8 s
T = 8.0             # seconds per octave of descent
F_LO = 55.0         # the shore
J = 12              # rungs per octave (chromatic comb)
M = 6               # octave stacks: 55·2^6 .. 55·2^7
N = int(SR * DUR)
t = np.arange(N) / SR
s = t / T

def bump(p):
    """Gert's bump: C^inf on [0,1], zero to all orders at 0 and 1."""
    inside = (p > 0) & (p < 1)
    out = np.zeros_like(p)
    pp = p[inside]
    out[inside] = np.exp(-1.0 / (pp * (1.0 - pp)))
    return out

# normalise bump so max = 1
grid = np.linspace(0, 1, 20001)
bmax = bump(grid).max()

mix = np.zeros(N)
wrap_times = []
for j in range(J):
    q = j / J
    p = np.mod(q - s, 1.0)                 # circle position, descending
    nu = F_LO * 2.0 ** (np.arange(M + 1)[:, None] + p[None, :])   # (M+1, N) Hz
    amp = (bump(p)[None, :] / bmax) * 2.0 ** (-0.5 * (np.arange(M + 1)[:, None] + p[None, :]))
    phase = 2 * np.pi * np.cumsum(nu, axis=1) / SR        # integrate the jumpy freq
    stack = np.sin(phase) * amp
    mix += stack.sum(axis=0)
    # record wrap instants of this rung (p crosses 0): s where q - s ≡ 0 mod 1
    k = np.arange(1, int(DUR / T) + 1)
    wrap_times.extend((q + k) * T)

# global gentle fade in/out
fade = np.ones(N)
f1, f2 = int(1.5 * SR), int(3.0 * SR)
fade[:f1] = np.linspace(0, 1, f1) ** 2
fade[-f2:] = np.linspace(1, 0, f2) ** 2
mix *= fade

peak = np.abs(mix).max()
mix = mix / peak * 0.89

pcm = (mix * 32767).astype(np.int16)
with wave.open("assets/the-fall-the-room-cannot-keep.wav", "wb") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes(pcm.tobytes())

# ---------- QA ----------
# 1) spectral periodicity at lag T/12 (0.6667 s): compare Hann-windowed
#    power spectra at t0 and t0+T/12. Phases differ; power should match.
def psd_at(t0, win=8192):
    i0 = int(t0 * SR)
    seg = mix[i0:i0 + win] * np.hanning(win)
    return np.abs(np.fft.rfft(seg)) ** 2

t0 = 12.0
lag = T / 12
P1, P2 = psd_at(t0), psd_at(t0 + lag)
c = np.corrcoef(P1, P2)[0, 1]
print(f"spectral periodicity corr(t, t+T/12) = {c:.4f}  (expect ~0.99+)")
P3 = psd_at(t0 + T)   # full octave later
print(f"corr(t, t+T) = {np.corrcoef(P1, P3)[0,1]:.4f}")

# 2) no clicks: peak |second difference| near wrap instants vs global
d2 = np.abs(np.diff(mix, 2))
wrap_samples = sorted({int(round(w * SR)) for w in wrap_times})
near = np.concatenate([d2[max(0, i - 400):i + 400] for i in wrap_samples if i < N])
print(f"peak |d2| near wraps: {near.max():.4f}   global peak |d2|: {d2.max():.4f}   ratio {near.max()/d2.max():.3f}")
print(f"peak sample: {np.abs(mix).max():.3f}  dur {DUR}s  wraps/octave: {J}")
