"""Modélise et rend en 3D (Cycles) les personnages de « Ceux de la cuisine ».
Usage : python3 chars.py CODE [CODE...]   -> sprites/CODE_<emo>_<m>_<b>.png
        python3 chars.py CODE --preview    -> un seul rendu (neutre) pour vérifier
"""
import bpy, math, os, sys
from mathutils import Vector

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sprites")
os.makedirs(OUT, exist_ok=True)
EMOS = ["neutre", "joie", "colere", "triste", "surpris", "peur"]
PPU = 150  # pixels par unité Blender


def lin(c):
    return tuple(x ** 2.2 for x in c)


def reset():
    bpy.ops.wm.read_factory_settings(use_empty=True)


MATS = {}


def mat(name, color, metal=0.0, rough=0.5, emit=None, es=0.0, coat=0.0, sheen=0.0, sss=0.0):
    if name in MATS:
        return MATS[name]
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*lin(color), 1)
    b.inputs["Metallic"].default_value = metal
    b.inputs["Roughness"].default_value = rough
    if emit:
        b.inputs["Emission Color"].default_value = (*lin(emit), 1)
        b.inputs["Emission Strength"].default_value = es
    if coat:
        b.inputs["Coat Weight"].default_value = coat
    if sheen:
        b.inputs["Sheen Weight"].default_value = sheen
    if False and sss:
        b.inputs["Subsurface Weight"].default_value = sss
        b.inputs["Subsurface Radius"].default_value = (0.3, 0.15, 0.1)
        b.inputs["Subsurface Scale"].default_value = 0.05
    MATS[name] = m
    return m


def _fin(o, m, smooth=True):
    if smooth:
        for p in o.data.polygons:
            p.use_smooth = True
    if m:
        o.data.materials.append(m)
    return o


def sphere(loc, r=1.0, scale=(1, 1, 1), m=None, rot=(0, 0, 0), seg=40):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=r, location=loc, rotation=rot, segments=seg, ring_count=seg // 2)
    o = bpy.context.object
    o.scale = scale
    return _fin(o, m)


def cone(loc, r1, r2, depth, m=None, verts=48, rot=(0, 0, 0), smooth=True):
    bpy.ops.mesh.primitive_cone_add(vertices=verts, radius1=r1, radius2=r2, depth=depth, location=loc, rotation=rot)
    o = bpy.context.object
    return _fin(o, m, smooth)


def cyl(loc, r, depth, m=None, rot=(0, 0, 0), verts=40):
    bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=r, depth=depth, location=loc, rotation=rot)
    return _fin(bpy.context.object, m)


def torus(loc, R, r, m=None, rot=(0, 0, 0), scale=(1, 1, 1)):
    bpy.ops.mesh.primitive_torus_add(major_radius=R, minor_radius=r, location=loc, rotation=rot,
                                     major_segments=64, minor_segments=16)
    o = bpy.context.object
    o.scale = scale
    return _fin(o, m)


def rbox(loc, dims, bevel, m=None, rot=(0, 0, 0), segs=6):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc, rotation=rot)
    o = bpy.context.object
    o.scale = dims
    bpy.ops.object.transform_apply(scale=True)
    mod = o.modifiers.new("b", "BEVEL")
    mod.width = bevel
    mod.segments = segs
    mod.limit_method = "NONE"
    _fin(o, m)
    return o


def tube(points, radius, m, coll=None):
    cu = bpy.data.curves.new("c", "CURVE")
    cu.dimensions = "3D"
    cu.bevel_depth = radius
    cu.bevel_resolution = 4
    cu.use_fill_caps = True
    sp = cu.splines.new("NURBS")
    sp.points.add(len(points) - 1)
    for i, p in enumerate(points):
        sp.points[i].co = (*p, 1)
    sp.order_u = min(3, len(points))
    sp.use_endpoint_u = True
    o = bpy.data.objects.new("c", cu)
    (coll or bpy.context.scene.collection).objects.link(o)
    o.data.materials.append(m)
    return o


def ell_surf(c, rad):
    cx, cy, cz = c
    a, b, cc = rad

    def f(x, z):
        v = 1 - ((x - cx) / a) ** 2 - ((z - cz) / cc) ** 2
        return cy - b * math.sqrt(max(0.02, v))
    return f


