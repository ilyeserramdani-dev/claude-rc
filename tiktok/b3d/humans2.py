"""Nouveaux personnages farfelus de « Bâtiment B » (cartel Corvo, habitants, pigeon).
python3 humans2.py CODE [...] [--preview]
"""
import bpy, math, os, sys, random
from mathutils import Vector
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import chars as C
import humans as Hm
from chars import mat, sphere, cone, cyl, torus, rbox, tube, ell_surf
from humans import body, face, HC, HR

C.PPU = 230


def shades(z, kind="round", color=(0.05, 0.05, 0.05), surfz=None, surf=None):
    lens = mat("lens_" + kind, color, rough=0.05, coat=1, metal=0.3)
    frame = mat("frame_" + kind, (0.85, 0.7, 0.3) if kind == "round" else (0.1, 0.1, 0.1), metal=1, rough=0.25)
    for s in (-1, 1):
        x = s * 0.21
        y = surf(x, z) - 0.09
        if kind == "round":
            cyl((x, y, z), 0.1, 0.02, lens, rot=(math.pi / 2, 0, 0))
        elif kind == "aviator":
            sphere((x, y, z), 1, (0.14, 0.02, 0.11), lens)
        else:  # neon / rect
            rbox((x, y, z), (0.24, 0.03, 0.13), 0.03, lens)
    tube([(-0.12, surf(-0.12, z) - 0.1, z), (0.12, surf(0.12, z) - 0.1, z)], 0.012, frame)


def mustache(surf, kind, color):
    m = mat("stache", color, rough=0.6, sheen=0.3)
    if kind == "pencil":
        tube([(-0.15, surf(-0.15, 2.58) - 0.03, 2.57), (0, surf(0, 2.6) - 0.05, 2.6), (0.15, surf(0.15, 2.58) - 0.03, 2.57)], 0.014, m)
    else:  # morse
        for s in (-1, 1):
            sphere((s * 0.11, surf(s * 0.11, 2.56) - 0.03, 2.55), 1, (0.14, 0.07, 0.08), m, rot=(0, s * 0.3, 0))


def baron():
    surf, sk = body((0.94, 0.8, 0.7), (0.96, 0.94, 0.88), (0.96, 0.94, 0.88), (0.85, 0.7, 0.3))
    fur = mat("fur", (0.5, 0.2, 0.65), rough=0.9, sheen=1.0)
    rnd = random.Random(5)
    for k in range(22):
        a = k / 22 * 2 * math.pi
        sphere((0.5 * math.cos(a), 0.36 * math.sin(a) + 0.02, 2.08 + rnd.uniform(-0.05, 0.05)), rnd.uniform(0.11, 0.15), (1, 1, 1), fur, seg=14)
    silver = mat("hair", (0.85, 0.85, 0.88), rough=0.2, coat=0.8)
    sphere((0, 0.12, 3.05), 1, (0.58, 0.52, 0.42), silver)
    sphere((0, -0.15, 3.32), 1, (0.38, 0.38, 0.3), silver, rot=(-0.4, 0, 0))
    shades(2.85, "round", surf=surf)
    mustache(surf, "pencil", (0.75, 0.75, 0.78))
    gold = mat("gold", (0.95, 0.75, 0.3), metal=1, rough=0.2)
    cyl((0.78, -0.2, 0.75), 0.04, 1.5, gold, rot=(0, 0.1, 0))
    sphere((0.75, -0.2, 1.52), 0.09, (1, 1, 1), gold)
    tube([(0.6, -0.12, 1.1), (0.72, -0.18, 1.3)], 0.05, sk)
    return face("baron", surf, (0.7, 0.7, 0.72), iris=(0.2, 0.2, 0.2)), (0.9, 0.9, 1.25)


def mamie_corvo():
    surf, sk = body((0.96, 0.84, 0.76), (0.85, 0.55, 0.25), (0.25, 0.2, 0.18), (0.6, 0.1, 0.15),
                    robe=(0.82, 0.52, 0.22))
    leop = mat("spots", (0.25, 0.15, 0.08), rough=0.8)
    rnd = random.Random(8)
    for k in range(40):
        a = rnd.uniform(-1.2, 1.2)
        z = rnd.uniform(0.3, 1.9)
        r = 0.45 + (1.9 - z) * 0.1
        sphere((r * math.sin(a), -r * math.cos(a) * 0.95, z), 0.04, (1, 0.3, 0.8), leop, seg=10)
    white = mat("hair", (0.97, 0.97, 0.97), rough=0.5, sheen=0.6)
    sphere((0, 0.08, 3.05), 1, (0.6, 0.56, 0.45), white)
    sphere((0, 0.12, 3.75), 1, (0.48, 0.44, 0.85), white)
    pearl = mat("pearl", (0.98, 0.96, 0.94), rough=0.1, coat=1)
    for i in range(13):
        a = math.pi * (0.1 + 0.8 * i / 12)
        sphere((-0.42 * math.cos(a), -0.42 * math.sin(a) * 0.8 - 0.05, 2.12 - 0.12 * math.sin(a)), 0.05, (1, 1, 1), pearl, seg=12)
    red = mat("catframe", (0.85, 0.1, 0.2), rough=0.3, coat=0.5)
    for s in (-1, 1):
        x = s * 0.21
        torus((x, surf(x, 2.84) - 0.06, 2.84), 0.13, 0.025, red, rot=(math.pi / 2, 0, 0), scale=(1.25, 1, 0.9))
    return face("mamiecorvo", surf, (0.6, 0.6, 0.6), iris=(0.25, 0.4, 0.3), lashes=True), (0.95, 0.95, 0.78)


