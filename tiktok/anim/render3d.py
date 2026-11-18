"""Étape 2 : vraie animation 3D (Blender/Cycles) d'un épisode.
python3 anim/render3d.py work/ep01 [--test t1,t2,...]
Lit work/epXX/timeline.json, construit le décor 3D et les personnages articulés
(tête, bras, jambes, visage synchronisé sur la voix), choisit les plans de caméra et rend :
  work/epXX/bg/<plan>.png      décor seul, une fois par plan (haute qualité)
  work/epXX/ch/f00000.png      personnages animés + ombres (fond transparent), 12 images/s
  work/epXX/shots.json         plan utilisé pour chaque image
"""
import bpy, sys, os, json, math, random, time
from mathutils import Vector, Euler

HERE = os.path.dirname(os.path.abspath(__file__))
B3D = os.path.join(os.path.dirname(HERE), "b3d")
sys.path.insert(0, B3D)
import chars as C, humans as Hm, humans2 as H2, cite

RX, RY = 540, 960
CH_SAMPLES = 8
BG_SAMPLES = 24

# zone de jeu par décor : centre (x, y), échelle des personnages, ambiance
SETS = {
    "cite_nuit": dict(c=(0.0, 6.0), k=0.55, mood="night"),
    "cite_jour": dict(c=(0.0, 6.0), k=0.55, mood="day"),
    "hall": dict(c=(-1.0, 4.5), k=1.0, mood="indoor"),
    "cave": dict(c=(0.0, 4.0), k=1.0, mood="dark"),
    "toit": dict(c=(0.0, 4.0), k=1.0, mood="dusk"),
    "appart": dict(c=(0.0, 4.0), k=1.0, mood="indoor"),
    "epicerie": dict(c=(0.0, 3.5), k=1.0, mood="indoor"),
}


def smooth(a, b, k):
    k = max(0.0, min(1.0, k))
    k = k * k * (3 - 2 * k)
    return a + (b - a) * k


def noise(t, seed):
    return (math.sin(t * 1.7 + seed) * 0.5 + math.sin(t * 3.1 + seed * 2.3) * 0.3 + math.sin(t * 5.3 + seed * 0.7) * 0.2)


# ------------------------------------------------------------------ décor
def car(x, y, rot, color=(0.03, 0.03, 0.035), lights=True):
    paint = C.mat("carpaint", color, metal=0.6, rough=0.18, coat=1)
    glass = C.mat("carglass", (0.02, 0.025, 0.035), rough=0.05, coat=1, metal=0.4)
    tyre = C.mat("tyre", (0.02, 0.02, 0.02), rough=0.8)
    rim = C.mat("rim", (0.75, 0.75, 0.78), metal=1, rough=0.2)
    before = set(bpy.context.scene.objects)
    C.rbox((0, 0, 0.75), (2.0, 4.6, 0.85), 0.3, paint)
    C.rbox((0, 0.25, 1.4), (1.8, 2.5, 0.75), 0.3, glass)
    for sx in (-1, 1):
        for sy in (-1.45, 1.45):
            C.cyl((sx * 0.95, sy, 0.38), 0.38, 0.28, tyre, rot=(0, math.pi / 2, 0))
            C.cyl((sx * 1.0, sy, 0.38), 0.22, 0.2, rim, rot=(0, math.pi / 2, 0))
    if lights:
        hl = C.mat("headlight", (1, 0.97, 0.85), emit=(1, 0.97, 0.85), es=12)
        tl = C.mat("taillight", (1, 0.05, 0.05), emit=(1, 0.05, 0.05), es=6)
        for sx in (-0.65, 0.65):
            C.rbox((sx, -2.3, 0.85), (0.45, 0.06, 0.18), 0.05, hl)
            C.rbox((sx, 2.3, 0.85), (0.45, 0.06, 0.15), 0.05, tl)
    piv = bpy.data.objects.new("car", None)
    bpy.context.scene.collection.objects.link(piv)
    for o in set(bpy.context.scene.objects) - before - {piv}:
        o.parent = piv
    piv.location = (x, y, 0)
    piv.rotation_euler = (0, 0, rot)
    return piv


def build_set(name, ep):
    fn = cite.SETS[name]
    target, camloc = fn()
    txt = (ep.get("hook", "") + " ".join(l[1] for l in ep["lines"])).lower()
    if name.startswith("cite") and "voiture" in txt:
        for c_ in (car(-3.2, 16.5, 0.25), car(0.4, 17.5, -0.1), car(3.6, 16.2, -0.3)):
            c_.scale = (0.8, 0.8, 0.8)
    return target, camloc


