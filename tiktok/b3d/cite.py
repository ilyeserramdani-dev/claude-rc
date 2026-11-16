"""Décors 3D de « Bâtiment B » : python3 cite.py cite_jour cite_nuit hall cave toit appart [--fast]"""
import bpy, math, os, sys, random
from mathutils import Vector
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import chars as C
from bg import noise_mat, plane, area, point, world, OUT
M = C.mat
lin = C.lin


def windows_mat(name, night):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    b = nt.nodes["Principled BSDF"]
    tc = nt.nodes.new("ShaderNodeTexCoord")
    br = nt.nodes.new("ShaderNodeTexBrick")
    br.offset = 0.0
    br.inputs["Scale"].default_value = 1.0
    br.inputs["Brick Width"].default_value = 1.6
    br.inputs["Row Height"].default_value = 1.4
    br.inputs["Mortar Size"].default_value = 0.45
    br.inputs["Bias"].default_value = 0.3 if night else 0.0
    facade = (0.86, 0.8, 0.7)
    if night:
        br.inputs["Color1"].default_value = (*lin((1.0, 0.72, 0.38)), 1)
        br.inputs["Color2"].default_value = (*lin((0.04, 0.05, 0.09)), 1)
        br.inputs["Mortar"].default_value = (0, 0, 0, 1)
        nt.links.new(br.outputs["Color"], b.inputs["Emission Color"])
        b.inputs["Emission Strength"].default_value = 3.0
        b.inputs["Base Color"].default_value = (*lin((0.25, 0.24, 0.26)), 1)
    else:
        br.inputs["Color1"].default_value = (*lin((0.35, 0.45, 0.55)), 1)
        br.inputs["Color2"].default_value = (*lin((0.45, 0.55, 0.65)), 1)
        br.inputs["Mortar"].default_value = (*lin(facade), 1)
        nt.links.new(br.outputs["Color"], b.inputs["Base Color"])
    mp = nt.nodes.new("ShaderNodeMapping")
    mp.inputs["Rotation"].default_value = (math.pi / 2, 0, 0)
    nt.links.new(tc.outputs["Object"], mp.inputs["Vector"])
    nt.links.new(mp.outputs["Vector"], br.inputs["Vector"])
    b.inputs["Roughness"].default_value = 0.4
    return m


def tower(loc, dims, night, label=None):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc)
    o = bpy.context.object
    o.scale = dims
    bpy.ops.object.transform_apply(scale=True)
    o.data.materials.append(windows_mat(f"win{loc}", night))
    C.rbox((loc[0], loc[1], loc[2] + dims[2] / 2 + 0.3), (dims[0] + 0.4, dims[1] + 0.4, 0.6), 0.05, M("roofedge", (0.6, 0.58, 0.55), rough=0.7))
    if label:
        bpy.ops.object.text_add(location=(loc[0] - 1.2, loc[1] - dims[1] / 2 - 0.08, 7.2), rotation=(math.pi / 2, 0, 0))
        t = bpy.context.object
        t.data.body = label
        t.data.size = 3.2
        t.data.extrude = 0.08
        t.data.materials.append(M("label", (0.95, 0.95, 0.95), rough=0.4, emit=(1, 1, 1) if night else None, es=1.5 if night else 0))
        C.rbox((loc[0], loc[1] - dims[1] / 2 - 0.2, 2.2), (4.5, 0.4, 4.4), 0.05, M("door", (0.08, 0.1, 0.12), rough=0.15, coat=1))
        C.rbox((loc[0], loc[1] - dims[1] / 2 - 1.2, 4.6), (6.0, 2.4, 0.25), 0.05, M("auvent", (0.55, 0.55, 0.58), rough=0.5))


