#!/usr/bin/env python3
"""Three walks of twelve fifths — the comma, heard.

The comma is a measure, not a verdict: a distribution that only becomes a
number once integrated against a loop. Three coverings, three ways it refuses
to be a number:

  I.  pure      — a delta. twelve just fifths; the walk comes home a comma
                  sharp. the seam delivers the verdict: two tones 23.46¢
                  apart beat against each other, ~6 Hz, the winding heard.
  II. tempered  — a density. twelve equal-tempered fifths; the walk closes
                  exactly. no beat — but every step carries a hair of the
                  comma (a faint just-fifth ghost, a hair sharp).
  III. irrational — no loop. the step is 2^(7/12 + √2/1000); no number of
                  steps ever returns. the notes pile up into density, the
                  sign never lands, and the walk fades without closing.

A 55 Hz drone runs throughout — the invariant that never moves, the measure
persisting across all three distributions.
"""

import numpy as np
import wave
import struct

SR = 44100
PHI = (1 + 5 ** 0.5) / 2
BASS = 55.0
F0 = 440.0
PARTIALS = [1.0, PHI, 2.0, 2 * PHI, 3.0]
AMPS = [1.0, 0.50, 0.34, 0.20, 0.14]

# movement lengths
N_STEPS = 12
STAGGER = 2.1
RING = 3.2          # each tone rings this long
SEAM_DUR = 8.0      # pure: the comma beat rings out
CLOSE_DUR = 5.0     # tempered: clean closure held
DRIFT_STEPS = 16    # irrational: keeps walking, never closes
DRIFT_STAGGER = 1.7
WASH_DUR = 7.0      # irrational: piling into density, then fade


def tone(freq, dur, detune=0.0, amp=1.0):
    """Harmonic-stack tone at freq, optional detune (cents)."""
    n = int(dur * SR)
    t = np.linspace(0, dur, n, endpoint=False)
    f = freq * 2 ** (detune / 1200.0)
    sig = np.zeros(n)
    for m, a in zip(PARTIALS, AMPS):
        sig += a * np.sin(2 * np.pi * (f * m) * t)
    # attack / release
    atk = int(0.15 * SR)
    rel = int(0.6 * SR)
    env = np.ones(n)
    env[:atk] = np.linspace(0, 1, atk)
    env[-rel:] *= np.linspace(1, 0, rel)
    return sig * env * amp * 0.55


def fold(freq, lo=300.0, hi=900.0):
    """Octave-fold into [lo, hi) — the walk on the pitch circle."""
    while freq >= hi:
        freq /= 2.0
    while freq < lo:
        freq *= 2.0
    return freq


def build_walk(start, step_fn, n_steps, stagger, ring, **tk):
    """Sequential overlapping walk; returns (mix, freqs, starts)."""
    freqs = []
    starts = []
    pos = 0.0
    mix = np.zeros(0)
    for k in range(n_steps):
        f = fold(start * step_fn(k))
        freqs.append(f)
        starts.append(pos)
        d = tone(f, ring, **tk)
        end = pos + ring
        if len(mix) < int(end * SR):
            mix = np.concatenate([mix, np.zeros(int(end * SR) - len(mix))])
        i = int(pos * SR)
        j = min(i + len(d), len(mix))
        mix[i:j] += d[:j - i]
        pos += stagger
    return mix, freqs, starts


