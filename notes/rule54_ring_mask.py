import sys
import numpy as np

RULE = 54
WIDTH = int(sys.argv[1]) if len(sys.argv) > 1 else 2050
SEED = int(sys.argv[2]) if len(sys.argv) > 2 else 1025
ROWS = 1024
START = 256
K = 31
CEIL = 254

table = np.array([(RULE >> i) & 1 for i in range(8)], dtype=np.uint8)

state = np.zeros((ROWS, WIDTH), dtype=np.uint8)
state[0, SEED] = 1
prev2 = np.zeros(WIDTH, dtype=np.uint8)
for t in range(1, ROWS):
    row = state[t - 1]
    l = np.roll(row, 1)
    r = np.roll(row, -1)
    idx = 4 * l + 2 * row + r
    nxt = table[idx] ^ np.roll(row, 1) ^ (state[t - 2] if t >= 2 else prev2)
    state[t] = nxt

age = np.zeros((ROWS, WIDTH), dtype=np.int32)
for t in range(1, ROWS):
    same = state[t] == state[t - 1]
    age[t] = np.where(same, age[t - 1] + 1, 0)

window = age[START:ROWS]
masked = ((window >= K) & (window <= CEIL)).any(axis=0)
unmasked = (window >= K).any(axis=0)
cols_masked = np.nonzero(masked)[0]
cols_unmasked = np.nonzero(unmasked)[0]
odd = lambda cols: int((cols % 2 == 1).sum())
print(f"width {WIDTH} seed {SEED}")
print(f"masked (age {K}-{CEIL}): {len(cols_masked)} columns, {odd(cols_masked)} odd")
print(f"unmasked (age >= {K}):   {len(cols_unmasked)} columns, {odd(cols_unmasked)} odd")
extra = np.setdiff1d(cols_unmasked, cols_masked)
print(f"unmasked only: {len(extra)} columns; max age there {int(window[:, extra].max()) if len(extra) else 0}")
constant = (state[START:, extra] == state[START, extra]).all(axis=0)
print(f"unmasked only, constant over rows {START}-{ROWS - 1}: {int(constant.sum())} of {len(extra)}")