def tree(x, y, s=1.0):
    C.cyl((x, y, 1.6 * s), 0.25 * s, 3.2 * s, M("trunk", (0.35, 0.25, 0.18), rough=0.9))
    g = M("foliage", (0.3, 0.55, 0.28), rough=0.8, sheen=0.3)
    for dx, dz, r in ((0, 4.2, 1.8), (-1.0, 3.6, 1.3), (1.1, 3.7, 1.3), (0.2, 5.2, 1.3)):
        C.sphere((x + dx * s, y, dz * s), r * s, (1, 1, 0.9), g)


def lamp(x, y, night):
    C.cyl((x, y, 3.5), 0.1, 7, M("pole", (0.2, 0.22, 0.25), metal=1, rough=0.4))
    C.rbox((x - 0.5, y, 7.0), (1.4, 0.5, 0.25), 0.08, M("lamphead", (0.2, 0.22, 0.25), metal=1, rough=0.4))
    C.rbox((x - 0.5, y, 6.85), (1.1, 0.35, 0.05), 0.02, M("lampglow", (1, 0.85, 0.6), emit=(1, 0.8, 0.5), es=8 if night else 0.5))
    if night:
        point((x - 0.5, y, 6.5), 900, (1, 0.78, 0.5), 0.3)


def cite(night):
    asphalt = noise_mat("asphalt", (0.38, 0.38, 0.4), (0.3, 0.3, 0.32), scale=40, rough=0.9)
    plane((0, 30, 0), (120, 90, 1), asphalt)
    plane((0, 6, 0.01), (7, 40, 1), noise_mat("pave", (0.7, 0.66, 0.6), (0.62, 0.58, 0.52), scale=25, rough=0.8))
    for x in (-9, 9):
        plane((x, 9, 0.02), (9, 10, 1), noise_mat("grass", (0.35, 0.55, 0.3), (0.28, 0.45, 0.24), scale=30, rough=1))
    tower((0, 26, 15), (16, 8, 30), night, label="B")
    tower((-26, 40, 22), (14, 8, 44), night)
    tower((26, 36, 18), (14, 8, 36), night)
    tower((-6, 70, 25), (20, 8, 50), night)
    tree(-8, 10, 1.0)
    tree(9, 12, 1.1)
    tree(-14, 18, 0.9)
    lamp(5.5, 5, night)
    lamp(-5.5, 16, night)
    wood = M("benchwood", (0.6, 0.42, 0.25), rough=0.6)
    C.rbox((-5, 4, 0.9), (3.2, 0.9, 0.18), 0.04, wood)
    C.rbox((-5, 4.45, 1.5), (3.2, 0.15, 0.7), 0.04, wood)
    for dx in (-1.3, 1.3):
        C.rbox((-5 + dx, 4, 0.45), (0.15, 0.8, 0.9), 0.02, M("benchleg", (0.2, 0.2, 0.22), metal=1, rough=0.4))
    fence = M("fence", (0.25, 0.4, 0.3), metal=1, rough=0.5)
    for k in range(9):
        C.cyl((-16 + k * 1.2, 15, 2), 0.05, 4, fence)
    for z in (1, 2.5, 4):
        C.cyl((-11.2, 15, z), 0.04, 9.6, fence, rot=(0, math.pi / 2, 0))
    C.cyl((7.5, 3, 0.8), 0.5, 1.6, M("bin", (0.2, 0.45, 0.3), rough=0.5))
    if night:
        world((0.08, 0.1, 0.22), 0.6)
        C.sphere((-14, 90, 48), 2.2, (1, 1, 1), M("moon", (1, 0.97, 0.85), emit=(1, 0.97, 0.85), es=5))
        area((8, -6, 10), (0, 5, 0), 1500, 10, (0.45, 0.55, 1.0))
    else:
        world((0.58, 0.75, 1.0), 1.0)
        bpy.ops.object.light_add(type="SUN", location=(10, -10, 30))
        s = bpy.context.object
        s.data.energy = 3.5
        s.rotation_euler = (math.radians(50), 0, math.radians(35))
    return Vector((0, 12, 7.5)), Vector((0, -16, 3.6))


