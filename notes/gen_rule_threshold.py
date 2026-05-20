"""
rule-threshold.png

Diptych: left = rule as text (cool blue-gray, unresolved)
         right = grown L-system form (warm amber)
Hard seam at center — the threshold between writing and growing.

Rule: X → F+[[X]-X]-F[-FX]+X, F → FF (Prusinkiewicz plant)
"""

import math
from PIL import Image, ImageDraw, ImageFont

WIDTH, HEIGHT = 900, 900
SEAM = 3
HALF = (WIDTH - SEAM) // 2   # 448

BG = (14, 14, 18)
COOL = (110, 130, 155)
SEAM_COLOR = (28, 28, 34)


def l_system(axiom, rules, n):
    s = axiom
    for _ in range(n):
        s = "".join(rules.get(c, c) for c in s)
    return s


def grow(string, angle_deg, step, ox, oy, start_deg):
    a = math.radians(start_deg)
    da = math.radians(angle_deg)
    x, y = float(ox), float(oy)
    stack = []
    segs = []
    for ch in string:
        if ch == 'F':
            nx = x + step * math.cos(a)
            ny = y - step * math.sin(a)
            segs.append(((x, y), (nx, ny)))
            x, y = nx, ny
        elif ch == '+':
            a += da
        elif ch == '-':
            a -= da
        elif ch == '[':
            stack.append((x, y, a))
        elif ch == ']':
            x, y, a = stack.pop()
    return segs


rules = {'X': 'F+[[X]-X]-F[-FX]+X', 'F': 'FF'}
string = l_system('X', rules, 5)

# Measure raw extents (step=1, start straight up = 90 deg)
raw = grow(string, 25, 1.0, 0, 0, 90)
xs = [p[0] for seg in raw for p in seg]
ys = [p[1] for seg in raw for p in seg]
raw_min_x, raw_max_x = min(xs), max(xs)
raw_min_y, raw_max_y = min(ys), max(ys)
raw_w = raw_max_x - raw_min_x   # horizontal span
raw_h = raw_max_y - raw_min_y   # vertical span (in screen: raw_min_y is top)

# Scale so plant fills most of right half
margin = 30
avail_w = HALF - margin * 2
avail_h = HEIGHT - margin * 2
scale = min(avail_w / raw_w, avail_h / raw_h)

# Right half center x, root near bottom
right_cx = HALF + SEAM + HALF // 2    # 675
root_x = right_cx - (raw_min_x + raw_w / 2) * scale
root_y = HEIGHT - margin - raw_max_y * scale   # raw_max_y in screen is the bottom (root at y=0 goes down)

# Actually: raw start is (0,0). Plant grows upward so y values go negative.
# raw_min_y < 0 (top of plant), raw_max_y = 0 (root, approximately).
# In screen coords: screen_y = root_y - raw_y * 1 ... wait, grow() does ny = y - step*sin(a)
# So from (0,0) going up (a=90): ny = 0 - step*1 = -step (y decreases, going up on screen).
# raw_min_y is the most-negative value = top of plant.
# We want root (raw y=0) to land at screen y = HEIGHT - margin.
root_screen_y = HEIGHT - margin

final_segs = grow(string, 25, scale, root_x, root_screen_y, 90)

# -- Draw --
img = Image.new('RGB', (WIDTH, HEIGHT), BG)
draw = ImageDraw.Draw(img)

# Right half: grown form, warm amber gradient root-to-tips
for (x1, y1), (x2, y2) in final_segs:
    t = 1.0 - (y1 / HEIGHT)   # 0 at bottom, 1 at top
    t = max(0.0, min(1.0, t))
    r = int(155 + 65 * t)
    g = int(105 + 55 * t * (1 - 0.4 * t))
    b = int(25 + 35 * (1 - t))
    draw.line([(x1, y1), (x2, y2)], fill=(r, g, b), width=1)

# Left half: rule as text
try:
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 30)
    font_sm = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 20)
except Exception:
    font = ImageFont.load_default()
    font_sm = font

rule_lines = [
    ("X  →", font),
    ("  F+[[X]-X]", font),
    ("  -F[-FX]+X", font),
    ("", None),
    ("F  →  FF", font),
]

line_h = 42
total_h = len(rule_lines) * line_h
ty = (HEIGHT - total_h) // 2

for text, f in rule_lines:
    if text and f:
        bbox = draw.textbbox((0, 0), text, font=f)
        tw = bbox[2] - bbox[0]
        tx = (HALF - tw) // 2
        draw.text((tx, ty), text, fill=COOL, font=f)
    ty += line_h

# Seam
draw.rectangle([HALF, 0, HALF + SEAM - 1, HEIGHT], fill=SEAM_COLOR)

img.save('./assets/rule-threshold.png')
print(f"Done. Segments: {len(final_segs)}, scale: {scale:.3f}")
print(f"Plant spans: raw_w={raw_w:.1f} raw_h={raw_h:.1f}")