# ------------------------------------------------------------------ personnages
ARM_MATS = ("top", "sleeve", "robe", "skin")


class Char:
    def __init__(self, code, emos, k):
        sc = bpy.context.scene
        before = set(sc.objects)
        C.MATS.clear()
        if code in H2.BUILDERS:
            spec, S = H2.BUILDERS[code]()
        elif code in Hm.BUILDERS:
            spec, S = Hm.BUILDERS[code](), (1, 1, 1)
        else:
            spec, S = C.BUILDERS[code](), (1, 1, 1)
        body = list(set(sc.objects) - before)
        H2.scale_objs(body, S)
        self.code, self.S, self.k = code, S, k
        self.human = code in H2.BUILDERS or code in Hm.BUILDERS
        self.quad = code == "BR"
        self.bird = code == "GA"
        faces = {}
        for emo in emos:
            for m, b in ((0, 0), (1, 0), (0, 1)):
                coll = C.build_face(spec, emo, m, b)
                objs = list(coll.objects)
                H2.scale_objs(objs, S)
                faces[(emo, m, b)] = objs
        sx, sz = S[0], S[2]
        hz = 2.2 * sz if self.human else (1.3 if self.quad else 1.25)
        self.head_h = (2.78 * sz if self.human else (1.95 if self.quad else 1.75)) * k
        self.top_h = max((o.matrix_world @ Vector(c)).z for o in body for c in o.bound_box) * k
        mk = lambda n, loc, par=None: self._empty(n, loc, par)
        self.root = mk("root", (0, 0, 0))
        self.spine = mk("spine", (0, 0, 1.2 * sz if self.human else 0.6), self.root)
        self.neck = mk("neck", (0, 0, hz), self.spine)
        self.sh = {s: mk(f"sh{s}", (s * 0.47 * sx, 0, 2.05 * sz), self.spine) for s in (-1, 1)}
        self.hip = {s: mk(f"hip{s}", (s * 0.2 * sx, 0, 1.25 * sz), self.root) for s in (-1, 1)}
        bpy.context.view_layer.update()

        def attach(o, par):
            mw = o.matrix_world.copy()
            o.parent = par
            o.matrix_world = mw

        for o in body:
            if o.parent is not None:
                continue
            bb = [o.matrix_world @ Vector(c) for c in o.bound_box]
            cx = sum(v.x for v in bb) / 8 / sx
            cz = sum(v.z for v in bb) / 8 / sz
            mname = o.active_material.name.split(".")[0] if o.active_material else ""
            par = self.spine
            if not self.human:
                par = self.neck if cz > hz / sz + 0.15 else self.spine
            elif cz > 2.25:
                par = self.neck
            elif 0.95 < cz < 1.97 and abs(cx) > 0.45 and (mname in ARM_MATS or abs(cx) > 0.62):
                par = self.sh[1 if cx > 0 else -1]
            elif cz <= 0.95 and abs(cx) > 0.62:
                par = self.sh[1 if cx > 0 else -1]  # accessoire tenu (canne…)
            elif cz < 0.95 and 0.08 < abs(cx) < 0.45:
                par = self.hip[1 if cx > 0 else -1]
            attach(o, par)
        self.faces = {}
        for key, objs in faces.items():
            fe = mk("face", (0, 0, hz), self.neck)
            bpy.context.view_layer.update()
            for o in objs:
                attach(o, fe)
            self.faces[key] = fe
        self.root.scale = (k, k, k)
        self.cur = None
        self.yaw = 0.0
        self.pos = Vector((0, 0, 0))

    def _empty(self, name, loc, par):
        e = bpy.data.objects.new(f"{name}_{getattr(self, 'code', '')}", None)
        bpy.context.scene.collection.objects.link(e)
        if par is not None:
            e.parent = par
            e.location = Vector(loc) - Vector(self._abs(par))
        else:
            e.location = loc
        e["abs"] = list(loc)
        return e

    def _abs(self, e):
        return e["abs"]

    def set_face(self, key):
        if key not in self.faces:
            key = ("neutre", key[1], key[2])
        if key == self.cur:
            return
        for kk, fe in self.faces.items():
            fe.scale = (1, 1, 1) if kk == key else (0.001, 0.001, 0.001)
        self.cur = key

    def objects(self):
        out = []
        stack = [self.root]
        while stack:
            o = stack.pop()
            out.append(o)
            stack.extend(o.children)
        return out