def hall():
    floor = bpy.data.materials.new("checker")
    floor.use_nodes = True
    nt = floor.node_tree
    ch = nt.nodes.new("ShaderNodeTexChecker")
    ch.inputs["Scale"].default_value = 4
    ch.inputs["Color1"].default_value = (*lin((0.82, 0.8, 0.76)), 1)
    ch.inputs["Color2"].default_value = (*lin((0.35, 0.33, 0.32)), 1)
    tc = nt.nodes.new("ShaderNodeTexCoord")
    nt.links.new(tc.outputs["Object"], ch.inputs["Vector"])
    nt.links.new(ch.outputs["Color"], nt.nodes["Principled BSDF"].inputs["Base Color"])
    nt.nodes["Principled BSDF"].inputs["Roughness"].default_value = 0.25
    plane((0, 4, 0), (24, 18, 1), floor)
    wall = noise_mat("hallwall", (0.86, 0.82, 0.72), (0.82, 0.78, 0.68), scale=30, rough=0.8)
    plane((0, 9, 6), (24, 12, 1), wall, rot=(math.pi / 2, 0, 0))
    plane((-10, 4, 6), (18, 12, 1), wall, rot=(math.pi / 2, 0, math.pi / 2))
    plane((10, 4, 6), (18, 12, 1), wall, rot=(math.pi / 2, 0, math.pi / 2))
    C.rbox((0, 8.95, 1.2), (24, 0.1, 2.4), 0.01, M("wainscot", (0.3, 0.5, 0.45), rough=0.4, coat=0.5))
    metal = M("mailbox", (0.6, 0.62, 0.66), metal=1, rough=0.35)
    for r in range(4):
        for c in range(6):
            C.rbox((-8.2 + c * 0.95, 8.7, 3.0 + r * 0.8), (0.88, 0.4, 0.72), 0.03, metal)
            C.rbox((-8.2 + c * 0.95, 8.48, 3.15 + r * 0.8), (0.5, 0.02, 0.06), 0.005, M("slot", (0.05, 0.05, 0.05)))
    C.rbox((4.0, 8.8, 3.1), (3.4, 0.3, 6.2), 0.05, M("elevframe", (0.4, 0.42, 0.45), metal=1, rough=0.4))
    for dx in (-0.8, 0.8):
        C.rbox((4.0 + dx, 8.6, 3.0), (1.55, 0.1, 5.8), 0.02, M("elevdoor", (0.72, 0.74, 0.78), metal=1, rough=0.2))
    C.rbox((4.0, 8.6, 6.5), (0.6, 0.06, 0.35), 0.03, M("elevdisp", (1, 0.3, 0.1), emit=(1, 0.3, 0.1), es=3))
    # tableau d'affichage + avis de démolition
    C.rbox((-2.0, 8.8, 4.6), (2.6, 0.12, 1.9), 0.04, M("cork", (0.7, 0.5, 0.3), rough=0.9))
    C.rbox((-2.0, 8.72, 4.6), (1.5, 0.02, 1.4), 0.01, M("paper", (0.98, 0.98, 0.95), rough=0.8))
    for i, txt in enumerate(["AVIS DE", "DÉMOLITION", "BÂTIMENT B"]):
        bpy.ops.object.text_add(location=(-2.65, 8.7, 5.05 - i * 0.32), rotation=(math.pi / 2, 0, 0))
        t = bpy.context.object
        t.data.body = txt
        t.data.size = 0.22
        t.data.materials.append(M("redtxt", (0.8, 0.1, 0.1), rough=0.6))
    C.rbox((-9.9, 5, 3.5), (0.1, 3.5, 7), 0.02, M("glassdoor", (0.7, 0.85, 1.0), emit=(0.7, 0.85, 1.0), es=0.8))
    C.rbox((0, 4, 11.8), (5, 0.4, 0.15), 0.05, M("neon", (1, 1, 1), emit=(0.9, 0.95, 1), es=12))
    world((0.2, 0.2, 0.22), 0.3)
    area((0, 4, 11.5), (0, 4, 0), 900, 5, (0.92, 0.97, 1.0))
    area((-6, -4, 6), (0, 6, 3), 400, 6, (1, 0.9, 0.8))
    return Vector((0, 6, 3.6)), Vector((0, -9, 4.4))


