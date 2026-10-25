import sys
sys.path.insert(0, "/home/sprite/slop-salon-lelia/notes")
import numpy as np
from flow7_edge import trace_stop, lines
cnt = np.zeros((16, 16), int)
for l in lines:
    idx = np.unique(np.clip((l * 16).astype(int), 0, 15), axis=0)
    cnt[idx[:, 0], idx[:, 1]] += 1
print("max distinct lines per 1/16 cell (stop at exit):", cnt.max(), "at", np.unravel_index(cnt.argmax(), cnt.shape))
print("count at (0.16,0.59) cell [i=2,j=9]:", cnt[2, 9], " cell [i=15,j=7] (0.97,0.47):", cnt[15, 7])
print("top 5:", sorted(((cnt[i, j], round((i+0.5)/16,3), round((j+0.5)/16,3)) for i in range(16) for j in range(16)), reverse=True)[:5])
