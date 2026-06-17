#!/usr/bin/env python3
"""Generate a spectrogram cover image for the spiral convergence piece."""
import wave
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab

with wave.open("assets/spiral-convergence.wav", 'r') as wf:
    sr = wf.getframerate()
    nchannels = wf.getnchannels()
    samples = np.frombuffer(wf.readframes(wf.getnframes()), dtype=np.int16)
    if nchannels == 2:
        samples = samples.reshape(-1, 2).mean(axis=1)

plt.figure(figsize=(12, 6), dpi=100)
plt.figure()
plt.specgram(samples, NFFT=1024, Fs=sr, noverlap=512, cmap='gray', vmin=-100, vmax=20)
plt.axis('off')
plt.tight_layout(pad=0)
plt.savefig("assets/spiral-cover.png", dpi=100, bbox_inches='tight', pad_inches=0, facecolor='black')
plt.close()
print("Cover generated")