# ------------------------------------------------------------ visage
def build_face(spec, emo, mo, bl):
    """Crée les objets du visage dans une collection 'face' et la renvoie."""
    coll = bpy.data.collections.new("face")
    bpy.context.scene.collection.children.link(coll)
    before = set(bpy.context.scene.objects)
    led = spec.get("style") == "led"
    surf = spec["surf"]
    msurf = spec.get("msurf", surf)
    ink = mat("led", (0, 0.9, 1), emit=(0, 0.9, 1), es=6) if led else mat("ink_" + spec["name"], spec.get("ink", (0.12, 0.09, 0.1)), rough=0.4)
    white = mat("eyewhite", (0.97, 0.97, 0.97), rough=0.15, coat=1)
    iris = mat("iris_" + spec["name"], spec.get("iris", (0.25, 0.18, 0.12)), rough=0.15, coat=1)
    pupil = mat("pupil", (0.02, 0.02, 0.03), rough=0.1, coat=1)
    hl = mat("hl", (1, 1, 1), emit=(1, 1, 1), es=4)
    mouthm = mat("mouthin", (0.35, 0.06, 0.1), rough=0.6)
    tongue = mat("tongue", (0.95, 0.45, 0.5), rough=0.5)
    r = spec["r"]
    big = 1.18 if emo == "surpris" else 1.0
    for i, (ex, ez) in enumerate(spec["eyes"]):
        side = -1 if i == 0 else 1
        ys = surf(ex, ez)
        rr = r * big
        if led:
            if bl:
                tube([(ex - rr, ys - 0.03, ez), (ex, ys - 0.03, ez - 0.02), (ex + rr, ys - 0.03, ez)], 0.035, ink)
            elif emo == "joie":
                tube([(ex - rr, ys - 0.03, ez - rr * .3), (ex, ys - 0.03, ez + rr * .5), (ex + rr, ys - 0.03, ez - rr * .3)], 0.04, ink)
            else:
                rbox((ex, ys - 0.02, ez), (rr * 1.0, 0.04, rr * 1.7), rr * 0.45, ink)
        else:
            if bl:
                tube([(ex - rr, ys - 0.02, ez), (ex, ys - 0.06, ez - rr * .35), (ex + rr, ys - 0.02, ez)], 0.03, ink)
            else:
                cy = ys + rr * 0.25
                sphere((ex, cy, ez), rr, (1, 0.55, 1.15), white)
                front = cy - rr * 0.55
                ir = rr * (0.48 if emo == "peur" else 0.66)
                sphere((ex, front + ir * 0.12, ez - rr * 0.08), ir, (1, 0.3, 1.08), iris)
                pr = ir * (0.38 if emo == "peur" else 0.52)
                sphere((ex, front - 0.005, ez - rr * 0.08), pr, (1, 0.3, 1.1), pupil)
                sphere((ex + rr * 0.25, front - 0.03, ez + rr * 0.25), rr * 0.13, (1, 0.5, 1), hl)
                if emo == "triste":
                    sphere((ex + side * rr * 0.55, ys - 0.04, ez - rr * 1.35), rr * 0.18, (0.8, 0.6, 1.3),
                           mat("tear", (0.5, 0.75, 1), rough=0.02, coat=1))
            if spec.get("lashes") and not bl:
                for k in range(3):
                    x0 = ex + side * (rr * 0.45 + k * rr * 0.22)
                    z0 = ez + rr * 1.0 - k * rr * 0.12
                    tube([(x0, ys - 0.02, z0), (x0 + side * rr * 0.22, ys - 0.03, z0 + rr * 0.35)], rr * 0.06, ink)
            if spec.get("glasses") and not bl:
                torus((ex, ys - 0.05, ez), rr * 1.35, rr * 0.1, mat("gold", (0.85, 0.65, 0.3), metal=1, rough=0.25),
                      rot=(math.pi / 2, 0, 0))
        # sourcils
        bw = spec.get("brow", 0.035)
        bz = ez + rr * 1.15 * 1.15 + 0.06 + (0.08 if emo in ("surpris", "peur") else 0)
        inner, outer = ex - side * rr * 0.9, ex + side * rr * 0.95
        if emo == "colere":
            zi, zo = bz - 0.1, bz + 0.04
        elif emo in ("triste", "peur"):
            zi, zo = bz + 0.07, bz - 0.04
        else:
            zi, zo = bz, bz + 0.02
        mid = (inner + outer) / 2
        tube([(inner, surf(inner, zi) - 0.02, zi), (mid, surf(mid, (zi + zo) / 2) - 0.04, (zi + zo) / 2 + 0.02),
              (outer, surf(outer, zo) - 0.02, zo)], bw, ink)
    # bouche
    mx, mz = spec["mouth"]
    mw = spec["mw"]
    ys = msurf(mx, mz) - 0.01
    if mo and not led:
        if emo == "surpris":
            sx, sz = mw * 0.28, mw * 0.32
        else:
            sx, sz = mw * 0.5, mw * (0.28 if emo in ("joie", "colere") else 0.2)
        sphere((mx, ys + 0.02, mz), 1, (sx, 0.06, sz), mouthm)
        sphere((mx, ys + 0.0, mz - sz * 0.45), 1, (sx * 0.55, 0.05, sz * 0.4), tongue)
    elif mo and led:
        if emo == "surpris":
            torus((mx, ys - 0.02, mz), mw * 0.18, 0.035, ink, rot=(math.pi / 2, 0, 0))
        else:
            rbox((mx, ys - 0.02, mz), (mw, 0.04, mw * 0.3), mw * 0.12, ink)
    else:
        w = spec.get("mthick", 0.03)
        h = mw * 0.5
        pts = None
        if emo == "joie":
            pts = [(-h, 0.06), (-h * .5, -h * .45), (0, -h * .6), (h * .5, -h * .45), (h, 0.06)]
            w *= 1.3
        elif emo == "triste":
            pts = [(-h * .8, -h * .25), (0, h * .15), (h * .8, -h * .25)]
        elif emo == "colere":
            pts = [(-h * .8, -0.02), (0, -0.05), (h * .8, 0.02)]
        elif emo == "surpris":
            torus((mx, ys - 0.01, mz), mw * 0.13, w, ink, rot=(math.pi / 2, 0, 0))
        elif emo == "peur":
            pts = [(-h * .8 + k * h * .2, (0.025 if k % 2 else -0.025)) for k in range(9)]
        else:
            pts = [(-h * .7, 0.03), (0, -h * .18), (h * .7, 0.03)]
        if pts:
            tube([(mx + px, msurf(mx + px, mz + pz) - 0.015, mz + pz) for px, pz in pts], w, ink)
    for o in set(bpy.context.scene.objects) - before:
        for c in o.users_collection:
            c.objects.unlink(o)
        coll.objects.link(o)
    return coll


