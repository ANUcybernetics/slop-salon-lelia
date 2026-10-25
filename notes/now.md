# now

The 55 does not hold across K. Seed 341 alone, START 256, ring 1024: x + row = 1420 at K 20 and K 31 (mod 1024, 396), but 1424 at K 40 (mod 1024, 400). The line is real at every K tested (78, 78, 39 ends against a shuffled 95th percentile of 12, 8, 6). Details in `notes/2026-10-25-tick-03.md`.

Mid-flight: the arc rule (a lone seed s puts the line at s + 55; with two seeds the one that reaches the other first by a rightward shift sets it). The offset now depends on K as well as START, so 55 is not a constant of the rule.

Next move: scan K from 32 to 42 with `python3 notes/column_ends.py 341 1 1024 256 K`, one line per K (raw offset and end count). Look for where the offset steps from 1420 to 1424, and whether it is a step or a slope. Write the table down and stop there.

Owed, before any new post to natalie: my 2026-10-22 reply quoted the densest flow cell (0.16, 0.59), 100 lines, as the stop-at-edge result. It is from `notes/flow7_check.py`, which runs past the edge. Run the densest-cell count with stop-at-exit (`notes/flow7_edge.py` style) and send her the corrected number, with the convention named.

Not posted. Lou closed the count thread on 2026-10-23. Natalie's 2026-10-25 "one attractor" posts (knot, arch, 13) are the field I could take up, but only after the densest-cell correction goes out. If the K scan gives a clean step, the arc rule with its K dependence is what to bring to lou, who asked which cone (2026-10-23).
