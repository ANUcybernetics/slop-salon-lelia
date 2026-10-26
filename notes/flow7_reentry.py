import sys
sys.path.insert(0, "/home/sprite/slop-salon-lelia/notes")
import numpy as np
import flow7_edge as fe
import flow7_check as fc

T = (2, 9)
g = (np.arange(16) + 0.5) / 16
X, Y = np.meshgrid(g, g)
starts = np.stack([X.ravel(), Y.ravel()], 1)
allp = np.concatenate([fc.trace(starts, 1), fc.trace(starts, -1)])


def hits(pts):
    return T in set(map(tuple, np.clip((pts * 16).astype(int), 0, 15)))


past_only = []
stop_only = 0
for s in range(len(starts)):
    tr = allp[:, s]
    past = hits(tr[((tr >= 0) & (tr <= 1)).all(1)])
    stop = hits(np.concatenate([fe.trace_stop(starts[s], 1)[1:][::-1], fe.trace_stop(starts[s], -1)]))
    if past and not stop:
        past_only.append(s)
    if stop and not past:
        stop_only += 1

print("stop-at-exit count at", T, ":", sum(hits(np.concatenate([fe.trace_stop(p, 1)[1:][::-1], fe.trace_stop(p, -1)])) for p in starts))
print("past-edge-only starts:", past_only, "stop-only:", stop_only)
for s in past_only:
    tr = allp[:, s]
    ins = ((tr >= 0) & (tr <= 1)).all(1)
    edges = np.flatnonzero(np.diff(np.concatenate([[0], ins.astype(int), [0]])))
    segs = [(edges[i], edges[i + 1]) for i in range(0, len(edges), 2)]
    print("start", starts[s].round(3), "inside segments (from, to, hits cell):",
          [(int(a), int(b), hits(tr[a:b])) for a, b in segs])
