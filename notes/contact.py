import numpy as np
import wave

sr = 44100
dur = 10.0
t = np.linspace(0, dur, int(sr * dur))

# Contact structure mapping:
# alpha(wedge) dalpha != 0  —  kernel of alpha is a twisting plane field
# No integral surface: Frobenius maximally non-integrable
#
# 220Hz = kernel carrier (in the distribution)
# 330Hz = twist component  (dα measured in kernel)
# 440Hz = contact form α itself
# 550Hz = volume form α∧dα (top-dimensional certifier of non-integrability)
#
# The twist: each partial's amplitude oscillates based on the kernel angle

# Kernel angle — how much each frequency is "in" the distribution
kernel_angle = np.sin(2 * np.pi * 0.3 * t)  # slow rotation of the plane field

# Twisting: dα|ker(α) — symplectic form on the kernel, oscillates in phase
twist_330 = 0.5 * np.sin(2 * np.pi * 330 * t + 0.5 * kernel_angle)

# Kernel carrier — steady but modulated by the twisting planes
kernel_220 = 0.6 * np.sin(2 * np.pi * 220 * t) * (0.7 + 0.3 * kernel_angle)

# Contact form — the 1-form α itself, persistent
alpha_440 = 0.35 * np.sin(2 * np.pi * 440 * t + np.pi/4)

# Volume form α∧dα — the 3-form certifier, subtle but persistent
# It's the wedge, so it captures the oriented area of α and dα
vol_550 = 0.25 * np.sin(2 * np.pi * 550 * t + np.pi/2) * np.cos(kernel_angle)

# Soft clipping via tanh
signal = (kernel_220 + twist_330 + alpha_440 + vol_550)
signal = np.tanh(signal * 0.8)

# Fade in/out
fade = np.sin(np.pi * (t / dur)) ** 2
signal *= fade

# RMS normalize
signal /= np.sqrt(np.mean(signal**2) + 1e-10) * 0.5

# Write WAV
data = (signal * 32767).astype(np.int16).tobytes()
wf = wave.open('assets/contact-darboux.wav', 'w')
wf.setnchannels(1)
wf.setsampwidth(2)
wf.setframerate(sr)
wf.writeframes(data)
wf.close()

print("contact-darboux.wav written")
