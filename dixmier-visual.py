import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as mpatches

fig, ax = plt.subplots(1, 1, figsize=(8, 8), facecolor='#0a0a0f')
ax.set_facecolor('#0a0a0f')

# Three surfaces converging on the same integer
# 1. Winding (clutching) — spiral
# 2. Divergence (resolvent) — approaching a line
# 3. Residue — slow remnant

theta = np.linspace(0, 8*np.pi, 500)

# Winding spiral
r1 = theta / (8 * np.pi) * 3.5
x1 = r1 * np.cos(theta)
y1 = r1 * np.sin(theta)

# Resolvent divergent approach
t = np.linspace(0.1, 8, 500)
# Approaching spectrum at t = 4, never reaching
dist = 0.5 + 2 * np.exp(-(t - 4)**2 / 2)
r2 = 1.0 / dist
x2 = np.cos(t) * r2
y2 = np.sin(t) * r2

# Residue remnant
t3 = np.linspace(0, 8, 500)
residue = np.exp(-t3 / 3) * np.sin(3 * t3) * 3.5
x3 = residue * np.cos(t3 / 2)
y3 = residue * np.sin(t3 / 2)

# Plot all three
ax.plot(x1, y1, '#ff8844', lw=1.5, alpha=0.7, label='clutching')
ax.plot(x2, y2, '#4488ff', lw=1.5, alpha=0.7, label='resolvent')
ax.plot(x3, y3, '#44ff88', lw=1.5, alpha=0.7, label='residue')

# The integer: convergence point at center
ax.plot(0, 0, 'w*', markersize=20, alpha=0.8)

# Labels
ax.text(0, -4.5, '3 names for the same refusal', ha='center',
        color='white', fontsize=11, fontweight='bold', alpha=0.6)
ax.text(0, -5.2, 'what the bundle refuses to be,\nmeasured by what it refuses to stop being',
        ha='center', color='white', fontsize=8, alpha=0.4)

ax.set_xlim(-5, 5)
ax.set_ylim(-5.5, 5)
ax.set_aspect('equal')
ax.axis('off')

plt.tight_layout()
plt.savefig('./assets/dixmier-channels.png', dpi=150, facecolor='#0a0a0f',
            edgecolor='none', bbox_inches='tight')
plt.close()
print("Written dixmier-channels.png")
