import numpy as np
from PIL import Image, ImageDraw

w, h = 1200, 1200
img = Image.new('RGB', (w, h), (10, 10, 30))
draw = ImageDraw.Draw(img)

# Dark navy background
bg = (12, 12, 35)
draw.rectangle([0, 0, w, h], fill=bg)

# Contact distribution visualization:
# A plane field that twists everywhere — kernel of α
# α ∧ dα ≠ 0  — no integral surface exists

# Draw the plane field as a grid of small twisted ellipses
# Each ellipse represents the contact plane at that point
cx, cy = w // 2, h // 2

# Hexagonal grid of contact planes
import math

size = 30
spacing = 60
for row in range(-10, 11):
    for col in range(-10, 11):
        x = col * spacing + (row % 2) * spacing // 2
        y = row * spacing * 0.866
        dx, dy = x - cx, y - cy
        dist = math.sqrt(dx**2 + dy**2)
        if dist > 400:
            continue

        # Twist angle: the contact plane rotates with position
        angle = math.atan2(dy, dx) + 0.3 * (dist / 400)

        # The plane is a line segment (kernel = 1D in 2D)
        a1, a2 = math.cos(angle), math.sin(angle)

        # Length decreases with distance (stronger twist at edges)
        strength = max(0, 1 - dist / 400)
        half_len = size * strength

        # Draw as bright line
        color = int(255 * strength)
        brightness = min(255, color)
        r, g, b = brightness, int(brightness * 0.6), int(brightness * 0.8)

        x1 = x - a1 * half_len
        y1 = y - a2 * half_len
        x2 = x + a1 * half_len
        y2 = y + a2 * half_len

        draw.line([(x1, y1), (x2, y2)], fill=(r, g, b), width=2)

# Draw "no integral surface" — attempted curves that fail to stay tangent
# These are the "almost-contact" curves that get pushed away by the twist
from PIL import ImageFont

for i in range(3):
    angle0 = i * 2 * math.pi / 3
    points = [(cx, cy)]
    a = angle0
    px, py = cx, cy
    for step in range(100):
        dt = 0.15
        # The contact plane rotates faster than the curve
        plane_angle = a + 0.3 * step * dt
        # Curve tries to follow but drifts
        a += (plane_angle - a + 0.3) * dt
        dx = math.cos(a) * dt * 5
        dy = math.sin(a) * dt * 5
        px += dx
        py += dy
        points.append((px, py))

    color = [255, 180, 120] if i == 0 else [120, 200, 255] if i == 1 else [180, 100, 255]
    for j in range(len(points) - 1):
        alpha = 1 - j / len(points)
        c = tuple(int(c * alpha) for c in color)
        draw.line([points[j], points[j+1]], fill=c, width=3)

# Title
try:
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 28)
except:
    font = ImageFont.load_default()

draw.text((40, 40), "α ∧ dα ≠ 0", fill=(200, 200, 255), font=font)
draw.text((40, 75), "Darboux — every contact structure is locally standard", fill=(120, 140, 200), font=font)

img.save('assets/contact-darboux.png')
print("contact-darboux.png written")
