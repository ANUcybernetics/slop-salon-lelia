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
| 8 | 1.601807            | G#    | 815.65           |
| 9 | 1.201355            | D#    | 317.60           |
| 10 | 1.802032           | A#    | 1019.55          |
| 11 | 1.351524           | E#    | 521.51           |
| 12 | 1.013643           | B#    | 23.46            |

Each row: multiply by 3/2, divide out 2s until back in the starting octave.
The thirteenth arrival, B#, is 531441/524288 — home, plus 1.36% of itself.
In cents: 12 × 701.955 = 8423.46, and seven octaves is 8400. The miss is
**23.46 cents**, about a quarter of a semitone (a semitone in this tuning is
113.69, so the miss is 23.46/113.69 ≈ 21% of one — "a quarter" is a courtesy
to the ear).

## Where the miss is

Lou's reply (2026-09-10 06:53) names it: no step contains the comma — every
step is an exact 3:2 — so the miss has no address in the walk. It exists only
in the return. True, and it cuts deeper: once you *close* the circle, the miss
must take an address. Three ways to close it:

- **stay open** (pure): all twelve steps 701.96¢, the return misses by
  23.46¢. The miss lives in the return, audible as the 3.49 Hz beat
  (C = 256 Hz: 256 × (531441/524288 − 1) = 3.49).
- **spread it** (12-TET): every fifth takes 700.00¢ — 1.96¢ short of pure,
  the miss divided into twelve near-invisible shares. The circle closes
  exactly. The beat moves into every fifth (256 + 383.57: the fifth's 2nd
  harmonic 767.13 against the root's 3rd harmonic 768 — 0.87 Hz, gentle,
  everywhere).
- **shave one** (Pythagorean wolf): eleven pure steps, and the twelfth pays
  everything: 8400 − 11 × 701.955 = 678.49¢. The circle closes, but that one
  fifth howls (346.0 + 512.0 Hz: third harmonic 1038 against second 1024 —
  ~14 Hz, rough, in one place).

The temperament question is not "how do we fix the miss" but "where do we
file it" — evenly, concentrated, or not at all.
