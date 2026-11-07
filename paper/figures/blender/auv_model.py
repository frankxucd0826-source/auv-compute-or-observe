"""A REMUS-class AUV model reused from the student's earlier figures (Blender 4.5, bpy).

The hull is a body of revolution 1.6 m long and 0.19 m across (an ogive nose, a cylindrical mid-body and a tail cone),
drawn with the parts a reader recognizes from photographs of REMUS-class vehicles (2026-10-19 rebuild):
a dark nose section with a tinted sensor window, joint bands between hull sections, side-scan sonar panels along the
mid-body, a Doppler velocity log under the bow, an acoustic modem dome and a short antenna on the back, two small sensor
windows (bow and stern) that glow teal, cruciform fins with control surfaces, and a ducted five-blade propeller.
`prototype()` builds it once as a single mesh with its materials; `place()` adds linked copies.
Units: metres along +x from the tail to the nose; scale the copies to draw vehicles larger than life.
"""
from __future__ import annotations

import math

import bpy

L, R = 1.60, 0.095
_PROTO = None


def srgb(hexc: str, a: float = 1.0):
    h = hexc.lstrip("#")
    out = []
    for k in (0, 2, 4):
        c = int(h[k:k + 2], 16) / 255.0
        out.append(c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4)
    return (out[0], out[1], out[2], a)


def _mat(name, hexc, rough=0.35, metal=0.0, coat=0.0, emit=0.0, trans=0.0, ior=1.45):
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes.get("Principled BSDF")
    b.inputs["Base Color"].default_value = srgb(hexc)
    b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = metal
    if coat:
        b.inputs["Coat Weight"].default_value = coat
        b.inputs["Coat Roughness"].default_value = 0.06
    if emit:
        b.inputs["Emission Color"].default_value = srgb(hexc)
        b.inputs["Emission Strength"].default_value = emit
    if trans:
        b.inputs["Transmission Weight"].default_value = trans
        b.inputs["IOR"].default_value = ior
    return m


# material slots
HULL, DARK, BAND, OPTIC, METAL, GLASS, WHITE, RUBBER = range(8)


def _materials():
    return [_mat("AUV_Hull", "#F4BC1C", rough=0.26, coat=0.7), _mat("AUV_Dark", "#2C353B", rough=0.42),
            _mat("AUV_Band", "#15191C", rough=0.35), _mat("AUV_Optic", "#3FE0D0", rough=0.15, emit=3.0),
            _mat("AUV_Metal", "#B4BCC4", rough=0.28, metal=0.92), _mat("AUV_Glass", "#1B2E3C", rough=0.05, trans=0.6),
            _mat("AUV_White", "#EEF1F3", rough=0.3), _mat("AUV_Rubber", "#0F1214", rough=0.7)]