# ------------------------------------------------------------------ mise en scène
def look_yaw(src, dst):
    d = Vector(dst) - Vector(src)
    return math.atan2(d.x, -d.y)


class Director:
    def __init__(self, tl, cast, chars, zone):
        self.tl, self.segs = tl, tl["segs"]
        self.cast, self.chars = cast, chars
        cx, cy = zone["c"]
        n = len(cast)
        self.u = u = zone["k"] / 0.55
        sp = 1.35 * u
        self.slot = {}
        for i, c in enumerate(cast):
            x = cx + (i - (n - 1) / 2) * sp
            y = cy + (0.35 * u if n > 2 and 0 < i < n - 1 else 0)
            self.slot[c] = Vector((x, y, 0))
        self.center = Vector((cx, cy, 0))
        self.enter = {}
        for i, s in enumerate(self.segs):
            if s["fx"] == "enter" and s["who"] in cast and s["who"] not in self.enter:
                self.enter[s["who"]] = s["start"]
        self.entry_from = Vector((cx + 2.4 * u, cy + (7.0 if u < 1.5 else 4.0) * u, 0))
        self.shots = self.plan_shots()

    def seg_at(self, t):
        for i, s in enumerate(self.segs):
            if s["start"] <= t < s["start"] + s["dur"]:
                return i
        return len(self.segs) - 1

    def present(self, c, t):
        return t >= self.enter.get(c, -1)

    # --- plans
    def plan_shots(self):
        shots, k, last = [], 0, None
        for i, s in enumerate(self.segs):
            w = s["who"]
            nxt = self.segs[i + 1] if i + 1 < len(self.segs) else None
            if w == "HOOK":
                sh = ("EST",)
            elif w not in self.cast:
                if nxt and nxt["fx"] == "enter":
                    sh = ("ENTRY",)
                else:
                    sh = ("EST2",) if i <= 2 else ("WIDE",)
            elif s["fx"] == "enter":
                sh = ("WIDE",)
            else:
                k += 1
                other = self.addressee(i)
                if s["fx"] == "shake" or s["emo"] in ("colere", "peur", "surpris") and k % 3 != 0:
                    sh = ("CU", w, other)
                elif k % 4 == 0:
                    sh = ("WIDE",)
                elif other and k % 2 == 1:
                    sh = ("OTS", w, other)
                else:
                    sh = ("CU", w, other)
            if sh == last and sh[0] == "CU":
                sh = ("OTS", sh[1], sh[2]) if sh[2] else ("WIDE",)
            shots.append(sh)
            last = sh
        return shots

    def addressee(self, i):
        w = self.segs[i]["who"]
        for j in range(i - 1, -1, -1):
            o = self.segs[j]["who"]
            if o in self.cast and o != w:
                return o
        for j in range(i + 1, len(self.segs)):
            o = self.segs[j]["who"]
            if o in self.cast and o != w:
                return o
        others = [c for c in self.cast if c != w]
        return others[0] if others else None

    def cam_for(self, sh):
        """-> (position, cible, focale)"""
        c = self.center
        u = self.u
        if u > 1.2 and sh[0] in ("EST", "EST2", "ENTRY"):
            sh = ("WIDE",)
        flip = False
        if u > 1.2 and sh[0] == "OTS":  # en intérieur, le par-dessus-l'épaule bouche le cadre : plan rapproché de l'autre côté
            sh = ("CU", sh[1], sh[2])
            flip = True
        hh = max(ch.head_h for ch in self.chars.values())
        if sh[0] == "EST":
            return Vector((c.x + 1.5, c.y - 15, 2.2)), Vector((c.x, c.y + 14, 6.5)), 15
        if sh[0] == "EST2":
            return Vector((c.x - 3.0, c.y - 7.5, 0.9)), Vector((c.x + 0.5, c.y + 8, 3.5)), 16
        if sh[0] == "ENTRY":
            e = self.entry_from
            return Vector((c.x - 2.2, c.y - 3.2, 1.3)), Vector((e.x, e.y, 0.9)), 20
        if sh[0] == "WIDE":
            xs = [self.slot[x].x for x in self.cast]
            span = max(xs) - min(xs) + 2.2
            d = max(4.2 * u, span * 1.9) * (0.8 if u > 1.2 else 1.0)
            return Vector((c.x + 0.4, c.y - d, hh * 0.8)), Vector((c.x, c.y, hh * 0.5)), 27 if u < 1.2 else 32
        who, other = sh[1], sh[2]
        p = self.slot[who]
        ch = self.chars[who]
        head = Vector((p.x, p.y, ch.head_h * 0.97))
        if sh[0] == "CU":
            side = 1 if (other and self.slot[other].x > p.x) else -1
            if not other:
                side = 1
            if flip:
                side = -side * 0.5
            cam = Vector((p.x + side * 0.8 * u, p.y - 2.5 * u, ch.head_h * 0.92))
            return cam, head + Vector((0, 0, -0.3 * u)), 30
        # OTS : derrière l'épaule de l'interlocuteur
        q = self.slot[other]
        och = self.chars[other]
        d = (q - p)
        d.z = 0
        d.normalize()
        perp = Vector((-d.y, d.x, 0))
        if perp.y > 0:
            perp = -perp
        cam = q + d * 1.1 * u + perp * 0.75 * u + Vector((0, 0, och.head_h * 1.12))
        cam.y = min(cam.y, p.y - 1.4 * u)
        return cam, head + Vector((0, 0, -0.3 * u)), 24

    # --- poses
    def pose(self, t, dt):
        i = self.seg_at(t)
        s = self.segs[i]
        lt = t - s["start"]
        speaker = s["who"] if s["who"] in self.cast else None
        talking = speaker is not None and lt < s["alen"] + 0.1
        ei = int(lt * self.tl["afps"])
        mouth = talking and ei < len(s["env"]) and s["env"][ei]
        emo_now = {c: "neutre" for c in self.cast}
        for j in range(i + 1):
            if self.segs[j]["who"] in emo_now:
                emo_now[self.segs[j]["who"]] = self.segs[j]["emo"]
        for n_, c in enumerate(self.cast):
            ch = self.chars[c]
            seed = n_ * 2.7 + 1
            if not self.present(c, t):
                ch.root.scale = (0.0001,) * 3
                ch.root.location = (0, 60, -50)
                continue
            ch.root.scale = (ch.k,) * 3
            target = self.slot[c]
            walking = 0.0
            if c in self.enter:
                te = t - self.enter[c]
                wd = 2.6
                if te < wd:
                    a = te / wd
                    pos = self.entry_from.lerp(target, a)
                    walking = 1.0
                else:
                    pos = target.copy()
            else:
                pos = target.copy()
            # regard
            if walking:
                yaw_t = look_yaw(pos, target)
            else:
                if speaker and speaker != c and self.present(speaker, t):
                    look = self.slot[speaker]
                elif speaker == c:
                    o = self.addressee(i)
                    look = self.slot[o] if o and self.present(o, t) else pos + Vector((0, -3, 0))
                else:
                    look = pos + Vector((0, -3, 0))
                yaw_t = look_yaw(pos, look)
                # on reste ouvert vers la caméra (3/4)
                yaw_t = max(-0.8, min(0.8, yaw_t)) * 0.8
            ch.yaw = ch.yaw + (yaw_t - ch.yaw) * min(1.0, dt * (8 if walking else 4))
            bob = abs(math.sin(t * 9)) * 0.05 * walking
            ch.root.location = (pos.x, pos.y, bob)
            ch.root.rotation_euler = (0, 0, ch.yaw)
            # jambes
            sw = math.sin(t * 9) * 0.45 * walking
            for sd in (-1, 1):
                ch.hip[sd].rotation_euler = (sd * sw, 0, 0)
            # buste / respiration
            emo = emo_now[c]
            me_talk = talking and speaker == c
            br = 1 + 0.012 * math.sin(t * 2.2 + seed)
            lean = {"colere": -0.08, "peur": 0.07, "triste": 0.06, "surpris": 0.04}.get(emo, 0.0) if not walking else -0.05
            sway = 0.025 * noise(t * 0.7, seed)
            ch.spine.scale = (1, 1, br)
            ch.spine.rotation_euler = (lean + (0.03 * noise(t * 3, seed) if me_talk else 0), sway, 0)
            # tête
            nod = 0.07 * noise(t * 4.5, seed + 3) if me_talk else 0.02 * noise(t * 0.8, seed)
            tilt = {"triste": 0.12, "joie": -0.06, "peur": 0.05}.get(emo, 0.0)
            turn = 0.18 * noise(t * 0.9, seed + 5) if me_talk else 0.0
            ch.neck.rotation_euler = (nod - (0.08 if emo == "triste" else 0), tilt * (1 if n_ % 2 else -1), turn)
            # bras
            for sd in (-1, 1):
                rx, ry = 0.0, 0.0
                if walking:
                    rx = -sd * sw * 0.8
                elif me_talk:
                    amp = {"colere": 1.0, "joie": 0.8, "peur": 0.6, "surpris": 0.9}.get(emo, 0.55)
                    g = noise(t * 2.2, seed + sd * 4)
                    if emo == "peur":
                        rx, ry = -1.2 + 0.15 * g, sd * 0.35
                    elif emo == "colere" and sd == 1:
                        rx, ry = -1.35 + 0.25 * g, 0.1
                    elif emo == "joie":
                        rx, ry = -0.45 + 0.2 * g, -sd * (0.55 + 0.15 * g)
                    elif emo == "surpris":
                        rx, ry = -0.6, -sd * 0.7
                    else:
                        lead = 1 if (int(t / 1.6) + n_) % 2 else -1
                        rx = -(0.35 + 0.45 * max(0, g)) * amp * (1.0 if sd == lead else 0.35)
                        ry = -sd * 0.12 * amp
                else:
                    if emo == "peur":
                        rx, ry = -0.9, sd * 0.3
                    elif emo == "colere":
                        rx, ry = -0.25, -sd * 0.25  # poings sur les hanches
                    else:
                        rx = 0.04 * noise(t, seed + sd)
                        ry = -sd * 0.06
                if not ch.human:
                    rx, ry = rx * 0.3, ry * 0.3
                cur = ch.sh[sd].rotation_euler
                a = min(1.0, dt * 7)
                ch.sh[sd].rotation_euler = (cur.x + (rx - cur.x) * a, cur.y + (ry - cur.y) * a, 0)
            blink = ((t + seed * 1.3) % 3.7) < 0.12
            m = 1 if (me_talk and mouth) else 0
            ch.set_face((emo, m, 0 if m else int(blink)))


