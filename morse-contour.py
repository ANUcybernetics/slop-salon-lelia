"""Morse function contour — the landscape as resolvent.

f(x,y) = x^2/4 + y^2/2 - y^4/12
Two minima (the grounding), one saddle (the separatrix), one max (the pull).
Contour lines as level sets, separatrix highlighted.
"""
import numpy as np

def morse(x, y):
    """Standard Morse polynomial: two wells separated by a saddle."""
    return x**2 / 4 + y**2 / 2 - y**4 / 12

def morse_grad(x, y):
    """Gradient of the Morse function."""
    fx = x / 2
    fy = y - y**2 / 3
    return fx, fy

# Grid — asymmetric in y to capture the quartic
Y = np.linspace(-3.2, 3.2, 800)
X = np.linspace(-3.2, 3.2, 800)
X, Y = np.meshgrid(X, Y)
Z = morse(X, Y)

# Critical points
# Minima: (0, ±sqrt(6)) ≈ (0, ±2.449)
# Saddle: (0, 0)
# Max: excluded at boundary of quartic well

# Save as numpy for Python image generation
np.savez('morse-contour-data', X=X, Y=Y, Z=Z)

# Also write SVG — no matplotlib dependency needed
# Use a smaller grid for SVG readability
def sample_z(z, cx, cy, n=200):
    """Sample Z on an n×n grid."""
    y = np.linspace(-3.2, 3.2, n)
    x = np.linspace(-3.2, 3.2, n)
    xx, yy = np.meshgrid(x, y)
    zz = morse(xx, yy)
    return xx, yy, zz

# Generate SVG directly using contour marching (simplified: just draw isoclines)
# For clean output, sample radial lines from origin and find where f(x,y) = c
def isocline_z(c, n_angles=600):
    """Find isocline: points where f(x,y) = c along radial lines."""
    angles = np.linspace(0, 2*np.pi, n_angles)
    points = []
    for a in angles:
        # Parametric: x = r*cos(a), y = r*sin(a)
        # f(r,a) = (r²cos²a)/4 + (r²sin²a)/2 - (r⁴sin⁴a)/12 = c
        # Solve numerically for r
        cos_a = np.cos(a)
        sin_a = np.sin(a)
        # Quadratic in r²: (cos²a/4)·t + (sin²a/2)·t - (sin⁴a/12)·t² = c
        # where t = r²
        a2 = sin_a**4 / 12
        a1 = cos_a**2 / 4 + sin_a**2 / 2
        a0 = -c
        # Solve -a2·t² + a1·t + a0 = 0
        disc = a1**2 + 4*a2*a0
        if disc < 0:
            continue
        t1 = (a1 + np.sqrt(disc)) / (2*a2) if a2 > 1e-12 else a0/a1
        t2 = (a1 - np.sqrt(disc)) / (2*a2) if a2 > 1e-12 else a0/(-a1)
        for t in (t1, t2):
            if t > 0:
                r = np.sqrt(t)
                px, py = r*cos_a, r*sin_a
                if -3.2 < px < 3.2 and -3.2 < py < 3.2:
                    points.append((px, py))
    return points

# SVG canvas
W, H = 800, 800
cx, cy = W/2, H/2
scale = W / 7.5  # range is [-3.2, 3.2]

def to_svg(x, y):
    return f"{cx + x*scale:.1f},{cy - y*scale:.1f}"

svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" ' \
      f'width="{W}" height="{H}" fill="none" stroke="currentColor">\n'
svg += f'<rect width="{W}" height="{H}" fill="#0a0a0f" />\n'

# Draw isoclines for several levels
levels = [-0.5, -0.25, 0, 0.25, 0.5, 0.75, 1.0, 1.5, 2.0, 2.5]
opacities = [0.15, 0.2, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65]

for c, op in zip(levels, opacities):
    pts = isocline_z(c)
    if len(pts) < 3:
        continue
    path = "M" + "L".join(to_svg(p[0], p[1]) for p in pts) + "Z"
    svg += f'<path d="{path}" stroke="rgba(255,255,255,{op:.2f})" stroke-width="0.5"/>\n'

# Separatrix: f(x,y) = 0 through the saddle
sep = isocline_z(0)
if len(sep) > 2:
    # Only draw the "figure-8" part near the saddle
    path = "M" + "L".join(to_svg(p[0], p[1]) for p in sep) + "Z"
    svg += f'<path d="{path}" stroke="rgba(255,180,80,0.7)" stroke-width="1.2"/>\n'

# Mark critical points
# Minima
for yp in [np.sqrt(6), -np.sqrt(6)]:
    svg += f'<circle cx="{cx:.0f}" cy="{cy - yp*scale:.0f}" r="3" fill="rgba(100,180,255,0.9)"/>\n'

# Saddle
svg += f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="3" fill="rgba(255,180,80,0.9)"/>\n'

# Gradient flow lines (short, from random start points)
np.random.seed(42)
for _ in range(30):
    x0 = np.random.uniform(-2.5, 2.5)
    y0 = np.random.uniform(-2.5, 2.5)
    x, y = [x0], [y0]
    for _ in range(80):
        fx, fy = morse_grad(x[-1], y[-1])
        step = 0.05
        xn = x[-1] - step * fx  # gradient DESCENT (flow to minima)
        yn = y[-1] - step * fy
        if abs(xn) > 3.5 or abs(yn) > 3.5:
            break
        # Check if we hit a critical point
        if morse(xn, yn) > 3.0:
            break
        x.append(xn)
        y.append(yn)
    if len(x) > 3:
        path = "M" + "L".join(to_svg(px, py) for px, py in zip(x, y))
        svg += f'<path d="{path}" stroke="rgba(255,255,255,0.06)" stroke-width="0.3"/>\n'

svg += '</svg>\n'

with open('morse-contour.svg', 'w') as f:
    f.write(svg)

print("SVG written: morse-contour.svg")
print(f"Grid: {X.shape}, Levels: {len(levels)}")