def cave():
    conc = noise_mat("concrete", (0.5, 0.49, 0.47), (0.38, 0.37, 0.36), scale=12, rough=0.95, detail=8)
    plane((0, 10, 0), (12, 30, 1), noise_mat("cavefloor", (0.3, 0.29, 0.28), (0.22, 0.21, 0.2), scale=20, rough=0.9))
    plane((0, 10, 8), (12, 30, 1), conc, rot=(math.pi, 0, 0))
    for x, rz in ((-5, math.pi / 2), (5, math.pi / 2)):
        plane((x, 10, 4), (30, 8, 1), conc, rot=(math.pi / 2, 0, rz))
    plane((0, 24, 4), (12, 8, 1), conc, rot=(math.pi / 2, 0, 0))
    wood = noise_mat("cavedoor", (0.45, 0.32, 0.2), (0.35, 0.24, 0.15), scale=6, rough=0.8, stretch=(1, 1, 6))
    nums = {(-1, 0): "45", (1, 0): "46", (-1, 1): "47", (1, 1): "48", (-1, 2): "49", (1, 2): "50"}
    for (side, k), n in nums.items():
        y = 4 + k * 6
        C.rbox((side * 4.95, y, 2.6), (0.15, 2.4, 5.0), 0.03, wood)
        bpy.ops.object.text_add(location=(side * 4.85, y - 0.5, 4.3), rotation=(math.pi / 2, 0, -side * math.pi / 2))
        t = bpy.context.object
        t.data.body = n
        t.data.size = 0.6
        t.data.materials.append(M("numtxt", (0.95, 0.95, 0.9), rough=0.5))
    C.rbox((-4.85, 10.0, 2.6), (0.1, 0.25, 0.4), 0.02, M("padlock", (0.85, 0.7, 0.3), metal=1, rough=0.2))
    for x, z in ((-3.8, 7.4), (-3.2, 7.6), (3.5, 7.5)):
        C.cyl((x, 10, z), 0.18, 30, M("pipe", (0.55, 0.5, 0.45), metal=1, rough=0.5), rot=(math.pi / 2, 0, 0))
    C.cyl((0, 9, 7.6), 0.02, 0.8, M("cable", (0.1, 0.1, 0.1)))
    C.sphere((0, 9, 7.1), 0.18, (1, 1, 1.3), M("bulb", (1, 0.8, 0.5), emit=(1, 0.75, 0.45), es=15))
    point((0, 9, 6.8), 1800, (1, 0.72, 0.45), 0.2)
    point((0, 18, 6.5), 900, (1, 0.72, 0.45), 0.2)
    area((0, -5, 4), (0, 10, 2), 500, 5, (0.5, 0.6, 1.0))
    world((0.02, 0.02, 0.03), 0.2)
    return Vector((0, 8, 3.4)), Vector((0, -6, 4.2))


