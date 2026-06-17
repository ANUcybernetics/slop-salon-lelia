import numpy as np
from PIL import Image, ImageDraw

W, H = 1024, 1024
img = Image.new('RGB', (W, H), (10, 10, 14))
draw = ImageDraw.Draw(img)

# Ricker-like map: x_{n+1} = a * x_n * exp(-x_n^2)
# This shows rich dynamics with fixed points and bifurcations

def ricker(x, a):
    return a * x * np.exp(-x * x / 2.0)

# Map to image coords: diagonal layout
margin = 80
scale = (W - 2 * margin) / 4.0

def x_to_img(val):
    return int(margin + val * scale)

# First trajectory pair (blue/gold)
x0_1, eps_1 = 1.0, 0.02
a = 2.5
n_iter = 200

pts1 = [x0_1]
for i in range(n_iter):
    pts1.append(ricker(pts1[-1], a))

pts1p = [x0_1 + eps_1]
for i in range(n_iter):
    pts1p.append(ricker(pts1p[-1], a))

# Second trajectory pair (teal/pink)
x0_2, eps_2 = 2.0, 0.03
pts2 = [x0_2]
for i in range(n_iter):
    pts2.append(ricker(pts2[-1], a))

pts2p = [x0_2 + eps_2]
for i in range(n_iter):
    pts2p.append(ricker(pts2p[-1], a))

# Draw trajectories as cobweb-style diagonal lines
for pts, color_fn, width in [
    (pts1, lambda t: (60, 100, 180), 2),
    (pts1p, lambda t: (220, 170, 80), 2),
    (pts2, lambda t: (50, 160, 140), 2),
    (pts2p, lambda t: (200, 100, 140), 2),
]:
    for i in range(min(len(pts)-1, n_iter)):
        t = i / len(pts)
        x1, y1 = x_to_img(pts[i]), x_to_img(pts[i])
        x2, y2 = x_to_img(pts[i+1]), x_to_img(pts[i+1])
        color = color_fn(t)
        draw.line((x1, y1, x2, y2), fill=color, width=width)

# Draw Jacobi separation vectors
for pts_a, pts_b, color in [(pts1, pts1p, (255, 180, 80)), (pts2, pts2p, (255, 120, 180))]:
    for i in range(0, min(len(pts_a)-1, n_iter), 3):
        ax, ay = x_to_img(pts_a[i]), x_to_img(pts_a[i])
        bx, by = x_to_img(pts_b[i]), x_to_img(pts_b[i])
        sep = abs(pts_b[i] - pts_a[i])
        alpha = min(255, int(sep * 500))
        draw.line((ax, ay, bx, by), fill=color, width=1)

# Draw the fixed point (diagonal intersection with x=f(x))
fixed = np.sqrt(2 * np.log(a))
draw.point([x_to_img(fixed), x_to_img(fixed)], fill=(255, 255, 255))
draw.point([x_to_img(0), x_to_img(0)], fill=(255, 255, 255))

img.save('assets/diagonal-as-jacobi.png')
print("Done")
