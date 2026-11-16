"""Personnages humains stylisés 3D de la série « Bâtiment B ».
python3 humans.py CODE [...] [--preview]  -> sprites/CODE_<emo>_<m>_<b>.png
"""
import bpy, math, os, sys
from mathutils import Vector
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import chars as C
from chars import mat, sphere, cone, cyl, torus, rbox, tube, ell_surf

C.PPU = 230
HC, HR = (0, 0, 2.78), (0.56, 0.52, 0.62)   # tête


def body(skin, top, pants, shoes, robe=None, sleeves=None):
    sk = mat("skin", skin, rough=0.5, sss=0.0, sheen=0.2)
    tp = mat("top", top, rough=0.8, sheen=0.3) if top else None
    pt = mat("pants", pants, rough=0.85) if pants else None
    sh = mat("shoes", shoes, rough=0.4, coat=0.3)
    for s in (-1, 1):
        sphere((s * 0.21, -0.08, 0.1), 1, (0.16, 0.28, 0.11), sh)
    if robe:
        cone((0, 0, 0.95), 0.62, 0.42, 1.7, mat("robe", robe, rough=0.75, sheen=0.4))
    else:
        for s in (-1, 1):
            cyl((s * 0.2, 0, 0.7), 0.15, 1.1, pt)
        sphere((0, 0, 1.22), 1, (0.42, 0.3, 0.25), pt)
    rbox((0, 0, 1.68), (0.98, 0.6, 1.0), 0.28, tp if not robe else mat("robe", robe, rough=0.75, sheen=0.4))
    am = mat("sleeve", sleeves, rough=0.8) if sleeves else (tp if not robe else mat("robe", robe, rough=0.75, sheen=0.4))
    for s in (-1, 1):
        tube([(s * 0.47, 0, 2.05), (s * 0.63, -0.04, 1.6), (s * 0.6, -0.1, 1.18)], 0.12, am)
        sphere((s * 0.6, -0.12, 1.06), 0.12, (1, 1, 1.15), sk)
    cyl((0, 0, 2.2), 0.13, 0.25, sk)
    sphere(HC, 1, HR, sk)
    for s in (-1, 1):
        sphere((s * 0.55, 0.02, 2.74), 1, (0.07, 0.1, 0.13), sk)
    surf = ell_surf(HC, HR)
    sphere((0, surf(0, 2.66) - 0.02, 2.66), 1, (0.07, 0.07, 0.08), mat("nose", tuple(c * 0.92 for c in skin), rough=0.5))
    return surf, sk


def face(name, surf, hair, iris=(0.25, 0.16, 0.1), lashes=False, mw=0.24, extra=None):
    d = dict(name=name, surf=surf, eyes=[(-0.21, 2.84), (0.21, 2.84)], r=0.105, iris=iris, mouth=(0, 2.5),
             mw=mw, lashes=lashes, ink=hair, brow=0.028)
    if extra:
        d.update(extra)
    return d


def cap_hair(color, z0=2.9, front=-0.25, scale=(0.6, 0.56, 0.4), m=None):
    m = m or mat("hair", color, rough=0.55, sheen=0.4)
    sphere((0, 0.03, z0), 1, scale, m)
    return m


def ines():
    surf, sk = body((0.78, 0.55, 0.4), (0.92, 0.66, 0.15), (0.45, 0.45, 0.5), (0.97, 0.97, 0.97))
    hair = (0.1, 0.06, 0.05)
    hm = mat("hair", hair, rough=0.7, sheen=0.5)
    sphere((0, 0.14, 3.08), 1, (0.6, 0.55, 0.46), hm)
    import random
    rnd = random.Random(2)
    for k in range(26):
        a = rnd.uniform(0, 2 * math.pi)
        z = rnd.uniform(2.9, 3.35)
        sphere((0.5 * math.cos(a) * 0.85, 0.35 + 0.18 * math.sin(a), z), rnd.uniform(0.14, 0.2), (1, 1, 1), hm, seg=16)
    sphere((0, 0.25, 3.45), 0.34, (1, 1, 0.9), hm)  # chignon
    torus((0, 0.12, 2.18), 0.3, 0.07, mat("hood", (0.85, 0.6, 0.12), rough=0.8), rot=(1.2, 0, 0))
    gold = mat("gold", (0.95, 0.75, 0.3), metal=1, rough=0.2)
    for s in (-1, 1):
        torus((s * 0.57, -0.02, 2.55), 0.08, 0.012, gold, rot=(0, math.pi / 2, 0))
        tube([(s * 0.12, -0.31, 1.95), (s * 0.13, -0.33, 1.65)], 0.015, mat("string", (1, 1, 1), rough=0.6))
    return face("ines", surf, hair, iris=(0.3, 0.18, 0.08), lashes=True)


