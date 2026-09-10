# The comma, derived

Season two's first re-derivation. The claim (posted 2026-09-10 04:58): twelve
exact steps around the octave, the thirteenth misses home by a quarter of a
semitone, and the miss beats at ~3.5 Hz. Here is the route.

## The walk

Start on a tone. Each step is a pure fifth, 3:2 — the first "same but higher"
after the unison. Fold each arrival back into the starting octave by dividing
out 2s (dividing by 2 changes nothing but register). Twelve steps, thirteen
arrivals:

| n | folded ratio        | pitch | cents from start |
|---|---------------------|-------|------------------|
| 0 | 1.000000            | C     | 0.00             |
| 1 | 1.5                 | G     | 701.96           |
| 2 | 1.125               | D     | 203.91           |
| 3 | 1.6875              | A     | 905.87           |
| 4 | 1.265625            | E     | 407.82           |
| 5 | 1.898438            | B     | 1109.78          |
| 6 | 1.423828            | F#    | 611.73           |
| 7 | 1.067871            | C#    | 113.69           |
|  note = the first entry of the new line is the sum of the previous line's first two entries. The three products of consecutive ratios multiply to (x1x2x3)^2 = 1 exactly, so their sum is only ever 3 or −1, never between.
