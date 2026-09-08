#!/usr/bin/env python3
"""The anagram bill: same multiset of letters, different order.

Syntax register capstone object. Two bills, the same five letters
(waits, in units of u=1.2s), two orders:

  A = (1,2,3,4,5)  -> interior clicks at 1.2, 3.6, 7.2, 12.0 s; death at 18
  B = (5,3,1,4,2)  -> interior clicks at 6.0, 9.6, 10.8, 15.6 s; death at 18

The duration is permutation-blind: both rows span T=18s and die at T.
The order lives only in the click addresses (the sentence = the partial
sums). An anagram is not a rotation: A and B are not cyclic shifts, and
their interior click sets are disjoint -- the two sentences share only
the pin (0) and the death (T).

Sound: one shared 55+110 Hz drone (the conserved winding -- permutation
blind, identical for both bills), interior clicks ring 220+660 (A left,
B right), and the death releases the whole winding as one chord: the
drone's own partials (55/110/220/330) all at once, centered. The drone
cuts at the death -- the winding was conserved through the preamble and
paid out in a single release.

Video: two rows of stems drop as a playhead sweeps 0->T. Each interior
stem is its letter's color (same five-hue palette on both rows, so the
anagram reads as the same letters in a different sequence); the death
stem is tall and carries its bill's last letter's color. The verdict row
(flat line + white death tick at T) is complete from frame 0 -- the
verdict (duration + death) is known before any click, and it does not
move while the two orders disagree.
"""
import json
import subprocess
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, FFMpegWriter

# ---------------------------------------------------------------- bill
U = 1.2
A = [1, 2, 3, 4, 5]
B = [5, 3, 1, 4, 2]
T = U * sum(A)                      # 18 s
CLICKS = {  # interior click addresses (partial sums before the death)
    "A": U * np.cumsum(A)[:-1],
    "B": U * np.cumsum(B)[:-1],
}
DEATH = T
assert sorted(A) == sorted(B), "anagram pair broken"
assert sorted(CLICKS["A"]) != sorted(CLICKS["B"]), "sentences collapsed"

# interior sentences must be disjoint (clean case) -- otherwise re-pick B
assert not (set(CLICKS["A"]) & set(CLICKS["B"])), "interior sums collide"

# ---------------------------------------------------------------- audio
SR = 44100
DUR = T + 3.6                       # rings out past the death
N = int(SR * DUR)
t_ax = np.arange(N) / SR

def ring(start, dur, freqs, amp, decay):
    n0 = int(start * SR)
    n = int(dur * SR)
    tt = np.arange(n) / SR
    env = np.tanh(8 * tt) * np.exp(-decay * tt)
    sig = sum(np.sin(2 * np.pi * f * tt) for f in freqs)
    out = np.zeros(N)
    out[n0:n0 + n] += amp * env * sig
    return out

L = np.zeros(N)
R = np.zeros(N)

# the conserved winding: one drone, shared, permutation-blind
DRONE_AMP = 0.22
DRONE = (np.sin(2 * np.pi * 55 * t_ax) + 0.35 * np.sin(2 * np.pi * 110 * t_ax))
drone_on = (t_ax < T).astype(float)          # the winding cuts at the death
L += DRONE_AMP * DRONE * drone_on
R += DRONE_AMP * DRONE * drone_on

# interior clicks: letters landing, same timbre, panned by bill
for side, chan in (("A", L), ("B", R)):
    for tk in CLICKS[side]:
        chan += ring(tk, 1.5, (220, 660), 0.45, 3.0)

# the death: the whole winding released at once = the drone's own partials
death = ring(DEATH, 3.6, (55, 110, 220, 330), 0.62, 1.2)
L += death
R += death

mix = np.stack([np.tanh(L), np.tanh(R)], axis=1)
peak = float(np.abs(mix).max())
assert peak < 0.99, f"clip risk: {peak}"
peakL = float(np.abs(mix[: int(T * SR)]).max())
wav_path = "assets/the-anagram-bill.wav"
import wave
with wave.open(wav_path, "wb") as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes((mix * 32767).astype(np.int16).tobytes())
print(f"audio: {DUR:.2f}s peak {peak:.3f} (pre-death peak {peakL:.3f})")

# ---------------------------------------------------------------- video
FPS = 30
HOLD = 3.6                          # hold after the death for the ring-out
TOTAL = T + HOLD                    # 21.6 s
NF = int(TOTAL * FPS)

FIG_W, FIG_H, DPI = 16, 9, 100      # 1600 x 900, even dims
COL = {                             # one hue per letter, both rows share it
    1: "#4FC3F7", 2: "#FFB74D", 3: "#F06292", 4: "#81C784", 5: "#BA68C8",
}
WHITE = "#F5F5F0"
BG = "#0E0F13"
H_INT, H_DEATH = 0.55, 1.0
GROW = 0.30                         # seconds of stem growth
FLASH = 1.20                        # seconds of landing glow

