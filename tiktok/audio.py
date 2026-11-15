"""Bande son générée : musique douce + « voix » façon Animal Crossing + effets."""
import numpy as np, wave, random

SR = 44100
VOICE = {"L": (880, "sine"), "G": (200, "tri"), "NEO": (620, "square"), "B": (480, "sine"), "R": (760, "tri"),
         "P": (1050, "square"), "BR": (170, "tri"), "C": (640, "sine"), "H": (300, "sine")}


def osc(freq, dur, kind="sine", vib=0.0):
    t = np.arange(int(SR * dur)) / SR
    f = freq * (1 + vib * np.sin(2 * np.pi * 6 * t))
    ph = 2 * np.pi * np.cumsum(f) / SR
    if kind == "square":
        return np.sign(np.sin(ph)) * 0.5
    if kind == "tri":
        return 2 / np.pi * np.arcsin(np.sin(ph))
    return np.sin(ph)


def env(n, a=0.005, r=0.03):
    e = np.ones(n)
    na, nr = int(a * SR), int(r * SR)
    e[:na] = np.linspace(0, 1, na)
    if nr:
        e[-nr:] *= np.linspace(1, 0, nr)
    return e


def add(buf, sig, t):
    i = int(t * SR)
    j = min(len(buf), i + len(sig))
    if i < len(buf):
        buf[i:j] += sig[:j - i]


def music(total, mood):
    buf = np.zeros(int(SR * total) + SR)
    bpm = 78 if mood != "nuit" else 66
    beat = 60 / bpm
    if mood in ("nuit",):
        prog = [[57, 60, 64], [53, 57, 60], [48, 52, 55], [55, 59, 62]]  # Am F C G
    else:
        prog = [[48, 52, 55], [57, 60, 64], [53, 57, 60], [55, 59, 62]]  # C Am F G
    mf = lambda m: 440 * 2 ** ((m - 69) / 12)
    t, k = 0.0, 0
    while t < total:
        ch = prog[k % 4]
        bar = beat * 4
        pad = sum(osc(mf(n), bar, "sine") for n in ch) / 3
        e = np.minimum(1, np.linspace(0, 6, len(pad))) * np.minimum(1, np.linspace(6, 0, len(pad)))
        add(buf, pad * e * 0.05, t)
        add(buf, osc(mf(ch[0] - 12), bar, "sine") * np.exp(-np.linspace(0, 3, int(SR * bar))) * 0.06, t)
        for i in range(8):
            n = ch[[0, 1, 2, 1, 2, 0, 1, 2][i]] + 12
            d = beat / 2
            add(buf, osc(mf(n), 0.6, "sine") * np.exp(-np.linspace(0, 7, int(SR * 0.6))) * 0.035, t + i * d)
        t += bar
        k += 1
    return buf


def track(segs, cps, total, mood, end_start):
    buf = music(total, mood)
    rnd = random.Random(7)
    t0 = 0.0
    for s in segs:
        who = s["who"]
        n = len(s["txt"])
        if who in VOICE:
            base, kind = VOICE[who]
            for i in range(0, n, 2):
                ch = s["txt"][i]
                if ch in " .,!?…«»:'":
                    continue
                f = base * 2 ** (rnd.choice([0, 2, 4, 5, 7, -2]) / 12)
                if s["emo"] in ("colere",):
                    f *= 0.9
                if s["emo"] in ("peur", "surpris"):
                    f *= 1.12
                bl = osc(f, 0.055, kind, vib=0.02)
                bl *= env(len(bl), 0.004, 0.025)
                add(buf, bl * (0.11 if kind == "square" else 0.17), t0 + i / cps)
        elif who == "N":
            for i in range(0, n, 3):
                noise = np.random.default_rng(i).standard_normal(int(SR * 0.012))
                add(buf, noise * env(len(noise), 0.001, 0.006) * 0.035, t0 + i / cps)
        if s["fx"] == "shake":
            d = 0.45
            th = osc(55, d) * np.exp(-np.linspace(0, 8, int(SR * d))) * 0.5
            th += np.random.default_rng(1).standard_normal(len(th)) * np.exp(-np.linspace(0, 14, len(th))) * 0.12
            add(buf, th, t0)
        if s["fx"] == "enter":
            d = 0.35
            sw = osc(300, d) * 0
            tt = np.arange(int(SR * d)) / SR
            sw = np.sin(2 * np.pi * (300 + 900 * tt / d) * tt) * env(len(tt), 0.01, 0.1) * 0.12
            add(buf, sw, t0)
        t0 += s["dur"]
    # fin : petit carillon
    for i, m in enumerate([72, 76, 79, 84]):
        f = 440 * 2 ** ((m - 69) / 12)
        add(buf, osc(f, 1.2) * np.exp(-np.linspace(0, 5, int(SR * 1.2))) * 0.12, end_start + 0.15 + i * 0.14)
    buf = buf[:int(SR * total)]
    buf = np.tanh(buf * 1.4) / 1.2
    return buf


def save(buf, path):
    a = (np.clip(buf, -1, 1) * 32000).astype(np.int16)
    st = np.repeat(a[:, None], 2, axis=1)
    with wave.open(path, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(st.tobytes())