def yanis():
    surf, sk = body((0.72, 0.5, 0.35), (0.15, 0.58, 0.35), (0.2, 0.28, 0.45), (0.1, 0.1, 0.12), sleeves=(0.12, 0.5, 0.3))
    hair = (0.06, 0.05, 0.05)
    cap_hair(hair, z0=3.08, scale=(0.585, 0.53, 0.4))
    rbox((0, 0.55, 1.8), (0.9, 0.55, 0.9), 0.08, mat("bag", (0.1, 0.65, 0.4), rough=0.5))
    for s in (-1, 1):
        tube([(s * 0.3, -0.3, 2.1), (s * 0.32, -0.32, 1.4)], 0.035, mat("strap", (0.08, 0.08, 0.08), rough=0.5))
    rbox((0, -0.31, 1.55), (0.05, 0.02, 0.7), 0.01, mat("zip", (0.85, 0.85, 0.85), metal=1, rough=0.3))
    stub = mat("stubble", (0.3, 0.22, 0.17), rough=0.9)
    sphere((0, surf(0, 2.3) + 0.05, 2.3), 1, (0.26, 0.1, 0.1), stub)
    return face("yanis", surf, hair, iris=(0.22, 0.14, 0.08), mw=0.26, extra=dict(msurf=lambda x, z: surf(x, z)))


def fatou():
    surf, sk = body((0.42, 0.27, 0.18), None, None, (0.55, 0.3, 0.15), robe=(0.55, 0.18, 0.55))
    wrap = mat("wrap", (0.95, 0.5, 0.1), rough=0.7, sheen=0.5)
    sphere((0, 0.05, 3.08), 1, (0.62, 0.58, 0.55), wrap)
    sphere((0, 0.1, 3.5), 1, (0.5, 0.45, 0.35), wrap, rot=(0.3, 0, 0))
    sphere((0.3, -0.25, 3.45), 0.16, (1, 0.6, 1), mat("wrap2", (0.75, 0.15, 0.55), rough=0.7))
    torus((0, 0.05, 2.95), 0.6, 0.06, mat("wrap2", (0.75, 0.15, 0.55), rough=0.7), scale=(1, 0.95, 1))
    for s in (-1, 1):
        sphere((s * 0.58, -0.02, 2.55), 0.05, (1, 1, 1.4), mat("gold", (0.95, 0.75, 0.3), metal=1, rough=0.2))
    return face("fatou", surf, (0.12, 0.08, 0.06), iris=(0.2, 0.12, 0.06), lashes=True,
                extra=dict(glasses=True))