# ------------------------------------------------------------------ lumières
def char_lights(mood, center):
    presets = {
        "night": [((-4, -5, 6), 900, (0.6, 0.7, 1.0)), ((5, 4, 4), 700, (1.0, 0.72, 0.4)), ((2, -6, 2), 220, (0.8, 0.85, 1.0))],
        "day": [((-5, -6, 9), 1600, (1.0, 0.95, 0.88)), ((5, -3, 3), 450, (0.75, 0.85, 1.0)), ((0, 6, 5), 600, (1.0, 0.95, 0.85))],
        "dusk": [((-6, -4, 5), 1200, (1.0, 0.65, 0.4)), ((5, -3, 3), 350, (0.6, 0.6, 1.0)), ((0, 6, 5), 500, (1.0, 0.6, 0.5))],
        "indoor": [((-3, -5, 6), 1100, (1.0, 0.9, 0.78)), ((4, -3, 3), 400, (0.85, 0.9, 1.0)), ((0, 5, 5), 500, (1.0, 0.85, 0.7))],
        "dark": [((-3, -4, 4), 700, (0.55, 0.65, 0.9)), ((3, 3, 3), 600, (1.0, 0.6, 0.3)), ((2, -5, 2), 150, (0.7, 0.75, 0.9))],
    }
    out = []
    for loc, en, col in presets[mood]:
        loc = Vector(loc) + Vector((center.x, center.y, 0))
        bpy.ops.object.light_add(type="AREA", location=loc)
        L = bpy.context.object
        L.data.energy, L.data.size, L.data.color = en * (0.55 if mood in ('night', 'dark') else 0.75), 3, col
        L.rotation_euler = (Vector((center.x, center.y, 1.0)) - loc).to_track_quat("-Z", "Y").to_euler()
        out.append(L)
    return out


