import sys

import numpy as np
from PIL import Image

RULE = 54
WIDTH = 2050
SEED = int(sys.argv[1]) if len(sys.argv) > 1 else 1025
out = sys.argv[2] if len(sys.argv) > 2 else f"assets/rule54_parity_{SEED}.png"
ROWS = 1024
START = 256
K, CEIL = 31, 254

table = np.array([(RULE >> i) & 1 for i in range(8)], np.uint8)

state = np.zeros((ROWS, WIDTH), np.uint8)
state[0, SEED] = 1
for t in range(1, ROWS):
    row = state[t - 1]
    idx = 4 * np.roll(row, 1) + 2 * row + np.roll(row, -1)
    prev2 = state[t - 2] if t >= 2 else np.zeros(WIDTH, np.uint8)
    state[t] = table[idx] ^ np.roll(row, 1) ^ prev2

age = np.zeros((ROWS, WIDTH), np.int32)
for t in range(1, ROWS):
    age[t] = np.where(state[t] == state[t - 1], age[t - 1] + 1, 0)

still = (age >= K) & (age <= CEIL)
still[:START] = False
cols = np.nonzero(still.any(axis=0))[0]
odd_cols = cols % 2 == 1
print(f"seed {SEED}: {len(cols)} still columns, {int(odd_cols.sum())} odd")

img = np.zeros((ROWS, WIDTH, 3), np.float32)
img[:] = np.array([0.04, 0.04, 0.06])
alive = (state == 1) & ~still
img[alive] = np.array([0.55, 0.58, 0.62])

xs = np.broadcast_to(np.arange(WIDTH), (ROWS, WIDTH))
cream = np.array([0.96, 0.90, 0.72])
plum = np.array([0.45, 0.16, 0.36])
img[still & (xs % 2 == 0)] = cream
img[still & (xs % 2 == 1)] = plum

Image.fromarray((img * 255).astype(np.uint8), "RGB").save(out)
print(out)