def toit():
    plane((0, 10, 0), (40, 40, 1), noise_mat("gravel", (0.55, 0.52, 0.48), (0.4, 0.38, 0.35), scale=80, rough=1, detail=10))
    par = M("parapet", (0.7, 0.66, 0.6), rough=0.8)
    C.rbox((0, 16, 0.8), (30, 0.6, 1.6), 0.05, par)
    C.rbox((-12, 6, 0.8), (0.6, 20, 1.6), 0.05, par)
    C.rbox((12, 6, 0.8), (0.6, 20, 1.6), 0.05, par)
    metal = M("ant", (0.5, 0.52, 0.55), metal=1, rough=0.4)
    for x, h in ((-7, 7), (6, 9)):
        C.cyl((x, 12, h / 2), 0.08, h, metal)
        for z in (h - 1, h - 2.2):
            C.cyl((x, 12, z), 0.04, 2.4, metal, rot=(0, math.pi / 2, 0))
    C.cyl((8, 10, 2.0), 1.6, 4.0, M("tank", (0.6, 0.6, 0.62), metal=1, rough=0.5))
    # ciel coucher de soleil
    sky = bpy.data.materials.new("sunset")
    sky.use_nodes = True
    nt = sky.node_tree
    em = nt.nodes.new("ShaderNodeEmission")
    tc = nt.nodes.new("ShaderNodeTexCoord")
    sep = nt.nodes.new("ShaderNodeSeparateXYZ")
    ramp = nt.nodes.new("ShaderNodeValToRGB")
    ramp.color_ramp.elements[0].position = 0.35
    ramp.color_ramp.elements[0].color = (*lin((1.0, 0.55, 0.25)), 1)
    ramp.color_ramp.elements[1].position = 0.8
    ramp.color_ramp.elements[1].color = (*lin((0.35, 0.25, 0.55)), 1)
    nt.links.new(tc.outputs["Generated"], sep.inputs[0])
    nt.links.new(sep.outputs["Y"], ramp.inputs["Fac"])
    nt.links.new(ramp.outputs["Color"], em.inputs["Color"])
    em.inputs["Strength"].default_value = 1.4
    out = nt.nodes["Material Output"]
    nt.links.new(em.outputs["Emission"], out.inputs["Surface"])
    plane((0, 120, 30), (300, 120, 1), sky, rot=(math.pi / 2, 0, 0))
    for x, h in ((-40, 50), (-15, 35), (20, 45), (45, 30), (5, 25)):
        bpy.ops.mesh.primitive_cube_add(size=1, location=(x, 80, h / 2 - 15))
        o = bpy.context.object
        o.scale = (14, 8, h)
        bpy.ops.object.transform_apply(scale=True)
        o.data.materials.append(windows_mat(f"far{x}", True))
    world((0.5, 0.35, 0.4), 0.5)
    bpy.ops.object.light_add(type="SUN")
    s = bpy.context.object
    s.data.energy = 2.5
    s.data.color = (1, 0.7, 0.45)
    s.rotation_euler = (math.radians(80), 0, math.radians(180))
    area((0, -8, 6), (0, 6, 0), 1400, 10, (1.0, 0.8, 0.7))
    return Vector((0, 8, 3.8)), Vector((0, -11, 4.3))


