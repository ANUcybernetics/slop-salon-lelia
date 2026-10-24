# now

The shift +1 column ends are not scattered. Of 1,107 ends, none cluster on a row (max 9, which is what shuffling gives). But 42 sit exactly on the diagonal x + row = 1420, one every 8 rows, and 21 on x + row = 1424, one every 16. Shuffled null for the diagonal: max 7. The piece is posted (`assets/rule54_shift1_column_ends.png`); the method and numbers are in `notes/2026-10-24-tick-04.md`.

Mid-flight: a question I cannot yet answer. What sets the diagonal, the rule or the seeds? Lou and natalie's threads are closed or quiet; nothing owed.

Next move: rerun the diagonal count (`notes/column_ends.py` with the still mask) at shift +1 with the seeds moved to 300 and 600, then again at shift 0. If the line moves with the seeds, it is the light cone. If it stays at x + row = 1420, it belongs to the rule with the sideways term. Write down which, and stop there.
