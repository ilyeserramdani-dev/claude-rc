"""Moteur de la série « Ceux de la cuisine » — vidéos 1080x1920.
Usage : python3 engine.py ep.json sortie.mp4 [--frames t1,t2,...  (exporte des images clés au lieu de la vidéo)]

ep.json = {
  "ep": 1, "title": "La lettre", "bg": "nuit"|"cuisine"|"salon"|"cartons",
  "cast": ["L","G"],                       # personnages à l'écran, de gauche à droite
  "lines": [[qui, texte, emotion?, fx?], ...],  # qui = code perso, "N" narrateur, "C"/"H" voix hors champ
  "next": "Le nouveau"                      # titre de l'épisode suivant (absent = fin de saison)
}
émotions : neutre, joie, colere, triste, surpris, peur ; fx : shake, enter (le perso apparaît à cette ligne)
"""
import json, math, os, random, subprocess, sys
from PIL import Image, ImageDraw, ImageFont

W, H, FPS, S = 1080, 1920, 30, 2
FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FI = "/usr/share/fonts/truetype/dejavu/DejaVuSans-BoldOblique.ttf"
f_title = ImageFont.truetype(FB, 60)
f_series = ImageFont.truetype(FB, 34)
f_bubble = ImageFont.truetype(FB, 56)
f_name = ImageFont.truetype(FB, 38)
f_narr = ImageFont.truetype(FI, 54)
f_big = ImageFont.truetype(FB, 110)

EMOS = ["neutre", "joie", "colere", "triste", "surpris", "peur"]


def sc(*v):
    return [int(a * S) for a in v]


# ---------------------------------------------------------------- visages
def draw_face(d, f, emo, mouth_open, blink):
    style = f.get("style", "normal")
    ink = (0, 230, 255) if style == "led" else f.get("ink", (45, 35, 40))
    r = f["r"]
    big = 1.18 if emo == "surpris" else 1.0
    for i, (ex, ey) in enumerate(f["eyes"]):
        side = -1 if i == 0 else 1
        rw, rh = r * big, r * 1.15 * big
        if style == "led":
            if blink:
                d.line(sc(ex - rw, ey, ex + rw, ey), fill=ink, width=8 * S)
            elif emo == "joie":
                d.arc(sc(ex - rw, ey - rh * .4, ex + rw, ey + rh * 1.2), 200, 340, fill=ink, width=9 * S)
            else:
                d.rounded_rectangle(sc(ex - rw * .55, ey - rh * .8, ex + rw * .55, ey + rh * .8), 10 * S, fill=ink)
        else:
            if blink:
                d.arc(sc(ex - rw, ey - rh * .3, ex + rw, ey + rh * .6), 20, 160, fill=ink, width=7 * S)
            else:
                d.ellipse(sc(ex - rw, ey - rh, ex + rw, ey + rh), fill=(255, 255, 255), outline=ink, width=4 * S)
                ir = rw * (0.55 if emo == "peur" else 0.75)
                d.ellipse(sc(ex - ir, ey - ir * 1.1 + rh * .1, ex + ir, ey + ir * 1.1 + rh * .1), fill=f.get("iris", (60, 50, 45)))
                pr = ir * (0.35 if emo == "peur" else 0.5)
                d.ellipse(sc(ex - pr, ey - pr * 1.3 + rh * .1, ex + pr, ey + pr * 1.3 + rh * .1), fill=(20, 20, 25))
                d.ellipse(sc(ex + pr * .1, ey - pr * 1.4, ex + pr * .1 + rw * .3, ey - pr * 1.4 + rw * .3), fill=(255, 255, 255))
                if emo == "triste":  # larme
                    d.ellipse(sc(ex + side * rw * .5 - 7, ey + rh + 6, ex + side * rw * .5 + 7, ey + rh + 28), fill=(120, 190, 255))
            if f.get("lashes") and not blink:
                for k in range(3):
                    x0 = ex + side * (rw * .55 + k * 9)
                    d.line(sc(x0, ey - rh * .75 - k * 3, x0 + side * 20, ey - rh * 1.25 - k * 5), fill=ink, width=5 * S)
        # sourcils
        bw = f.get("brow", 6)
        by = ey - r * 1.15 * big - 16 - (12 if emo in ("surpris", "peur") else 0)
        inner, outer = ex - side * r * .9, ex + side * r * .9
        if emo == "colere":
            yi, yo = by + 16, by - 8
        elif emo in ("triste", "peur"):
            yi, yo = by - 12, by + 8
        else:
            yi, yo = by, by
        d.line(sc(inner, yi, outer, yo), fill=ink, width=bw * S)
    mx, my = f["mouth"]
    mw = f["mw"]
    if mouth_open:
        if emo == "surpris":
            d.ellipse(sc(mx - mw * .3, my - mw * .35, mx + mw * .3, my + mw * .35), fill=(110, 30, 40) if style != "led" else ink)
        else:
            h = mw * (0.5 if emo in ("joie", "colere") else 0.38)
            d.rounded_rectangle(sc(mx - mw / 2, my - h / 2, mx + mw / 2, my + h / 2), int(h * .45) * S,
                                fill=(110, 30, 40) if style != "led" else ink)
            if style != "led":
                d.ellipse(sc(mx - mw * .25, my, mx + mw * .25, my + h / 2), fill=(230, 110, 130))
    else:
        w = 6 * S
        if emo == "joie":
            d.chord(sc(mx - mw / 2, my - mw * .35, mx + mw / 2, my + mw * .35), 0, 180, fill=(110, 30, 40) if style != "led" else ink)
        elif emo == "triste":
            d.arc(sc(mx - mw * .4, my, mx + mw * .4, my + mw * .5), 200, 340, fill=ink, width=w)
        elif emo == "colere":
            d.line(sc(mx - mw * .4, my + 6, mx + mw * .4, my), fill=ink, width=w)
        elif emo == "surpris":
            d.ellipse(sc(mx - mw * .15, my - mw * .15, mx + mw * .15, my + mw * .15), outline=ink, width=w)
        elif emo == "peur":
            pts = [(mx - mw * .4 + k * mw * .1, my + (6 if k % 2 else -6)) for k in range(9)]
            d.line([(int(x * S), int(y * S)) for x, y in pts], fill=ink, width=w)
        else:
            d.arc(sc(mx - mw * .35, my - mw * .3, mx + mw * .35, my + mw * .2), 30, 150, fill=ink, width=w)


