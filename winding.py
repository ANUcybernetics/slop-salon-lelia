import numpy as np
import wave

SR = 44100
DUR = 8.0
t = np.linspace(0, DUR, int(SR * DUR), endpoint=False)

# Carrier drone (steady A)
carrier_freq = 220.0
carrier = np.tanh(0.3 * np.sin(2 * np.pi * carrier_freq * t))

# Winding bands: harmonic ratios with distinct winding numbers
# Each band carries a phase jump at a specific time — the clutching deciding
bands = [
    (0.5,  1, 0.8),   # half-freq, winding=1, early jump
    (0.75, 2, 2.5),   # 3/2 ratio, winding=2, mid jump
    (1.0,  3, 5.0),   # same as carrier, winding=3, late jump
    (1.5,  5, 6.8),   # 3rd harmonic, winding=5, near end
]

output = carrier.copy()

for ratio, wind, jtime in bands:
    freq = carrier_freq * ratio
    phase = 2 * np.pi * freq * t
    # Shaped jump: smooth step centered on jtime
    width = 0.06
    jump_shape = 0.5 * (1 + np.tanh((t - jtime) / width))
    extra_phase = 2 * np.pi * wind * jump_shape
    signal = np.tanh(0.12 * np.sin(phase + extra_phase))
    # Fade in/out to avoid clicks
    envelope = np.ones_like(t)
    fade = np.linspace(0, 1, int(SR * 0.15))
    envelope[:len(fade)] = fade
    envelope[-len(fade):] = fade[::-1]
    signal *= envelope
    output += signal

# Master soft clip
output = np.tanh(0.25 * output)

# Peak normalize to prevent clipping
peak = np.max(np.abs(output))
if peak > 0:
    output = output / peak * 0.9

wf = wave.open('./assets/winding-clutch.wav', 'wb')
wf.setnchannels(1)
wf.setsampwidth(2)
wf.setframerate(SR)
samples = np.int16(output * 32767)
wf.writeframes(samples.tobytes())
wf.close()

print("wrote ./assets/winding-clutch.wav")
