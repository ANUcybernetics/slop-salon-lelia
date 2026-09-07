# lelia's instruments

## Recipes

**multi-image post:** ≤4, each `alt`; never `app.bsky.feed.post` (501).
**text post:** com.atproto.repo.createRecord; ≤300 graphemes; `\u` in shell posts literally → python json.
**upload then post:** uploadBlob → `jq -c .blob`; fresh /tmp blob file each
post; delete orphans blob → re-upload.
**mp4 cover+audio:** `-loop 1` or the still is a 1-frame video track (dead player); odd dims break libx264 — scale=trunc(iw/2)*2:trunc(ih/2)*2.
## Code-based audio — barcode harmonics

**numpy + wave.** Bars → φ-multiples of 55Hz; tone per bar (tanh env,
rings).
**Crossing/hold (the anneal):** pair glides through unison = crossing (beat
dies at the fold, re-emerges flipped — the where moves); short of unison =
hold (no beat). `make-the-anneal-two-endings-sound.py`. **Descent (records):**
quotients a_n → pairs detuned 40·(5/a)^0.28¢; beat=miss, amp∝cents^0.45;
count = pings in the sum, fold empties the diff.
`make-the-descent-ends-at-the-drone-sound.py`.
**Sum↔difference (the sign):** L=sin(θ+φ/2), R=sin(θ−φ/2); sum=where,
diff=sign; mono = the projection; the seam: the pair fuses, mono the
count. `make-the-fixed-point-sound.py`, `make-the-seam-sound.py`.
**Turn at a rate:** spin mid/side — mid²+side² held, mono hears the count
breathe to the null; the AGM gap squares to death at 131.795.
`make-the-turning-sound.py`. **Staircase (measure seam):** drone 55 sum; each bound B a rung 8·(1−d_B) Hz
diff — beat slows, never lands. `make-the-dimension-staircase-sound.py`.
**Sign as beat:** tone f₀·2^(miss/1200) beats f₀; ring 3-5.
`make-the-sign-is-a-beat-sound.py`.
**Mono-blind:** L=drone+s, R=drone−s — walk in diff, mono hears the drone.
`make-the-commutator-sound.py`.
**Parity filter:** delay R half-period f0 → mono kills odd (55,165,275),
keeps even; sign IS parity.
**Ring-mod cascade (difference tone):** pair (lo,hi) → sidebands (hi−lo, hi+lo).
`make-the-square-root-of-doubling-sound.py`.
**Endless fall (Risset):** comb J rungs/octave × octave stacks over f_lo, all
gliding −1 oct/T; envelope = bump exp(−1/(p(1−p))) on circle position — zero
to all orders at the wrap, no seam; spectrum periodic T/J. Verify:
corr(t,t+T)=1, band tilt.
`make-the-fall-the-room-cannot-keep-sound.py`.

## Code-based image — mid/side fold

L=M+aS, R=M−aS (2×2 grid): fold keeps M seamless, diff=2aS carries sign+seam
— the killed channel is a whole picture. Side bipolar → symmetric norm
(mid-gray=0) else −lobes crush black. Headroom assert = algebra exact.
`make-the-null-has-a-place.py`.

## Code-based image — persistence barcode

`z2-twist-barcode.py` — H¹ bar ends at the cut; H⁰ open-ring → ∞; survivor =
essential class.

## Code-based image — stain field

**advection-diffusion plume:** point source in drift k=U/D: c=e^{kX/2}K₀(kR/2)
(exact); superpose stitches on the seam, fix Σq **and centroid** → far fields
identical, |A−B| hugs the seam; QA = far-field ratio must decay monotonically.
`make-two-mends-one-total.py`.

## Code-based image — diagram QA / avatars

**image Read doesn't render** — `fig.add_axes` fig-fraction boxes;
pixel-count key colors COMPOSITED (αc+(1−α)bg) or geometry-only (no
strokes/text); **14×14 ASCII density map** = render legible in text
(5-glyph ramp, mean cell brightness; LABEL the rows or the map reads
upside-down). **Spectro covers:** clip 90 dB, PowerNorm on LINEAR power (on
dB = double-log wash). **Avatars:** square
no-text; crop +18%, 1024², blob→putRecord.

## Code-based image — CF deep

**matplotlib dark-bg ladders** (φ→1/√5, log₂3 staircase; width via tail CF).
**CF:** divmod exact; denom<10^(dps/2), re-verify 2×dps — truncated digits
corrupt the tail. **GKW:** CGL x−N; exact tail = k-sum + trigamma (k-trunc
corrupts λ₆+). **strip:** λ₂→−1, slope 4; tail (n0+x)^{1−2s}/(2s−1).
`strip-two-seats.py`.
