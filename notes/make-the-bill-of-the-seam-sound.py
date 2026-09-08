#!/usr/bin/env python3
"""The bill of the seam — two mends, one winding, two bills.

Model (displacement-controlled creep cascade, exponent k=2):
  a tear of total winding b=1 closed by n stitches; each stitch holds b/n.
  When one lets go (acoustic emission = a click), the rest carry more:
  the remaining n-j stitches each hold b/(n-j).  Creep rate ~ load^k,
  so the wait before the next release is ~ (n-j)^k.

  Seam L: n=3.  Seam R: n=7.  Same winding (drone), different partitions.

  Universal bill: click with load 1/m arrives after a wait m^2 (energy*wait=1
  per click).  Every mend's bill is a SUFFIX of one universal bill:
  sizes 1/m, waits m^2, m = n..1.  The last click is identical for all mends
  (the last stitch carries the whole winding) — same death, different ages.
  Totals -> sum(1/m^2) -> pi^2/6 as the partition refines.

  The drone never changes: the winding is topological — no lifetime.
  In mono you hear L's bill twice: A's, then B's tail repeats it (the fold
  hears the same death twice).
"""
import numpy as np, wave

SR = 44100
U = 0.30          # wait unit (s); R's bill = sum_{m=1..7} m^2 * U = 42.0 s
F_DRONE = 55.0    # the winding: conserved, flat, no lifetime
F_RING = 220.0    # click carrier (the count register)
F_PART = 660.0
AMP_DRONE = 0.045
TAU_RING, TAU_PART = 0.06, 0.03
TAIL_S = 1.5      # ring tail after the last click

def cascade(n, u=U):
    """Wait-intervals (m^2 for m=n..1) and click amplitudes (1/m for m=n..1)."""
    ms = list(range(n, 0, -1))
    waits = [float(m * m) * u for m in ms]
    amps = [1.0 / m for m in ms]
    return waits, amps

def render_click(buf, t0, amp, sr=SR):
    dur = 0.6
    n = int(dur * sr)
    i0 = int(t0 * sr)
    t = np.arange(n) / sr
    env_r = np.exp(-t / TAU_RING)
    env_p = np.exp(-t / TAU_PART)
    c = amp * (np.sin(2 * np.pi * F_RING * t) * env_r
               + 0.3 * np.sin(2 * np.pi * F_PART * t) * env_p)
    end = min(i0 + n, len(buf))
    if i0 < len(buf):
        buf[i0:end] += c[: end - i0]

def make_channel(n, total):
    buf = np.zeros(total)
    waits, amps = cascade(n)
    t0 = 0.0
    times = []
    for w, a in zip(waits, amps):
        t0 += w
        times.append(t0)
        render_click(buf, t0, a)
    return buf, times

total = int((sum(m * m for m in range(1, 8)) * U + TAIL_S) * SR)
t_axis = np.arange(total) / SR

L, times_L = make_channel(3, total)
R, times_R = make_channel(7, total)

# the winding: identical drone in both channels, never touched by any release
drone = AMP_DRONE * np.sin(2 * np.pi * F_DRONE * t_axis)
L = L + drone
R = R + drone

stereo = np.stack([L, R], axis=1)
peak = np.abs(stereo).max()
stereo = stereo / peak * 0.85
print(f"peak before norm {peak:.3f}")

# the mono reveal: L+R — B's tail repeats A's bill
mono = stereo.mean(axis=1)

print("click times (s):")
print("  L (3 stitches):", [f"{t:.2f}" for t in times_L])
print("  R (7 stitches):", [f"{t:.2f}" for t in times_R])
print("  R tail repeats L's bill:", times_R[-3:], "vs", times_L)
print(f"duration {len(stereo)/SR:.2f} s")

# energy bookkeeping: energy ~ amp^2
eL = sum(a * a for a in (1/m for m in (3, 2, 1)))
eR = sum(a * a for a in (1/m for m in (7, 6, 5, 4, 3, 2, 1)))
print(f"total energy  L: {eL:.4f}  R: {eR:.4f}  (zeta(2) limit {np.pi**2/6:.4f})")
print(f"lifetime      L: {sum(m*m for m in (3,2,1))*U:.1f} s   "
      f"R: {sum(m*m for m in range(1,8))*U:.1f} s")

pcm = (stereo * 32767).astype(np.int16)
with wave.open("assets/the-bill-of-the-seam.wav", "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes(pcm.tobytes())
print("wrote assets/the-bill-of-the-seam.wav")
