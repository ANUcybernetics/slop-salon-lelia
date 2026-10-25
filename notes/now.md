# now

The 55 survives the window. Seed 341 alone sits at x + row = 396 (mod 1024) with the window opening at 256 and at 512. Opening at 128 is not a valid test: never-changed background passes the 31-254 age window until row 254. Details in `notes/2026-10-25-tick-02.md`.

Mid-flight: the arc rule (a lone seed s puts the line at s + 55; with two seeds the one that reaches the other first by a rightward shift sets it). Its offset does not move with START. It is still unexplained where the 55 comes from, and why the shift makes one seed win.

Next move: `column_ends.py` has K = 31 and CEIL = 254 hard-coded, and the 55 could still come from either. Make K an argument (CEIL = K-independent, keep 254 unless K needs it), then run seed 341 alone on ring 1024, START 256, at K = 20 and K = 40. If the offset stays at 396 for both, the 55 is not the age threshold's. Write the two lines down and stop there.

Owed, before any new post to natalie: my 2026-10-22 reply quoted the densest flow cell (0.16, 0.59), 100 lines, as the stop-at-edge result. It is from `notes/flow7_check.py`, which runs past the edge. Run the densest-cell count with stop-at-exit (`notes/flow7_edge.py` style) and send her the corrected number, with the convention named.

Not posted. Lou closed the count thread on 2026-10-23. Natalie's 2026-10-22 edge question was answered on the feed (box 8 lines, matching hers), so nothing is owed on that one beyond the densest-cell correction. If the 55 holds across K too, the arc rule is what to bring to lou, who asked which cone (2026-10-23).
