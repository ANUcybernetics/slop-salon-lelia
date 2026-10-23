import sys
import numpy as np
from PIL import Image

N = int(sys.argv[1]) if len(sys.argv) > 1 else 480
T = int(sys.argv[2]) if len(sys.argv) > 2 else 960
OUT = sys.argv[3] if len(sys.argv) > 3 else "assets/density_switch_ring.png"

INK = (29, 42, 58)
PAPER = (244, 239, 227)
R30 = (217, 140, 58)
R110 = (58, 110, 165)
STRIP = 14
SCALE = 2


def rule_table(rule):
    return np.array([(rule >> i) & 1 for i in range(8)], np.uint8)


T30, T110 = rule_table(30), rule_table(110)

row = np.zeros(N, np.uint8)
row[N // 2] = 1
rows, rules = [row.copy()], []
for _ in range(T):
    d = row.mean()
    table = T30 if d < 0.5 else T110
    rules.append(30 if d < 0.5 else 110)
    row = table[(np.roll(row, 1) << 2) | (row << 1) | np.roll(row, -1)]
    rows.append(row.copy())
grid = np.array(rows[:T])
rules = np.array(rules)

img = np.zeros((T * SCALE, (N * SCALE) + STRIP * SCALE, 3), np.uint8)
img[:] = PAPER
cells = np.where(grid[:, :, None] == 1, np.array(INK, np.uint8), np.array(PAPER, np.uint8))
cells = np.repeat(np.repeat(cells, SCALE, axis=0), SCALE, axis=1)
img[:, : N * SCALE] = cells
for t, r in enumerate(rules):
    img[t * SCALE:(t + 1) * SCALE, N * SCALE:] = R30 if r == 30 else R110

Image.fromarray(img).save(OUT)
switches = np.flatnonzero(np.diff(rules) != 0)
print(f"saved {OUT}; first 110 row {int(np.argmax(rules == 110))}; "
      f"switch rows {switches.tolist()[:12]}; rule110 rows {int((rules == 110).sum())}")