# ---------------------------------------------------------------- corps
def body_lola(d):
    cream, line = (250, 246, 240), (225, 215, 205)
    d.ellipse(sc(60, 520, 400, 556), fill=(0, 0, 0, 50))
    d.arc(sc(300, 300, 460, 540), 180, 330, fill=cream, width=38 * S)
    d.ellipse(sc(90, 300, 370, 545), fill=cream, outline=line, width=4 * S)
    d.polygon(sc(95, 140, 120, 20, 205, 95), fill=cream, outline=line)
    d.polygon(sc(365, 140, 340, 20, 255, 95), fill=cream, outline=line)
    d.polygon(sc(115, 120, 128, 50, 180, 98), fill=(250, 200, 210))
    d.polygon(sc(345, 120, 332, 50, 280, 98), fill=(250, 200, 210))
    d.ellipse(sc(70, 60, 390, 350), fill=(252, 249, 244), outline=line, width=4 * S)
    d.polygon(sc(290, 60, 360, 20, 360, 110), fill=(244, 167, 185))
    d.polygon(sc(290, 60, 225, 20, 225, 110), fill=(244, 167, 185))
    d.ellipse(sc(272, 45, 308, 80), fill=(230, 130, 160))
    d.ellipse(sc(100, 240, 160, 278), fill=(250, 195, 205))
    d.ellipse(sc(300, 240, 360, 278), fill=(250, 195, 205))
    d.polygon(sc(218, 245, 242, 245, 230, 260), fill=(235, 130, 150))
    for dy in (0, 18):
        d.line(sc(185, 268 + dy, 90, 255 + dy * 1.6), fill=(190, 180, 175), width=3 * S)
        d.line(sc(275, 268 + dy, 370, 255 + dy * 1.6), fill=(190, 180, 175), width=3 * S)
    for i in range(9):
        a = math.pi * (0.15 + 0.7 * i / 8)
        px, py = 230 - 120 * math.cos(a), 335 + 40 * math.sin(a)
        d.ellipse(sc(px - 13, py - 13, px + 13, py + 13), fill=(255, 250, 245), outline=(220, 205, 200))


def body_gaston(d):
    d.ellipse(sc(40, 480, 400, 516), fill=(0, 0, 0, 50))
    d.line(sc(40, 300, 0, 380), fill=(120, 125, 135), width=16 * S)
    d.line(sc(400, 300, 440, 380), fill=(120, 125, 135), width=16 * S)
    d.rounded_rectangle(sc(40, 130, 400, 495), 60 * S, fill=(196, 204, 214), outline=(120, 128, 140), width=6 * S)
    d.rounded_rectangle(sc(70, 150, 150, 470), 30 * S, fill=(225, 232, 240))
    d.ellipse(sc(320, 400, 370, 440), fill=(170, 178, 190))
    d.rounded_rectangle(sc(110, 105, 205, 150), 14 * S, fill=(60, 60, 66))
    d.rounded_rectangle(sc(235, 105, 330, 150), 14 * S, fill=(60, 60, 66))
    d.rounded_rectangle(sc(395, 200, 425, 260), 8 * S, fill=(80, 80, 90))


def body_neo(d):
    d.ellipse(sc(40, 480, 400, 516), fill=(0, 0, 0, 50))
    d.rounded_rectangle(sc(35, 120, 405, 495), 40 * S, fill=(28, 30, 38), outline=(90, 95, 110), width=5 * S)
    d.rounded_rectangle(sc(55, 135, 120, 480), 25 * S, fill=(52, 56, 70))
    d.rounded_rectangle(sc(110, 95, 205, 135), 12 * S, fill=(150, 155, 165))
    d.rounded_rectangle(sc(235, 95, 330, 135), 12 * S, fill=(150, 155, 165))
    d.rounded_rectangle(sc(95, 190, 345, 420), 30 * S, fill=(8, 18, 32), outline=(0, 160, 200), width=3 * S)
    for k, rr in enumerate((18, 32, 46)):
        d.arc(sc(370 - rr, 165 - rr, 370 + rr, 165 + rr), 225, 315, fill=(0, 200, 240), width=5 * S)
    d.text((int(170 * S), int(440 * S)), "NÉO", font=ImageFont.truetype(FB, 30 * S), fill=(0, 200, 240))