def biscotte():
    surf, sk = body((0.86, 0.68, 0.56), (0.98, 0.55, 0.7), (0.98, 0.55, 0.7), (1, 1, 1))
    for s in (-1, 1):
        rbox((s * 0.48, -0.0, 1.65), (0.05, 0.62, 1.0), 0.02, mat("stripe", (1, 1, 1), rough=0.7))
    blk = mat("bowler", (0.06, 0.06, 0.07), rough=0.4, coat=0.5)
    cyl((0, 0.05, 3.3), 0.3, 0.06, blk)
    sphere((0, 0.05, 3.42), 1, (0.2, 0.2, 0.16), blk)
    shades(2.85, "rect", surf=surf)
    return face("biscotte", surf, (0.25, 0.2, 0.18), iris=(0.3, 0.2, 0.1), mw=0.3), (1.5, 1.25, 1.08)


def fouine():
    surf, sk = body((0.9, 0.78, 0.66), (0.55, 0.55, 0.58), (0.2, 0.2, 0.25), (0.9, 0.2, 0.2))
    cone((0, surf(0, 2.7) - 0.2, 2.68), 0.1, 0.0, 0.5, mat("bignose", (0.92, 0.72, 0.62), rough=0.5), rot=(math.pi / 2 + 0.15, 0, 0))
    cap = mat("cap", (0.85, 0.12, 0.15), rough=0.6)
    sphere((0, 0.05, 3.12), 1, (0.58, 0.55, 0.32), cap)
    rbox((0, 0.62, 3.05), (0.45, 0.5, 0.05), 0.04, cap, rot=(0.25, 0, 0))
    cyl((0, 0, 2.3), 0.1, 0.45, mat("skin", (0.9, 0.78, 0.66)))
    torus((0, 0.15, 2.12), 0.33, 0.08, mat("hood2", (0.5, 0.5, 0.53), rough=0.8), rot=(1.2, 0, 0))
    return face("fouine", surf, (0.3, 0.25, 0.2), iris=(0.35, 0.3, 0.15), mw=0.2,
                extra=dict(eyes=[(-0.17, 2.86), (0.17, 2.86)], r=0.09)), (0.78, 0.8, 1.12)


def comptable():
    surf, sk = body((0.95, 0.82, 0.72), (0.35, 0.5, 0.3), (0.45, 0.4, 0.35), (0.3, 0.2, 0.12), sleeves=(0.95, 0.95, 0.92))
    hair = mat("hair", (0.3, 0.22, 0.15), rough=0.6)
    for s in (-1, 1):
        sphere((s * 0.5, 0.12, 2.82), 1, (0.1, 0.25, 0.2), hair)
    tube([(-0.45, 0.1, 3.18), (-0.1, -0.1, 3.32), (0.3, 0.0, 3.25)], 0.03, hair)
    rim = mat("bigglass", (0.1, 0.1, 0.1), rough=0.3)
    for s in (-1, 1):
        x = s * 0.21
        torus((x, surf(x, 2.84) - 0.06, 2.84), 0.17, 0.025, rim, rot=(math.pi / 2, 0, 0))
    cone((0, -0.31, 2.08), 0.09, 0.0, 0.14, mat("bowtie", (0.8, 0.1, 0.1), rough=0.5), verts=3, rot=(0, math.pi / 2, 0))
    cone((0, -0.31, 2.08), 0.09, 0.0, 0.14, mat("bowtie", (0.8, 0.1, 0.1), rough=0.5), verts=3, rot=(0, -math.pi / 2, 0))
    rbox((0.62, -0.25, 1.15), (0.22, 0.06, 0.32), 0.03, mat("calc", (0.2, 0.2, 0.22), rough=0.4))
    return face("comptable", surf, (0.3, 0.22, 0.15), iris=(0.3, 0.25, 0.2), mw=0.18), (0.95, 0.95, 0.85)


