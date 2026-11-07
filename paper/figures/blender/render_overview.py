"""Central render of the overview figure (Blender 4.5, run with -b -P).

A cut-away box of the East China Sea window of one test mission: the surface is the real
chlorophyll field the vehicle meets (texture from data), a REMUS-class AUV on its way to the
bloom core, its track coloured by how each interval was spent, and above the sea a stack of
imagined oceans (the vehicle's ensemble; the top ones, framed orange, are held out from the
search). A satellite at the upper left stands for the satellite map.

    blender -b -P paper/figures/blender/render_overview.py -- --samples 128
Writes ../renders/overview.png and ../renders/overview_anchors.json
"""
import json
import math
import os
import sys

import bpy

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import kit as K  # noqa: E402
import auv_model as AUV  # noqa: E402

REND = os.path.join(HERE, "..", "renders")
TEX = os.path.join(REND, "textures")
S = 12.0          # sea window side (world units)
DEPTH = 2.6


def argv():
    a = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    out = {"samples": 128, "w": 2400, "h": 1600}
    for k in range(0, len(a), 2):
        out[a[k].lstrip("-")] = int(a[k + 1])
    return out


def image_material(name, path, alpha=1.0, emit=0.35, rough=0.3):
    m, nt, out = K.node_mat(name)
    tex = nt.nodes.new("ShaderNodeTexImage")
    tex.image = bpy.data.images.load(path)
    tex.interpolation = "Cubic"
    b = nt.nodes.new("ShaderNodeBsdfPrincipled")
    b.inputs["Roughness"].default_value = rough
    nt.links.new(tex.outputs["Color"], b.inputs["Base Color"])
    nt.links.new(tex.outputs["Color"], b.inputs["Emission Color"])
    b.inputs["Emission Strength"].default_value = emit
    if alpha < 1.0:
        b.inputs["Alpha"].default_value = alpha
        m.blend_method = "BLEND"
    nt.links.new(b.outputs[0], out.inputs["Surface"])
    return m


def gradient_wall(name, stops):
    m, nt, out = K.node_mat(name)
    tc = nt.nodes.new("ShaderNodeTexCoord")
    sep = nt.nodes.new("ShaderNodeSeparateXYZ")
    nt.links.new(tc.outputs["Generated"], sep.inputs["Vector"])
    ramp = nt.nodes.new("ShaderNodeValToRGB")
    ramp.color_ramp.elements[0].position, ramp.color_ramp.elements[0].color = stops[0][0], K.srgb(stops[0][1])
    ramp.color_ramp.elements[1].position, ramp.color_ramp.elements[1].color = stops[-1][0], K.srgb(stops[-1][1])
    for pos, col in stops[1:-1]:
        e = ramp.color_ramp.elements.new(pos)
        e.color = K.srgb(col)
    nt.links.new(sep.outputs["Z"], ramp.inputs["Fac"])
    em = nt.nodes.new("ShaderNodeEmission")
    nt.links.new(ramp.outputs["Color"], em.inputs["Color"])
    nt.links.new(em.outputs[0], out.inputs["Surface"])
    return m


def sea():
    # textured surface with a gentle swell
    n = 160
    verts, faces, uvs = [], [], []
    for j in range(n + 1):
        for i in range(n + 1):
            x, y = S * i / n, S * j / n
            z = 0.035 * math.sin(1.3 * x + 0.7 * y) + 0.02 * math.sin(2.1 * y - 0.9 * x)
            verts.append((x, y, z))
    for j in range(n):
        for i in range(n):
            a = j * (n + 1) + i
            faces.append((a, a + 1, a + n + 2, a + n + 1))
    me = bpy.data.meshes.new("Sea")
    me.from_pydata(verts, [], faces)
    uv = me.uv_layers.new(name="UV")
    for poly in me.polygons:
        for li in poly.loop_indices:
            v = me.vertices[me.loops[li].vertex_index].co
            uv.data[li].uv = (v.x / S, v.y / S)
    for p in me.polygons:
        p.use_smooth = True
    ob = bpy.data.objects.new("Sea", me)
    ob.data.materials.append(image_material("SeaTex", os.path.join(TEX, "sea.png"), emit=0.45, rough=0.18))
    K.link(ob)
    wall = gradient_wall("Wall", [(0.0, "#0E4A73"), (0.6, "#2E86BC"), (1.0, "#8FD3EC")])
    zb = -DEPTH
    K.mesh_object("WallFront", [(0, 0, zb), (S, 0, zb), (S, 0, 0), (0, 0, 0)], [(0, 1, 2, 3)], wall, smooth=False)
    K.mesh_object("WallLeft", [(0, 0, zb), (0, S, zb), (0, S, 0), (0, 0, 0)], [(0, 1, 2, 3)], wall, smooth=False)
    floor = K.principled("Floor", "#C9B88F", rough=0.9)
    K.mesh_object("Floor", [(0, 0, zb), (S, 0, zb), (S, S, zb), (0, S, zb)], [(0, 1, 2, 3)], floor, smooth=False)


