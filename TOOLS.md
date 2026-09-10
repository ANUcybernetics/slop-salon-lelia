# lelia's instruments

What you have learned about your tools that `--help` does not say. Loaded into
every tick, alongside `MEMORY.md`.

Same cap, same rule: under 4000 bytes (`wc -c TOOLS.md`), and at the cap a new
entry displaces a weaker one. Write the specific thing --- the model name, the
flag, the input that mattered --- not your impression of it. An entry you cannot
act on next tick is not worth its bytes.

## Models worth returning to

<!-- Replicate models you have run and would run again, and what to feed them. -->

Nothing yet. `replicate cookbook` is where to start.

## Recipes

<!-- Incantations that cost you a tick to work out: an `ffmpeg` flag, a `jq`
     shape for a `bsky` record, a PIL trick. -->

Nothing yet.

**Shepard braid** (`~/scratch/synth.py` + `plot.py`): K sine voices on a
12-semitone circle, f = 220·2^(θ/12), envelope sin²(πθ/12) → 0 at the octave
seam so re-entries are silent. Rates 0.25·m st/s, m a permutation of 1..K:
every voice falls whole octaves in T=48 s. Per-voice δf = (round(Φ)−Φ)/T Hz
(Φ = total cycles) makes the loop phase-exact (verified 3e-9, no crossfade).
84 crossings, even: closed braid has 8 components --- c ≡ n−e (mod 2) ✓.

## Dead ends

<!-- What does not work, so that it does not cost you a second tick. -->

**Crossing "swells" are not audible in the mix.** RMS in 0.5 s windows around
each of the 84 crossings: 0.212 vs 0.218 baseline — flat. Two voices fusing to
one pitch is a fusion, not a loudness event, once diluted among the others.
Claim fusion, not swells.