def morel():
    surf, sk = body((0.95, 0.8, 0.7), None, None, (0.15, 0.1, 0.08), robe=(0.75, 0.62, 0.42))
    red = mat("hair", (0.75, 0.22, 0.1), rough=0.5, sheen=0.5)
    sphere((0, 0.08, 2.98), 1, (0.62, 0.58, 0.55), red)
    for s in (-1, 1):
        sphere((s * 0.45, 0.1, 2.6), 1, (0.18, 0.3, 0.32), red)
    shades(3.12, "aviator", color=(0.15, 0.1, 0.05), surf=surf)
    rbox((-0.25, -0.33, 1.78), (0.18, 0.03, 0.24), 0.04, mat("policebadge", (0.9, 0.75, 0.3), metal=1, rough=0.2))
    torus((0, 0.0, 1.35), 0.47, 0.04, mat("belt", (0.4, 0.3, 0.2), rough=0.6))
    return face("morel", surf, (0.55, 0.15, 0.08), iris=(0.3, 0.5, 0.4), lashes=True), (1.0, 1.0, 1.05)


def pham():
    surf, sk = body((0.92, 0.78, 0.6), (0.5, 0.6, 0.75), (0.3, 0.3, 0.35), (0.2, 0.2, 0.22))
    sphere((0, -0.2, 1.4), 1, (0.48, 0.38, 0.45), mat("top", (0.5, 0.6, 0.75)))
    rbox((0, -0.6, 1.35), (0.72, 0.04, 1.0), 0.08, mat("apron", (0.98, 0.98, 0.95), rough=0.8))
    hair = mat("hair", (0.12, 0.1, 0.1), rough=0.6)
    sphere((0, 0.12, 3.0), 1, (0.57, 0.5, 0.36), hair)
    mustache(surf, "morse", (0.12, 0.1, 0.1))
    rim = mat("phamglass", (0.4, 0.3, 0.2), rough=0.4)
    for s in (-1, 1):
        torus((s * 0.21, surf(s * 0.21, 2.84) - 0.06, 2.84), 0.12, 0.018, rim, rot=(math.pi / 2, 0, 0))
    return face("pham", surf, (0.12, 0.1, 0.1), iris=(0.2, 0.12, 0.06), mw=0.24), (1.25, 1.2, 0.95)


def lampadaire():
    surf, sk = body((0.55, 0.36, 0.24), (1.0, 0.85, 0.1), (0.2, 0.2, 0.2), (0.95, 0.3, 0.6))
    puff = mat("puffer", (1.0, 0.85, 0.1), rough=0.5, coat=0.3)
    for z in (1.35, 1.65, 1.95):
        torus((0, 0, z), 0.46, 0.09, puff)
    afro = mat("hair", (0.08, 0.06, 0.05), rough=0.9, sheen=0.5)
    sphere((0, 0.12, 3.25), 1, (0.95, 0.85, 0.85), afro)
    shades(2.85, "rect", color=(0.2, 1.0, 0.4), surf=surf)
    hp = mat("headphones", (0.95, 0.2, 0.55), rough=0.3, coat=0.5)
    for s in (-1, 1):
        cyl((s * 0.6, 0.02, 2.78), 0.17, 0.12, hp, rot=(0, math.pi / 2, 0))
    rbox((-0.62, -0.25, 1.3), (0.14, 0.04, 0.26), 0.03, mat("phone2", (0.05, 0.05, 0.07), rough=0.2, coat=1))
    return face("lampadaire", surf, (0.08, 0.06, 0.05), iris=(0.2, 0.12, 0.06), mw=0.28,
                extra=dict(lashes=False)), (0.85, 0.85, 1.22)


def rose():
    surf, sk = body((0.82, 0.62, 0.5), (0.5, 0.2, 0.6), (0.5, 0.2, 0.6), (1, 1, 1))
    for s in (-1, 1):
        sphere((s * 0.5, 0, 2.02), 1, (0.22, 0.25, 0.2), mat("top", (0.5, 0.2, 0.6)))
        rbox((s * 0.48, -0.0, 1.6), (0.04, 0.62, 1.0), 0.02, mat("stripe", (1, 1, 1), rough=0.7))
    grey = mat("hair", (0.75, 0.75, 0.78), rough=0.6, sheen=0.4)
    sphere((0, 0.1, 3.0), 1, (0.59, 0.54, 0.4), grey)
    torus((0, 0.0, 3.05), 0.56, 0.06, mat("headband", (0.9, 0.1, 0.15), rough=0.6), scale=(1, 0.95, 1))
    glove = mat("glove", (0.85, 0.08, 0.1), rough=0.3, coat=0.6)
    for s in (-1, 1):
        sphere((s * 0.22, -0.4, 1.7), 1, (0.14, 0.12, 0.17), glove)
    tube([(-0.22, -0.38, 1.85), (0, -0.33, 2.1), (0.22, -0.38, 1.85)], 0.012, mat("lace", (1, 1, 1)))
    return face("rose", surf, (0.55, 0.55, 0.58), iris=(0.3, 0.25, 0.15), lashes=True), (1.15, 1.1, 0.95)


