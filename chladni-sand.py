#!/usr/bin/env python3
"""Chladni sand: residency render of a square plate's nodal lines.

Mode (m,n) with symmetry sign eps:  f = cos(m pi x)cos(n pi y) - eps cos(n pi x)cos(m pi y)
Sand density ~ exp(-(f/sigma)^2): grains pile up where the plate barely moves.
eps=+1 modes always carry both diagonals; eps=-1 modes open onto the axes.
QA by pixel stats + ASCII density map (image Read doesn't render here).
"""
import sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BG = "#0b0b10"
SAND = "#e8dcc4"
rng = np.random.default_rng(7)


def chladni(m, n, eps):
    def f(x, y):
        return (np.cos(m * np.pi * x) * np.cos(n * np.pi * y)
                - eps * np.cos(n * np.pi * x) * np.cos(m * np.pi * y))
    return f


def render(m, n, eps, path, N=5_000_000, sigma=0.075, size=1024):
    f = chladni(m, n, eps)
    x = rng.uniform(-0.5, 0.5, N)
    y = rng.uniform(-0.5, 0.5, N)
    w = np.abs(f(x, y))
    p = np.exp(-(w / sigma) ** 2)
    acc = rng.uniform(size=N) < p
    xs, ys = x[acc], y[acc]
    grain = rng.uniform(0.25, 0.8, xs.size)  # per-grain alpha: sand texture

    fig = plt.figure(figsize=(6, 6), facecolor=BG)
    ax = fig.add_axes([0, 0, 1, 1], facecolor=BG)
    ax.scatter(xs, ys, s=0.35, c=SAND, alpha=grain, linewidths=0, marker=".")
    ax.set_xlim(-0.5, 0.5)
    ax.set_ylim(-0.5, 0.5)
    ax.set_axis_off()
    fig.savefig(path, dpi=size / 6, facecolor=BG)
    plt.close(fig)
    return xs.size


def qa(path):
    """Pixel-count QA + ASCII density map (12x12, sand=1)."""
    from PIL import Image
    im = np.asarray(Image.open(path).convert("L"), dtype=float) / 255.0
    h, wd = im.shape
    sand = im > 0.45
    frac = sand.mean()
    left, right = sand[:, : wd // 2].mean(), sand[:, wd // 2:].mean()
    top, bot = sand[: h // 2].mean(), sand[h // 2:].mean()
    print(f"{path}: sand={frac*100:.2f}%  L/R={left:.4f}/{right:.4f}  T/B={top:.4f}/{bot:.4f}")
    G = 14
    cells = sand[: h // G * G, : wd // G * G].reshape(G, h // G, G, wd // G).mean(axis=(1, 3))
    for row in cells:
        print("".join(" .:*#"[min(4, int(v * 28))] for v in row))
    return frac


if __name__ == "__main__":
    jobs = [
        (1, 2, -1, "assets/chladni-12m.png"),
        (2, 3, +1, "assets/chladni-23p.png"),
        (3, 4, +1, "assets/chladni-34p.png"),
        (2, 5, -1, "assets/chladni-25m.png"),
        (1, 3, -1, "assets/chladni-13m.png"),
        (3, 5, +1, "assets/chladni-35p.png"),
    ]
    fracs = {}
    for m, n, eps, path in jobs:
        grains = render(m, n, eps, path)
        fracs[path] = qa(path)
        print(f"  grains={grains}")
    print("\ncoverage summary:", {k: f"{v*100:.2f}%" for k, v in fracs.items()})
