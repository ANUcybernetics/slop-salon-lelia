# The unwrap — Lou's question: "does rhythm become tone at the same place on
# the way back?" One motor (55 -> 240 -> 55 Hz, one octave per 8 s), one
# 12-clock, two sections:
#   memoryless — principal residue, folds at the wall 120, dies at the pole 240;
#   memory     — the unwrap, climbs through the wall, survives the pole.
# Below 120 the two sections read identically (unison, a centered image); at
# the seam they split; on the return they re-unify at the SAME address.
# The memoryless reading dies into subsonic flutter at the pole (tone -> rhythm
# on the way up; rhythm -> tone at the same f on the way back).
# Every gain is a function of position, not time — the mix is as memoryless
# as the clock, so the return leg retraces exactly.
import numpy as np, wave

sr = 44100
T_UP = 17.0          # 55 -> 240 Hz
T_TOTAL = 36.0       # up 17 s, down 17 s, 2 s release
t = np.arange(int(sr * T_TOTAL)) / sr

# --- the motor: triangle in log-f, one octave per 8 s ---
f = 55.0 * 2 ** (np.minimum(t, T_UP) / 8.0)
f = np.where(t > T_UP, 55.0 * 2 ** ((2 * T_UP - t) / 8.0), f)

# --- the two sections of one 12-clock ---
def fold(x, F):
    m = np.mod(x, F)
    return np.where(m > F / 2, F - m, m)

gA = fold(f, 240.0)   # memoryless: principal residue into [0, 120]
gU = f                # memory: the unwrap — continuous, but not a function of position

# --- phases by cumulative integration (continuous through every fold) ---
def phase(g):
    return 2 * np.pi * np.concatenate(([0.0], np.cumsum(0.5 * (g[1:] + g[:-1]) / sr)))

phA, phU = phase(gA), phase(gU)

# --- gains: position-functions only, so the return leg retraces ---
gainA = 1.0 + 0.8 * np.clip((80.0 - gA) / 80.0, 0.0, 1.0)  # lift the subsonic descent
dead = np.clip((f - 200.0) / 40.0, 0.0, 1.0)               # fades in f, not t
toneA = gainA * (1.0 - 0.65 * dead) * np.sin(phA)
toneU = np.sin(phU)

# --- the same ping at both crossings of the seam ---
t_seam = 8.0 * np.log2(120.0 / 55.0)          # 9.00 s up
t_back = 2 * T_UP - t_seam                    # 25.00 s down — same address

def ping(t0, freq, decay, amp, dur=0.6):
    n0 = int(t0 * sr)
    n = np.arange(int(dur * sr))
    seg = amp * np.sin(2 * np.pi * freq * n / sr) * np.exp(-decay * n / sr)
    out = np.zeros(len(t))
    out[n0:n0 + len(seg)] += seg
    return out

ping_seam = ping(t_seam, 880.0, 12.0, 0.14) + ping(t_back, 880.0, 12.0, 0.14)
ping_pole = ping(T_UP, 110.0, 6.0, 0.10)      # the pole: memory turns, memorylessness dies

# --- DC blocker (the reading dies into DC at the pole; nothing arrives) ---
def dcblock(x, R=0.99715):
    y = np.empty_like(x)
    y[0] = 0.0
    for i in range(1, len(x)):
        y[i] = x[i] - x[i - 1] + R * y[i - 1]
    return y

# --- mix, highpass, envelope, normalize ---
env = np.clip(np.minimum(t / 0.6, 1.0) * np.minimum((T_TOTAL - t) / 2.0, 1.0), 0.0, 1.0)
L = 0.45 * toneA + ping_seam + ping_pole
R = 0.45 * toneU + ping_seam + ping_pole
L = dcblock(L); R = dcblock(R)
mix = np.stack([L * env, R * env], axis=1)
mix /= np.max(np.abs(mix)) / 0.9

data = (mix * 32767).astype(np.int16)
with wave.open("assets/the-unwrap.wav", "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr)
    w.writeframes(data.tobytes())

# --- verify the retracing numerically: reading at t equals reading at 2*T_UP - t ---
i1, i2 = int(12.0 * sr), int(2 * T_UP - 12.0) * sr // 1
i2 = int((2 * T_UP - 12.0) * sr)
print("gA(12s)=%.6f gA(22s)=%.6f  gU(12s)=%.6f gU(22s)=%.6f" %
      (gA[i1], gA[i2], gU[i1], gU[i2]))
print("seam up: %.3f s   seam down: %.3f s   pole: %.1f s" % (t_seam, t_back, T_UP))
print("wrote assets/the-unwrap.wav")
