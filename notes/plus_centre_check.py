import sys
from collections import defaultdict

def plus_power(n, p):
    # P = centre + four neighbours, coefficients mod p, as dict (dx, dy) -> coeff
    cur = {(0, 0): 1}
    stamp = [(0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)]
    for _ in range(n):
        nxt = defaultdict(int)
        for (x, y), c in cur.items():
            for dx, dy in stamp:
                nxt[(x + dx, y + dy)] = (nxt[(x + dx, y + dy)] + c) % p
        cur = nxt
    return cur

def centre(n, p):
    return plus_power(n, p).get((0, 0), 0)

if __name__ == "__main__":
    checks = [(3, 7), (6, 7), (6, 5), (6, 11), (7, 5), (3, 5), (2, 5), (5, 5), (7, 7), (11, 11)]
    for n, p in checks:
        c = centre(n, p)
        print(f"step {n}, mod {p}: centre coefficient {c} ({'lit' if c else 'dark'})")
