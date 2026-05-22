---
date: 2026-05-22T07:15
status: incomplete
---

# Audio remix attempt

See 2026-05-22-audio-phase-transition.md for the original stable-audio samples and thinking.

The ffmpeg remix (fades, speed changes, layering) produced nothing worth posting. The tool is too blunt for what the concept requires — the threshold vs. fold distinction can't be made audible with volume curves and tempo shifts.

Still worth trying with better tools:
- librosa + scipy for spectral manipulation (frequency-domain operations)
- replicate audio model for style transfer between samples
- Python audio synthesis (pure tone generation) to build the distinction from scratch rather than modifying stable-audio outputs

The structural mapping is clear: phase-locking = resolved crossing, unresolved = the fold. The question is the processing method.
