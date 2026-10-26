import sys
from collections import Counter

import numpy as np

SEED = int(sys.argv[1]) if len(sys.argv) > 1 else 341
K_A = int(sys.argv[2]) if len(sys.argv) > 2 else 33
K_B = int(sys.argv[3]) if len(sys.argv) > 3 else 34
W, H, START, CEIL, RULE, SHIFT = 1024, 1024, 256, 254, 54, 1
TABLE = np.array([(RULE >> i) & 1 for i in range(8)], np.uint8)


def run():
    g = np.zeros((H, W), np.uint8)
    g[0, SEED] = 1
    age = np.zeros((H, W), np.int32)
    last = np.zeros(W, np.int32)
    zero = np.zeros(W, np.uint8)
    for t in range(1, H):
        p1 = g[t - 1]
        idx = (np.roll(p1, 1) << 2) | (p1 << 1) | np.roll(p1, -1)
        new = TABLE[idx] ^ (g[t - 2] if t >= 2 else zero) ^ np.roll(p1, SHIFT)
        g[t] = new
        last = np.where(new != p1, t, last)
        age[t] = t - last
    return age


def still(age, k):
    return (age >= k) & (age <= CEIL)


def ends(mask):
    rows, xs = np.nonzero(mask[START:])
    rows = rows + START
    out = set()
    for r, x in zip(rows, xs):
        if r < H - 1 and not mask[r + 1, x]:
            out.add((int(r), int(x)))
    return out


age = run()
ma, mb = still(age, K_A), still(age, K_B)
ma[:START] = False
mb[:START] = False
ea, eb = ends(ma), ends(mb)

print("still cells K%d %d, K%d %d" % (K_A, ma.sum(), K_B, mb.sum()))
print("ends K%d %d, K%d %d" % (K_A, len(ea), K_B, len(eb)))
print("cells leaving still set at K%d: %d, ages %s" % (K_B, (ma & ~mb).sum(), Counter(age[ma & ~mb].tolist()).most_common(5)))

vanished = ea - eb
appeared = eb - ea
print("ends vanished going K%d->K%d: %d; appeared: %d" % (K_A, K_B, len(vanished), len(appeared)))


def on_line(r, x, target=396):
    return (x + r) % W == target


for name, s in (("vanished", vanished), ("appeared", appeared)):
    if not s:
        continue
    ages = Counter(int(age[r, x]) for r, x in s)
    line = sum(on_line(r, x) for r, x in s)
    rowsc = Counter(r for r, _ in s).most_common(3)
    print("%s: ages %s; on x+row=396 mod 1024: %d of %d; top rows %s" % (name, ages.most_common(6), line, len(s), rowsc))

    for r, x in sorted(s)[:12]:
        print("   row %d x %d age %d x+row %d" % (r, x, age[r, x], x + r))
