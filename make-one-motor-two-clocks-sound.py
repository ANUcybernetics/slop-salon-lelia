# One motor, two clocks — the aliasing register's sound.
# One continuous glide (the motor), read by two clocks (12-fold and 20-fold
# spoke symmetry, mapped 1 spoke = 20 Hz: walls at 120 and 200 Hz).
# Each clock hears the principal residue: fold(f mod F) into [0, F/2].
# The two readings are in unison until the first wall; at the wall the beat
# between them dies and they separate. When the motor reaches the 12-clock's
# clock rate (240 Hz), its reading is exactly zero — perfect aliasing,
# nothing arrives. The 20-clock ends still reading.
import numpy as np, wave

sr = 44100
T_MOTOR = 17.0        # motor runs 55 -> 240 Hz
T_TOTAL = 21.0        # tail: readings hold, then release
t = np.arange(int(sr * T_TOTAL)) / sr

# --- the motor: one glide, 55 -> 240 Hz, one octave per 8 s ---
f = 55.0 * 2 ** (np.minimum(t, T_MOTOR) / 8.0)

# --- principal residue = fold into [0, F/2] ---
def fold(f, F):
    m = np.mod(f, F)
    return np.where(m > F / 2, F - m, m)

gA = fold(f, 240.0)   # 12-clock, wall 120
gB = fold(f, 400.0)   # 20-clock, wall 200

# --- phases by cumulative integration (smooth through each fold) ---
def phase(g):
    ph = 2 * np.pi * np.concatenate(([0.0], np.cumsum(0.5 * (g[1:] + g[:-1]) / sr)))
    return ph

phA, phB = phase(gA), phase(gB)

# --- gains: lift the subsonic descent so the collapse reads as flutter ---
gainA = 1.0 + 0.8 * np.clip((80.0 - gA) / 80.0, 0.0, 1.0)
toneA = gainA * np.sin(phA)
toneB = np.sin(phB)

# --- the clocks as rhythms: 12 and 20 pulses per second, same ping pitch ---
def tickenv(r):
    return np.exp(-45.0 * np.mod(t * r, 1.0))

ping = np.sin(2 * np.pi * 880.0 * t)
tkA = tickenv(12.0) * ping
tkB = tickenv(20.0) * ping

# --- seam accents: the beat dies where the readings cross at the wall ---
t_seamA = 8.0 * np.log2(120.0 / 55.0)   # ~9.00 s
t_seamB = 8.0 * np.log2(200.0 / 55.0)   # ~14.90 s
for t_s, env in ((t_seamA, tkA), (t_seamB, tkB)):
    mask = 3.0 * np.exp(-((t - t_s) / 0.15) ** 2)
    env[:] *= (1.0 + mask)

# --- the 12-clock's reading dies at f = 240: fade its tone into the pole ---
dead = np.clip((t - (T_MOTOR - 1.2)) / 1.2, 0.0, 1.0)
toneA *= (1.0 - 0.65 * dead)

# --- fades, mix, normalize ---
env = np.clip(np.minimum(t / 0.6, 1.0) * np.minimum((T_TOTAL - t) / 2.5, 1.0), 0.0, 1.0)
L = 0.42 * toneA + 0.10 * tkA
R = 0.42 * toneB + 0.10 * tkB
mix = np.stack([L * env, R * env], axis=1)
mix /= np.max(np.abs(mix)) / 0.9

# --- write wav, then ffmpeg to mp3 outside ---
data = (mix * 32767).astype(np.int16)
with wave.open("assets/one-motor-two-clocks.wav", "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr)
    w.writeframes(data.tobytes())
print("wrote assets/one-motor-two-clocks.wav")
print("seams:", round(float(t_seamA), 2), round(float(t_seamB), 2))
print("gA end:", float(gA[-1]), "gB end:", float(gB[-1]))