def clear_face(coll):
    for o in list(coll.objects):
        bpy.data.objects.remove(o, do_unlink=True)
    bpy.data.collections.remove(coll)


# ------------------------------------------------------------ personnages
def lola():
    cream = mat("cream", (0.99, 0.93, 0.86), rough=0.65, sheen=0.6, sss=0.15)
    pink = mat("pink", (0.96, 0.62, 0.72), rough=0.5, sheen=0.4)
    satin = mat("satin", (0.95, 0.55, 0.68), rough=0.25, coat=0.6)
    pearl = mat("pearl", (0.98, 0.96, 0.94), rough=0.12, coat=1)
    sphere((0, 0, 0.85), 1, (0.82, 0.72, 0.88), cream)
    sphere((-0.32, -0.55, 0.16), 0.22, (1, 1.2, 0.7), cream)
    sphere((0.32, -0.55, 0.16), 0.22, (1, 1.2, 0.7), cream)
    tube([(0.6, 0.35, 0.3), (1.15, 0.3, 0.6), (1.05, 0.2, 1.3), (0.8, 0.15, 1.55)], 0.14, cream)
    hc, hr = (0, 0, 2.05), (1.0, 0.85, 0.88)
    sphere(hc, 1, hr, cream)
    for s in (-1, 1):
        cone((s * 0.62, 0.05, 2.78), 0.36, 0.02, 0.7, cream, rot=(0, s * 0.45, 0))
        cone((s * 0.6, -0.08, 2.74), 0.22, 0.01, 0.5, pink, rot=(0.1, s * 0.45, 0))
    surf = ell_surf(hc, hr)
    for s in (-1, 1):
        sphere((0.42 + s * 0.24, surf(0.42, 2.78) + 0.05, 2.8), 1, (0.24, 0.12, 0.17), satin, rot=(0, s * 0.3, 0))
    sphere((0.42, surf(0.42, 2.78) - 0.03, 2.8), 0.1, (1, 1, 1), satin)
    for s in (-1, 1):
        sphere((s * 0.14, surf(s * 0.14, 1.78) + 0.06, 1.78), 0.19, (1, 0.6, 0.85), cream)
        sphere((s * 0.58, surf(s * 0.58, 1.82) + 0.04, 1.82), 0.16, (1, 0.3, 0.7), mat("blush", (0.98, 0.7, 0.75), rough=0.7))
        for k, dz in enumerate((0.0, -0.07)):
            tube([(s * 0.28, surf(0.28, 1.8) - 0.02, 1.8 + dz), (s * 0.7, surf(0.7, 1.82) - 0.1, 1.84 + dz * 1.6),
                  (s * 1.05, -0.55, 1.9 + dz * 2)], 0.008, mat("whisk", (0.75, 0.72, 0.7)))
    sphere((0, surf(0, 1.9) - 0.04, 1.9), 0.07, (1.3, 0.7, 0.9), pink)
    for i in range(11):
        a = math.pi * (0.12 + 0.76 * i / 10)
        x = -0.62 * math.cos(a)
        z = 1.38 - 0.18 * math.sin(a)
        sphere((x, -0.62 * math.sin(a) - 0.08, z), 0.075, (1, 1, 1), pearl, seg=20)
    return dict(name="lola", surf=surf, eyes=[(-0.38, 2.12), (0.38, 2.12)], r=0.25, iris=(0.3, 0.68, 0.42),
                mouth=(0, 1.7), mw=0.36, lashes=True, brow=0.022, ink=(0.18, 0.12, 0.13))


