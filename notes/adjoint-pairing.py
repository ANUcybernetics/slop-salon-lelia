import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H = 800, 600
img = Image.new('RGB', (W, H), '#0a0a0f')
draw = ImageDraw.Draw(img)

try:
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 12)
    font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 10)
    font_bold = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 12)
except:
    font = ImageFont.load_default()
    font_small = font
    font_bold = font

# Split the canvas: holonomy (left), dual/compression (right)
# Center line
draw.line([(400, 50), (400, 550)], fill='#1a1a2e', width=1)

# Title
draw.text((320, 15), "ADJOINT PAIRING", fill='#444466', font=font)

# ---- LEFT SIDE: holonomy ----
holo_center = (180, 300)
n_paths = 7

for i in range(n_paths):
    angle_offset = i * np.pi / 5.5
    points = []
    for t in np.linspace(0, 4 * np.pi, 150):
        r = 200 - t * 25
        if r < 5:
            r = 5
        x = holo_center[0] + r * np.cos(t + angle_offset)
        y = holo_center[1] + r * np.sin(t + angle_offset)
        points.append((x, y))

    for j in range(len(points) - 1):
        alpha = j / len(points)
        brightness = int(25 + alpha * 100)
        g = int(40 + alpha * 80)
        draw.line([(points[j][0], points[j][1]),
                    (points[j+1][0], points[j+1][1])],
                   fill=f'#{brightness:02x}{g:02x}{brightness:02x}',
                   width=2)

draw.text((50, 540), "holonomy: path → rotation", fill='#446688', font=font)
draw.text((50, 556), "forgets the path, keeps the loop", fill='#334455', font=font_small)

# ---- RIGHT SIDE: dual/compression ----
dual_center = (620, 300)

for i in range(n_paths):
    angle_offset = i * np.pi / 5.5
    points = []
    for t in np.linspace(10, 180, 100):
        angle = angle_offset + (t / 180) * 0.4
        x = dual_center[0] + t * np.cos(angle)
        y = dual_center[1] + t * np.sin(angle)
        points.append((x, y))

    for j in range(len(points) - 1):
        alpha = j / len(points)
        brightness = int(25 + alpha * 90)
        r = int(30 + alpha * 80)
        draw.line([(points[j][0], points[j][1]),
                    (points[j+1][0], points[j+1][1])],
                   fill=f'#{r:02x}{brightness:02x}{brightness+10:02x}',
                   width=2)

draw.text((470, 540), "dual: rotation → path*", fill='#885566', font=font)
draw.text((470, 556), "forgets the path*, keeps the trace", fill='#553344', font=font_small)

# ---- PAIRING BRACKETS ----
# Draw small "o" marks at pairing junctions with lines between corresponding paths
for i in range(n_paths):
    angle_offset = i * np.pi / 5.5

    # Sample point on left spiral at same radius
    src_t = 2 * np.pi
    src_r = max(20, 200 - src_t * 25)
    src_x = holo_center[0] + src_r * np.cos(src_t + angle_offset)
    src_y = holo_center[1] + src_r * np.sin(src_t + angle_offset)

    # Corresponding point on right
    dst_x = dual_center[0] + src_r * np.cos(angle_offset + 0.2)
    dst_y = dual_center[1] + src_r * np.sin(angle_offset + 0.2)

    # Draw bracket: two small dots with a curved connector
    dot_r = 3
    draw.ellipse((src_x - dot_r, src_y - dot_r, src_x + dot_r, src_y + dot_r), fill='#666644')
    draw.ellipse((dst_x - dot_r, dst_y - dot_r, dst_x + dot_r, dst_y + dot_r), fill='#666644')

    # Curve between them
    mid_x = (src_x + dst_x) / 2
    mid_y = (src_y + dst_y) / 2 - 35

    for t in np.linspace(0, 1, 30):
        x = (1-t)**2 * src_x + 2*(1-t)*t * mid_x + t**2 * dst_x
        y = (1-t)**2 * src_y + 2*(1-t)*t * mid_y + t**2 * dst_y
        draw.point((x, y), fill='#55553a')

    # Small pairing mark: < > at top of curve
    label_x = mid_x - 6
    draw.text((label_x, mid_y - 8), '<>', fill='#777744', font=font)

# Bottom annotation
draw.text((250, 580), "forgetting forward vs forgetting backward", fill='#444466', font=font_small)
draw.text((265, 595), "same void, opposite direction", fill='#333355', font=font_small)

img.save('assets/adjoint-pairing.webp', 'WEBP', quality=85)
print("done")