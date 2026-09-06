#!/usr/bin/env python3
"""Gray-Scott reaction-diffusion: global form from nothing but local exchange.

du/dt = Du L u - u v^2 + F (1-u)
dv/dt = Dv L v + u v^2 - (F+k) v

Nine-point Laplacian, roll-based. QA: coverage + ASCII density map.
"""
import sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BG = "#0b0b10"
INK = "#e8dcc4"
rng = np.random.default_rng(11)


def lap(u):
    return (0.05 * (np.roll(u, 2, 0) + np.roll(u, -2, 0) + np.roll(u, 2, 1) + np.roll(u, -2, 1))
            + 0.2 * (np.roll(u, 1, 0) + np.roll(u, -1, 0) + np.roll(u, 1, 1) + np.roll(u, -1, 1))
            - u)


def run(F, k, steps=6000, n=384, seed_mode="corner"):
    u = np.ones((n, n))
    v = np.zeros((n, n))
    if seed_mode == "corner":
        s = 24
        v[n//2-s:n//2+s, n//2-s:n//2+s] = 0.55
        u[n//2-s:n//2+s, n//2+s:] = 0.25
    else:  # scatter
        for _ in range(9):
            i, j = rng.integers(60, n - 60, 2)
            s = rng.integers(6, 14)
            v[i-s:i+s, j-s:j+s] = 0.5
            u[i-s:i+s, j-s:j+s] = 0.25
    for _ in range(steps):
        uvv = u * v * v
        u += 0.16 * lap(u) - uvv + F * (1 - u)
        v += 0.08 * lap(v) + uvv - (F + k) * v
        np.clip(u, 0, 1, out=u)
        np.clip(v, 0, 0.6, out=v)
    return v


def render(v, path, size=1024):
    fig = plt.figure(figsize=(6, 6), facecolor=BG)
    ax = fig.add_axes([0, 0, 1, 1], facecolor=BG)
    im = ax.imshow(v, cmap="copper", vmin=0.0, vmax=0.38, interpolation="bicubic")
    ax.set_axis_off()
    fig.savefig(path, dpi=size / 6, facecolor=BG)
    plt.close(fig)


def qa(path):
    from PIL import Image
    im = np.asarray(Image.open(path).convert("L"), dtype=float) / 255.0
    h, wd = im.shape
    ink = im > 0.45
    frac = ink.mean()
    G = 14
    cells = ink[: h // G * G, : wd // G * G].reshape(G, h // G, G, wd // G).mean(axis=(1, 3))
    print(f"{path}: ink={frac*100:.2f}%")
    for row in cells:
        print("".join(" .:*#"[min(4, int(v * 22))] for v in row))
    return frac


if __name__ == "__main__":
    jobs = [
        (0.030, 0.062, "corner", "assets/gs-mitosis.png"),
        (0.0545, 0.062, "corner", "assets/gs-coral.png"),
        (0.058, 0.065, "corner", "assets/gs-worms.png"),
        (0.026, 0.056, "scatter", "assets/gs-scatter.png"),
        (0.062, 0.061, "corner", "assets/gs-labyrinth.png"),
    ]
    for F, k, mode, path in jobs:
        v = run(F, k, steps=6000, seed_mode=mode)
        render(v, path)
        qa(path)
        print()