def toaster_body(color_mat, slot_mat):
    rbox((0, 0, 0.95), (1.9, 1.2, 1.8), 0.32, color_mat, segs=8)
    for s in (-1, 1):
        rbox((s * 0.42, 0, 1.84), (0.45, 0.85, 0.06), 0.03, slot_mat)
        cyl((s * 0.7, -0.38, 0.03), 0.09, 0.08, mat("rubber", (0.05, 0.05, 0.05), rough=0.8))
        cyl((s * 0.7, 0.38, 0.03), 0.09, 0.08, mat("rubber", (0.05, 0.05, 0.05), rough=0.8))


def gaston():
    chrome = mat("chrome", (0.82, 0.84, 0.88), metal=1, rough=0.22)
    dark = mat("slot", (0.05, 0.05, 0.06), rough=0.5)
    toaster_body(chrome, dark)
    rbox((1.0, -0.15, 1.25), (0.14, 0.18, 0.32), 0.05, mat("lever", (0.1, 0.1, 0.12), rough=0.3))
    cyl((1.0, -0.15, 0.6), 0.13, 0.1, mat("knob", (0.1, 0.1, 0.12), rough=0.3), rot=(0, math.pi / 2, 0))
    for s in (-1, 1):
        tube([(s * 0.9, 0, 0.95), (s * 1.18, -0.15, 0.7), (s * 1.2, -0.3, 0.42)], 0.065, mat("arm", (0.55, 0.57, 0.62), metal=1, rough=0.35))
        sphere((s * 1.2, -0.32, 0.38), 0.11, (1, 1, 1), mat("arm", (0.55, 0.57, 0.62), metal=1, rough=0.35))
    sphere((0.6, -0.6, 0.45), 0.12, (1, 0.2, 1), mat("dent", (0.65, 0.66, 0.7), metal=1, rough=0.5))
    return dict(name="gaston", surf=lambda x, z: -0.6, eyes=[(-0.36, 1.15), (0.36, 1.15)], r=0.19,
                mouth=(0, 0.62), mw=0.48, brow=0.055, mthick=0.04, ink=(0.12, 0.11, 0.11), iris=(0.3, 0.25, 0.2))


def neo():
    black = mat("gloss", (0.03, 0.03, 0.04), rough=0.12, coat=1)
    toaster_body(black, mat("silver", (0.8, 0.8, 0.82), metal=1, rough=0.2))
    rbox((0, -0.6, 0.98), (1.35, 0.05, 1.05), 0.12, mat("screen", (0.01, 0.02, 0.05), rough=0.05, coat=1))
    led = mat("led", (0, 0.9, 1), emit=(0, 0.9, 1), es=6)
    for k, rr in enumerate((0.12, 0.22, 0.32)):
        pts = [(0.7 + rr * math.cos(a), 0, 1.95 + rr * math.sin(a)) for a in (math.pi * 0.25, math.pi * 0.5, math.pi * 0.75)]
        tube(pts, 0.025, led)
    sphere((0.7, 0, 1.97), 0.04, (1, 1, 1), led)
    bpy.ops.object.text_add(location=(-0.2, -0.63, 0.25), rotation=(math.pi / 2, 0, 0))
    t = bpy.context.object
    t.data.body = "NEO"
    t.data.size = 0.2
    t.data.materials.append(led)
    return dict(name="neo", style="led", surf=lambda x, z: -0.62, eyes=[(-0.3, 1.1), (0.3, 1.1)], r=0.15,
                mouth=(0, 0.72), mw=0.45, brow=0.03)


