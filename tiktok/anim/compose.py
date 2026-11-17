"""Étape 3 : montage final 1080x1920 / 24 i/s (décor + personnages 3D + mouvements de caméra,
sous-titres, accroche, générique de fin, son) -> mp4.
python3 anim/compose.py work/ep01 videos_c/s1/ep01.mp4 [--frames t1,t2]
"""
import json, math, os, random, subprocess, sys
from PIL import Image, ImageDraw, ImageFilter, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
from engine3 import CHARS, OFF, FB, FI, wrap

W, H, FPS = 1080, 1920, 24
f_sub = ImageFont.truetype(FB, 58)
f_narr = ImageFont.truetype(FI, 56)
f_name = ImageFont.truetype(FB, 40)
f_series = ImageFont.truetype(FB, 34)
f_title = ImageFont.truetype(FB, 54)
f_hook = ImageFont.truetype(FB, 74)
f_big = ImageFont.truetype(FB, 110)
PINK = (233, 84, 140)


def outlined(d, xy, text, font, fill, stroke=6):
    d.text(xy, text, font=font, fill=fill, stroke_width=stroke, stroke_fill=(10, 8, 14))


def subtitle(d, who, txt, lt, alen):
    if who in OFF:
        name, col = OFF[who], (150, 150, 165)
    else:
        name, col = CHARS[who]["name"], CHARS[who]["col"]
    lines = wrap(txt, f_sub, 960)
    # affichage par blocs de 2 lignes, calé sur la voix
    blocks = [lines[i:i + 2] for i in range(0, len(lines), 2)]
    n = len(blocks)
    k = min(n - 1, int(lt / max(alen, 0.5) * n)) if n > 1 else 0
    blk = blocks[k]
    y = 1430
    nw = f_name.getlength(name) + 44
    d.rounded_rectangle([(W - nw) / 2, y - 70, (W + nw) / 2, y - 14], 28, fill=col)
    d.text(((W - f_name.getlength(name)) / 2, y - 64), name, font=f_name, fill=(255, 255, 255))
    for i, ln in enumerate(blk):
        outlined(d, ((W - f_sub.getlength(ln)) / 2, y + i * 74), ln, f_sub, (255, 255, 255))


def narration(d, txt, lt, alen):
    lines = wrap(txt, f_narr, 940)
    blocks = [lines[i:i + 2] for i in range(0, len(lines), 2)]
    n = len(blocks)
    k = min(n - 1, int(lt / max(alen, 0.5) * n)) if n > 1 else 0
    y = 1440
    for i, ln in enumerate(blocks[k]):
        outlined(d, ((W - f_narr.getlength(ln)) / 2, y + i * 72), ln, f_narr, (255, 228, 150))


def title_band(d, ep):
    s = f"BÂTIMENT B · ÉPISODE {ep['ep']}/21" if ep.get("season", 1) == 1 else f"BÂTIMENT B · S{ep['season']} · ÉP. {ep['ep']}"
    outlined(d, ((W - f_series.getlength(s)) / 2, 120), s, f_series, (244, 167, 185), 4)
    outlined(d, ((W - f_title.getlength(ep["title"])) / 2, 168), ep["title"], f_title, (255, 225, 120), 5)


def hook(d, txt, lt):
    lines = wrap(txt, f_hook, 940)
    a = min(1.0, lt / 0.25)
    y0 = 640
    for i, ln in enumerate(lines):
        outlined(d, ((W - f_hook.getlength(ln)) / 2, y0 + i * 96 + (1 - a) * 30), ln, f_hook, (255, 225, 120), 8)


def end_card(im, ep, k):
    im = im.filter(ImageFilter.GaussianBlur(14))
    ov = Image.new("RGBA", im.size, (14, 10, 24, 170))
    im = Image.alpha_composite(im.convert("RGBA"), ov).convert("RGB")
    d = ImageDraw.Draw(im)
    nxt = ep.get("next")
    t = "À SUIVRE..." if nxt else "FIN DE LA SAISON"
    outlined(d, ((W - f_big.getlength(t)) / 2, 650), t, f_big, (255, 225, 120), 8)
    if nxt:
        for i, ln in enumerate(wrap(f"Épisode suivant : « {nxt} »", f_sub, 940)):
            outlined(d, ((W - f_sub.getlength(ln)) / 2, 840 + i * 72), ln, f_sub, (255, 255, 255))
    s2 = "Abonne-toi pour ne pas le rater" if nxt else "Abonne-toi pour la suite"
    p = 1 + 0.04 * math.sin(k * 6)
    bw, bh = 800 * p, 120 * p
    d.rounded_rectangle([(W - bw) / 2, 1110 - bh / 2 + 60, (W + bw) / 2, 1110 + bh / 2 + 60], 60, fill=PINK)
    d.text(((W - f_name.getlength(s2)) / 2, 1148), s2, font=f_name, fill=(255, 255, 255))
    return im


