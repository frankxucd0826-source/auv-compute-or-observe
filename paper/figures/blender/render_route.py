"""Central render of Fig. 1 (Blender 4.5, run with -b -P).

A cut-away box of the sea around the example mission (2022-01-18): the surface is the real current of that
day (texture from data), a red cylinder marks the no-go zone, the two fastest routes in the real current
(right side faster) are glowing tubes, an AUV sits at the start, and above the sea floats a stack of fields
from the plausible set (texture from data: the coarse map in the middle, the counterexample on top).
A satellite at the upper left stands for a fresh current map obtained by surfacing.

    blender -b -P paper/figures/blender/render_route.py -- --samples 128
Writes ../renders/route_scene.png and ../renders/route_anchors.json
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
S = 12.0
DEPTH = 2.4


def argv():
    a = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    out = {"samples": 128, "w": 2400, "h": 1500}
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


def swell(x, y):
    return 0.03 * math.sin(1.3 * x + 0.7 * y) + 0.018 * math.sin(2.1 * y - 0.9 * x)


def sea():
    n = 180
    verts, faces = [], []
    for j in range(n + 1):
        for i in range(n + 1):
            x, y = S * i / n, S * j / n
            verts.append((x, y, swell(x, y)))
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
    ob.data.materials.append(image_material("SeaTex", os.path.join(TEX, "route_sea.png"), emit=0.35, rough=0.15))
    K.link(ob)
    wall = gradient_wall("Wall", [(0.0, "#0B2C4A"), (0.6, "#1F5F8F"), (1.0, "#6FB6D6")])
    zb = -DEPTH
    K.mesh_object("WallFront", [(0, 0, zb), (S, 0, zb), (S, 0, 0), (0, 0, 0)], [(0, 1, 2, 3)], wall, smooth=False)
    K.mesh_object("WallLeft", [(0, 0, zb), (0, S, zb), (0, S, 0), (0, 0, 0)], [(0, 1, 2, 3)], wall, smooth=False)
    floor = K.principled("Floor", "#B9A782", rough=0.9)
    K.mesh_object("Floor", [(0, 0, zb), (S, 0, zb), (S, S, zb), (0, S, zb)], [(0, 1, 2, 3)], floor, smooth=False)


def route(name, pts_uv, colour, radius, strength):
    pts = [(u * S, v * S, swell(u * S, v * S) + 0.07) for u, v in pts_uv]
    ob = K.tube(name, pts, radius, K.emission(name + "Mat", colour, strength))
    ob.visible_shadow = False
    return pts


def nogo(c_uv, r_uv):
    c = (c_uv[0] * S, c_uv[1] * S)
    R = r_uv * S
    red = K.emission("NoGo", "#E03131", 2.0, alpha=0.5)
    K.frustum("NoGoCyl", (c[0], c[1], -DEPTH), (c[0], c[1], 0.32), R, R, red, verts=96, cap=True)
    top = K.emission("NoGoTop", "#FF8787", 1.5, alpha=0.45)
    K.frustum("NoGoTop", (c[0], c[1], 0.30), (c[0], c[1], 0.33), R, R, top, verts=96, cap=True)
    ring = K.ring("NoGoRing", (c[0], c[1], 0.33), (0, 0, 1), R, 0.045, K.emission("NoGoRingMat", "#FF6B6B", 4.0))
    ring.visible_shadow = False
    return (c[0], c[1], 0.33)


def stack(x0, y0, z0, side, gap=0.46):
    frames = {0: ("#28476B", 0.03), 1: ("#28476B", 0.03), 2: ("#8A99A8", 0.05), 3: ("#28476B", 0.03),
              4: ("#3B82F6", 0.06)}
    corners = {}
    for k in range(5):
        z = z0 + k * gap
        m = image_material(f"Stack{k}", os.path.join(TEX, f"route_stack{k}.png"), alpha=0.95, emit=0.4)
        K.mesh_object(f"Sheet{k}", [(x0, y0, z), (x0 + side, y0, z), (x0 + side, y0 + side, z), (x0, y0 + side, z)],
                      [(0, 1, 2, 3)], m, smooth=False)
        ob = bpy.data.objects[f"Sheet{k}"]
        ob.visible_shadow = False
        uvl = ob.data.uv_layers.new(name="UV")
        for li, (u, v) in zip(range(4), [(0, 0), (1, 0), (1, 1), (0, 1)]):
            uvl.data[li].uv = (u, v)
        col, rad = frames[k]
        pts = [(x0, y0, z), (x0 + side, y0, z), (x0 + side, y0 + side, z), (x0, y0 + side, z), (x0, y0, z)]
        fr = K.tube(f"Frame{k}", pts, rad, K.emission(f"FrameMat{k}", col, 2.5 if k == 4 else 1.4))
        fr.visible_shadow = False
        corners[k] = {"right": (x0 + side, y0 + side * 0.5, z), "front": (x0 + side * 0.5, y0, z),
                      "left": (x0, y0 + side * 0.5, z)}
    return corners


def satellite(c):
    gold = K.principled("Foil", "#D9A440", rough=0.35, metal=0.8)
    panel = K.principled("Panel", "#1D3B78", rough=0.25, metal=0.3, coat=0.5)
    K.box("SatBody", c, (0.5, 0.5, 0.72), gold, bevel=0.04)
    K.box("SatPanelL", (c[0] - 0.95, c[1], c[2]), (1.25, 0.05, 0.5), panel)
    K.box("SatPanelR", (c[0] + 0.95, c[1], c[2]), (1.25, 0.05, 0.5), panel)
    K.tube("SatBoom", [(c[0] - 0.32, c[1], c[2]), (c[0] + 0.32, c[1], c[2])], 0.03, K.principled("Boom", "#888888"))


def main():
    a = argv()
    K.reset()
    sc = K.setup_render(a["w"], a["h"], a["samples"])
    K.world_hdri("kloofendal_48d_partly_cloudy_puresky", 0.65, rotation_deg=120)
    meta = json.load(open(os.path.join(TEX, "route_meta.json")))
    sea()
    ptsR = route("RouteR", meta["route_R"], "#FF5C8A", 0.10, 5.0)
    ptsL = route("RouteL", meta["route_L"], "#FFC53D", 0.065, 3.0)
    centre = nogo(meta["centre"], meta["radius"])
    s = (meta["start"][0] * S, meta["start"][1] * S)
    g = (meta["goal"][0] * S, meta["goal"][1] * S)
    goal_mat = K.emission("GoalMat", "#FFFFFF", 3.0)
    gr = K.ring("GoalRing", (g[0], g[1], 0.09), (0, 0, 1), 0.28, 0.05, goal_mat)
    gr.visible_shadow = False
    # vehicle a little way down the common first leg, nose along the first leg of the right route
    p0, p1 = ptsR[0], ptsR[min(3, len(ptsR) - 1)]
    heading = math.atan2(p1[1] - p0[1], p1[0] - p0[0])
    auv_xy = (p0[0] + 0.25 * math.cos(heading), p0[1] + 0.25 * math.sin(heading))
    AUV.place("AUV", (auv_xy[0], auv_xy[1], 0.10), heading, scale=2.0)
    corners = stack(7.6, 7.4, 2.5, 3.6)
    sat = (1.6, 9.2, 7.4)
    satellite(sat)
    K.area_light("Key", (-4.0, -8.0, 16.0), (6.0, 6.0, 0.0), 2600.0, 12.0)
    K.area_light("Fill", (20.0, -6.0, 10.0), (6.0, 6.0, 1.0), 1200.0, 10.0, (0.8, 0.9, 1.0))
    cam = K.camera((-7.2, -10.4, 9.6), (6.4, 6.6, 1.2), lens=36.0)
    mid = lambda P: P[len(P) // 2]  # noqa: E731
    anchors = K.project(sc, cam, {"auv": (auv_xy[0], auv_xy[1], 0.1), "start": (s[0], s[1], 0.1),
                                  "goal": (g[0], g[1], 0.1), "nogo": centre, "nogo_base": (centre[0], centre[1], -DEPTH),
                                  "routeL": mid(ptsL), "routeR": mid(ptsR), "sat": sat,
                                  "sheet_map": corners[2]["right"], "sheet_cx": corners[4]["right"],
                                  "sheet_low": corners[0]["right"], "sheet_map_l": corners[2]["left"],
                                  "sheet_cx_l": corners[4]["left"], "sea_corner": (S, 0, 0), "sea_back": (S, S, 0)})
    out = os.path.join(REND, "route_scene.png")
    sc.render.filepath = out
    bpy.ops.render.render(write_still=True)
    json.dump(anchors, open(os.path.join(REND, "route_anchors.json"), "w"), indent=1)
    print("rendered", out, anchors)


if __name__ == "__main__":
    main()