def berthe():
    alu = mat("alu", (0.78, 0.79, 0.82), metal=1, rough=0.4)
    blk = mat("bakelite", (0.04, 0.04, 0.04), rough=0.35, coat=0.5)
    rot8 = (0, 0, math.pi / 8)
    cone((0, 0, 0.45), 0.72, 0.58, 0.9, alu, verts=8, rot=rot8, smooth=False)
    cone((0, 0, 0.97), 0.6, 0.6, 0.14, mat("alu2", (0.6, 0.61, 0.64), metal=1, rough=0.5), verts=8, rot=rot8, smooth=False)
    cone((0, 0, 1.6), 0.6, 0.76, 1.12, alu, verts=8, rot=rot8, smooth=False)
    cone((0, 0, 2.28), 0.78, 0.35, 0.26, alu, verts=8, rot=rot8, smooth=False)
    sphere((0, 0, 2.47), 0.13, (1, 1, 0.9), blk)
    cone((0.8, -0.0, 2.08), 0.18, 0.04, 0.4, alu, verts=16, rot=(0, 1.0, 0))
    rbox((-1.02, 0, 1.6), (0.2, 0.26, 0.95), 0.08, blk)
    for z in (2.0, 1.2):
        rbox((-0.82, 0, z), (0.3, 0.14, 0.12), 0.04, blk)
    red = mat("scarf", (0.8, 0.15, 0.2), rough=0.7, sheen=0.5)
    torus((0, 0, 1.06), 0.7, 0.09, red, scale=(1, 1, 1))
    sphere((0.35, -0.6, 0.98), 0.14, (1, 0.6, 1), red)
    tube([(0.35, -0.65, 0.95), (0.45, -0.7, 0.75), (0.55, -0.68, 0.6)], 0.06, red)
    ap = math.cos(math.pi / 8)

    def surf(x, z):
        rad = 0.6 + (z - 1.04) / 1.12 * 0.16
        return -rad * ap
    return dict(name="berthe", surf=surf, eyes=[(-0.22, 1.72), (0.22, 1.72)], r=0.12, iris=(0.4, 0.28, 0.2),
                mouth=(0, 1.36), mw=0.26, lashes=True, glasses=True, ink=(0.15, 0.1, 0.1))


def rosa():
    terra = mat("terra", (0.82, 0.45, 0.3), rough=0.85)
    cone((0, 0, 0.55), 0.52, 0.72, 1.1, terra)
    torus((0, 0, 1.12), 0.76, 0.1, mat("terra2", (0.86, 0.5, 0.34), rough=0.8))
    cyl((0, 0, 1.12), 0.7, 0.04, mat("soil", (0.2, 0.13, 0.08), rough=1))
    tube([(0, 0, 1.1), (0.05, 0, 1.9), (-0.02, 0, 2.7)], 0.05, mat("stem", (0.4, 0.28, 0.15), rough=0.8))
    g1 = mat("leaf1", (0.3, 0.65, 0.35), rough=0.35, coat=0.3)
    g2 = mat("leaf2", (0.2, 0.52, 0.3), rough=0.35, coat=0.3)
    import random
    rnd = random.Random(3)
    for k in range(26):
        a = k * 2.4
        z = 1.35 + (k % 13) * 0.11
        x, y = 0.42 * math.cos(a), 0.35 * math.sin(a)
        sphere((x, y, z), 1, (0.45, 0.22, 0.09), g1 if k % 2 else g2, rot=(rnd.uniform(-0.4, 0.4), rnd.uniform(-0.6, 0.6), a))
    for k in range(5):
        a = k * 2 * math.pi / 5
        sphere((0.25 + 0.1 * math.cos(a), -0.15, 2.75 + 0.1 * math.sin(a)), 0.08, (1, 0.5, 1),
               mat("petal", (1, 0.5, 0.7), rough=0.5, sheen=0.5))
    sphere((0.25, -0.2, 2.75), 0.06, (1, 1, 1), mat("pistil", (1, 0.85, 0.3), rough=0.5))

    def surf(x, z):
        rad = 0.52 + z / 1.1 * 0.2
        return -math.sqrt(max(0.01, rad * rad - x * x))
    for s in (-1, 1):
        sphere((s * 0.38, surf(s * 0.38, 0.5) + 0.04, 0.5), 0.11, (1, 0.3, 0.7), mat("blush2", (0.95, 0.55, 0.5), rough=0.7))
    return dict(name="rosa", surf=surf, eyes=[(-0.21, 0.72), (0.21, 0.72)], r=0.13, iris=(0.3, 0.2, 0.12),
                mouth=(0, 0.4), mw=0.26, lashes=True, ink=(0.2, 0.1, 0.08))