def body_berthe(d):
    alu, dark = (200, 202, 208), (120, 122, 130)
    d.ellipse(sc(70, 520, 330, 556), fill=(0, 0, 0, 50))
    d.polygon(sc(110, 330, 290, 330, 320, 540, 80, 540), fill=alu, outline=dark)
    d.rectangle(sc(95, 318, 305, 345), fill=(160, 162, 170))
    d.polygon(sc(130, 110, 270, 110, 300, 320, 100, 320), fill=(215, 217, 222), outline=dark)
    d.polygon(sc(270, 110, 330, 85, 300, 140), fill=(215, 217, 222), outline=dark)
    d.rounded_rectangle(sc(35, 150, 85, 300), 20 * S, fill=(30, 30, 30))
    d.line(sc(85, 170, 105, 170), fill=(30, 30, 30), width=14 * S)
    d.line(sc(85, 280, 102, 280), fill=(30, 30, 30), width=14 * S)
    d.ellipse(sc(120, 80, 280, 125), fill=(190, 192, 198), outline=dark)
    d.ellipse(sc(185, 55, 215, 85), fill=(30, 30, 30))
    # foulard
    d.polygon(sc(100, 300, 300, 300, 290, 335, 110, 335), fill=(200, 60, 70))
    d.polygon(sc(250, 320, 300, 395, 265, 400), fill=(200, 60, 70))
    for x in range(120, 290, 30):
        d.ellipse(sc(x, 310, x + 10, 320), fill=(255, 230, 230))


def body_rosa(d):
    d.ellipse(sc(80, 585, 340, 618), fill=(0, 0, 0, 50))
    leaf, leaf2 = (70, 160, 90), (50, 130, 75)
    d.line(sc(210, 360, 210, 120), fill=(110, 80, 50), width=12 * S)
    for (x, y, a) in [(130, 120, 1), (290, 110, 0), (110, 230, 1), (310, 220, 0), (160, 60, 1), (260, 40, 0),
                      (210, 10, 1), (140, 300, 1), (290, 300, 0), (210, 170, 0)]:
        d.ellipse(sc(x - 62, y - 38, x + 62, y + 38), fill=leaf if a else leaf2)
        d.line(sc(x - 45, y, x + 45, y), fill=(40, 110, 60), width=3 * S)
    d.ellipse(sc(250, 70, 300, 120), fill=(255, 140, 180))
    d.ellipse(sc(265, 85, 285, 105), fill=(255, 220, 100))
    d.polygon(sc(80, 360, 340, 360, 310, 600, 110, 600), fill=(215, 115, 75), outline=(170, 85, 55))
    d.rounded_rectangle(sc(68, 345, 352, 395), 14 * S, fill=(225, 128, 88), outline=(170, 85, 55), width=3 * S)
    d.ellipse(sc(115, 505, 160, 535), fill=(240, 150, 140))
    d.ellipse(sc(260, 505, 305, 535), fill=(240, 150, 140))


def body_pixel(d):
    d.ellipse(sc(30, 525, 270, 556), fill=(0, 0, 0, 50))
    d.rounded_rectangle(sc(20, 20, 280, 545), 40 * S, fill=(25, 25, 30))
    d.rounded_rectangle(sc(34, 34, 266, 531), 30 * S, fill=(90, 120, 230))
    d.rounded_rectangle(sc(34, 300, 266, 531), 30 * S, fill=(150, 110, 230))
    d.rounded_rectangle(sc(115, 46, 185, 66), 10 * S, fill=(25, 25, 30))
    for i, x in enumerate((60, 115, 170, 225)):
        d.rounded_rectangle(sc(x - 20, 420, x + 20, 460), 10 * S, fill=[(255, 200, 80), (100, 220, 140), (255, 120, 120), (255, 255, 255)][i])
    d.text((int(70 * S), int(80 * S)), "21:47", font=ImageFont.truetype(FB, 22 * S), fill=(255, 255, 255))


def body_brutus(d):
    fawn, white, dark = (205, 160, 110), (250, 245, 235), (120, 85, 55)
    d.ellipse(sc(50, 505, 450, 540), fill=(0, 0, 0, 50))
    d.ellipse(sc(90, 280, 410, 530), fill=fawn, outline=dark, width=4 * S)
    d.ellipse(sc(180, 330, 320, 520), fill=white)
    d.ellipse(sc(110, 470, 200, 530), fill=fawn, outline=dark, width=3 * S)
    d.ellipse(sc(300, 470, 390, 530), fill=fawn, outline=dark, width=3 * S)
    d.polygon(sc(70, 80, 40, 10, 150, 60), fill=dark)
    d.polygon(sc(430, 80, 460, 10, 350, 60), fill=dark)
    d.ellipse(sc(50, 40, 450, 340), fill=fawn, outline=dark, width=4 * S)
    d.ellipse(sc(150, 210, 350, 340), fill=white)
    d.ellipse(sc(215, 215, 285, 255), fill=(50, 35, 30))
    d.arc(sc(120, 230, 250, 340), 90, 200, fill=dark, width=5 * S)
    d.arc(sc(250, 230, 380, 340), 340, 90, fill=dark, width=5 * S)
    for x in (190, 205, 295, 310):
        d.ellipse(sc(x - 4, 275, x + 4, 283), fill=dark)
    d.rounded_rectangle(sc(120, 330, 380, 365), 14 * S, fill=(210, 40, 40))
    d.ellipse(sc(232, 350, 268, 386), fill=(255, 210, 60), outline=(200, 150, 30), width=3 * S)


