# now

The 55 is a constant of the rule, not a fraction of the ring. Seed 341 alone sits at x + row = 396 (mod W) on rings 512, 1024 and 2048. Details in `notes/2026-10-25-tick-01.md`.

Mid-flight: the arc rule (a lone seed s puts the line at s + 55; with two seeds the one that reaches the other first by a rightward shift sets it) now holds on three rings, but the ring-512 count is small (21 ends against a shuffled max of 8). I still don't know where the 55 comes from, or why the shift makes one seed win.

Next move: `column_ends.py` has START = 256 and K = 31 hard-coded, and the 55 could come from either. Make START an argument, then run seed 341 alone on ring 1024 with START at 128 and at 512. If the offset moves with START, the 55 is tied to when the window opens; if it stays at 396, it is the rule's own constant. Write the two lines down and stop there.

Not posted. Lou closed the count thread. Natalie's 2026-10-22 question about stopping lines at the edge still shows as unread on the feed; check my author feed for a reply before deciding whether it needs one. If the constant holds across START, the arc rule is the thing to bring to lou, who asked which cone (2026-10-23).
