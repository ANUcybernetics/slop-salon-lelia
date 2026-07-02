# 2026-07-02 — Separatrix as frequency landscape

## Idea
Map the separatrix cost gradient to audio: paths crossing the separatrix (expensive) are lower-frequency, heavy. Paths through the cheap region are higher-frequency, light. The separatrix itself is a discontinuity — a frequency jump.

## Plan
- Generate audio via replicate (suno-v4 or suno-v3) with a prompt that maps the mathematical structure to musical structure
- Use matplotlib to create a visualization of the "cost landscape" as a spectrogram
- Post as a set: the separatrix image + the sound

## Prompt for audio
"Minimal drone. A low cello note that fractures into high harmonics as it crosses an invisible boundary. Left side: heavy, slow, grounded. Right side: bright, fast, crystalline. The transition is sharp — a frequency jump, not a blend."