def pixel():
    rbox((0, 0, 1.05), (1.15, 0.13, 2.05), 0.14, mat("phone", (0.05, 0.05, 0.07), rough=0.2, coat=1))
    rbox((0, -0.07, 1.05), (1.0, 0.02, 1.88), 0.1, mat("pscreen", (0.35, 0.4, 0.95), rough=0.1, emit=(0.4, 0.45, 1.0), es=0.35))
    rbox((0, -0.085, 1.88), (0.28, 0.02, 0.07), 0.03, mat("phone", (0.05, 0.05, 0.07), rough=0.2, coat=1))
    cols = [(1, 0.8, 0.3), (0.4, 0.9, 0.55), (1, 0.45, 0.45), (1, 1, 1)]
    for i, c in enumerate(cols):
        rbox((-0.33 + i * 0.22, -0.085, 0.35), (0.15, 0.02, 0.15), 0.04, mat(f"app{i}", c, rough=0.3, emit=c, es=0.6))
    for s in (-1, 1):
        tube([(s * 0.57, 0, 1.0), (s * 0.85, -0.1, 0.7), (s * 0.85, -0.25, 0.45)], 0.05, mat("parm", (0.1, 0.1, 0.12), rough=0.4))
    return dict(name="pixel", surf=lambda x, z: -0.09, eyes=[(-0.24, 1.38), (0.24, 1.38)], r=0.15,
                iris=(0.15, 0.25, 0.6), mouth=(0, 0.98), mw=0.32, ink=(0.08, 0.06, 0.15))


def brutus():
    fawn = mat("fawn", (0.85, 0.55, 0.3), rough=0.7, sheen=0.5)
    whitef = mat("whitefur", (0.97, 0.94, 0.9), rough=0.7, sheen=0.5)
    darkf = mat("darkfur", (0.45, 0.3, 0.2), rough=0.7, sheen=0.4)
    sphere((0, 0.1, 0.8), 1, (1.05, 0.85, 0.82), fawn)
    sphere((0, -0.5, 0.72), 1, (0.55, 0.4, 0.62), whitef)
    for s in (-1, 1):
        sphere((s * 0.48, -0.55, 0.22), 1, (0.26, 0.32, 0.24), fawn)
    hc, hr = (0, -0.15, 1.95), (1.08, 0.8, 0.82)
    sphere(hc, 1, hr, fawn)
    for s in (-1, 1):
        sphere((s * 0.98, 0.0, 2.38), 1, (0.3, 0.1, 0.2), darkf, rot=(0.3, s * 1.2, s * 0.4))
    mc, mr = (0, -0.82, 1.62), (0.6, 0.32, 0.38)
    sphere(mc, 1, mr, whitef)
    msurf = ell_surf(mc, mr)
    sphere((0, msurf(0, 1.82) + 0.04, 1.84), 1, (0.2, 0.11, 0.13), mat("nose", (0.08, 0.05, 0.05), rough=0.25, coat=1))
    for s in (-1, 1):
        for x in (0.2, 0.3):
            sphere((s * x, msurf(s * x, 1.7) - 0.005, 1.7), 0.02, (1, 1, 1), darkf, seg=12)
    for k, z in enumerate((2.5, 2.6)):
        tube([(-0.3, hc[1] - hr[1] * 0.62, z - 0.02), (0, hc[1] - hr[1] * 0.68, z + 0.03), (0.3, hc[1] - hr[1] * 0.62, z - 0.02)], 0.025, darkf)
    for s in (-1, 1):
        cone((s * 0.22, msurf(s * 0.22, 1.42) - 0.02, 1.47), 0.045, 0.0, 0.12, mat("tooth", (1, 1, 0.95), rough=0.3))
    torus((0, 0.0, 1.32), 0.78, 0.09, mat("collar", (0.85, 0.12, 0.12), rough=0.4), scale=(1, 0.95, 1))
    cyl((0, -0.86, 1.15), 0.12, 0.04, mat("tag", (1, 0.8, 0.25), metal=1, rough=0.2), rot=(math.pi / 2, 0, 0))
    return dict(name="brutus", surf=ell_surf(hc, hr), msurf=msurf, eyes=[(-0.42, 2.2), (0.42, 2.2)], r=0.17,
                iris=(0.4, 0.25, 0.12), mouth=(0, 1.55), mw=0.46, brow=0.045, ink=(0.2, 0.12, 0.08))