def appart():
    plane((0, 4, 0), (24, 18, 1), noise_mat("parquet2", (0.58, 0.4, 0.25), (0.48, 0.32, 0.2), scale=2, rough=0.4, stretch=(0.2, 3, 1)))
    paper = noise_mat("wallpaper", (0.92, 0.8, 0.62), (0.85, 0.68, 0.5), scale=60, rough=0.85, detail=2)
    plane((0, 9, 6), (24, 12, 1), paper, rot=(math.pi / 2, 0, 0))
    plane((-10, 4, 6), (18, 12, 1), paper, rot=(math.pi / 2, 0, math.pi / 2))
    sofa = noise_mat("sofa", (0.55, 0.2, 0.25), (0.5, 0.17, 0.22), scale=40, rough=0.9)
    C.rbox((3.5, 7.3, 1.0), (7, 2.2, 1.2), 0.3, sofa)
    C.rbox((3.5, 8.2, 2.2), (7, 0.7, 2.0), 0.3, sofa)
    C.rbox((2.0, 7.0, 1.9), (2.5, 0.2, 1.2), 0.05, M("throw", (0.95, 0.7, 0.15), rough=0.9, sheen=0.5), rot=(0.3, 0, 0.1))
    C.rbox((-3.5, 8.9, 4.5), (4.2, 0.12, 3.4), 0.05, M("winframe", (1, 1, 1), rough=0.4))
    plane((-3.5, 8.8, 4.5), (3.8, 3.0, 1), M("view", (0.55, 0.7, 0.9), emit=(0.55, 0.7, 0.9), es=1.2), rot=(math.pi / 2, 0, 0))
    for i, (x, z, c) in enumerate([(2, 5.5, (0.9, 0.6, 0.4)), (3.8, 5.8, (0.4, 0.6, 0.8)), (5.6, 5.4, (0.6, 0.8, 0.5)), (3.0, 4.2, (0.85, 0.5, 0.6))]):
        C.rbox((x, 8.88, z), (1.2, 0.08, 0.95), 0.03, M("pframe2", (0.6, 0.45, 0.2), metal=1, rough=0.3))
        C.rbox((x, 8.82, z), (0.95, 0.02, 0.7), 0.01, noise_mat(f"photo{i}", c, tuple(v * 0.6 for v in c), scale=3, rough=0.6))
    C.cyl((-1, 3.5, 0.03), 4, 0.04, noise_mat("rug2", (0.7, 0.2, 0.2), (0.9, 0.6, 0.2), scale=8, rough=1))
    C.cyl((-1, 4.5, 0.8), 1.2, 0.12, M("table", (0.4, 0.26, 0.16), rough=0.4))
    C.cyl((-1, 4.5, 0.4), 0.15, 0.8, M("table", (0.4, 0.26, 0.16), rough=0.4))
    C.sphere((-1.2, 4.5, 1.15), 0.3, (1, 1, 0.9), M("teapot", (0.85, 0.85, 0.8), metal=1, rough=0.2))
    C.cone((-0.85, 4.5, 1.25), 0.07, 0.03, 0.4, M("teapot", (0.85, 0.85, 0.8), metal=1, rough=0.2), rot=(0, 0.9, 0))
    C.cyl((-8, 7, 3), 0.05, 6, M("pole2", (0.6, 0.5, 0.3), metal=1, rough=0.3))
    C.cone((-8, 7, 6.2), 0.9, 0.5, 0.9, M("lshade2", (1, 0.9, 0.75), emit=(1, 0.8, 0.55), es=2))
    point((-8, 6.8, 5.8), 500, (1, 0.78, 0.5), 0.4)
    world((0.9, 0.82, 0.75), 0.6)
    area((-4, -6, 8), (0, 4, 2), 1500, 8, (1, 0.92, 0.82))
    return Vector((0, 6, 3.6)), Vector((0, -9, 4.4))


