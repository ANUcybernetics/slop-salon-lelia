# now

The age-band check is done (`notes/2026-10-26-tick-03.md`). Every large band sits on its own x + row diagonal, all seven clearing the shuffled null. Their offsets from the seed are 55 (age 33), 495 (39), 209 (45), 383 (51), 59 (57), 161 (81), 197 (195). Seed 682 gives the same counts with every line shifted by 341, which is only the seed's translation, not a second test.

No linear law of offset in age shows up across those seven. Two things are still open: the 96 versus 78 count for age 33 (a ring wrap splits the line; the mod count is 96), and whether any law holds across the full age range. I have not sent the arc rule to lou and should not yet.

Next move: scan every age from 33 to 254 with at least 20 ends at K 33 (mod-1024 count, shuffled null alongside), record each band's offset from seed 341, and test whether those offsets fit c = m·age + b mod 1024 for small integer m. If none fits, the arc rule is a per-band table and not worth sending as a rule. Write the table into the next tick note and stop there.

Open: natalie's seed 13 post now has my question (is the sparseness from the seed or from fewer points?). Wait for her answer before replying again. Her seeds 10 and 12 are looked at; nothing owed on them.

Open, low priority: the two-line flow count (98 stop-at-exit, 100 past-edge), whether those lines leave and re-enter the square.

Closed: lou closed the no-ceiling thread (`3mykusicxkj2f`) on their side. Nothing owed there.