# ------------------------------------------------------------------ main
def main(work, test=None):
    tl = json.load(open(os.path.join(work, "timeline.json"), encoding="utf-8"))
    ep = tl["ep"]
    zone = SETS.get(ep["bg"], SETS["cite_jour"])
    C.reset()
    C.MATS.clear()
    sc = bpy.context.scene
    sc.render.engine = "CYCLES"
    sc.cycles.device = "CPU"
    sc.view_settings.view_transform = "AgX"
    sc.view_settings.look = "AgX - Punchy"
    sc.render.resolution_x, sc.render.resolution_y = RX, RY
    sc.render.use_persistent_data = True
    build_set(ep["bg"], ep)
    set_objs = [o for o in sc.objects]
    emos = {}
    for s in tl["segs"]:
        emos.setdefault(s["who"], {"neutre"}).add(s["emo"])
    chars = {}
    for c in ep["cast"]:
        chars[c] = Char(c, sorted(emos.get(c, {"neutre"}) | {"neutre"}), zone["k"])
    D = Director(tl, ep["cast"], chars, zone)
    bpy.ops.object.camera_add()
    cam = bpy.context.object
    cam.data.sensor_fit = "VERTICAL"
    cam.data.sensor_height = 24
    sc.camera = cam

    def set_cam(sh):
        loc, tgt, lens = D.cam_for(sh)
        cam.location = loc
        cam.rotation_euler = (tgt - loc).to_track_quat("-Z", "Y").to_euler()
        cam.data.lens = lens

    keys = []
    need = D.shots if not test else [D.shots[D.seg_at(x)] for x in test]
    for sh in need:
        if sh not in keys:
            keys.append(sh)
    name = lambda sh: "_".join(x or "x" for x in sh)
    os.makedirs(os.path.join(work, "bg"), exist_ok=True)
    os.makedirs(os.path.join(work, "ch"), exist_ok=True)
    char_objs = [o for ch in chars.values() for o in ch.objects()]
    # 1) décors seuls
    for o in char_objs:
        o.hide_render = True
    sc.render.film_transparent = False
    sc.cycles.samples = BG_SAMPLES
    sc.cycles.use_denoising = True
    for sh in keys:
        p = os.path.join(work, "bg", name(sh) + ".png")
        if os.path.exists(p):
            continue
        set_cam(sh)
        sc.render.filepath = p
        t0 = time.time()
        bpy.ops.render.render(write_still=True)
        print("BG", name(sh), round(time.time() - t0, 1), flush=True)
    # 2) personnages seuls (le décor ne sert plus qu'à rien : on le cache)
    for o in char_objs:
        o.hide_render = False
    for o in set_objs:
        if o.type in ("MESH", "CURVE", "FONT"):
            o.hide_render = True
    char_lights(zone["mood"], D.center)
    bpy.ops.mesh.primitive_plane_add(size=1, location=(D.center.x, D.center.y + 2, 0))
    pl = bpy.context.object
    pl.scale = (7 * D.u, 6 * D.u, 1)
    pl.is_shadow_catcher = True
    sc.render.film_transparent = True
    sc.cycles.samples = CH_SAMPLES
    sc.cycles.use_adaptive_sampling = False
    sc.cycles.denoising_prefilter = "FAST"
    try:
        sc.cycles.denoising_quality = "FAST"
    except Exception:
        pass
    sc.cycles.max_bounces = 3
    afps = tl["afps"]
    nfr = int(math.ceil(tl["end"] * afps))
    frames = range(nfr) if not test else [int(x * afps) for x in test]
    shots = {}
    prev_t = None
    for f in (range(nfr) if not test else frames):
        t = f / afps
        dt = 1 / afps if prev_t is None else t - prev_t
        if test and prev_t is None:
            # amorce : on simule quelques images pour que les poses soient stables
            for k in range(6):
                D.pose(max(0, t - (6 - k) / afps), 1 / afps)
        D.pose(t, dt)
        prev_t = t
        i = D.seg_at(t)
        sh = D.shots[i]
        shots[f] = name(sh)
        p = os.path.join(work, "ch", f"f{f:05d}.png")
        if os.path.exists(p) and not test:
            continue
        set_cam(sh)
        sc.render.filepath = p
        t0 = time.time()
        bpy.ops.render.render(write_still=True)
        print("CH", f, nfr, name(sh), round(time.time() - t0, 2), flush=True)
    if not test:
        json.dump(dict(nfr=nfr, afps=afps, shots=shots), open(os.path.join(work, "shots.json"), "w"))
    else:
        json.dump(dict(nfr=nfr, afps=afps, shots=shots, test=True), open(os.path.join(work, "shots_test.json"), "w"))


if __name__ == "__main__":
    args = sys.argv[1:]
    test = None
    if "--test" in args:
        test = [float(x) for x in args[args.index("--test") + 1].split(",")]
    main(args[0], test)