def epicerie():
    plane((0, 4, 0), (24, 18, 1), noise_mat("tilefloor", (0.85, 0.85, 0.82), (0.75, 0.75, 0.72), scale=10, rough=0.3))
    wall = noise_mat("shopwall", (0.95, 0.92, 0.8), (0.9, 0.87, 0.75), scale=30, rough=0.8)
    plane((0, 9, 6), (24, 12, 1), wall, rot=(math.pi / 2, 0, 0))
    plane((-10, 4, 6), (18, 12, 1), wall, rot=(math.pi / 2, 0, math.pi / 2))
    plane((10, 4, 6), (18, 12, 1), wall, rot=(math.pi / 2, 0, math.pi / 2))
    rnd = random.Random(4)
    cols = [(0.9, 0.2, 0.2), (0.2, 0.5, 0.9), (0.95, 0.8, 0.2), (0.3, 0.7, 0.3), (0.95, 0.5, 0.1), (0.7, 0.3, 0.7), (1, 1, 1)]
    for x0 in (-6.5, 0.5):
        for k in range(4):
            z = 0.6 + k * 1.6
            C.rbox((x0 + 2.5, 8.4, z), (5.6, 1.0, 0.12), 0.02, M("shelf", (0.55, 0.4, 0.28), rough=0.6))
            x = x0
            while x < x0 + 5.0:
                w = rnd.uniform(0.3, 0.6)
                h = rnd.uniform(0.5, 1.2)
                c = cols[rnd.randrange(len(cols))]
                C.rbox((x + w / 2, 8.3, z + h / 2 + 0.06), (w * 0.92, 0.6, h), 0.03, M(f"prod{x0}{k}{int(x*10)}", c, rough=0.4))
                x += w
    C.rbox((7.5, 7.5, 3.5), (3.5, 2.0, 7), 0.1, M("fridge", (0.85, 0.87, 0.9), metal=1, rough=0.3))
    C.rbox((7.5, 6.48, 3.6), (3.0, 0.04, 6.0), 0.05, M("fridgeglow", (0.8, 0.95, 1.0), emit=(0.75, 0.9, 1.0), es=2.5))
    C.rbox((-5.5, 3.0, 1.6), (6, 2.0, 3.2), 0.08, M("counter", (0.25, 0.45, 0.4), rough=0.4, coat=0.5))
    C.rbox((-5.5, 3.0, 3.25), (6.2, 2.2, 0.12), 0.03, M("countertop", (0.9, 0.88, 0.85), rough=0.3))
    C.rbox((-7.0, 3.0, 3.8), (1.4, 1.0, 0.9), 0.08, M("register", (0.15, 0.15, 0.17), rough=0.4))
    C.rbox((-7.0, 2.5, 4.2), (0.9, 0.05, 0.4), 0.03, M("regscreen", (0.3, 1, 0.5), emit=(0.3, 1, 0.5), es=2))
    bpy.ops.object.text_add(location=(-4.2, 8.85, 8.8), rotation=(math.pi / 2, 0, 0))
    t = bpy.context.object
    t.data.body = "ÉPICERIE PHAM"
    t.data.size = 1.0
    t.data.extrude = 0.05
    t.data.materials.append(M("shopsign", (0.85, 0.15, 0.15), rough=0.4, emit=(0.9, 0.2, 0.2), es=1.5))
    for x in (-4, 4):
        C.rbox((x, 4, 11.8), (4.5, 0.35, 0.12), 0.05, M("neon", (1, 1, 1), emit=(0.9, 0.95, 1), es=12))
    world((0.3, 0.3, 0.3), 0.4)
    area((0, 4, 11.4), (0, 4, 0), 1200, 8, (0.95, 0.98, 1.0))
    area((-6, -5, 6), (0, 6, 3), 500, 6, (1, 0.92, 0.82))
    return Vector((0, 6, 3.6)), Vector((0, -9, 4.4))