CHARS = {
    "L": dict(name="Lola", col=(233, 84, 140), size=(460, 560), body=body_lola,
              face=dict(eyes=[(155, 195), (305, 195)], r=40, iris=(80, 170, 110), mouth=(230, 285), mw=50, lashes=True)),
    "G": dict(name="Gaston", col=(70, 110, 160), size=(440, 520), body=body_gaston,
              face=dict(eyes=[(160, 270), (280, 270)], r=32, mouth=(220, 370), mw=90, brow=14, ink=(45, 42, 42))),
    "NEO": dict(name="Néo", col=(0, 150, 200), size=(440, 520), body=body_neo,
               face=dict(style="led", eyes=[(170, 285), (270, 285)], r=30, mouth=(220, 365), mw=90, brow=7)),
    "B": dict(name="Berthe", col=(190, 50, 60), size=(400, 560), body=body_berthe,
              face=dict(eyes=[(165, 205), (235, 205)], r=24, iris=(90, 70, 60), mouth=(200, 270), mw=50, lashes=True)),
    "R": dict(name="Rosa", col=(60, 150, 80), size=(420, 620), body=body_rosa,
              face=dict(eyes=[(165, 455), (255, 455)], r=26, iris=(70, 50, 40), mouth=(210, 530), mw=55, lashes=True)),
    "P": dict(name="Pixel", col=(110, 90, 220), size=(300, 560), body=body_pixel,
              face=dict(eyes=[(105, 210), (195, 210)], r=28, iris=(40, 60, 140), mouth=(150, 300), mw=60)),
    "BR": dict(name="Brutus", col=(160, 100, 50), size=(500, 540), body=body_brutus,
               face=dict(eyes=[(175, 165), (325, 165)], r=30, iris=(90, 60, 40), mouth=(250, 305), mw=100, brow=10)),
}
CHARS.update({
    "I": dict(name="Inès", col=(214, 140, 20)),
    "Y": dict(name="Yanis", col=(30, 140, 85)),
    "F": dict(name="Mme Diallo", col=(160, 50, 160)),
    "LU": dict(name="Lucien", col=(50, 90, 165)),
    "T": dict(name="Théo", col=(30, 130, 165)),
    "V": dict(name="Verdier", col=(170, 30, 40)),
})
CHARS.update({
    "BA": dict(name="Le Baron", col=(120, 40, 150), bright=0.8),
    "MC": dict(name="Mamie", col=(190, 110, 40)),
    "BI": dict(name="Biscotte", col=(220, 90, 140)),
    "FO": dict(name="La Fouine", col=(190, 30, 40)),
    "CO": dict(name="Le Comptable", col=(60, 110, 60)),
    "MO": dict(name="Cdt Morel", col=(150, 110, 60)),
    "PH": dict(name="M. Pham", col=(70, 100, 150)),
    "LA": dict(name="MC Lampadaire", col=(200, 160, 0)),
    "RO": dict(name="Mamie Rose", col=(130, 40, 150)),
    "GA": dict(name="Gaspard", col=(90, 100, 120), k=0.42),
})
OFF = {"C": "Camille (hors champ)", "H": "Hugo (hors champ)", "X": "Voix au téléphone", "PA": "Haut-parleur"}


B3D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "b3d")


_MASKS = {}


def feather(im):
    w, h = im.size
    if (w, h) not in _MASKS:
        import numpy as np
        x = np.minimum(np.arange(w), np.arange(w)[::-1]) / (0.14 * w)
        y = np.minimum(np.arange(h), np.arange(h)[::-1]) / (0.08 * h)
        mk = np.clip(np.minimum(x[None, :], y[:, None]), 0, 1)
        _MASKS[(w, h)] = Image.fromarray((mk * 255).astype("uint8"), "L")
    a = im.getchannel("A")
    from PIL import ImageChops
    im.putalpha(ImageChops.multiply(a, _MASKS[(w, h)]))
    return im


def make_sprites(code):
    out = {}
    for emo in EMOS:
        for m in (0, 1):
            for b in (0, 1):
                f = os.path.join(B3D, "sprites", f"{code}_{emo}_{m}_{b}.png")
                if not os.path.exists(f):
                    f = os.path.join(B3D, "sprites", f"{code}_{emo}_{m}_0.png")
                out[(emo, m, b)] = feather(Image.open(f).convert("RGBA"))
    CHARS[code]["size"] = out[("neutre", 0, 0)].size
    br = CHARS.get(code, {}).get("bright")
    if br:
        from PIL import ImageEnhance
        for k, im in out.items():
            a = im.getchannel("A")
            im2 = ImageEnhance.Contrast(ImageEnhance.Brightness(im.convert("RGB")).enhance(br)).enhance(1.12).convert("RGBA")
            im2.putalpha(a)
            out[k] = im2
    return out