def lucien():
    surf, sk = body((0.95, 0.78, 0.68), (0.18, 0.32, 0.58), (0.4, 0.3, 0.22), (0.2, 0.15, 0.1))
    grey = (0.78, 0.78, 0.8)
    gm = mat("hair", grey, rough=0.6, sheen=0.4)
    for s in (-1, 1):
        sphere((s * 0.47, 0.12, 2.85), 1, (0.14, 0.3, 0.22), gm)
    sphere((0, 0.35, 2.9), 1, (0.42, 0.18, 0.25), gm)
    tube([(-0.17, surf(-0.17, 2.58) - 0.03, 2.56), (0, surf(0, 2.6) - 0.06, 2.6), (0.17, surf(0.17, 2.58) - 0.03, 2.56)], 0.045, gm)
    for k in range(2):
        rbox((-0.22 + k * 0.44, -0.31, 1.75), (0.22, 0.03, 0.2), 0.03, mat("pocket", (0.15, 0.28, 0.52), rough=0.8))
    tube([(0, -0.25, 2.0), (0.2, -0.32, 1.7), (0.25, -0.31, 1.62)], 0.012, mat("keys", (0.8, 0.8, 0.8), metal=1))
    sphere((0.25, -0.33, 1.58), 0.05, (1, 0.3, 1), mat("keys", (0.8, 0.8, 0.8), metal=1))
    return face("lucien", surf, (0.55, 0.55, 0.58), iris=(0.3, 0.45, 0.6), mw=0.26,
                extra=dict(mouth=(0, 2.47)))


def theo():
    surf, sk = body((0.96, 0.8, 0.7), (0.15, 0.2, 0.35), (0.82, 0.74, 0.58), (0.35, 0.22, 0.12))
    hair = (0.45, 0.3, 0.18)
    hm = cap_hair(hair, z0=3.07, scale=(0.6, 0.54, 0.42))
    sphere((-0.18, -0.25, 3.18), 1, (0.38, 0.2, 0.14), hm, rot=(0, 0.2, 0))
    rbox((0, -0.31, 1.75), (0.32, 0.02, 0.85), 0.03, mat("shirt", (0.97, 0.97, 0.97), rough=0.6))
    tube([(-0.12, -0.31, 2.08), (0, -0.33, 1.6)], 0.012, mat("lanyard", (0.9, 0.2, 0.2), rough=0.5))
    rbox((0.0, -0.34, 1.52), (0.16, 0.02, 0.22), 0.02, mat("badge", (1, 1, 1), rough=0.3))
    return face("theo", surf, hair, iris=(0.3, 0.5, 0.35))


def verdier():
    surf, sk = body((0.93, 0.74, 0.62), (0.12, 0.12, 0.14), (0.12, 0.12, 0.14), (0.05, 0.05, 0.05))
    hair = (0.6, 0.6, 0.62)
    hm = mat("hair", hair, rough=0.25, coat=0.6)
    sphere((0, 0.14, 3.06), 1, (0.59, 0.53, 0.41), hm)
    rbox((0, -0.31, 1.8), (0.28, 0.02, 0.75), 0.03, mat("shirt", (0.95, 0.95, 0.97), rough=0.6))
    cone((0, -0.33, 1.72), 0.07, 0.03, 0.6, mat("tie", (0.75, 0.08, 0.1), rough=0.4), verts=4, rot=(math.pi, 0, 0))
    torus((0.6, -0.12, 1.22), 0.12, 0.025, mat("watch", (0.95, 0.75, 0.3), metal=1, rough=0.2), rot=(0, 0, 0))
    return face("verdier", surf, (0.35, 0.33, 0.33), iris=(0.35, 0.3, 0.25))


BUILDERS = {"I": ines, "Y": yanis, "F": fatou, "LU": lucien, "T": theo, "V": verdier}


def render(code, preview=False):
    C.reset()
    C.MATS.clear()
    C.setup_scene()
    spec = BUILDERS[code]()
    C.frame_camera(margin=0.3)
    sc = bpy.context.scene
    sc.cycles.samples = 12
    states = [("neutre", 0, 0)] if preview else [(e, m, b) for e in C.EMOS for m in (0, 1) for b in (0, 1) if not (m and b)]
    for emo, mo, bl in states:
        coll = C.build_face(spec, emo, mo, bl)
        sc.render.filepath = os.path.join(C.OUT, f"{code}_{emo}_{mo}_{bl}.png")
        bpy.ops.render.render(write_still=True)
        C.clear_face(coll)
        print("OK", code, emo, mo, bl, flush=True)


if __name__ == "__main__":
    for c in [a for a in sys.argv[1:] if not a.startswith("--")]:
        render(c, "--preview" in sys.argv)
