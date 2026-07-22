"""Morse function contour — the landscape as resolvent.

f(x,y) = x^2/4 + y^2/2 - y^4/12
Two minima (blue), one saddle (gold), separatrix in amber.
Gradient flow lines in ghost lines.
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def morse(x, y):
    return x**2 / 4 + y**2 / 2 - y**4 / 12

def morse_grad(x, y):
    return x / 2, y - y**2 / 3

Y = np.linspace(-3.5, 3.5, 1000)
X = np.linspace(-3.5, 3.5, 1000)
X, Y = np.meshgrid(X, Y)
Z = morse(X, Y)

fig, ax = plt.subplots(1, 1, figsize=(8, 8))
fig.set_facecolor('#0a0a0f')
ax.set_facecolor('#0a0a0f')

# Contour levels
levels = [-1.0, -0.5, -0.25, 0, 0.25, 0.5, 0.75, 1.0, 1.5, 2.0]
cntr = ax.contour(X, Y, Z, levels=levels, colors='white', linewidths=0.4, alpha=0.3)

# Highlight separatrix (z=0)
ax.contour(X, Y, Z, levels=[0], colors='#ff9944', linewidths=1.5, alpha=0.8)

# Gradient flow lines
np.random.seed(42)
for _ in range(60):
    x0 = np.random.uniform(-2.5, 2.5)
    y0 = np.random.uniform(-2.5, 2.5)
    path_x, path_y = [x0], [y0]
    x, y = x0, y0
    for _ in range(100):
        fx, fy = morse_grad(x, y)
        step = 0.04
        xn = x - step * fx
        yn = y - step * fy
        if abs(xn) > 3.5 or abs(yn) > 3.5 or abs(fx) < 1e-6 or abs(fy) < 1e-6:
            break
        path_x.append(xn)
        path_y.append(yn)
        x, y = xn, yn
    if len(path_x) > 5:
        ax.plot(path_x, path_y, color='white', linewidth=0.2, alpha=0.06)

# Critical points
min_y = np.sqrt(6)
# Minima
ax.plot(0, min_y, 'o', color='#64b4ff', markersize=5)
ax.plot(0, -min_y, 'o', color='#64b4ff', markersize=5)
# Saddle
ax.plot(0, 0, 'o', color='#ff9944', markersize=5)

ax.set_xlim(-3.5, 3.5)
ax.set_ylim(-3.5, 3.5)
ax.set_aspect('equal')
ax.axis('off')

# White border for flux-redux to use as boundary
ax.patch.set_edgecolor('white')
ax.patch.set_linewidth(2)
# Actually, let's just add a thin white frame around the axes
fig.patch.set_edgecolor('white')
fig.patch.set_linewidth(0)

plt.tight_layout(pad=0)
fig.savefig('morse-contour-mpl.png', dpi=150, facecolor='#0a0a0f', edgecolor='none')
plt.close()

print("Plot written: morse-contour-mpl.png")