def main(work, out, frames_at=None):
    tl = json.load(open(os.path.join(work, "timeline.json"), encoding="utf-8"))
    test = frames_at is not None
    sj = json.load(open(os.path.join(work, "shots_test.json" if test else "shots.json")))
    ep, segs = tl["ep"], tl["segs"]
    afps, nfr, shots = sj["afps"], sj["nfr"], {int(k): v for k, v in sj["shots"].items()}
    total = tl["total"]
    bgs = {}
    rnd = random.Random(3)

    def seg_at(t):
        for i, s in enumerate(segs):
            if s["start"] <= t < s["start"] + s["dur"]:
                return i
        return None

    def frame3d(t):
        f = min(int(t * afps), nfr - 1)
        if test:
            f = min(shots, key=lambda x: abs(x - f))
        sh = shots[f]
        if sh not in bgs:
            bgs[sh] = Image.open(os.path.join(work, "bg", sh + ".png")).convert("RGB")
        im = bgs[sh].copy()
        ch = Image.open(os.path.join(work, "ch", f"f{f:05d}.png")).convert("RGBA")
        im.paste(ch, (0, 0), ch)
        return im, sh

    last = None
    if not test:
        ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
                               "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-i", os.path.join(work, "audio.wav"),
                               "-shortest", "-c:v", "libx264", "-preset", "medium", "-crf", "21", "-pix_fmt", "yuv420p",
                               "-af", "loudnorm=I=-16:TP=-1.5", "-c:a", "aac", "-b:a", "160k",
                               "-movflags", "+faststart", out], stdin=subprocess.PIPE)
        targets = range(int(total * FPS))
    else:
        targets = [int(t * FPS) for t in frames_at]
    for j in targets:
        t = j / FPS
        i = seg_at(t)
        if i is None or t >= tl["end"]:
            if last is None:
                last, _ = frame3d(tl["end"] - 0.01)
                last = last.resize((W, H), Image.LANCZOS)
            frame = end_card(last, ep, t - tl["end"])
        else:
            s = segs[i]
            lt = t - s["start"]
            im, sh = frame3d(t)
            # mouvement de caméra (travelling avant lent) + tremblement
            z = 1.0 + (0.12 if sh.startswith("EST") else 0.06) * min(1.0, lt / max(s["dur"], 0.1))
            ox = oy = 0
            if s["fx"] == "shake" and lt < 0.7:
                amp = 12 * (1 - lt / 0.7)
                ox, oy = rnd.uniform(-amp, amp), rnd.uniform(-amp, amp)
            w, h = im.size
            cw, chh = w / z, h / z
            if ox or oy:
                z = max(z, 1.05)
                cw, chh = w / z, h / z
            x0 = min(max((w - cw) / 2 + ox, 0), w - cw)
            y0 = min(max((h - chh) / 2 + oy, 0), h - chh)
            frame = im.resize((W, H), Image.BICUBIC, box=(x0, y0, x0 + cw, y0 + chh))
            # fondu au noir au début d'un nouveau plan
            d = ImageDraw.Draw(frame)
            title_band(d, ep)
            if s["who"] == "HOOK":
                hook(d, s["txt"], lt)
            elif s["who"] == "N":
                narration(d, s["txt"], lt, s["alen"] or s["dur"])
            else:
                subtitle(d, s["who"], s["txt"], lt, s["alen"] or s["dur"])
        d = ImageDraw.Draw(frame)
        d.rectangle([0, H - 12, int(W * j / (total * FPS)), H], fill=PINK)
        if test:
            frame.save(f"{out}_{t:05.1f}.png")
        else:
            ff.stdin.write(frame.tobytes())
    if not test:
        ff.stdin.close()
        ff.wait()
    print(out, f"{total:.1f}s")


if __name__ == "__main__":
    fa = None
    if "--frames" in sys.argv:
        fa = [float(x) for x in sys.argv[sys.argv.index("--frames") + 1].split(",")]
    main(sys.argv[1], sys.argv[2], fa)