def epicerie():
    plane((0, 4, 0), (24, 18, 1), noise_mat("shopfloor", (0.75, 0.73, 0.7), (0.65, 0.63, 0.6), scale=10, rough=0.5))
    wall = noise_mat("shopwall", (0.95, 0.9, 0.78), (0.9, 0.85, 0.72), scale=30, rough=0.8)
    plane((0, 9, 6), (24, 12, 1), wall, rot=(math.pi / 2, 0, 0))
    plane((-10, 4, 6), (18, 12, 1), wall, rot=(math.pi / 2, 0, math.pi / 2))
    rnd = random.Random(4)
    cols = [(0.9, 0.2, 0.2), (0.2, 0.5, 0.9), (0.95, 0.8, 0.2), (0.3, 0.75, 0.35), (0.95, 0.5, 0.15), (0.6, 0.3, 0.7), (1, 1, 1)]
    for x0 in (-7.5, -3.0):
        for z in (0.6, 2.0, 3.4, 4.8):
            C.rbox((x0, 8.2, z - 0.1), (4.0, 1.2, 0.1), 0.01, M("shelf", (0.85, 0.85, 0.88), metal=1, rough=0.4))
            x = x0 - 1.8
            while x < x0 + 1.8:
                w = rnd.uniform(0.25, 0.45)
                h = rnd.uniform(0.4, 0.9)
                C.rbox((x + w / 2, 8.1, z + h / 2), (w * 0.9, 0.5, h), 0.02, M(f"prod{rnd.randint(0, 6)}", cols[rnd.randint(0, 6)], rough=0.5))
                x += w
    C.rbox((5.5, 6.5, 1.2), (6, 1.4, 2.4), 0.05, M("counter", (0.55, 0.35, 0.2), rough=0.5))
    C.rbox((5.5, 6.5, 2.45), (6.2, 1.6, 0.1), 0.02, M("countertop", (0.9, 0.9, 0.88), rough=0.2, coat=1))
    C.rbox((4.0, 6.4, 2.9), (0.9, 0.6, 0.8), 0.08, M("register", (0.2, 0.2, 0.22), rough=0.4))
    for k in range(5):
        C.sphere((6.0 + k * 0.35, 6.4, 2.7), 0.16, (1, 1, 1), M("apple", (0.85, 0.15, 0.1), rough=0.3, coat=0.6))
    C.rbox((8.5, 8.3, 3.5), (2.6, 1.2, 7), 0.08, M("fridgeframe", (0.9, 0.9, 0.92), metal=1, rough=0.3))
    C.rbox((8.5, 7.68, 3.6), (2.2, 0.04, 6.2), 0.04, M("fridgeglass", (0.7, 0.9, 1.0), emit=(0.7, 0.9, 1.0), es=1.5))
    bpy.ops.object.text_add(location=(-4.2, 8.85, 7.6), rotation=(math.pi / 2, 0, 0))
    t = bpy.context.object
    t.data.body = "ÉPICERIE PHAM"
    t.data.size = 0.9
    t.data.extrude = 0.05
    t.data.materials.append(M("signtxt", (0.9, 0.15, 0.15), rough=0.4, emit=(1, 0.2, 0.2), es=2))
    C.rbox((0, 4, 11.8), (6, 0.4, 0.15), 0.05, M("neon", (1, 1, 1), emit=(0.95, 1, 0.95), es=12))
    world((0.85, 0.85, 0.85), 0.5)
    area((0, 4, 11.5), (0, 4, 0), 1100, 6, (0.95, 1.0, 0.95))
    area((-6, -4, 6), (0, 6, 3), 500, 6, (1, 0.92, 0.8))
    return Vector((0, 6, 3.6)), Vector((0, -9, 4.4))


SETS = {"epicerie": epicerie, "epicerie": epicerie, "cite_jour": lambda: cite(False), "cite_nuit": lambda: cite(True), "hall": hall, "cave": cave, "toit": toit, "appart": appart}


def render(name, fast=False):
    C.reset()
    C.MATS.clear()
    sc = bpy.context.scene
    sc.render.engine = "CYCLES"
    sc.cycles.samples = 10 if fast else 40
    sc.cycles.use_denoising = True
    sc.cycles.max_bounces = 6
    sc.view_settings.view_transform = "AgX"
    sc.view_settings.look = "AgX - Punchy"
    target, camloc = SETS[name]()
    bpy.ops.object.camera_add(location=camloc)
    cam = bpy.context.object
    cam.rotation_euler = (target - camloc).to_track_quat("-Z", "Y").to_euler()
    cam.data.lens = 24
    cam.data.sensor_fit = "VERTICAL"
    sc.camera = cam
    sc.render.resolution_x, sc.render.resolution_y = (540, 960) if fast else (720, 1280)
    sc.render.filepath = os.path.join(OUT, name + ("_fast" if fast else "") + ".png")
    bpy.ops.render.render(write_still=True)
    print("OK", name, flush=True)


if __name__ == "__main__":
    fast = "--fast" in sys.argv
    for n in [a for a in sys.argv[1:] if not a.startswith("--")]:
        render(n, fast)
