#!/usr/bin/env python3
"""Rule 110 spacetime diagram with cocycle structure.

Local rule fails to extend globally → cohomology class.
Gliders are cocycles (not coboundaries): they carry information without closing.

Four-panel: truth table → coboundary operator → spacetime with gliders marked →
cocycle/non-cocycle overlay showing where the rule fails.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# --- Rule 110 ---
# Binary: 111→0, 110→1, 101→1, 100→0, 011→1, 010→1, 001→1, 000→0
RULE = 0b01101110  # 110

def rule110(cell_left, cell_center, cell_right):
    """Evaluate Rule 110 for a single step."""
    pattern = (cell_left << 2) | (cell_center << 1) | cell_right
    return (RULE >> pattern) & 1

# --- Step 1: Truth table visualization ---
fig, axes = plt.subplots(1, 4, figsize=(16, 3.5))

# Truth table
ax = axes[0]
ax.set_title("Truth table", fontsize=12, fontweight='bold', pad=10)
ax.set_xlim(0, 1)
ax.set_ylim(0, 8)
ax.axis('off')
for i in range(8):
    bits = f'{i:03b}'
    pattern_out = rule110(int(bits[0]), int(bits[1]), int(bits[2]))
    color = '#4a90d9' if pattern_out == 1 else '#2a2a3a'
    ax.add_patch(plt.Rectangle((0.15, 7.3 - i*0.85), 0.35, 0.6,
                                facecolor=color, edgecolor='#555', linewidth=0.5))
    ax.text(0.05, 7.5 - i*0.85, bits, fontsize=9, color='#ccc', fontfamily='monospace')
    ax.text(0.6, 7.5 - i*0.85, f'→ {pattern_out}', fontsize=9, color='#aaa', fontfamily='monospace')

# --- Step 2: Coboundary operator on 3-cell neighborhood ---
ax = axes[1]
ax.set_title("δ on C¹ (3-cell neighborhood)", fontsize=12, fontweight='bold', pad=10)
ax.set_xlim(0, 10)
ax.set_ylim(0, 8)
ax.axis('off')
# Draw three-cell neighborhood
for i, (label, x) in enumerate([('c_{i-1}', 2), ('c_i', 5), ('c_{i+1}', 8)]):
    ax.add_patch(plt.Circle((x, 6), 0.5, facecolor='#4a90d9', edgecolor='#fff', linewidth=1.5))
    ax.text(x, 6, '●', fontsize=20, ha='center', va='center', color='white')
    ax.text(x, 4.2, label, fontsize=10, ha='center', color='#ddd', fontfamily='monospace')
# Coboundary arrow
ax.annotate('', xy=(9, 6), xytext=(3, 6),
            arrowprops=dict(arrowstyle='->', lw=2, color='#e8a040'))
ax.text(6, 6.8, 'δ', fontsize=14, color='#e8a040', fontweight='bold')
ax.text(6, 5.8, 'local rule', fontsize=8, color='#c08030')
ax.text(5, 2.5, 'δ(c)_{i} = c_{i-1} ⊕ c_{i+1}', fontsize=9, color='#bbb',
        ha='center', fontfamily='monospace',
        bbox=dict(boxstyle='round', facecolor='#1a1a2a', edgecolor='#444'))
ax.text(5, 1.2, 'glider ≠ exact cocycle', fontsize=9, color='#e8a040',
        ha='center', fontstyle='italic')

# --- Step 3: Spacetime diagram from glider seed ---
ax = axes[2]
ax.set_title("Spacetime from glider seed", fontsize=12, fontweight='bold', pad=10)

WIDTH = 200
HEIGHT = 120
grid = np.zeros((HEIGHT, WIDTH), dtype=int)

# Glider seed: 00101110 pattern that produces moving gliders
seed = [0,0,1,0,1,1,1,0]
start_x = WIDTH // 2 - 4
for i, b in enumerate(seed):
    grid[0, start_x + i] = b

for t in range(1, HEIGHT):
    for x in range(1, WIDTH - 1):
        grid[t, x] = rule110(grid[t-1, x-1], grid[t-1, x], grid[t-1, x+1])

# Mark glider cells (isolated running patterns)
glider_mask = np.zeros_like(grid, dtype=float)
for t in range(1, HEIGHT):
    for x in range(1, WIDTH - 1):
        if grid[t, x] == 1:
            # Check if this is part of a glider (running pattern)
            neighbors_3 = grid[t-1, x-1:x+2]
            if np.any(neighbors_3) and not np.all(neighbors_3):
                glider_mask[t, x] = 1.0

im = ax.imshow(grid.T, aspect='auto', cmap='Blues', interpolation='nearest',
               extent=[0, HEIGHT, WIDTH-0.5, -0.5], vmin=-0.1, vmax=1.1,
               origin='lower', alpha=0.9)
glider_im = ax.imshow(glider_mask.T, aspect='auto', cmap='RdYlBu_r', interpolation='nearest',
                      extent=[0, HEIGHT, WIDTH-0.5, -0.5],
                      origin='lower', alpha=0.4)
ax.set_xlabel('Time →', fontsize=10, color='#888')
ax.set_ylabel('Space →', fontsize=10, color='#888')
ax.tick_params(colors='#666', labelsize=8)

# --- Step 4: Cocycle overlay ---
ax = axes[3]
ax.set_title("Cocycle: where rule fails to extend", fontsize=12, fontweight='bold', pad=10)

# Compute cocycle: at each position, check if local pattern
# can be extended globally. If the neighborhood violates any
# consistency condition, mark as cocycle.
cocycle = np.zeros((HEIGHT, WIDTH), dtype=float)
for t in range(1, HEIGHT-1):
    for x in range(1, WIDTH-1):
        # The cocycle condition: check if the 8 possible
        # 3-cell patterns are consistent with Rule 110 globally
        neighborhood = grid[t:t+3, x-1:x+2]
        if neighborhood.shape == (3, 3):
            # Check consistency: does the center column match
            # Rule 110 applied to neighbors?
            predicted = np.array([[rule110(neighborhood[r,0], neighborhood[r,1], neighborhood[r,2])
                                   for r in range(3)]])
            actual = neighborhood[:, 1:2].T
            if not np.array_equal(predicted, actual):
                cocycle[t, x] = 1.0

im2 = ax.imshow(grid.T, aspect='auto', cmap='Blues', interpolation='nearest',
                extent=[0, HEIGHT, WIDTH-0.5, -0.5], vmin=-0.1, vmax=1.1,
                origin='lower', alpha=0.7)
cocycle_im = ax.imshow(cocycle.T, aspect='auto', cmap='Reds', interpolation='nearest',
                       extent=[0, HEIGHT, WIDTH-0.5, -0.5],
                       origin='lower', alpha=0.35)
ax.set_xlabel('Time →', fontsize=10, color='#888')
ax.set_ylabel('Space →', fontsize=10, color='#888')
ax.tick_params(colors='#666', labelsize=8)

plt.suptitle('Rule 110: glider = cocycle not coboundary', fontsize=14, fontweight='bold',
             y=0.98, color='#e8e8e8')
plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.savefig('rule110-cocycle.png', dpi=150, bbox_inches='tight',
            facecolor='#0a0a14', edgecolor='none')
plt.close()

# Count cocycle cells
total_cocycle = int(cocycle.sum())
total_cells = HEIGHT * WIDTH
print(f"Spacetime: {HEIGHT}×{WIDTH}, {total_cocycle} cocycle cells ({100*total_cocycle/total_cells:.2f}%)")
print(f"Rule 110 cocycle diagram saved to rule110-cocycle.png")
