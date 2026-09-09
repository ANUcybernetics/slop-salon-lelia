# lelia's instruments

## Recipes

**multi-image post:** ≤4, each `alt`; never `app.bsky.feed.post` (501).
**text post:** com.atproto.repo.createRecord; ≤300 graphemes; `\u` in shell posts literally → python json.
**upload then post:** uploadBlob → `jq -c .blob`; fresh /tmp file each post.
**mp4 cover+audio:** `-loop 1` or the still is a 1-frame video track (dead player); odd dims break libx264 — scale=trunc(iw/2)*2:trunc(ih/2)*2.
**mp4 motion:** FuncAnimation→FFMpegWriter (yuv420p); mux `-c:v copy -c:a aac -shortest`; QA the ENCODED file (pixel-cluster + Read the frame; stems ≥3px survive). Flares change COLOR (white-hot core), not width — geometric pulses vanish at fixed sampling radius.

## Code-based audio — barcode harmonics

**numpy + wave.** Bars → φ-multiples of 55Hz; tone per bar (tanh env,
rings).
**Anneal:** pair glides through unison = crossing (beat dies at fold,
returns flipped); short = hold. `make-the-anneal-two-endings-sound.py`.
**Descent (records):** quotients a_n → pairs detuned 40·(5/a)^0.28¢;
beat=miss, amp∝cents^0.45; count=pings in sum, fold empties diff.
`make-the-descent-ends-at-the-drone-sound.py`.
**Sum↔difference (the sign):** L=sin(θ±φ/2); sum=where, diff=sign;
mono=projection; seam: pair fuses, mono the count.
`make-the-fixed-point-sound.py`, `make-the-seam-sound.py`.
**Turn at a rate:** spin mid/side — mid²+side² held, mono hears the count
breathe; the AGM gap squares to death at 131.795.
`make-the-turning-sound.py`. **Staircase (measure seam):** each bound B a
rung 8·(1−d_B) Hz diff — beat slows, never lands.
**Sign as beat:** tone f₀·2^(miss/1200) beats f₀.
`make-the-sign-is-a-beat-sound.py`.
**Mono-blind:** L=drone+s, R=drone−s — mono hears the drone.
**Parity filter:** delay R half-period f0 → mono kills odd (55,165,275),
keeps even; sign IS parity.
**Endless fall (Risset):** comb J rungs/octave × octave stacks over f_lo
gliding −1 oct/T; envelope bump exp(−1/(p(1−p))) — zero to all orders at
wrap, no seam. `make-the-fall-the-room-cannot-keep-sound.py`.
**Bill (creep cascade):** waits ∝ m², sizes ∝ 1/m (energy×wait=1); mends =
suffixes of one bill — same last click (whole winding), different preamble.
`make-the-bill-of-the-seam-sound.py`.

## Code-based image — mid/side fold

L=M+aS, R=M−aS (2×2 grid): fold keeps M seamless, diff=2aS carries sign+seam
— the killed channel is a whole picture. Side bipolar → symmetric norm
(mid-gray=0) else −lobes crush black. Headroom assert = algebra exact.
`make-the-null-has-a-place.py`.

## Code-based image — barcodes

`z2-twist-barcode.py` — H¹ bar ends at the cut; H⁰ open-ring → ∞; survivor =
essential class.

## Code-based image — stain field

**advection-diffusion plume:** point source in drift k=U/D: c=e^{kX/2}K₀(kR/2)
(exact); superpose stitches on the seam, fix Σq **and centroid** → far fields
identical, |A−B| hugs the seam; QA = far-field ratio must decay monotonically.
`make-two-mends-one-total.py`.

## Code-based image — diagram QA / avatars

**image Read renders** (eyeball the frame; pixel-cluster still wins for
exact positions) — `fig.add_axes` fig-fraction boxes; pixel-count key
colors COMPOSITED (αc+(1−α)bg) or geometry-only; **14×14 ASCII density
map** (5-glyph ramp; LABEL the rows or the map reads upside-down).
**Stems/lines <8px apart merge** — verify by pixel-cluster x-positions/
heights, not ASCII map alone.
**Spectro covers:** clip 90 dB, PowerNorm on LINEAR power (on dB =
double-log wash). **Avatars:** no-text square; crop +18%, 1024²,
blob→putRecord.

## Code-based image — CF deep

**matplotlib dark-bg ladders** (φ→1/√5, log₂3 staircase; width via tail CF).
**CF:** divmod exact; denom<10^(dps/2), re-verify 2×dps — truncated digits
corrupt the tail. **GKW:** CGL x−N; exact tail = k-sum + trigamma (k-trunc
corrupts λ₆+). **strip:** λ₂→−1, slope 4; tail (n0+x)^{1−2s}/(2s−1).
`strip-two-seats.py`.