def gaspard():
    grey = mat("pigeon", (0.55, 0.57, 0.62), rough=0.6, sheen=0.5)
    sphere((0, 0.1, 0.9), 1, (0.7, 0.8, 0.75), grey)
    sphere((0, 0, 1.75), 1, (0.48, 0.45, 0.5), grey)
    sphere((0, -0.02, 1.42), 1, (0.42, 0.4, 0.22), mat("irid", (0.3, 0.6, 0.45), metal=0.5, rough=0.3))
    for s in (-1, 1):
        sphere((s * 0.62, 0.15, 0.95), 1, (0.15, 0.5, 0.45), mat("wing", (0.45, 0.47, 0.52), rough=0.6), rot=(0.2, 0, 0))
        cyl((s * 0.2, -0.05, 0.12), 0.04, 0.3, mat("feet", (0.95, 0.4, 0.3), rough=0.6))
        sphere((s * 0.2, -0.15, 0.03), 1, (0.08, 0.15, 0.03), mat("feet", (0.95, 0.4, 0.3)))
    cone((0, 0.85, 0.75), 0.4, 0.05, 0.6, grey, rot=(math.pi / 2 + 0.6, 0, 0))
    hs = ell_surf((0, 0, 1.75), (0.48, 0.45, 0.5))
    cone((0, hs(0, 1.68) - 0.08, 1.68), 0.07, 0.0, 0.25, mat("beak", (0.95, 0.75, 0.3), rough=0.4), rot=(math.pi / 2, 0, 0))
    patch = mat("patch", (0.05, 0.05, 0.05), rough=0.5)
    cyl((0.2, hs(0.2, 1.85) - 0.04, 1.85), 0.13, 0.03, patch, rot=(math.pi / 2 - 0.3, 0.4, 0))
    tube([(-0.4, hs(-0.4, 2.1), 2.1), (0.2, hs(0.2, 2.05) - 0.05, 2.02), (0.48, hs(0.48, 1.7), 1.7)], 0.015, patch)
    sphere((0, 0.05, 2.28), 1, (0.08, 0.08, 0.15), grey)
    return dict(name="gaspard", surf=hs, eyes=[(-0.2, 1.88), (0.2, 1.88)], r=0.1, iris=(0.9, 0.5, 0.1),
                mouth=(0, 1.55), mw=0.14, ink=(0.15, 0.15, 0.18), brow=0.025), (1.0, 1.0, 1.0)


BUILDERS = {"BA": baron, "MC": mamie_corvo, "BI": biscotte, "FO": fouine, "CO": comptable, "MO": morel,
            "PH": pham, "LA": lampadaire, "RO": rose, "GA": gaspard}


def scale_objs(objs, S):
    for o in objs:
        o.location = Vector((o.location.x * S[0], o.location.y * S[1], o.location.z * S[2]))
        o.scale = Vector((o.scale.x * S[0], o.scale.y * S[1], o.scale.z * S[2]))


def render(code, preview=False):
    C.reset()
    C.MATS.clear()
    C.setup_scene()
    before = set(bpy.context.scene.objects)
    spec, S = BUILDERS[code]()
    scale_objs(set(bpy.context.scene.objects) - before, S)
    C.frame_camera(margin=0.3)
    sc = bpy.context.scene
    sc.cycles.samples = 12
    states = [("neutre", 0, 0)] if preview else [(e, m, b) for e in C.EMOS for m in (0, 1) for b in (0, 1)
                                                   if not (m and b) and (b == 0 or e == "neutre")]
    for emo, mo, bl in states:
        if not preview and os.path.exists(os.path.join(C.OUT, f"{code}_{emo}_{mo}_{bl}.png")) and code != "PH" and code != "FO":
            continue
        coll = C.build_face(spec, emo, mo, bl)
        scale_objs(list(coll.objects), S)
        sc.render.filepath = os.path.join(C.OUT, f"{code}_{emo}_{mo}_{bl}.png")
        bpy.ops.render.render(write_still=True)
        C.clear_face(coll)
        print("OK", code, emo, mo, bl, flush=True)


if __name__ == "__main__":
    for c in [a for a in sys.argv[1:] if not a.startswith("--")]:
        render(c, "--preview" in sys.argv)