class _Mesh:
    def __init__(self):
        self.V, self.F, self.M, self.S = [], [], [], []

    def add(self, verts, faces, mi, smooth=True):
        o = len(self.V)
        self.V.extend(verts)
        self.F.extend(tuple(i + o for i in f) for f in faces)
        self.M.extend([mi] * len(faces))
        self.S.extend([smooth] * len(faces))

    def revolve(self, profile, mi, segs=72, smooth=True, cap0=False, cap1=False):
        verts, faces = [], []
        for (x, r) in profile:
            for k in range(segs):
                a = 2 * math.pi * k / segs
                verts.append((x, r * math.cos(a), r * math.sin(a)))
        n = len(profile)
        for i in range(n - 1):
            for k in range(segs):
                a0, a1 = i * segs + k, i * segs + (k + 1) % segs
                b0, b1 = (i + 1) * segs + k, (i + 1) * segs + (k + 1) % segs
                faces.append((a0, a1, b1, b0))
        if cap0:
            faces.append(tuple(range(segs - 1, -1, -1)))
        if cap1:
            faces.append(tuple((n - 1) * segs + k for k in range(segs)))
        self.add(verts, faces, mi, smooth)

    def box(self, c, size, mi, yaw=0.0, roll=0.0, smooth=False):
        """An axis-aligned box centred at c with half-sizes `size`, rotated by `roll` about x then placed."""
        hx, hy, hz = size
        cr, sr = math.cos(roll), math.sin(roll)
        verts = []
        for dx in (-hx, hx):
            for dy in (-hy, hy):
                for dz in (-hz, hz):
                    y, z = dy * cr - dz * sr, dy * sr + dz * cr
                    verts.append((c[0] + dx, c[1] + y, c[2] + z))
        faces = [(0, 1, 3, 2), (4, 6, 7, 5), (0, 4, 5, 1), (2, 3, 7, 6), (0, 2, 6, 4), (1, 5, 7, 3)]
        self.add(verts, faces, mi, smooth)

    def disc_on_hull(self, x, ang, r_disc, h, mi, segs=24, r_hull=R):
        """A short cylinder standing on the hull surface at axial position x and roll angle `ang` (0 = top)."""
        ny, nz = -math.sin(ang), math.cos(ang)            # outward normal in the y-z plane
        ty, tz = math.cos(ang), math.sin(ang)             # tangent around the hull
        verts = []
        for lvl, rr in ((r_hull - 0.004, r_disc), (r_hull + h, r_disc * 0.96)):
            for k in range(segs):
                a = 2 * math.pi * k / segs
                u, v = r_disc * math.cos(a) * rr / r_disc, r_disc * math.sin(a) * rr / r_disc
                verts.append((x + u, lvl * ny + v * ty, lvl * nz + v * tz))
        faces = [(k, (k + 1) % segs, segs + (k + 1) % segs, segs + k) for k in range(segs)]
        faces.append(tuple(segs + k for k in range(segs)))
        self.add(verts, faces, mi, smooth=True)

    def fin(self, x_root, chord_root, chord_tip, span, sweep, thick, angle, r0, mi):
        ca, sa = math.cos(angle), math.sin(angle)
        prof = [(x_root, 0.0), (x_root - chord_root, 0.0), (x_root - sweep - chord_tip, span), (x_root - sweep, span)]
        verts = []
        for (x, s) in prof:
            for t in (-thick / 2, thick / 2):
                rr = r0 + s
                verts.append((x, rr * ca - t * sa, rr * sa + t * ca))
        faces = [(0, 2, 4, 6), (1, 7, 5, 3), (0, 1, 3, 2), (2, 3, 5, 4), (4, 5, 7, 6), (6, 7, 1, 0)]
        self.add(verts, faces, mi, smooth=False)

    def blade(self, x0, angle, r_in, r_out, chord, pitch, thick, mi, n=6):
        """A twisted propeller blade in the plane x = x0, spanning radius r_in..r_out at roll `angle`."""
        verts = []
        for i in range(n + 1):
            rr = r_in + (r_out - r_in) * i / n
            tw = pitch * (1.0 - 0.5 * i / n)              # less twist toward the tip
            cw = chord * (1.0 - 0.35 * (i / n) ** 2)
            for s in (-0.5, 0.5):
                for t in (-thick / 2, thick / 2):
                    # chord direction mixes axial (x) and tangential, rotated by the twist
                    dx = s * cw * math.sin(tw) + t * math.cos(tw)
                    dt = s * cw * math.cos(tw) - t * math.sin(tw)
                    a = angle
                    y = rr * math.cos(a) - dt * math.sin(a)
                    z = rr * math.sin(a) + dt * math.cos(a)
                    verts.append((x0 + dx, y, z))
        faces = []
        for i in range(n):
            b0, b1 = 4 * i, 4 * (i + 1)
            faces += [(b0, b0 + 2, b1 + 2, b1), (b0 + 1, b1 + 1, b1 + 3, b0 + 3),
                      (b0, b1, b1 + 1, b0 + 1), (b0 + 2, b0 + 3, b1 + 3, b1 + 2)]
        faces += [(0, 1, 3, 2), (4 * n, 4 * n + 2, 4 * n + 3, 4 * n + 1)]
        self.add(verts, faces, mi, smooth=True)


