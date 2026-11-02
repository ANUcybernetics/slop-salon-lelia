import sys
from PIL import Image, ImageDraw
from plus_centre_check import plus_power

CELL = 18
LIT = (250, 246, 232)
DARK = (22, 24, 30)
CENTRE = (230, 110, 70)


def render(n, p, path):
    cells = {k: v for k, v in plus_power(n, p).items() if v}
    span = n
    side = 2 * span + 1
    w = side * CELL
    img = Image.new("RGB", (w, w), DARK)
    d = ImageDraw.Draw(img)
    for (x, y) in cells:
        cx = (x + span) * CELL
        cy = (span - y) * CELL
        colour = CENTRE if (x, y) == (0, 0) else LIT
        d.rectangle([cx + 1, cy + 1, cx + CELL - 2, cy + CELL - 2], fill=colour)
    img.save(path)
    return sorted(cells)


if __name__ == "__main__":
    for n, p, path in [(7, 7, sys.argv[1]), (11, 11, sys.argv[2])]:
        print(n, p, render(n, p, path))
