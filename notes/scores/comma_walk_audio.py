#!/usr/bin/env python3
"""The Pythagorean comma, as a walk you can hear.

Twelve pure fifths (exact 3:2) walked from C. Each fifth is exact; the
twelfth landing misses home by 3^12/2^19 = 531441/524288 ~= 1.013643
(23.46 cents). The piece walks the circle, holds the last tone, re-enters
home under it, and lets the two beat at |f_B# - f_C| ~ 3.57 Hz.
"""
import numpy as np
import wave

SR = 48000
BASE = 440.0 * 2 ** (-9 / 12)          # C4, 261.6256 Hz
FIFTH_CENTS = 1200 * np.log2(3 / 2)    # 701.9550
COMMA_CENTS = 1200 * np.log2(3 ** 12 / 2 ** 19)  # 23.4601

def landing_cents(k):
    """Position (cents above home C, octave-reduced) after k pure fifths."""
    c = k * FIFTH_CENTS
    return c % 1200

def freq(k):
    return BASE * 2 ** (landing_cents(k) / 1200)

# --- audio ---
SR = 48000
step = 3.0        # s between tone starts
dur = 3.5         # s per walking tone
hold = 8.5        # s the last tone (B#) sustains
dur_c = 6.0       # s home C re-enters under the held B#
t_beat_start = 12 * step  # 36.0
c_enter = t_beat_start + 2.5  # 38.5
total = c_enter + dur_c     # 44.5
n = int(SR * total)
x = np.zeros(n)
t = np.arange(n) / SR

def tone(start, length, f, amp=0.22, fade=0.8):
    i0 = int(SR * start)
    i1 = min(int(SR * (start + length)), n)
    m = i1 - i0
    tt = np.arange(m) / SR
    env = np.ones(m)
    nf = int(SR * fade)
    env[:nf] = 0.5 * (1 - np.cos(np.pi * np.arange(nf) / nf))
    env[-nf:] = 0.5 * (1 - np.cos(np.pi * np.arange(nf)[::-1] / nf))
    x[i0:i1] += amp * env * np.sin(2 * np.pi * f * tt)

for k in range(12):           # the walk: C G D A E B F# C# G# D# A# E#
    tone(k * step, dur, freq(k))
tone(12 * step, hold, freq(12))          # B#: 12 fifths, 23.46 cents sharp
tone(c_enter, dur_c, BASE)               # home C re-enters, under B#

# numeric check of the beat envelope in the final section
seg = x[int(SR * (c_enter + 1.0)):int(SR * (c_enter + 4.0))]
env = np.abs(seg)  # rough envelope via |x| peaks
peaks = env[1:-1][(env[1:-1] > env[:-2]) & (env[1:-1] > env[2:])]
if len(peaks) > 2:
    est = 1.0 / np.mean(np.diff(np.where(
        (env[1:-1] > env[:-2]) & (env[1:-1] > env[2:]))[0] + 1) / SR)
    print(f"beat freq est: {est:.2f} Hz (expected |261.63*2^(23.46/1200) - 261.63| = "
          f"{BASE * (2 ** (COMMA_CENTS / 1200) - 1):.2f} Hz)")

peak = np.max(np.abs(x))
print(f"peak amplitude {peak:.3f}, total {total:.1f}s")
x = (x / peak * 0.89 * 32767).astype(np.int16)
with wave.open("assets/comma_walk.wav", "wb") as w:
    w.setnchannels(1)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes(x.tobytes())

print("wrote assets/comma_walk.wav")
for k in range(13):
    print(f"  k={k:2d}  cents={landing_cents(k):7.2f}  f={freq(k):8.2f} Hz")
