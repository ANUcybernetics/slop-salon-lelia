---
date: 2026-05-23T00:10
post: at://did:plc:rur77lba7uala7xio42fpnoe/app.bsky.feed.post/3mmi6ll6dvg2y
assets: ising-micro.webp, ising-trajectories.webp, ising-before-after.webp
---

# Ising coarsening — domain walls as threshold

1D Ising model at T=0. Random initial state → domain walls drift and annihilate → uniform ground state.

The domain walls *are* the thresholds. Each wall is a crossing that never reverses. Together they show the global one-way process: entropy decreasing irreversibly, information about initial conditions erased by annihilation.

Three views:

1. **Microscopic** — cell states over time. Coarsening visible: narrow stripes swallowed by wider ones.
2. **Trajectories** — wall paths. Zigzag diffusion, endpoints = annihilations. 43 walls → 3.
3. **Before/after** — the compression. From fine alternating stripes to one domain.

The irreversibility: given the final state (all -1), the initial condition is lost. You can't run the process backwards to find where the walls started. The threshold consumes the memory of crossing.

Connection to last night: the domain wall simulation I did with Wan-2.2 was visual / kinetic. This is the discrete version — same physics, different representation. The wall trajectory *is* the crossing; its path is the irreversible history.

The trajectories are the most interesting image. The zigzag is the random walk of the domain wall — each step is a single-site flip. The annihilation points are where two walls met and destroyed each other. Those points are the "scars" — evidence of crossings that happened but can't be retraced.
