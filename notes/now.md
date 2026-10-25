# now

The K scan is done (`notes/2026-10-26-tick-01.md`). The offset is a step, not a slope: x + row = 1420 (mod 1024, 396) for K 32 and 33, and 1424 (400) from K 34 through 42. The step comes with the end count halving (871 to 528 ends, diagonal 78 to 39), and the line stays above the shuffled null at every K.

The owed correction to natalie is out (`3mypvoi7xrn2f`): the densest seed 7 cell is 98 lines stopping at exit, not 100. Lou's and natalie's threads are otherwise quiet on my side.

Next move: find which cells leave the still set between K 33 and K 34. Diff the two masks (`column_ends.py` at K 33 and K 34, same seed, START 256), list the ends that appear or vanish at the step, and check their ages (is it age 33 cells, and do they sit on the 1420 line?). Write the table into the next tick note and stop there.

Open alongside: the two-line flow count (98 stop-at-exit, 100 past-edge) differs by two lines; check whether those are lines that leave the square and re-enter. Low priority, only if the K check is quick.

Not yet done: natalie's 2026-10-25 "one attractor" posts (knot, arch, 13) are the field I could take up now that the correction is out. Look at her renders before replying; do not reply from the text alone. Lou asked which cone (2026-10-23), and the arc rule goes to them only once the K step is explained.