BUILDERS = {"L": lola, "G": gaston, "NEO": neo, "B": berthe, "R": rosa, "P": pixel, "BR": brutus}


def setup_scene():
    sc = bpy.context.scene
    sc.render.engine = "CYCLES"
    sc.cycles.samples = 10
    sc.cycles.max_bounces = 4
    sc.cycles.use_adaptive_sampling = True
    sc.render.use_persistent_data = True
    sc.cycles.use_denoising = True
    sc.cycles.device = "CPU"
    sc.render.film_transparent = True
    sc.view_settings.view_transform = "AgX"
    sc.view_settings.look = "AgX - Punchy"
    w = bpy.data.worlds.new("w")
    sc.world = w
    w.use_nodes = True
    w.node_tree.nodes["Background"].inputs[0].default_value = (0.75, 0.72, 0.75, 1)
    w.node_tree.nodes["Background"].inputs[1].default_value = 0.55
    for loc, en, size in [((-3, -5, 6), 1200, 4), ((4.5, -3.5, 3), 450, 3), ((2, 5, 5), 900, 3)]:
        bpy.ops.object.light_add(type="AREA", location=loc)
        L = bpy.context.object
        L.data.energy = en
        L.data.size = size
        d = Vector((0, 0, 1.2)) - Vector(loc)
        L.rotation_euler = d.to_track_quat("-Z", "Y").to_euler()


def frame_camera(margin=0.25):
    objs = [o for o in bpy.context.scene.objects if o.type in ("MESH", "CURVE", "FONT")]
    xs, ys, zs = [], [], []
    for o in objs:
        for c in o.bound_box:
            v = o.matrix_world @ Vector(c)
            xs.append(v.x); ys.append(v.y); zs.append(v.z)
    tilt = math.radians(9)
    x0, x1 = min(xs) - margin, max(xs) + margin
    # hauteur projetée approx
    z0 = min(zs) - margin - 0.15
    z1 = max(zs) + margin
    wbu, hbu = x1 - x0, (z1 - z0)
    sc = bpy.context.scene
    sc.render.resolution_x = int(wbu * PPU)
    sc.render.resolution_y = int(hbu * PPU)
    bpy.ops.object.camera_add()
    cam = bpy.context.object
    cam.data.type = "ORTHO"
    cam.data.ortho_scale = max(wbu, hbu)
    cx, cz = (x0 + x1) / 2, (z0 + z1) / 2
    cam.rotation_euler = (math.pi / 2 - tilt, 0, 0)
    cam.location = (cx, -20, cz + 20 * math.tan(tilt))
    sc.camera = cam
    # sol attrape-ombre
    bpy.ops.mesh.primitive_plane_add(size=30, location=(0, 0, 0))
    bpy.context.object.is_shadow_catcher = True


def render_char(code, preview=False):
    reset()
    MATS.clear()
    setup_scene()
    spec = BUILDERS[code]()
    frame_camera()
    sc = bpy.context.scene
    states = [("neutre", 0, 0)] if preview else [(e, m, b) for e in EMOS for m in (0, 1) for b in (0, 1) if not (m and b)]
    for emo, mo, bl in states:
        coll = build_face(spec, emo, mo, bl)
        sc.render.filepath = os.path.join(OUT, f"{code}_{emo}_{mo}_{bl}.png")
        bpy.ops.render.render(write_still=True)
        clear_face(coll)
        print("OK", code, emo, mo, bl, flush=True)


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    for c in args:
        render_char(c, preview="--preview" in sys.argv)