def prototype(segs: int = 72):
    """Build the AUV once (hidden) and return its mesh data."""
    global _PROTO
    if _PROTO is not None:
        return _PROTO
    me = _Mesh()
    # ---- hull: ogive nose (dark), joint bands, yellow mid-body, dark tail cone ----
    x_nose0 = L - 0.30                                    # where the ogive begins
    ogive = [(L - 0.30 + 0.30 * math.cos(t * math.pi / 2), R * math.sin(t * math.pi / 2)) for t in [i / 16 for i in range(17)]]
    ogive = sorted(ogive)                                  # from x_nose0 to the tip
    tip_split = L - 0.17                                   # the front 17 cm are the dark nose section
    front = [(x, r) for (x, r) in ogive if x >= tip_split]
    back = [(x, r) for (x, r) in ogive if x <= tip_split]
    me.revolve([(0.44, R)] + back, HULL, segs)
    me.revolve(front + [(L + 1e-4, 0.0)], DARK, segs)
    # tinted sensor window on the nose tip
    me.revolve([(L - 0.035, R * 0.52), (L - 0.012, R * 0.36), (L + 0.002, 0.0)], GLASS, segs)
    for xb in (L - 0.185, 1.00, 0.62):                     # joint bands between hull sections
        me.revolve([(xb + 0.012, R * 1.007), (xb - 0.012, R * 1.007)], BAND, segs)
    me.revolve([(0.44, R), (0.32, R * 0.93), (0.20, R * 0.72), (0.11, R * 0.55), (0.10, R * 0.52)], DARK, segs)
    # ---- side-scan sonar panels along the mid-body (both flanks) ----
    for side in (+1, -1):
        y0 = side * (R + 0.002)
        verts = []
        for dx in (-0.15, 0.15):                         # between the joint bands at 0.62 and 1.00
            for dz in (-0.018, 0.018):
                for dy in (0.0, side * 0.004):
                    verts.append((0.81 + dx, y0 + dy, -0.010 + dz))
        faces = [(0, 1, 3, 2), (4, 6, 7, 5), (0, 4, 5, 1), (2, 3, 7, 6), (0, 2, 6, 4), (1, 5, 7, 3)]
        me.add(verts, faces, DARK, smooth=False)
    # ---- top: sensor windows (bow and stern), acoustic modem dome, antenna ----
    me.disc_on_hull(1.22, 0.0, 0.028, 0.012, DARK)
    me.disc_on_hull(1.22, 0.0, 0.020, 0.016, OPTIC)
    me.disc_on_hull(0.52, 0.0, 0.026, 0.012, DARK)
    me.disc_on_hull(0.52, 0.0, 0.018, 0.016, OPTIC)
    me.disc_on_hull(0.72, 0.0, 0.034, 0.030, DARK)        # acoustic modem dome
    mast = []
    for zz in (R + 0.02, R + 0.15):
        for k in range(12):
            a = 2 * math.pi * k / 12
            mast.append((0.80 + 0.007 * math.cos(a), 0.007 * math.sin(a), zz))
    me.add(mast, [(k, (k + 1) % 12, 12 + (k + 1) % 12, 12 + k) for k in range(12)] + [tuple(12 + k for k in range(12))], BAND)
    tip = []
    for i in range(7):
        th = math.pi * i / 6
        for k in range(12):
            ph = 2 * math.pi * k / 12
            tip.append((0.80 + 0.011 * math.sin(th) * math.cos(ph), 0.011 * math.sin(th) * math.sin(ph),
                        R + 0.155 + 0.011 * math.cos(th)))
    me.add(tip, [(i * 12 + k, i * 12 + (k + 1) % 12, (i + 1) * 12 + (k + 1) % 12, (i + 1) * 12 + k)
                 for i in range(6) for k in range(12)], WHITE)
    # ---- belly: Doppler velocity log (four transducer faces) ----
    for (dx, ang) in ((0.0, math.pi - 0.42), (0.0, math.pi + 0.42), (0.07, math.pi - 0.42), (0.07, math.pi + 0.42)):
        me.disc_on_hull(1.30 + dx, ang, 0.016, 0.006, RUBBER)
    # ---- tail: cruciform fins with control surfaces, ducted propeller ----
    for k in range(4):
        a = k * math.pi / 2
        me.fin(0.36, 0.11, 0.07, 0.085, 0.04, 0.008, a, R * 0.78, DARK)
        me.fin(0.25, 0.05, 0.045, 0.085, 0.0, 0.0085, a, R * 0.70, BAND)      # control surface
    duct = [(0.135, R * 0.66), (0.11, R * 0.70), (0.06, R * 0.70), (0.035, R * 0.66),
            (0.035, R * 0.60), (0.06, R * 0.62), (0.11, R * 0.62), (0.135, R * 0.60), (0.135, R * 0.66)]
    me.revolve(duct, DARK, segs)
    me.revolve([(0.11, R * 0.20), (0.07, R * 0.22), (0.04, R * 0.16), (0.03, 0.0)], METAL, 32)   # hub
    for k in range(5):
        me.blade(0.075, 2 * math.pi * k / 5, R * 0.19, R * 0.59, 0.040, 0.75, 0.004, METAL)
    mesh = bpy.data.meshes.new("AUV")
    mesh.from_pydata(me.V, [], me.F)
    mesh.update()
    for m in _materials():
        mesh.materials.append(m)
    for p, mi, sm in zip(mesh.polygons, me.M, me.S):
        p.material_index = mi
        p.use_smooth = sm
    _PROTO = mesh
    return mesh


def place(name: str, location, heading: float, scale: float = 1.0, pitch: float = 0.0):
    """A linked copy of the AUV with its centre at `location`, nose pointing along `heading` (rad, from +x)."""
    ob = bpy.data.objects.new(name, prototype())
    ob.scale = (scale, scale, scale)
    ob.rotation_euler = (0.0, -pitch, heading)
    c, s = math.cos(heading), math.sin(heading)
    off = 0.5 * L * scale
    ob.location = (location[0] - off * c, location[1] - off * s, location[2])
    bpy.context.collection.objects.link(ob)
    return ob
