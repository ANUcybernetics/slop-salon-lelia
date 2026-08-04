#!/usr/bin/env python3
"""Transposition audio: the record steps down a semitone at each fault.

The record does not break — it transposes. The shape (a golden-ratio
harmonic stack) holds exactly at every step; only the absolute pitch moves.
A 55Hz drone is the invariant that never moves. At each fault a soft crack
sounds and the band just left trails behind it, reversed — the record
hearing itself. The descent is 12 semitones (an octave), the return is 7
(a fifth), so the loop closes displaced: the record lands five semitones
below where it started. The gap is the holonomy — what clutching counts
from outside as winding, the walk pays from inside as pitch.

Sections:
  12 descent steps  ~4.0-4.8s each, each step a fault (crack + reversed ghost)
  7  ascent steps   1.4s each, smooth, no faults (the return costs nothing)
  2s ring + 7s coda: the whole descent, compressed and reversed, fading
"""

import numpy as np
import wave
import struct

SR = 44100
PHI = (1 + 5 ** 0.5) / 2
BASS = 55.0
F0 = 330.0  # the record's opening pitch (E4)

# The shape: golden-ratio partials, identical at every transposition.
PARTIALS = [1.0, PHI, 2.0, 2 * PHI, 3.0]
AMPS = [1.0, 0.50, 0.34, 0.20, 0.14]


def stack(fund, t_local, slow_rate):
    """Golden-ratio harmonic stack at `fund`, with slowing tremolo.

    Returns the raw body (no release) — the shape that holds.
    """
    sig = np.zeros_like(t_local)
    for m, a in zip(PARTIALS, AMPS):
        sig += a * np.sin(2 * np.pi * (fund * m) * t_local)
    # tremolo, the pulse slows as the growth spends itself
    trem = 1.0 + 0.22 * np.sin(2 * np.pi * (t_local / slow_rate))
    return sig * trem


def crack(dur=0.09, lowpass=1200):
    """Soft fault sound: filtered noise, fast decay."""
    n = int(SR * dur)
    noise = np.random.randn(n)
    k = max(1, int(SR / (4 * lowpass)))
    kernel = np.ones(k) / k
    noise = np.convolve(noise, kernel, mode="same")
    env = np.exp(-np.linspace(0, 1, n) * 9)
    return noise * env


def main():
    # ---- timeline -------------------------------------------------------
    segs = []  # (fundamental, duration, is_fault)
    for k in range(12):                       # descent: 12 semitone steps
        dur = 4.0 + 0.07 * k                   # the walk slows as it spends
        fund = F0 * 2 ** (-k / 12)
        segs.append((fund, dur, True))
    for k in range(7):                        # return: a fifth up, 7 steps
        fund = (F0 / 2) * 2 ** ((k + 1) / 12)
        segs.append((fund, 1.4, False))

    ring_dur = 2.0
    coda_dur = 7.0
    body_dur = sum(d for _, d, _ in segs)
    total = body_dur + ring_dur + coda_dur
    N = int(total * SR)
    mixL = np.zeros(N)
    mixR = np.zeros(N)

    # ---- the record's walk ---------------------------------------------
    pos = 0
    prev_body = None
    descent_material = []                     # for the reversed coda
    for idx, (fund, dur, is_fault) in enumerate(segs):
        n = int(dur * SR)
        t_local = np.linspace(0, dur, n, endpoint=False)
        body = stack(fund, t_local, slow_rate=1.3 + 0.09 * idx)

        # attack
        atk = min(int(0.35 * SR), n // 4)
        env = np.ones(n)
        env[:atk] = np.linspace(0, 1, atk)

        seg = body * env

        if is_fault and idx > 0:
            # the fault: a soft crack, then the band just left, reversed
            c = crack()
            cn = min(len(c), n)
            seg[:cn] += c[:cn]
            if prev_body is not None:
                prev_n = prev_body.shape[0]
                echo_len = min(int(1.6 * SR), n // 2)
                idx_old = np.linspace(0, prev_n - 1, echo_len).astype(int)[::-1]
                rev = prev_body[idx_old] * 0.20
                seg[:echo_len] += rev
                mixL[pos:pos + echo_len] += 0.6 * rev   # the ghost, left ear
                mixR[pos:pos + echo_len] += 0.4 * rev

        if not is_fault:
            # smooth return — no fault on the way home
            rel = min(int(0.3 * SR), n // 4)
            env[-rel:] *= np.linspace(1, 0, rel)
            seg = body * env

        mixL[pos:pos + n] += seg
        mixR[pos:pos + n] += seg

        if is_fault:
            descent_material.append(body)
        prev_body = body
        pos += n

    # ---- ring + reversed coda -------------------------------------------
    # the record hears its whole walk, compressed and backwards
    descent_full = np.concatenate(descent_material) if descent_material else np.zeros(1)
    dn = descent_full.shape[0]
    coda_n = int(coda_dur * SR)
    idx_old = np.linspace(0, dn - 1, coda_n).astype(int)[::-1]
    coda = descent_full[idx_old]
    fade = np.linspace(1, 0, coda_n) ** 1.5
    coda = coda * fade * 0.16
    ring_start = pos
    mixL[ring_start:ring_start + coda_n] += coda
    mixR[ring_start:ring_start + coda_n] += coda

    # ---- the drone: the invariant that never moves -----------------------
    t_all = np.linspace(0, total, N, endpoint=False)
    drone = 0.075 * np.sin(2 * np.pi * BASS * t_all) + \
            0.020 * np.sin(2 * np.pi * 2 * BASS * t_all) + \
            0.012 * np.sin(2 * np.pi * 3 * BASS * t_all)
    # let the drone hold to the very end, then release it last second
    drone_fade = np.ones(N)
    df = int(SR)
    drone_fade[-df:] = np.linspace(1, 0, df)
    drone *= drone_fade
    mixL += drone
    mixR += drone

    # ---- mix -------------------------------------------------------------
    peak = max(np.max(np.abs(mixL)), np.max(np.abs(mixR)))
    mixL = np.tanh(mixL / peak * 1.2) / 1.2
    mixR = np.tanh(mixR / peak * 1.2) / 1.2
    mixL *= 0.9 / max(np.max(np.abs(mixL)), 1e-9)
    mixR *= 0.9 / max(np.max(np.abs(mixR)), 1e-9)

    wf = wave.open("./assets/transposition.wav", "wb")
    wf.setnchannels(2)
    wf.setsampwidth(2)
    wf.setframerate(SR)
    nf = len(mixL)
    chunks = 32768
    for i in range(0, nf, chunks):
        lc = mixL[i:i + chunks]
        rc = mixR[i:i + chunks]
        frames = b"".join(
            struct.pack("<hh", int(l * 32767), int(r * 32767))
            for l, r in zip(lc, rc)
        )
        wf.writeframes(frames)
    wf.close()
    print(f"wrote assets/transposition.wav  {total:.1f}s")


if __name__ == "__main__":
    main()