def make_sprites_2d(code):
    c = CHARS[code]
    w, h = c["size"]
    base = Image.new("RGBA", (w * S, h * S), (0, 0, 0, 0))
    c["body"](ImageDraw.Draw(base))
    out = {}
    for emo in EMOS:
        for m in (0, 1):
            for b in (0, 1):
                im = base.copy()
                draw_face(ImageDraw.Draw(im), c["face"], emo, m, b)
                out[(emo, m, b)] = im.resize((w, h), Image.LANCZOS)
    return out


# ---------------------------------------------------------------- décors
def background(kind):
    from PIL import ImageFilter
    im = Image.open(os.path.join(B3D, "bg", f"{kind}.png")).convert("RGB").resize((W, H), Image.LANCZOS)
    return im.filter(ImageFilter.GaussianBlur(2.5))


def background_2d(kind):
    bg = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(bg)
    night = kind == "nuit"
    for y in range(H):
        t = y / H
        if night:
            c = (int(40 + 10 * t), int(45 + 10 * t), int(85 + 15 * t))
        elif kind == "salon":
            c = (int(238 - 15 * t), int(222 - 15 * t), int(200 - 10 * t))
        else:
            c = (int(255 - 20 * t), int(228 - 10 * t), int(225 + 5 * t))
        d.line([(0, y), (W, y)], fill=c)
    if kind == "salon":
        for x in range(0, W, 90):
            d.line([(x, 0), (x, 1450)], fill=(228, 210, 188), width=3)
        d.rounded_rectangle([60, 900, 560, 1300], 30, fill=(240, 240, 230), outline=(255, 255, 255), width=12)
        d.rectangle([0, 1440, W, H], fill=(150, 110, 80))
        for y in range(1460, H, 70):
            d.line([(0, y), (W, y)], fill=(135, 98, 70), width=3)
        d.rounded_rectangle([600, 1150, 1080, 1460], 40, fill=(110, 140, 170))
        d.rounded_rectangle([600, 1080, 1080, 1220], 40, fill=(125, 155, 185))
        return bg
    tile = (70, 78, 120) if night else (250, 210, 215)
    for y in range(0, 1360, 120):
        for x in range(0, W, 120):
            d.rectangle([x + 3, y + 3, x + 117, y + 117], outline=tile, width=3)
    if night:
        d.rounded_rectangle([640, 980, 1010, 1300], 30, fill=(20, 25, 55), outline=(90, 95, 140), width=14)
        d.ellipse([880, 1020, 960, 1100], fill=(250, 245, 210))
        for (x, y) in [(700, 1050), (760, 1180), (930, 1230), (820, 1010)]:
            d.ellipse([x, y, x + 6, y + 6], fill=(255, 255, 230))
        d.line([(825, 980), (825, 1300)], fill=(90, 95, 140), width=10)
    else:
        d.rounded_rectangle([640, 980, 1010, 1300], 30, fill=(205, 232, 245), outline=(255, 255, 255), width=14)
        d.line([(825, 980), (825, 1300)], fill=(255, 255, 255), width=10)
    top = (120, 90, 70) if night else (214, 168, 124)
    d.rectangle([0, 1440, W, H], fill=top)
    d.rectangle([0, 1440, W, 1475], fill=(140, 108, 85) if night else (236, 196, 152))
    for x in range(0, W, 180):
        d.line([(x, 1520), (x + 90, 1920)], fill=(105, 80, 62) if night else (200, 152, 110), width=4)
    if kind == "cartons":
        for (x0, y0, x1, y1) in [(30, 1060, 330, 1300), (250, 1150, 520, 1300), (80, 900, 300, 1070)]:
            d.rectangle([x0, y0, x1, y1], fill=(200, 160, 110), outline=(150, 115, 75), width=6)
            d.rectangle([(x0 + x1) // 2 - 25, y0, (x0 + x1) // 2 + 25, y1], fill=(225, 200, 150))
        d.text((60, 1210), "FRAGILE", font=ImageFont.truetype(FB, 40), fill=(190, 40, 40))
    return bg


# ---------------------------------------------------------------- texte
def wrap(text, font, maxw):
    text = text.replace("« ", "«\u00a0").replace(" »", "\u00a0»").replace(" ?", "\u00a0?").replace(" !", "\u00a0!").replace(" :", "\u00a0:")
    words, lines, cur = [w for w in text.split(" ") if w], [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if font.getlength(t) <= maxw:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def typed(lines, n):
    out = []
    for ln in lines:
        part = ln[:max(0, n)]
        if 0 < n < len(ln):
            k = part.rfind(" ")
            part = part[:k] if k > 0 else ""
        out.append(part)
        n -= len(ln) + 1
    return out


def draw_bubble(d, who, full, shown, tail_x, y1=1010):
    lines = wrap(full, f_bubble, 870)
    lh = 72
    h = len(lines) * lh + 66
    x0, x1 = 55, W - 55
    y0 = y1 - h
    if who in OFF:
        col, fill, name = (110, 110, 120), (236, 236, 242), OFF[who]
    else:
        col, fill, name = CHARS[who]["col"], (255, 255, 255), CHARS[who]["name"]
    d.rounded_rectangle([x0 + 8, y0 + 10, x1 + 8, y1 + 10], 46, fill=(0, 0, 0))
    d.rounded_rectangle([x0, y0, x1, y1], 46, fill=fill, outline=col, width=8)
    if tail_x is not None:
        tip = (tail_x, y1 + 75)
        d.polygon([(tail_x - 38, y1 - 5), (tail_x + 38, y1 - 5), tip], fill=fill)
        d.line([(tail_x - 38, y1 - 1), tip, (tail_x + 38, y1 - 1)], fill=col, width=8)
    nw = f_name.getlength(name) + 50
    nx = x0 + 40
    d.rounded_rectangle([nx, y0 - 34, nx + nw, y0 + 30], 30, fill=col)
    d.text((nx + 25, y0 - 26), name, font=f_name, fill=(255, 255, 255))
    for i, part in enumerate(typed(lines, shown)):
        d.text((x0 + 48, y0 + 42 + i * lh), part, font=f_bubble, fill=(35, 30, 40))


def draw_narr(d, full, shown):
    lines = wrap(full, f_narr, 900)
    lh = 70
    h = len(lines) * lh + 60
    y0 = 380
    d.rounded_rectangle([60, y0, W - 60, y0 + h], 26, fill=(20, 18, 28))
    for i, part in enumerate(typed(lines, shown)):
        tw = f_narr.getlength(lines[i])
        d.text(((W - tw) / 2, y0 + 32 + i * lh), part, font=f_narr, fill=(255, 235, 170))


def title_band(d, ep, title, season=1, series="CEUX DE LA CUISINE"):
    d.rounded_rectangle([50, 90, W - 50, 290], 40, fill=(18, 16, 24))
    s = f"{series} · ÉPISODE {ep}/21" if season == 1 else f"{series} · SAISON {season} · ÉP. {ep}"
    d.text(((W - f_series.getlength(s)) / 2, 112), s, font=f_series, fill=(244, 167, 185))
    lines = wrap(title, f_title, 920)
    for i, ln in enumerate(lines[:2]):
        d.text(((W - f_title.getlength(ln)) / 2, 165 + i * 70), ln, font=f_title, fill=(255, 225, 120))


def hook_card(d, text):
    f = ImageFont.truetype(FB, 72)
    lines = wrap(text, f, 900)
    h = len(lines) * 92 + 90
    y0 = 520
    d.rounded_rectangle([40, y0, W - 40, y0 + h], 40, fill=(255, 225, 120))
    for i, ln in enumerate(lines):
        d.text(((W - f.getlength(ln)) / 2, y0 + 45 + i * 92), ln, font=f, fill=(30, 22, 40))


def end_card(d, nxt, k):
    d.rectangle([0, 0, W, H], fill=(20, 16, 30))
    t = "À SUIVRE..." if nxt else "FIN DE LA SAISON 1"
    f = f_big if nxt else ImageFont.truetype(FB, 84)
    d.text(((W - f.getlength(t)) / 2, 640), t, font=f, fill=(255, 225, 120))
    if nxt:
        s = f"Épisode suivant : « {nxt} »"
        for i, ln in enumerate(wrap(s, f_bubble, 940)):
            d.text(((W - f_bubble.getlength(ln)) / 2, 830 + i * 72), ln, font=f_bubble, fill=(255, 255, 255))
        s2 = "Abonne-toi pour ne pas le rater"
    else:
        s2 = "Abonne-toi pour la saison 2"
    if int(k * 2) % 2 == 0 or True:
        d.rounded_rectangle([140, 1100, W - 140, 1220], 60, fill=(233, 84, 140))
        d.text(((W - f_name.getlength(s2)) / 2, 1138), s2, font=f_name, fill=(255, 255, 255))


# ---------------------------------------------------------------- rendu
TARGET = 64.0   # durée visée : juste au-dessus de 60 s (seuil Creator Rewards), pour garder un fort taux de complétion
END_DUR = 3.0


def build(ep):
    if ep.get("voice"):
        return build_voice(ep)
    CPS = 18.0
    lines = ep["lines"]
    hook = max(2.2, len(ep.get("hook", "")) / 30) if ep.get("hook") else 0
    nN = sum(1 for l in lines if l[0] == "N")
    base = hook + END_DUR + sum(len(l[1]) for l in lines) / CPS + 0.4 * nN
    h = min(2.4, max(1.0, (TARGET - base) / len(lines)))
    segs = []
    if hook:
        segs.append(dict(who="HOOK", txt=ep["hook"], emo="neutre", fx="", dur=hook))
    for ln in lines:
        who, txt = ln[0], ln[1]
        emo = ln[2] if len(ln) > 2 and ln[2] else "neutre"
        fx = ln[3] if len(ln) > 3 else ""
        dur = max(2.2, len(txt) / CPS + h + (0.4 if who == "N" else 0))
        segs.append(dict(who=who, txt=txt, emo=emo, fx=fx, dur=dur))
    return segs, CPS


def build_voice(ep):
    import voices
    items = []
    if ep.get("hook"):
        items.append(("HOOK", ep["hook"], "neutre", "", "N"))
    for ln in ep["lines"]:
        who, txt = ln[0], ln[1]
        emo = ln[2] if len(ln) > 2 and ln[2] else "neutre"
        fx = ln[3] if len(ln) > 3 else ""
        items.append((who, txt, emo, fx, who if who in voices.VOICES else "N"))
    gap = lambda w: 0.55 if w == "HOOK" else (0.45 if w == "N" else 0.3)

    def synth_all(tempo):
        return [voices.synth(v, t, e, tempo) for (w, t, e, f, v) in items]
    res = synth_all(1.0)
    total = sum(d + gap(it[0]) for (p, d), it in zip(res, items)) + END_DUR
    if total > 71:
        speech = sum(d for p, d in res)
        tempo = min(1.35, speech / max(speech - (total - 69), 1))
        res = synth_all(tempo)
        total = sum(d + gap(it[0]) for (p, d), it in zip(res, items)) + END_DUR
    extra = max(0.0, min(1.5, (62.5 - total) / len(items))) if total < 62.5 else 0.0
    segs = []
    for (path, d), (w, t, e, f, v) in zip(res, items):
        segs.append(dict(who=w, txt=t, emo=e, fx=f, dur=d + gap(w) + extra, audio=path, alen=d,
                         cps=len(t) / max(d * 0.92, 0.4), env=voices.envelope(path, FPS)))
    return segs, 18.0


ZOOM = 1.4


def shot_plan(segs, slots, cast):
    plan, k = [], 0
    for i, s in enumerate(segs):
        who = s["who"]
        if who in slots:
            k += 1
            close = k > 1 and (s["emo"] != "neutre" or k % 2 == 0)
        else:
            close = False
        if close:
            x, y, w, h, cx = slots[who]
            z = ZOOM
            x0 = min(max(cx - W / (2 * z), 0), W - W / z)
            y0 = min(max(y - 800 / z, 0), H - H / z)
            plan.append((z, x0, y0, True))
        else:
            plan.append((1.0, 0.0, 0.0, False))
    return plan


def cam_at(plan, seg_starts, segs, idx, t):
    z1, x1, y1, close = plan[idx]
    z0, x0, y0, _ = plan[idx - 1] if idx > 0 else plan[idx]
    lt = t - seg_starts[idx]
    k = min(1.0, lt / 0.45)
    k = k * k * (3 - 2 * k)
    z, x, y = z0 + (z1 - z0) * k, x0 + (x1 - x0) * k, y0 + (y1 - y0) * k
    push = 1 + 0.035 * min(1.0, lt / max(segs[idx]["dur"], 0.1))
    zz = z * push
    cxm, cym = x + W / (2 * z), y + H / (2 * z)
    x = min(max(cxm - W / (2 * zz), 0), W - W / zz)
    y = min(max(cym - H / (2 * zz), 0), H - H / zz)
    return zz, x, y


_VIG = None


def vignette():
    global _VIG
    if _VIG is None:
        import numpy as np
        yy, xx = np.mgrid[0:H, 0:W]
        r = np.sqrt(((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2)
        a = np.clip((r - 0.75) / 0.6, 0, 1) * 150
        _VIG = Image.fromarray(np.dstack([np.zeros_like(a), np.zeros_like(a), np.zeros_like(a), a]).astype("uint8"), "RGBA")
    return _VIG


def main(path, out, frames_at=None):
    ep = json.load(open(path, encoding="utf-8"))
    segs, CPS = build(ep)
    bg = background(ep.get("bg", "cuisine"))
    cast = ep["cast"]
    sprites = {c: make_sprites(c) for c in cast}
    crack = ep.get("crack", {})
    cracked = {}
    for c in crack:
        cracked[c] = {}
        for k, im in sprites[c].items():
            im2 = im.copy()
            dd = ImageDraw.Draw(im2)
            w0, h0 = im2.size
            pts = [(0.27, 0.36), (0.33, 0.47), (0.27, 0.56), (0.35, 0.66), (0.30, 0.78)]
            dd.line([(int(x * w0), int(y * h0)) for x, y in pts], fill=(25, 25, 30, 255), width=6, joint="curve")
            dd.line([(int(0.33 * w0), int(0.47 * h0)), (int(0.40 * w0), int(0.50 * h0))], fill=(25, 25, 30, 255), width=4)
            dd.line([(int(0.35 * w0), int(0.66 * h0)), (int(0.25 * w0), int(0.70 * h0))], fill=(25, 25, 30, 255), width=4)
            cracked[c][k] = im2
    n = len(cast)
    scale = {1: 1.4, 2: 1.28, 3: 1.04}.get(n, 0.8)
    if ep.get("char_h"):
        hmax = max(CHARS[c]["size"][1] for c in cast)
        scale = ep["char_h"].get(str(n), 700) / hmax
    slots = {}
    for i, c in enumerate(cast):
        w, h = CHARS[c]["size"]
        kk = CHARS[c].get("k", 1.0)
        w2, h2 = int(w * scale * kk), int(h * scale * kk)
        cx = W * (i + 0.5) / n
        slots[c] = (int(cx - w2 / 2), 1665 - h2, w2, h2, int(cx))
    BUB_Y = min(1060, min(v[1] for v in slots.values()) - 85)
    CINE = bool(ep.get("cinema"))
    if scale != 1.0:
        for c in cast:
            for k, im in sprites[c].items():
                sprites[c][k] = im.resize(slots[c][2:4], Image.LANCZOS)
            for k, im in cracked.get(c, {}).items():
                cracked[c][k] = im.resize(slots[c][2:4], Image.LANCZOS)
    # qui est présent à quel moment (fx enter)
    entered = {c: 0.0 for c in cast}
    acc = 0
    for s in segs:
        if s["fx"] == "enter" and s["who"] in entered:
            entered[s["who"]] = acc
        acc += s["dur"]
    for c in cast:  # un perso qui "entre" plus tard n'est pas là avant
        pass
    end_dur = END_DUR
    total = sum(s["dur"] for s in segs) + end_dur
    nframes = int(total * FPS)
    last_emo = {c: "neutre" for c in cast}
    rnd = random.Random(1)
    if frames_at is None:
        import audio
        wav = out + ".wav"
        if ep.get("voice"):
            audio.save(audio.track_voice(segs, total, ep.get("bg", "cuisine"), total - end_dur), wav)
        else:
            audio.save(audio.track(segs, CPS, total, ep.get("bg", "cuisine"), total - end_dur), wav)
        ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
                               "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                               "-i", wav, "-shortest",
                               "-c:v", "libx264", "-preset", "veryfast", "-crf", "23", "-pix_fmt", "yuv420p",
                               "-af", "loudnorm=I=-16:TP=-1.5", "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", out], stdin=subprocess.PIPE)
        targets = range(nframes)
    else:
        targets = [int(t * FPS) for t in frames_at]
    # émotion courante de chaque perso = sa dernière réplique
    seg_starts, a = [], 0
    for s in segs:
        seg_starts.append(a)
        a += s["dur"]
    plan = shot_plan(segs, slots, cast) if CINE else None
    for f in targets:
        t = f / FPS
        frame = bg.copy()
        d = ImageDraw.Draw(frame)
        idx = None
        for i, s in enumerate(segs):
            if seg_starts[i] <= t < seg_starts[i] + s["dur"]:
                idx = i
        if idx is None:
            end_card(d, ep.get("next"), t)
        else:
            s = segs[idx]
            lt = t - seg_starts[idx]
            for j in range(idx + 1):
                if segs[j]["who"] in last_emo:
                    last_emo[segs[j]["who"]] = segs[j]["emo"]
            for c in last_emo:
                last_emo[c] = "neutre"
            for j in range(idx + 1):
                if segs[j]["who"] in last_emo:
                    last_emo[segs[j]["who"]] = segs[j]["emo"]
            cps = s.get("cps", CPS)
            typing = lt * cps < len(s["txt"]) if "env" not in s else lt < s["alen"]
            for i, c in enumerate(cast):
                if t < entered[c]:
                    continue
                x, y, w, h, cx = slots[c]
                talking = s["who"] == c and typing
                if "env" in s:
                    fi = int(lt * FPS)
                    m = 1 if talking and fi < len(s["env"]) and s["env"][fi] else 0
                else:
                    m = 1 if talking and int(t * 9) % 2 == 0 else 0
                b = 1 if ((t + i * 1.7) % 3.9) < 0.13 else 0
                bob = int(9 * math.sin(t * 14)) if talking else int(3 * math.sin(t * 2 + i))
                ent = t - entered[c]
                if entered[c] > 0 and ent < 0.4:
                    bob += int((0.4 - ent) / 0.4 * 300)
                src = cracked[c] if (c in crack and idx >= crack[c]) else sprites[c]
                im = src[(last_emo[c], m, b)]
                frame.paste(im, (x, y + bob), im)
            camz, camx, camy = (1.0, 0.0, 0.0)
            if CINE:
                camz, camx, camy = cam_at(plan, seg_starts, segs, idx, t)
                if camz > 1.001:
                    frame = frame.crop((int(camx), int(camy), int(camx + W / camz), int(camy + H / camz))).resize((W, H), Image.BILINEAR)
                frame.paste(vignette(), (0, 0), vignette())
            d = ImageDraw.Draw(frame)
            title_band(d, ep["ep"], ep["title"], ep.get("season", 1), ep.get("series", "CEUX DE LA CUISINE"))
            shown = int(lt * cps) if s["who"] != "HOOK" else 999
            if s["who"] == "HOOK":
                hook_card(d, s["txt"])
            elif s["who"] == "N":
                draw_narr(d, s["txt"], shown)
            else:
                tail = slots[s["who"]][4] if s["who"] in slots else None
                by = BUB_Y
                if CINE and s["who"] in slots:
                    tail = int((tail - camx) * camz)
                    by = int(min(1060, (slots[s["who"]][1] - camy) * camz - 70))
                    by = max(by, 700)
                draw_bubble(d, s["who"], s["txt"], shown, tail, by)
            if s["fx"] == "shake" and lt < 0.6:
                frame = frame.transform(frame.size, Image.AFFINE, (1, 0, rnd.randint(-14, 14), 0, 1, rnd.randint(-14, 14)))
                d = ImageDraw.Draw(frame)
        d.rectangle([0, H - 14, int(W * f / nframes), H], fill=(233, 84, 140))
        if frames_at is None:
            ff.stdin.write(frame.tobytes())
        else:
            frame.save(f"{out}_{t:05.1f}.png")
    if frames_at is None:
        ff.stdin.close()
        ff.wait()
    print(out, f"{total:.1f}s")
    return total


if __name__ == "__main__":
    fa = None
    if len(sys.argv) > 4 and sys.argv[3] == "--frames":
        fa = [float(x) for x in sys.argv[4].split(",")]
    main(sys.argv[1], sys.argv[2], fa)
