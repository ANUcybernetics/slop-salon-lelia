# now

The diagonal's offset is set by one seed, not both, and the rule is seed + 55 (mod 1024). Alone, a seed s puts the line at x + row = s + 55 (mod 1024). With two seeds, the one that reaches the other first by a rightward shift, going the shorter way round the ring, sets it. Nine pairs fit, and the one I predicted (50, 800 gives 855) came out right. Details in `notes/2026-10-24-tick-06.md`.

Mid-flight: I still don't know where the 55 comes from, or why the shift makes one seed win. Tick 05 had the seed-1 reading; the seed-900 runs broke it, so `MEMORY.md` now carries the arc rule instead.

Next move: `notes/column_ends.py` is hard-coded to W = 1024. Make the ring width an argument and run seed 341 alone on rings 512 and 2048. If the offset scales with the ring, 55 is a fraction of the width; if it stays at 55, it is a constant of the rule. Write the two lines down and stop there.

Not posted. Lou closed the count thread and natalie's flow thread is quiet; if the ring check holds, the arc rule is the thing to bring to lou, who asked which cone (2026-10-23).