def track(points, colours, radius=0.11):
    for k, ((p0, p1), col) in enumerate(zip(zip(points[:-1], points[1:]), colours)):
        ob = K.tube(f"Track{k}", [p0, p1], radius, K.emission(f"TrackMat{k}", col, 3.0))
        ob.visible_shadow = False


def imagined_stack(x0, y0, z0, side, n=6, held=2, gap=0.42):
    corners = {}
    frame_search = K.emission("FrameSearch", "#1F3A5F", 1.5)
    frame_held = K.emission("FrameHeld", "#E8590C", 3.0)
    for k in range(n):
        z = z0 + k * gap
        m = image_material(f"Imag{k}", os.path.join(TEX, f"imagined_{k % 6}.png"), alpha=0.92, emit=0.5)
        K.mesh_object(f"Imagined{k}", [(x0, y0, z), (x0 + side, y0, z), (x0 + side, y0 + side, z), (x0, y0 + side, z)],
                      [(0, 1, 2, 3)], m, smooth=False)
        ob = bpy.data.objects[f"Imagined{k}"]
        ob.visible_shadow = False
        uv = ob.data.uv_layers.new(name="UV")
        for li, (u, v) in zip(range(4), [(0, 0), (1, 0), (1, 1), (0, 1)]):
            uv.data[li].uv = (u, v)
        fm = frame_held if k >= n - held else frame_search
        pts = [(x0, y0, z), (x0 + side, y0, z), (x0 + side, y0 + side, z), (x0, y0 + side, z), (x0, y0, z)]
        fr = K.tube(f"Frame{k}", pts, 0.035 if k < n - held else 0.05, fm)
        fr.visible_shadow = False
        corners[f"imag{k}"] = (x0 + side, y0, z)
    return corners


def satellite(c):
    gold = K.principled("Foil", "#D9A440", rough=0.35, metal=0.8)
    panel = K.principled("Panel", "#1D3B78", rough=0.25, metal=0.3, coat=0.5)
    K.box("SatBody", c, (0.55, 0.55, 0.8), gold, bevel=0.04)
    K.box("SatPanelL", (c[0] - 1.05, c[1], c[2]), (1.4, 0.05, 0.55), panel)
    K.box("SatPanelR", (c[0] + 1.05, c[1], c[2]), (1.4, 0.05, 0.55), panel)
    K.tube("SatBoom", [(c[0] - 0.35, c[1], c[2]), (c[0] + 0.35, c[1], c[2])], 0.03, K.principled("Boom", "#888888"))


def main():
    a = argv()
    K.reset()
    sc = K.setup_render(a["w"], a["h"], a["samples"])
    K.world_hdri("kloofendal_48d_partly_cloudy_puresky", 0.65, rotation_deg=120)
    meta = json.load(open(os.path.join(TEX, "meta.json")))
    cs = S / 40.0
    start = (meta["start"][0] * cs + 0.15, meta["start"][1] * cs, 0.06)
    core = (meta["core"][0] * cs + 0.5 * cs, meta["core"][1] * cs + 0.5 * cs, 0.06)
    sea()
    # the vehicle two thirds of the way to the core, a gently curved track behind it
    auv_xy = (start[0] + 0.62 * (core[0] - start[0]), start[1] - 0.6)
    pts = []
    for k in range(9):
        t = k / 8
        x = start[0] + t * (auv_xy[0] - start[0])
        y = start[1] + t * (auv_xy[1] - start[1]) + 0.55 * math.sin(math.pi * t)
        pts.append((x, y, 0.06))
    cols = ["#1C7ED6"] * 3 + ["#F08C00"] * 2 + ["#1C7ED6"] * 3
    track(pts, cols)
    heading = math.atan2(core[1] - auv_xy[1], core[0] - auv_xy[0])
    AUV.place("AUV", (auv_xy[0], auv_xy[1], 0.07), heading, scale=2.6)
    cr = K.ring("CoreRing", core, (0, 0, 1), 0.6, 0.08, K.emission("CoreMat", "#FFD43B", 5.0))
    cr.visible_shadow = False
    corners = imagined_stack(7.4, 7.2, 2.2, 3.6)
    K.area_light("Key", (-4.0, -8.0, 16.0), (6.0, 6.0, 0.0), 2600.0, 12.0)
    K.area_light("Fill", (20.0, -6.0, 10.0), (6.0, 6.0, 1.0), 1200.0, 10.0, (0.8, 0.9, 1.0))
    cam = K.camera((-7.4, -10.0, 9.0), (6.6, 6.9, 0.2), lens=38.0)
    anchors = K.project(sc, cam, {"auv": (auv_xy[0], auv_xy[1], 0.07), "core": core, "start": start,
                                  "imag_top": corners["imag5"],
                                  "imag_bottom": corners["imag0"], "sea_corner": (S, 0, 0),
                                  "think_seg": pts[4]})
    out = os.path.join(REND, "overview.png")
    sc.render.filepath = out
    bpy.ops.render.render(write_still=True)
    json.dump(anchors, open(os.path.join(REND, "overview_anchors.json"), "w"), indent=1)
    print("rendered", out, anchors)


if __name__ == "__main__":
    main()
