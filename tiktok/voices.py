"""Voix des personnages (Kokoro TTS, français) avec cache.
synth(code, texte, emotion) -> (chemin_wav, durée_s)
Modèle : tts/kokoro.onnx + tts/voices.bin (téléchargés depuis les releases GitHub de kokoro-onnx).
"""
import hashlib, os, subprocess
import numpy as np
import soundfile as sf

HERE = os.path.dirname(os.path.abspath(__file__))
TTS = os.environ.get("TTS_DIR", os.path.join(HERE, "tts"))
CACHE = os.path.join(HERE, "tts_cache")
os.makedirs(CACHE, exist_ok=True)

# code: (mélange de voix, vitesse, demi-tons, filtre)
VOICES = {
    "N":  ([("ff_siwis", 0.5), ("am_onyx", 0.5)], 0.9, -4.5, None),
    "I":  ([("ff_siwis", 1.0)], 1.02, 0, None),
    "Y":  ([("ff_siwis", 0.45), ("am_michael", 0.55)], 1.06, -2, None),
    "F":  ([("ff_siwis", 0.55), ("bf_emma", 0.45)], 0.9, -2, None),
    "LU": ([("ff_siwis", 0.4), ("am_santa", 0.6)], 0.84, -4, None),
    "T":  ([("ff_siwis", 0.5), ("am_adam", 0.5)], 1.0, -1, None),
    "V":  ([("ff_siwis", 0.4), ("bm_lewis", 0.6)], 0.98, -2, None),
    "BA": ([("ff_siwis", 0.3), ("bm_george", 0.7)], 0.86, -6, None),
    "MC": ([("ff_siwis", 0.55), ("af_sarah", 0.45)], 0.88, 3, None),
    "BI": ([("ff_siwis", 0.3), ("am_fenrir", 0.7)], 0.82, -9.5, None),
    "FO": ([("ff_siwis", 0.4), ("am_puck", 0.6)], 1.12, 6, None),
    "CO": ([("ff_siwis", 0.45), ("bm_daniel", 0.55)], 1.08, 0, "nasal"),
    "MO": ([("ff_siwis", 0.6), ("af_kore", 0.4)], 1.04, -2, None),
    "PH": ([("ff_siwis", 0.45), ("am_eric", 0.55)], 0.97, 1, None),
    "LA": ([("ff_siwis", 0.45), ("am_liam", 0.55)], 1.2, 1.5, None),
    "RO": ([("ff_siwis", 0.5), ("bf_isabella", 0.5)], 0.92, -6.5, None),
    "GA": ([("ff_siwis", 0.5), ("am_echo", 0.5)], 1.22, 8, None),
    "BR": ([("ff_siwis", 0.3), ("bm_fable", 0.7)], 0.9, -7, None),
    "X":  ([("ff_siwis", 0.4), ("am_santa", 0.6)], 0.84, -4, "phone"),
    "C":  ([("ff_siwis", 1.0)], 1.0, 2, None),
    "H":  ([("ff_siwis", 0.5), ("am_michael", 0.5)], 1.0, -3, None),
}
EMO_SPEED = {"colere": 1.06, "peur": 1.08, "triste": 0.92, "surpris": 1.04, "joie": 1.03, "neutre": 1.0}

_K = None


def kokoro():
    global _K
    if _K is None:
        from kokoro_onnx import Kokoro
        _K = Kokoro(os.path.join(TTS, "kokoro.onnx"), os.path.join(TTS, "voices.bin"))
    return _K


def style(mix):
    k = kokoro()
    names = set(k.get_voices())
    tot, acc = 0.0, None
    for n, w in mix:
        if n not in names:
            n = "am_michael" if n.startswith(("am", "bm")) else "af_bella"
        v = k.get_voice_style(n) * w
        acc = v if acc is None else acc + v
        tot += w
    return acc / tot


def clean(text):
    return text.replace("«", "").replace("»", "").replace("...", ", ").replace("…", ", ").strip()


def synth(code, text, emo="neutre", tempo=1.0):
    mix, speed, semi, filt = VOICES.get(code, VOICES["N"])
    speed = speed * EMO_SPEED.get(emo, 1.0)
    key = hashlib.md5(f"{code}|{text}|{emo}|{tempo:.3f}|{mix}|{speed:.3f}|{semi}|{filt}".encode()).hexdigest()[:16]
    out = os.path.join(CACHE, key + ".wav")
    if not os.path.exists(out):
        a, sr = kokoro().create(clean(text), voice=style(mix), speed=speed, lang="fr-fr")
        raw = out + ".raw.wav"
        sf.write(raw, a, sr)
        p = 2 ** (semi / 12)
        af = [f"asetrate={sr}*{p:.5f}", f"aresample={sr}", f"atempo={1 / p * tempo:.5f}"]
        if filt == "nasal":
            af += ["highpass=f=320", "equalizer=f=1200:t=q:w=1.2:g=6"]
        if filt == "phone":
            af += ["highpass=f=400", "lowpass=f=3200", "volume=1.6"]
        af += ["silenceremove=start_periods=1:start_threshold=-45dB", "areverse",
               "silenceremove=start_periods=1:start_threshold=-45dB", "areverse"]
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", raw, "-af", ",".join(af), "-ar", "44100", "-ac", "1", out], check=True)
        os.remove(raw)
    info = sf.info(out)
    return out, info.frames / info.samplerate


def envelope(path, fps=30):
    a, sr = sf.read(path)
    if a.ndim > 1:
        a = a.mean(axis=1)
    hop = int(sr / fps)
    n = len(a) // hop + 1
    env = np.array([np.sqrt(np.mean(a[i * hop:(i + 1) * hop] ** 2)) if len(a[i * hop:(i + 1) * hop]) else 0 for i in range(n)])
    thr = max(0.02, 0.25 * env.max())
    return (env > thr).tolist()