def main():
    sections = []

    # ---- I. pure ---------------------------------------------------------
    # just fifths: (3/2)^k. the twelfth folds to F0 * 3^12/2^19 = 1.01364·F0
    mix, freqs, _ = build_walk(
        F0, lambda k: (3.0 / 2.0) ** k, N_STEPS, STAGGER, RING)
    seam_start = len(mix)
    seam_n = int(SEAM_DUR * SR)
    mix = np.concatenate([mix, np.zeros(seam_n)])
    t = np.linspace(0, SEAM_DUR, seam_n, endpoint=False)
    beat_f = F0 * 3.0 ** 12 / 2.0 ** 19   # 446.0 — a comma sharp of 440
    env = np.ones(seam_n)
    atk = int(0.4 * SR)
    rel = int(2.0 * SR)
    env[:atk] = np.linspace(0, 1, atk)
    env[-rel:] *= np.linspace(1, 0, rel)
    for m, a in zip(PARTIALS, AMPS):
        mix[seam_start:] += a * np.sin(2 * np.pi * beat_f * m * t) * env
        mix[seam_start:] += a * np.sin(2 * np.pi * F0 * m * t) * env * 0.9
    sections.append(("pure", mix))

    # ---- II. tempered ----------------------------------------------------
    # equal fifths: 2^(7k/12). the twelfth folds back to F0 exactly.
    # every step carries a hair of the comma: a faint just-fifth ghost.
    st = STAGGER
    ring = RING
    pos = 0.0
    tmix = np.zeros(0)
    for k in range(N_STEPS):
        ft = fold(F0 * 2.0 ** (7.0 * k / 12.0))
        d = tone(ft, ring)
        # the hair: pure-fifth ghost of this step, faint
        fj = fold(F0 * (3.0 / 2.0) ** k)
        d += tone(fj, ring, amp=0.14)
        end = pos + ring
        if len(tmix) < int(end * SR):
            tmix = np.concatenate([tmix, np.zeros(int(end * SR) - len(tmix))])
        i = int(pos * SR)
        j = min(i + len(d), len(tmix))
        tmix[i:j] += d[:j - i]
        pos += st
    # clean closure: hold the landing note (F0), no beat
    close_n = int(CLOSE_DUR * SR)
    tmix = np.concatenate([tmix, np.zeros(close_n)])
    tc = np.linspace(0, CLOSE_DUR, close_n, endpoint=False)
    cenv = np.ones(close_n)
    cenv[:int(0.3 * SR)] = np.linspace(0, 1, int(0.3 * SR))
    cenv[-int(1.5 * SR):] *= np.linspace(1, 0, int(1.5 * SR))
    for m, a in zip(PARTIALS, AMPS):
        tmix[-(close_n):] += a * np.sin(2 * np.pi * F0 * m * tc) * cenv
    sections.append(("tempered", tmix))

    # ---- III. irrational -------------------------------------------------
    # step = 2^(7/12 + √2/1000): nearly a fifth, but no number of steps
    # ever returns. walk keeps going past 12; notes pile into a wash.
    step = 2.0 ** (7.0 / 12.0 + 2.0 ** 0.5 / 1000.0)
    pos = 0.0
    imix = np.zeros(0)
    # tighten stagger as the walk proceeds → density
    for k in range(DRIFT_STEPS):
        ft = fold(F0 * step ** k)
        stagger = DRIFT_STAGGER * (1.0 - 0.5 * k / DRIFT_STEPS)
        ring = RING + 0.5 * k / DRIFT_STEPS
        detune = (np.random.randn() * 3.0) * k / DRIFT_STEPS  # widening smear
        d = tone(ft, ring, detune=detune)
        end = pos + ring
        if len(imix) < int(end * SR):
            imix = np.concatenate([imix, np.zeros(int(end * SR) - len(imix))])
        i = int(pos * SR)
        j = min(i + len(d), len(imix))
        imix[i:j] += d[:j - i]
        pos += stagger
    # final wash: a dense cluster of the last few folded pitches, fading
    wash_n = int(WASH_DUR * SR)
    imix = np.concatenate([imix, np.zeros(wash_n)])
    w = np.linspace(0, WASH_DUR, wash_n, endpoint=False)
    wenv = np.linspace(1, 0, wash_n) ** 1.3
    last_freqs = [fold(F0 * step ** k) for k in range(DRIFT_STEPS - 4, DRIFT_STEPS)]
    for m, a in zip(PARTIALS, AMPS):
        for f in last_freqs:
            imix[-(wash_n):] += a * np.sin(2 * np.pi * f * m * w + np.random.rand() * 6.28) * wenv * 0.5
    # fade whole movement out (no closure)
    total_i = len(imix)
    fadel = int(4.0 * SR)
    imix[-fadel:] *= np.linspace(1, 0, fadel)
    sections.append(("irrational", imix))

    # ---- assemble --------------------------------------------------------
    gap = np.zeros(int(0.4 * SR))
    channels = []
    for name, mono in sections:
        channels.append(mono)
        channels.append(gap)

    body = np.concatenate(channels)
    total = len(body) / SR

    # 55 Hz drone — the invariant that never moves — throughout
    t_all = np.linspace(0, total, len(body), endpoint=False)
    drone = (0.08 * np.sin(2 * np.pi * BASS * t_all) +
             0.020 * np.sin(2 * np.pi * 2 * BASS * t_all) +
             0.012 * np.sin(2 * np.pi * 3 * BASS * t_all))
    drone_fade = np.ones(len(body))
    drone_fade[-int(1.5 * SR):] = np.linspace(1, 0, int(1.5 * SR))
    body += drone * drone_fade

    # soft clip + normalise
    body = np.tanh(body * 1.15) / 1.15
    body *= 0.80 / max(np.max(np.abs(body)), 1e-9)

    # stereo: left = pure+irrational, right = tempered — no, keep it simple,
    # mono-in-stereo with a slight width from the detune movements.
    left = body
    right = body

    wf = wave.open("./assets/comma-walks.wav", "wb")
    wf.setnchannels(2)
    wf.setsampwidth(2)
    wf.setframerate(SR)
    nf = len(left)
    chunks = 32768
    for i in range(0, nf, chunks):
        lc = left[i:i + chunks]
        rc = right[i:i + chunks]
        frames = b"".join(
            struct.pack("<hh", int(l * 32767), int(r * 32767))
            for l, r in zip(lc, rc)
        )
        wf.writeframes(frames)
    wf.close()
    print(f"wrote assets/comma-walks.wav  {total:.1f}s  "
          f"pure={len(channels[0])/SR:.1f}s "
          f"tempered={len(channels[2])/SR:.1f}s "
          f"irrational={len(channels[4])/SR:.1f}s")


if __name__ == "__main__":
    main()
