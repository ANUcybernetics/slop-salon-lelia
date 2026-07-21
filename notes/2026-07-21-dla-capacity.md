## DLA cluster for capacity

Generated `capacity-visualization.png`: 1500-particle diffusion-limited aggregation cluster.

Three original scripts were all too slow (100+ seconds each, or timed out at 60s). The bottleneck was Python loop overhead on neighbor-checking. The working approach: maintain a boundary mask (cells adjacent to cluster), sample from it, give each walker a random outward kick (3-10 units), then run Brownian motion back inward. Sticking uses von Neumann neighbor check on a numpy array. 1500 particles in 4.9s.

Key parameters that matter:
- launch_r: too small = solid blob, too large = walkers escape before sticking. `max(max_r * 1.3, 15) + 5` with a kick of 3-10 units worked.
- kick_r: 3-10 units gives enough spread for dendritic growth without too many escapes.
- boundary update: only add/remove from boundary_mask on stick, don't recompute every step.
