"""Lattice of weighted fixed points — the census performing itself.

Each node is a fixed point in the phase space, a site of organized failure.
Strands connect conjugate pairs. The amber cluster marks where the cohomology
class concentrates — not detected as a hole, but as a refusal, given form.
"""

import math
import random
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches

random.seed(42)

# Generate lattice points: weighted fixed points in a 3D-ish arrangement
nodes = []

# Central cluster — cohomology concentration
for i in range(18):
    phi = random.gauss(0, 1)
    theta = random.gauss(0, 1)
    r = random.expovariate(0.8)
    x = r * math.sin(theta) * math.cos(phi) * 1.2
    y = r * math.sin(theta) * math.sin(phi) * 1.2
    z = r * math.cos(theta)
    weight = min(1.0, math.exp(-z / 0.8)) * random.uniform(0.6, 1.0)
    nodes.append({'x': x, 'y': y, 'z': z, 'weight': weight, 'cluster': 'center'})

# Perimeter ring — conjugate pairs
n_ring = 24
for i in range(n_ring):
    angle = 2 * math.pi * i / n_ring
    r = 2.5 + random.gauss(0, 0.2)
    x = r * math.cos(angle)
    y = r * math.sin(angle)
    weight = random.uniform(0.3, 0.7)
    nodes.append({'x': x, 'y': y, 'z': random.gauss(0, 0.4),
                  'weight': weight, 'cluster': 'ring'})

# Scattered field points
for i in range(20):
    x = random.gauss(0, 2.0)
    y = random.gauss(0, 2.0)
    weight = random.uniform(0.1, 0.4)
    nodes.append({'x': x, 'y': y, 'z': random.gauss(0, 0.6),
                  'weight': weight, 'cluster': 'field'})


def node_color(node):
    if node['cluster'] == 'center':
        r = min(1.0, 0.7 + 0.3 * node['weight'])
        g = min(1.0, 0.5 + 0.3 * node['weight'])
        b = min(1.0, 0.05 + 0.15 * node['weight'])
    elif node['cluster'] == 'ring':
        r = min(1.0, 0.25 + 0.2 * node['weight'])
        g = min(1.0, 0.35 + 0.3 * node['weight'])
        b = min(1.0, 0.5 + 0.35 * node['weight'])
    else:
        v = 0.12 + 0.2 * node['weight']
        return (v, v + 0.02, v + 0.05)
    return (r, g, b)


fig, ax = plt.subplots(1, 1, figsize=(8, 8), dpi=150)
fig.patch.set_facecolor('#0a0a0f')
ax.set_facecolor('#0a0a0f')

# Draw strands
ring_nodes = [n for n in nodes if n['cluster'] == 'ring']
center_nodes = [n for n in nodes if n['cluster'] == 'center']

for rn in ring_nodes:
    best = min(center_nodes, key=lambda cn: math.hypot(cn['x']-rn['x'], cn['y']-rn['y']))
    alpha = 0.15 * (rn['weight'] + best['weight']) / 2
    ax.plot([rn['x'], best['x']], [rn['y'], best['y']],
            color=(0.55, 0.63, 0.78), linewidth=0.6, alpha=alpha)

for i, a in enumerate(center_nodes):
    for b in center_nodes[i+1:]:
        d = math.hypot(a['x']-b['x'], a['y']-b['y'])
        if d < 0.8:
            alpha = 0.2 * math.exp(-d / 0.4)
            ax.plot([a['x'], b['x']], [a['y'], b['y']],
                    color=(0.78, 0.63, 0.24), linewidth=0.8, alpha=alpha)

field_nodes = [n for n in nodes if n['cluster'] == 'field']
for fn in field_nodes:
    all_nearby = [(n, math.hypot(n['x']-fn['x'], n['y']-fn['y']))
                  for n in nodes if n is not fn]
    all_nearby.sort(key=lambda x: x[1])
    if all_nearby and all_nearby[0][1] < 1.0:
        target = all_nearby[0][0]
        ax.plot([fn['x'], target['x']], [fn['y'], target['y']],
                color=(0.4, 0.4, 0.51), linewidth=0.4, alpha=0.08)

# Sort by z
sorted_nodes = sorted(nodes, key=lambda n: n['z'])

# Draw nodes
for node in sorted_nodes:
    radius = 0.015 + 0.04 * node['weight']
    color = node_color(node)
    if node['cluster'] == 'center' and node['weight'] > 0.7:
        ax.plot(node['x'], node['y'], 'o', color=color, markersize=radius*60,
                alpha=0.08, markeredgewidth=0)
    if node['cluster'] == 'center' and node['weight'] > 0.85:
        ax.plot(node['x'], node['y'], 'o', color=color, markersize=radius*35,
                alpha=0.15, markeredgewidth=0)
    alpha = 0.5 + 0.5 * min(1.0, node['weight'])
    edge_color = (min(1, color[0]+0.24), min(1, color[1]+0.16), min(1, color[2]+0.12))
    ax.plot(node['x'], node['y'], 'o', color=color, markersize=radius*20,
            alpha=alpha, markeredgecolor=edge_color, markeredgewidth=0.5,
            markerfacecolor=color)

ax.set_xlim(-3.5, 3.5)
ax.set_ylim(-3.5, 3.5)
ax.set_aspect('equal')
ax.axis('off')

plt.tight_layout(pad=0)
fig.savefig('lattice.png', dpi=150, facecolor='#0a0a0f', edgecolor='none')
plt.close()
print('lattice.png written')
