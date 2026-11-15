"""Décors 3D : python3 bg.py cuisine|nuit|cartons|salon [--fast]  -> bg/<nom>.png (1080x1920)"""
import bpy, math, os, sys
from mathutils import Vector
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import chars as C

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bg")
os.makedirs(OUT, exist_ok=True)
lin = C.lin


def noise_mat(name, c1, c2, scale=6.0, rough=0.5, stretch=(1, 1, 1), detail=4.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    b = nt.nodes["Principled BSDF"]
    tc = nt.nodes.new("ShaderNodeTexCoord")
    mp = nt.nodes.new("ShaderNodeMapping")
    mp.inputs["Scale"].default_value = stretch
    nz = nt.nodes.new("ShaderNodeTexNoise")
    nz.inputs["Scale"].default_value = scale
    nz.inputs["Detail"].default_value = detail
    ramp = nt.nodes.new("ShaderNodeValToRGB")
    ramp.color_ramp.elements[0].color = (*lin(c1), 1)
    ramp.color_ramp.elements[1].color = (*lin(c2), 1)
    nt.links.new(tc.outputs["Object"], mp.inputs["Vector"])
    nt.links.new(mp.outputs["Vector"], nz.inputs["Vector"])
    nt.links.new(nz.outputs["Fac"], ramp.inputs["Fac"])
    nt.links.new(ramp.outputs["Color"], b.inputs["Base Color"])
    b.inputs["Roughness"].default_value = rough
    return m


def tile_mat(name, c1, c2, mortar, scale=4.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    b = nt.nodes["Principled BSDF"]
    tc = nt.nodes.new("ShaderNodeTexCoord")
    br = nt.nodes.new("ShaderNodeTexBrick")
    br.offset = 0.0
    br.inputs["Color1"].default_value = (*lin(c1), 1)
    br.inputs["Color2"].default_value = (*lin(c2), 1)
    br.inputs["Mortar"].default_value = (*lin(mortar), 1)
    br.inputs["Scale"].default_value = scale
    br.inputs["Mortar Size"].default_value = 0.015
    br.inputs["Brick Width"].default_value = 0.5
    br.inputs["Row Height"].default_value = 0.5
    nt.links.new(tc.outputs["Object"], br.inputs["Vector"])
    nt.links.new(br.outputs["Color"], b.inputs["Base Color"])
    b.inputs["Roughness"].default_value = 0.15
    b.inputs["Coat Weight"].default_value = 0.4
    return m


def plane(loc, size, m, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_plane_add(size=1, location=loc, rotation=rot)
    o = bpy.context.object
    o.scale = (size[0], size[1], 1)
    bpy.ops.object.transform_apply(scale=True)
    o.data.materials.append(m)
    return o


def area(loc, target, energy, size, color=(1, 1, 1)):
    bpy.ops.object.light_add(type="AREA", location=loc)
    L = bpy.context.object
    L.data.energy = energy
    L.data.size = size
    L.data.color = color
    L.rotation_euler = (Vector(target) - Vector(loc)).to_track_quat("-Z", "Y").to_euler()
    return L


def point(loc, energy, color, radius=0.2):
    bpy.ops.object.light_add(type="POINT", location=loc)
    L = bpy.context.object
    L.data.energy = energy
    L.data.color = color
    L.data.shadow_soft_size = radius


def world(color, strength):
    sc = bpy.context.scene
    w = bpy.data.worlds.new("w")
    sc.world = w
    w.use_nodes = True
    w.node_tree.nodes["Background"].inputs[0].default_value = (*lin(color), 1)
    w.node_tree.nodes["Background"].inputs[1].default_value = strength


def kitchen(night=False, boxes=False):
    M = C.mat
    wood = noise_mat("wood", (0.72, 0.5, 0.32), (0.58, 0.38, 0.22), scale=3, rough=0.35, stretch=(0.15, 1, 4))
    # plan de travail
    C.rbox((0, 0.3, -0.25), (14, 4.2, 0.5), 0.04, wood)
    C.rbox((0, 0.3, -3), (14, 3.9, 5), 0.02, M("cab", (0.93, 0.8, 0.78) if not night else (0.55, 0.5, 0.6), rough=0.4))
    for x in (-4.5, -1.5, 1.5, 4.5):
        C.rbox((x, -1.68, -1.6), (2.7, 0.06, 2.2), 0.05, M("door", (0.96, 0.85, 0.83), rough=0.35))
        C.rbox((x, -1.75, -0.8), (0.6, 0.06, 0.07), 0.03, M("handle", (0.8, 0.7, 0.4), metal=1, rough=0.3))
    # mur carrelé
    wall = tile_mat("tiles", (0.98, 0.86, 0.86), (0.96, 0.82, 0.83), (1, 1, 1), scale=1.3)
    plane((0, 2.4, 4), (16, 10, 1), wall, rot=(math.pi / 2, 0, 0))
    # placards hauts
    for x in (-4.6, -1.6):
        C.rbox((x, 1.9, 5.6), (2.9, 1.0, 2.6), 0.06, M("upper", (0.78, 0.88, 0.85), rough=0.4))
        C.rbox((x + 1.0, 1.36, 4.6), (0.07, 0.06, 0.5), 0.03, M("handle", (0.8, 0.7, 0.4), metal=1, rough=0.3))
    # fenêtre
    C.rbox((3.6, 2.35, 3.3), (3.6, 0.2, 3.4), 0.05, M("frame", (1, 1, 1), rough=0.3))
    sky = (0.12, 0.16, 0.35) if night else (0.72, 0.87, 1.0)
    plane((3.6, 2.22, 3.3), (3.2, 3.0, 1), M("sky", sky, emit=sky, es=1.5 if not night else 0.6), rot=(math.pi / 2, 0, 0))
    C.rbox((3.6, 2.15, 3.3), (0.08, 0.1, 3.0), 0.02, M("frame", (1, 1, 1), rough=0.3))
    C.rbox((3.6, 2.15, 3.3), (3.2, 0.1, 0.08), 0.02, M("frame", (1, 1, 1), rough=0.3))
    if night:
        C.sphere((3.1, 2.18, 4.3), 0.32, (1, 0.1, 1), M("moon", (1, 0.97, 0.85), emit=(1, 0.97, 0.85), es=6))
    # rebord fenêtre + petits pots
    C.rbox((3.6, 1.9, 1.55), (3.8, 0.7, 0.12), 0.03, M("frame", (1, 1, 1), rough=0.3))
    # étagère avec bocaux
    C.rbox((-3.0, 2.1, 3.0), (4.0, 0.5, 0.1), 0.02, wood)
    for i, (x, h, c) in enumerate([(-4.4, 0.8, (0.95, 0.75, 0.4)), (-3.6, 1.0, (0.85, 0.55, 0.35)), (-2.8, 0.7, (0.9, 0.9, 0.85)), (-2.0, 0.9, (0.7, 0.4, 0.3))]):
        C.cyl((x, 2.1, 3.05 + h / 2), 0.28, h, M(f"jar{i}", c, rough=0.2, coat=1))
        C.cyl((x, 2.1, 3.1 + h), 0.3, 0.12, M("lid", (0.85, 0.75, 0.6), metal=1, rough=0.3))
    # pot à ustensiles + planche, au fond du plan de travail
    C.cyl((-5.3, 1.7, 0.45), 0.4, 0.9, M("utpot", (0.3, 0.55, 0.6), rough=0.3, coat=1))
    for k in range(3):
        C.cyl((-5.3 + (k - 1) * 0.15, 1.7, 1.2), 0.04, 1.0, M("spoon", (0.6, 0.45, 0.3), rough=0.6), rot=(0, (k - 1) * 0.2, 0))
    C.rbox((5.6, 2.0, 0.8), (1.6, 0.12, 1.8), 0.08, wood, rot=(-0.15, 0, 0))
    # suspension
    C.cyl((-0.5, 0.3, 8.5), 0.02, 3.0, M("cable", (0.1, 0.1, 0.1)))
    C.cone((-0.5, 0.3, 6.9), 0.7, 0.15, 0.6, M("shade", (0.95, 0.75, 0.3), rough=0.4))
    if boxes:
        cb = noise_mat("cardboard", (0.78, 0.6, 0.4), (0.7, 0.52, 0.34), scale=20, rough=0.9)
        tape = M("tape", (0.85, 0.75, 0.55), rough=0.4)
        for (x, y, z, sx, sy, sz, rz) in [(-2.6, 1.6, 0.9, 2.2, 1.4, 1.8, 0.1), (-0.6, 1.8, 0.7, 1.8, 1.2, 1.4, -0.08),
                                          (-2.2, 1.7, 2.35, 1.6, 1.1, 1.1, 0.05), (2.4, 1.7, 0.8, 1.8, 1.2, 1.6, 0.12)]:
            C.rbox((x, y, z), (sx, sy, sz), 0.03, cb, rot=(0, 0, rz))
            C.rbox((x, y - sy / 2 - 0.01, z), (0.35, 0.02, sz * 1.0), 0.005, tape, rot=(0, 0, rz))
        bpy.ops.object.text_add(location=(-3.4, 0.88, 0.7), rotation=(math.pi / 2, 0, 0.1))
        t = bpy.context.object
        t.data.body = "FRAGILE"
        t.data.size = 0.35
        t.data.materials.append(M("red", (0.75, 0.1, 0.1), rough=0.5))
    if night:
        world((0.18, 0.2, 0.42), 0.35)
        point((-0.5, 0.3, 6.4), 450, (1, 0.75, 0.45), 0.3)
        C.sphere((-0.5, 0.3, 6.55), 0.18, (1, 1, 1), M("bulb", (1, 0.8, 0.5), emit=(1, 0.8, 0.5), es=12))
        area((5, -2, 5), (0, 1, 0), 300, 6, (0.5, 0.6, 1.0))
    else:
        world((1.0, 0.95, 0.9), 0.8)
        area((-5, -6, 9), (0, 1, 0), 2500, 8, (1, 0.95, 0.88))
        area((6, 0.5, 4), (0, 1, 1), 900, 4, (0.8, 0.9, 1))


def salon():
    M = C.mat
    floor = noise_mat("parquet", (0.62, 0.42, 0.26), (0.5, 0.32, 0.2), scale=2, rough=0.35, stretch=(0.2, 3, 1))
    plane((0, 3, 0), (20, 14, 1), floor)
    wall = noise_mat("paint", (0.86, 0.78, 0.7), (0.83, 0.75, 0.67), scale=40, rough=0.8)
    plane((0, 4.5, 5), (20, 10, 1), wall, rot=(math.pi / 2, 0, 0))
    C.rbox((0, 4.45, 0.15), (20, 0.1, 0.3), 0.01, M("plinth", (1, 1, 1), rough=0.4))
    # canapé
    blue = noise_mat("velvet", (0.38, 0.52, 0.66), (0.33, 0.47, 0.6), scale=30, rough=0.9)
    C.rbox((3.2, 3.4, 0.8), (6.5, 1.8, 1.0), 0.25, blue)
    C.rbox((3.2, 4.0, 1.9), (6.5, 0.7, 1.8), 0.3, blue)
    for x in (0.2, 6.2):
        C.rbox((x, 3.4, 1.4), (0.7, 1.9, 1.6), 0.3, blue)
    for x, c in ((1.8, (0.95, 0.75, 0.4)), (4.4, (0.9, 0.55, 0.6))):
        C.rbox((x, 3.4, 1.85), (1.2, 0.4, 1.0), 0.2, M(f"cush{x}", c, rough=0.9, sheen=0.5), rot=(0.2, 0, 0.1))
    # tapis
    C.cyl((0, 0.5, 0.02), 4.2, 0.04, noise_mat("rug", (0.92, 0.88, 0.8), (0.86, 0.8, 0.72), scale=60, rough=1))
    # cadre + lampadaire + plante
    C.rbox((-3.8, 4.38, 4.6), (2.6, 0.1, 1.9), 0.04, M("pframe", (0.25, 0.2, 0.15), rough=0.4))
    C.rbox((-3.8, 4.32, 4.6), (2.3, 0.04, 1.6), 0.02, noise_mat("art", (0.95, 0.6, 0.4), (0.4, 0.6, 0.75), scale=1.5, rough=0.6))
    C.cyl((-6.2, 3.5, 2.5), 0.05, 5, M("pole", (0.15, 0.15, 0.15), metal=1, rough=0.3))
    C.cone((-6.2, 3.5, 5.2), 0.8, 0.45, 0.8, M("lshade", (1, 0.95, 0.85), rough=0.7, emit=(1, 0.85, 0.6), es=1.5))
    point((-6.2, 3.3, 4.9), 300, (1, 0.8, 0.55), 0.4)
    world((0.95, 0.88, 0.82), 0.7)
    area((-4, -6, 8), (0, 2, 0), 2200, 8, (1, 0.93, 0.85))
    area((6, -1, 4), (0, 3, 1), 700, 4, (0.85, 0.9, 1))


def render(name, fast=False):
    C.reset()
    C.MATS.clear()
    sc = bpy.context.scene
    sc.render.engine = "CYCLES"
    sc.cycles.samples = 12 if fast else 48
    sc.cycles.use_denoising = True
    sc.cycles.max_bounces = 6
    sc.view_settings.view_transform = "AgX"
    sc.view_settings.look = "AgX - Punchy"
    if name == "salon":
        salon()
        target, camloc = Vector((0, 2.5, 2.9)), Vector((0, -10.5, 4.3))
    else:
        kitchen(night=(name == "nuit"), boxes=(name == "cartons"))
        target, camloc = Vector((0, 1.0, 2.9)), Vector((0, -10.5, 4.3))
    bpy.ops.object.camera_add(location=camloc)
    cam = bpy.context.object
    cam.rotation_euler = (target - camloc).to_track_quat("-Z", "Y").to_euler()
    cam.data.lens = 24
    cam.data.sensor_fit = "VERTICAL"
    sc.camera = cam
    sc.render.resolution_x, sc.render.resolution_y = (540, 960)
    sc.render.filepath = os.path.join(OUT, name + ("_fast" if fast else "") + ".png")
    bpy.ops.render.render(write_still=True)
    print("OK", name, flush=True)


if __name__ == "__main__":
    fast = "--fast" in sys.argv
    for n in [a for a in sys.argv[1:] if not a.startswith("--")]:
        render(n, fast)
