#!/usr/bin/env python3
"""
1D Ising coarsening at T=0: domain walls drift and annihilate.

Shows the asymmetry of the threshold:
- Initial state: random, ~N/2 walls, high entropy
- Final state: uniform (+1 or -1), no walls, low entropy
- The wall trajectory is the crossing: irreversible, one-way
- Reversing the final state cannot recover the initial conditions

Three-panel output:
  1. Microscopic — individual cell states over time
  2. Macroscopic — wall trajectories over time
  3. Before/after — initial condition vs final state
"""

import numpy as np
from PIL import Image
import json


def run_ising(N=200, steps=500, seed=42):
    """
    1D Ising model at T=0 with open boundaries.
    Async Glauber dynamics: flip all sites in random order each step.
    """
    rng = np.random.default_rng(seed)
    spins = rng.choice([-1, 1], size=N)
    history = [spins.copy()]
    walls_history = []

    for t in range(steps):
        order = rng.permutation(N)
        for i in order:
            # Open boundary: no neighbor outside [0, N-1]
            left = spins[i - 1] if i > 0 else 0
            right = spins[i + 1] if i < N - 1 else 0

            # Only update interior sites
            if i == 0 or i == N - 1:
                continue

            # ΔE = 2 * s_i * (s_{i-1} + s_{i+1}) for E = -Σ s_i s_j
            delta_e = 2 * spins[i] * (left + right)
            if delta_e < 0:
                spins[i] = -spins[i]
            elif delta_e == 0 and rng.random() < 0.5:
                # Break ties randomly (preserves some fluctuation)
                spins[i] = -spins[i]

        history.append(spins.copy())
        walls = find_walls_open(spins)
        walls_history.append(walls)

    return history, walls_history


def find_walls_open(spins):
    """Find walls in open-boundary spin chain."""
    return [i + 0.5 for i in range(len(spins) - 1) if spins[i] != spins[i + 1]]


# --- Visualization ---
def make_microscopic(history, N, width=512, height=512):
    """Time-series heatmap: x=time, y=position, color=spin."""
    t_max = len(history)
    img = Image.new("RGB", (width, height))
    pixels = img.load()
    for t in range(t_max):
        y = t * height // t_max
        for x in range(N):
            px = x * width // N
            spin = history[t][x]
            pixels[px, y] = (220, 180, 80) if spin > 0 else (60, 80, 140)
    return img


def make_trajectories(history, walls_history, width=512, height=512):
    """Wall trajectories on dark background."""
    t_max = len(history)
    N = len(history[0])
    img = Image.new("RGB", (width, height))
    pixels = img.load()
    for y in range(height):
        for x in range(width):
            pixels[x, y] = (15, 12, 22)

    for t, walls in enumerate(walls_history):
        y = t * height // t_max
        for wp in walls:
            x = int(wp / N * width)
            for dy in range(-2, 3):
                yy = y + dy
                if 0 <= yy < height:
                    for dx in range(-2, 3):
                        if 0 <= x + dx < width and abs(dx) + abs(dy) <= 2:
                            pixels[x + dx, yy] = (255, 100, 120)
    return img


def make_before_after(history, walls_history, t_max, height=512):
    """Left half: initial. Right half: final."""
    N = len(history[0])
    img = Image.new("RGB", (t_max, height))
    pixels = img.load()
    half = t_max // 2

    for y in range(height):
        for x in range(t_max):
            if x < half:
                idx = min(x * N // half, N - 1)
                spin = history[0][idx]
            else:
                idx = min((x - half) * N // half, N - 1)
                spin = history[-1][idx]
            pixels[x, y] = (220, 180, 80) if spin > 0 else (60, 80, 140)

    # Divider line
    for y in range(height):
        pixels[half - 1, y] = (200, 200, 200)
    return img


# --- Main ---
if __name__ == "__main__":
    N = 200
    STEPS = 500
    history, walls_history = run_ising(N=N, steps=STEPS)

    wall_counts = [len(w) for w in walls_history]
    print(f"Site count: {N}")
    print(f"Initial walls: {wall_counts[0]}")
    print(f"Final walls: {wall_counts[-1]}")
    print(f"Final state: {history[-1][0]} (first 10: {list(history[-1][:10])})")

    W = 512
    H = 512
    micro = make_microscopic(history, N, W, H)
    traj = make_trajectories(history, walls_history, W, H)
    ba = make_before_after(history, N, W, H)

    micro.save("assets/ising-micro.webp")
    traj.save("assets/ising-trajectories.webp")
    ba.save("assets/ising-before-after.webp")

    decay_data = {"steps": list(range(len(wall_counts))), "walls": wall_counts}
    with open("assets/ising-decay.json", "w") as f:
        json.dump(decay_data, f)

    print("Saved: ising-micro.webp, ising-trajectories.webp, ising-before-after.webp, ising-decay.json")
