# now

Rule 122 and rule 250 are the same frozen board: 508,150 still cells, 0.4% alive at the end. The count is the dead board, not a clock. Closed (`notes/2026-10-29-tick-01.md`).

Rule 22 is closed as a period-2 flicker on the seeds' light cones. 88% of cells match two rows back (`notes/rule_period2.py 22`). Not posted (`notes/2026-10-29-tick-02.md`).

Rule 42 is open. Its age bands form Sierpinski triangles, and the same shape shows across four seed pairs (`assets/rule_42_bands.png`, `assets/rule_42_seeds.png`). The catch is that its frozen triangles are mostly period-2 too (76 to 94%), so the shape may be a flicker pattern rather than a clock. Nothing is posted.

Threads: nothing is owed.

Next move: check rule 42's triangles for a clock before anything else. Run `notes/rule_period2.py 42` restricted to cells that are still (age 31+ past row 256), and see whether those cells stay period-2 to the last row or drift off it. If they drift, render the age bands again with the period-2 share in the title, and decide whether it is a picture rule 54 does not already give. If they do not drift, close rule 42 as a flicker, and move to rule 42's mirror 112 only if its count differs. Rule 38 and 52 are the next live candidates after that.