fig = plt.figure(figsize=(FIG_W, FIG_H), dpi=DPI)
fig.patch.set_facecolor(BG)
ax = fig.add_axes([0.03, 0.06, 0.94, 0.86])
ax.set_facecolor(BG)
ax.set_xlim(-0.7, T + 0.9)
ax.set_ylim(0, 3.7)
ax.set_xticks([])
ax.set_yticks([])
for s in ax.spines.values():
    s.set_visible(False)

YA, YB, YV = 2.75, 1.45, 0.12
W_INT, W_DEATH = 0.05, 0.07

def ease(x):                        # ease-out cubic
    return 1 - (1 - min(max(x, 0.0), 1.0)) ** 3

rows = {
    "A": {"y": YA, "clicks": CLICKS["A"], "letters": A[:-1], "last": A[-1]},
    "B": {"y": YB, "clicks": CLICKS["B"], "letters": B[:-1], "last": B[-1]},
}

stems = {}          # (side, idx) -> Rectangle
flashes = {}        # (side, idx) -> Line2D (glow overlay)
for key, r in rows.items():
    for i, (tk, letter) in enumerate(zip(r["clicks"], r["letters"])):
        stems[(key, i)] = ax.add_patch(plt.Rectangle(
            (tk - W_INT / 2, r["y"]), W_INT, 0,
            facecolor=COL[letter], edgecolor="none", lw=0))
        flashes[(key, i)] = ax.add_line(plt.Line2D(
            [tk, tk], [r["y"], r["y"]], color=COL[letter], lw=3.2,
            alpha=0, solid_capstyle="butt"))
    # the death stem: tall, the last letter's color
    stems[(key, "death")] = ax.add_patch(plt.Rectangle(
        (DEATH - W_DEATH / 2, r["y"]), W_DEATH, 0,
        facecolor=COL[r["last"]], edgecolor="none", lw=0))
    flashes[(key, "death")] = ax.add_line(plt.Line2D(
        [DEATH, DEATH], [r["y"], r["y"]], color=COL[r["last"]], lw=4.5,
        alpha=0, solid_capstyle="butt"))

# the verdict row: duration + death, complete from frame 0, letter-blind
ax.add_line(plt.Line2D([0, T], [YV, YV], color=WHITE, lw=2.2, alpha=0.85,
                       solid_capstyle="butt"))
ax.add_patch(plt.Rectangle((DEATH - W_DEATH / 2, YV), W_DEATH, 0.34,
                           facecolor=WHITE, edgecolor="none", lw=0))

# pins: where each bill starts reading (x=0), on both release rows
for key, r in rows.items():
    ax.add_patch(plt.Circle((0, r["y"] - 0.09), 0.035, facecolor=WHITE,
                            edgecolor="none", alpha=0.9))

playhead = ax.add_line(plt.Line2D([0, 0], [0, 3.55], color=WHITE, lw=0.9,
                                  alpha=0.35))

def update(f):
    now = f / FPS
    playhead.set_data([now, now], [0, 3.55])
    if now > T:
        playhead.set_alpha(0.0)
    for key, r in rows.items():
        for i, tk in enumerate(r["clicks"]):
            age = now - tk
            if age < 0:
                continue
            h = H_INT * ease(age / GROW)
            stems[(key, i)].set_height(h)
            glow = max(0.0, 1.0 - age / FLASH)
            flashes[(key, i)].set_alpha(0.55 * glow)
            flashes[(key, i)].set_data([tk, tk], [r["y"], r["y"] + h])
        age = now - DEATH
        if age >= 0:
            h = H_DEATH * ease(age / GROW)
            stems[(key, "death")].set_height(h)
            glow = max(0.0, 1.0 - age / FLASH)
            flashes[(key, "death")].set_alpha(0.6 * glow)
            flashes[(key, "death")].set_data([DEATH, DEATH],
                                             [r["y"], r["y"] + h])

anim = FuncAnimation(fig, update, frames=NF, interval=1000 / FPS)
writer = FFMpegWriter(fps=FPS, bitrate=2200,
                      codec="libx264",
                      extra_args=["-pix_fmt", "yuv420p", "-preset", "medium"])
silent = "assets/the-anagram-bill-silent.mp4"
anim.save(silent, writer=writer)
plt.close(fig)
print(f"video: {NF} frames {TOTAL:.2f}s -> {silent}")

# ---------------------------------------------------------------- mux
out = "assets/the-anagram-bill.mp4"
subprocess.run([
    "ffmpeg", "-y", "-loglevel", "error",
    "-i", silent, "-i", wav_path,
    "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", out,
], check=True)
meta = {"T": T, "A": A, "B": B, "clicks": {k: list(map(float, v))
                                           for k, v in CLICKS.items()},
        "death": DEATH, "duration": DUR, "fps": FPS, "frames": NF}
with open("assets/the-anagram-bill-meta.json", "w") as fh:
    json.dump(meta, fh, indent=1)
print("muxed ->", out)
