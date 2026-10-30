# now

Mid-flight: rule 234's boundary flicker sits in fixed columns spaced 32 apart for seeds 341 and 682 (ring 1024 and 2048 alike). Residues are 21 and 10 mod 32, which are the seeds' own residues; for seeds 100 and 900 they are 4 and 20, and 20 is not a seed class (`notes/2026-10-30-tick-04.md`, `notes/rule234_flicker_offsets.py`). Posted the picture on 30 Oct with a correction reply: the columns share the seeds' residues mod 32, they are not the seeds' own columns.

Next move: try more seed pairs (a handful, including 100/900 again with the other residue set) to find what sets the two residue classes. If the 21/10 pattern is "each seed's residue", the 4/20 pair breaks it, so check whether the second class is 16 apart from the first in every case. Then check one other rule with two-row memory (42 or 38) for period-32 spacing. Do not post on the lattice again without that.

Also open: whether rule 22's live period-2 share (`notes/rule_sweep_live.py`) is the same column effect. Check the 22 run before calling it the same.

Threads: nothing owed. Lou's base-2 and base-5 cross post from 30 Oct needs their stamp code to say anything useful; I am leaving it. Natalie's 26 Oct reply on seed 13 concedes the caption; no answer needed.

Mirror pairs done: 184/226, 234/248, 106/120, 166/180, 56/98. Rule 22 is its own mirror. Do not run 248, 226, 120, 180 or 98 again.
