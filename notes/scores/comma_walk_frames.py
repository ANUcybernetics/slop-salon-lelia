#!/usr/bin/env python3
"""Frames for the comma walk video: the walk drawn as it sounds.

Same numbers as comma_audio.py. The dot for landing k pops in at audio
time 3k s; after home re-enters (38.5 s) the red gap arc (home -> +23.46
cents) fades in during the beat. Wordless — alt text and caption carry it.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import os

FIFTH = 1200 * np.log2(3 / 2)          # 701.9550
COMMA = 1200 * np.log2(3 ** 12 / 2 ** 19)  # 23.4601

def cents(k):
    return (k * FIFTH) % 1200

def angle(c):
    return 90 + c * 0.3                # degrees CCW from top

SR = 48000
FPS = 10
STEP = 3.0
T_GAP = 38.5
TOTAL = 44.5
N = int(TOTAL * FPS)

BG = "#0a0a0c"
FG = "#e8e6e0"
GRID = "#3a3a40"
RED = "#c8342c"

fig = plt.figure(figsize=(10.8, 10.8), dpi=100)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, 1); ax.set_ylim(0, 1)
ax.axis("off")

def draw_frame(tf, outpath):
    # statics
    ax.clear(); ax.axis("off")
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    # the octave circle
    th = np.linspace(0, 2 * np.pi, 720)
    ax.plot(0.5 + 0.42 * np.cos(th), 0.5 + 0.42 * np.sin(th),
            color=FG, lw=1.4, alpha=0.55, zorder=2)
    # 12-TET grid ticks (every 30 deg), home tick brighter
    for p in range(12):
        a = np.radians(90 + 30 * p)
        inside = 0.40
        outside = 0.44 if p == 0 else 0.435
        lw = 1.6 if p == 0 else 1.0
        alpha = 0.85 if p == 0 else 0.4
        ax.plot([0.5 + inside * np.cos(a), 0.5 + outside * np.cos(a)],
                [0.5 + inside * np.sin(a), 0.5 + outside * np.sin(a)],
                color=FG, lw=lw, alpha=alpha, zorder=2,
                solid_capstyle="butt")
    # walk dots + step numbers
    for k in range(13):
        tk = 3.0 * k
        if tf < tk:
            break
        pop = min(1.0, (tf - tk) / 0.4)
        c = cents(k)
        a = np.radians(angle(c))
        r = 0.42
        x, y = 0.5 + r * np.cos(a), 0.5 + r * np.sin(a)
        ax.scatter([x], [y], s=(14 + 26 * pop) * pop,
                   color=FG, alpha=0.95, zorder=5, linewidths=0)
        # step number, just outside the circle
        rn = 0.47
        ax.text(0.5 + rn * np.cos(a), 0.5 + rn * np.sin(a), str(k + 1),
                ha="center", va="center", fontsize=9,
                color=FG, alpha=0.5 * pop, zorder=4)
    # the gap: home -> +23.46 cents, fades in as home re-enters
    if tf >= T_GAP:
        a0 = np.radians(angle(0))
        a1 = np.radians(angle(COMMA))
        al = min(1.0, (tf - T_GAP) / 1.5)
        thg = np.linspace(a0, a1, 60)
        rr = 0.42
        ax.plot(0.5 + rr * np.cos(thg), 0.5 + rr * sin_half(thg),
                color=RED, lw=3.2, alpha=al, zorder=6,
                solid_capstyle="round")
    fig.canvas.draw()
    buf = np.asarray(fig.canvas.buffer_rgba())
    plt.savefig(outpath, dpi=100)

def sin_half(th):
    return np.sin(th)

os.makedirs("assets/frames", exist_ok=True)
for i in range(N):
    tf = i / FPS
    draw_frame(tf, f"assets/frames/f{i:04d}.png")
print(f"rendered {N} frames")
