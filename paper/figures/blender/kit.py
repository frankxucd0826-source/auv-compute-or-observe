"""Shared Blender helpers for the paper's illustrations (run inside Blender 4.5, bpy).

Reused from the student's earlier figure kit: deterministic
scene construction, Cycles with denoising, transparent film, and the pixel positions of named points written to JSON
so that the vector overlay can point at them.  No image generation.
"""
from __future__ import annotations

import math
import os

import bpy
from mathutils import Matrix, Vector

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "cache")


def srgb(hexc: str, a: float = 1.0):
    """'#RRGGBB' -> linear RGBA."""
    h = hexc.lstrip("#")
    out = []
    for k in (0, 2, 4):
        c = int(h[k:k + 2], 16) / 255.0
        out.append(c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4)
    return (out[0], out[1], out[2], a)


def reset() -> None:
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.context.scene.unit_settings.system = "NONE"


def setup_render(width: int, height: int, samples: int, gpu: bool = True, look: str = "AgX - Base Contrast"):
    sc = bpy.context.scene
    sc.render.engine = "CYCLES"
    sc.cycles.samples = samples
    sc.cycles.use_denoising = True
    sc.cycles.seed = 0
    sc.render.resolution_x, sc.render.resolution_y = width, height
    sc.render.resolution_percentage = 100
    sc.render.film_transparent = True
    sc.render.image_settings.file_format = "PNG"
    sc.render.image_settings.color_mode = "RGBA"
    sc.view_settings.view_transform = "AgX"
    sc.view_settings.look = look
    sc.cycles.device = "CPU"
    if gpu:
        prefs = bpy.context.preferences.addons["cycles"].preferences
        for backend in ("OPTIX", "CUDA"):
            try:
                prefs.compute_device_type = backend
                prefs.get_devices()
                if any(d.type == backend for d in prefs.devices):
                    for d in prefs.devices:
                        d.use = d.type == backend
                    sc.cycles.device = "GPU"
                    break
            except TypeError:
                continue
    world = bpy.data.worlds.new("World")
    sc.world = world
    world.use_nodes = True
    return sc


def world_hdri(name: str, strength: float = 1.0, rotation_deg: float = 0.0):
    """Light the scene with an HDRI from the cache (camera rays stay transparent through the film)."""
    path = os.path.join(CACHE, name, f"{name}_2k.hdr")
    nt = bpy.context.scene.world.node_tree
    bg = nt.nodes.get("Background")
    env = nt.nodes.new("ShaderNodeTexEnvironment")
    env.image = bpy.data.images.load(path)
    mapping = nt.nodes.new("ShaderNodeMapping")
    mapping.inputs["Rotation"].default_value[2] = math.radians(rotation_deg)
    tc = nt.nodes.new("ShaderNodeTexCoord")
    nt.links.new(tc.outputs["Generated"], mapping.inputs["Vector"])
    nt.links.new(mapping.outputs["Vector"], env.inputs["Vector"])
    nt.links.new(env.outputs["Color"], bg.inputs["Color"])
    bg.inputs["Strength"].default_value = strength


def node_mat(name):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    nt.nodes.clear()
    return m, nt, nt.nodes.new("ShaderNodeOutputMaterial")


def principled(name, hexc, rough=0.45, metal=0.0, coat=0.0, alpha=1.0, sss=0.0):
    m, nt, out = node_mat(name)
    b = nt.nodes.new("ShaderNodeBsdfPrincipled")
    b.inputs["Base Color"].default_value = srgb(hexc)
    b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = metal
    b.inputs["Coat Weight"].default_value = coat
    if sss:
        b.inputs["Subsurface Weight"].default_value = sss
        b.inputs["Subsurface Radius"].default_value = (0.4, 0.4, 0.35)
    if alpha < 1.0:
        b.inputs["Alpha"].default_value = alpha
        m.blend_method = "BLEND"
    nt.links.new(b.outputs[0], out.inputs["Surface"])
    return m


def emission(name, hexc, strength, alpha=1.0):
    m, nt, out = node_mat(name)
    em = nt.nodes.new("ShaderNodeEmission")
    em.inputs["Color"].default_value = srgb(hexc)
    em.inputs["Strength"].default_value = strength
    if alpha < 1.0:
        tr = nt.nodes.new("ShaderNodeBsdfTransparent")
        mix = nt.nodes.new("ShaderNodeMixShader")
        mix.inputs["Fac"].default_value = alpha
        nt.links.new(tr.outputs[0], mix.inputs[1])
        nt.links.new(em.outputs[0], mix.inputs[2])
        nt.links.new(mix.outputs[0], out.inputs["Surface"])
        m.blend_method = "BLEND"
    else:
        nt.links.new(em.outputs[0], out.inputs["Surface"])
    return m


def link(ob):
    bpy.context.collection.objects.link(ob)
    return ob


def mesh_object(name, verts, faces, mat, smooth=True):
    me = bpy.data.meshes.new(name)
    me.from_pydata(verts, [], faces)
    me.update()
    if smooth:
        for p in me.polygons:
            p.use_smooth = True
    ob = bpy.data.objects.new(name, me)
    ob.data.materials.append(mat)
    return link(ob)


def box(name, center, dims, mat, bevel=0.0, segments=4):
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=center)
    ob = bpy.context.active_object
    ob.name = name
    ob.scale = dims
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    ob.data.materials.append(mat)
    if bevel > 0:
        mod = ob.modifiers.new("Bevel", "BEVEL")
        mod.width, mod.segments = bevel, segments
        ob.modifiers.new("WN", "WEIGHTED_NORMAL")
        for p in ob.data.polygons:
            p.use_smooth = True
    return ob


def frustum(name, p0, p1, r0, r1, mat, verts=64, cap=True):
    """A cylinder or truncated cone from point p0 (radius r0) to p1 (radius r1)."""
    p0, p1 = Vector(p0), Vector(p1)
    d = p1 - p0
    bpy.ops.mesh.primitive_cone_add(vertices=verts, radius1=r0, radius2=r1, depth=d.length,
                                    end_fill_type="NGON" if cap else "NOTHING", location=(p0 + p1) / 2)
    ob = bpy.context.active_object
    ob.name = name
    ob.rotation_euler = d.to_track_quat("Z", "Y").to_euler()
    ob.data.materials.append(mat)
    for p in ob.data.polygons:
        p.use_smooth = True
    ob.modifiers.new("WN", "WEIGHTED_NORMAL")
    return ob


def sphere(name, center, radius, mat, scale=(1, 1, 1), segs=48):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=segs, ring_count=segs // 2, radius=radius, location=center)
    ob = bpy.context.active_object
    ob.name = name
    ob.scale = scale
    ob.data.materials.append(mat)
    for p in ob.data.polygons:
        p.use_smooth = True
    return ob


def tube(name, pts, radius, mat, res=3):
    cu = bpy.data.curves.new(name, type="CURVE")
    cu.dimensions = "3D"
    cu.bevel_depth = radius
    cu.bevel_resolution = res
    cu.use_fill_caps = True
    sp = cu.splines.new("POLY")
    sp.points.add(len(pts) - 1)
    for k, p in enumerate(pts):
        sp.points[k].co = (p[0], p[1], p[2], 1.0)
    ob = bpy.data.objects.new(name, cu)
    ob.data.materials.append(mat)
    return link(ob)


def ring(name, center, normal, radius, thick, mat, segs=128):
    """A torus of the given radius whose axis is `normal`."""
    bpy.ops.mesh.primitive_torus_add(major_radius=radius, minor_radius=thick, major_segments=segs,
                                     minor_segments=10, location=center)
    ob = bpy.context.active_object
    ob.name = name
    ob.rotation_euler = Vector(normal).to_track_quat("Z", "Y").to_euler()
    ob.data.materials.append(mat)
    return ob


def append_object(blend_path):
    with bpy.data.libraries.load(blend_path, link=False) as (src, dst):
        dst.objects = list(src.objects)[:1]
    return link(dst.objects[0])


def area_light(name, location, target, energy, size, color=(1.0, 1.0, 1.0)):
    li = bpy.data.lights.new(name, type="AREA")
    li.energy, li.size, li.color = energy, size, color
    li.shape = "DISK"
    ob = bpy.data.objects.new(name, li)
    ob.location = location
    ob.rotation_euler = (Vector(target) - Vector(location)).to_track_quat("-Z", "Y").to_euler()
    return link(ob)


def camera(location, target, lens=35.0, ortho_scale=None):
    cam = bpy.data.cameras.new("Camera")
    cam.lens = lens
    cam.clip_end = 5000.0
    if ortho_scale:
        cam.type = "ORTHO"
        cam.ortho_scale = ortho_scale
    ob = link(bpy.data.objects.new("Camera", cam))
    ob.location = location
    ob.rotation_euler = (Vector(target) - Vector(location)).to_track_quat("-Z", "Y").to_euler()
    bpy.context.scene.camera = ob
    return ob


def place(ob, matrix):
    ob.matrix_world = matrix
    return ob


def frame_matrix(origin, x_axis, y_axis, z_axis):
    """World matrix whose local x, y, z axes are the given (orthonormal) vectors."""
    R = Matrix((x_axis, y_axis, z_axis)).transposed().to_4x4()
    return Matrix.Translation(Vector(origin)) @ R


def project(scene, cam, pts: dict) -> dict:
    """Pixel coordinates (x right, y down) of named world points."""
    from bpy_extras.object_utils import world_to_camera_view
    bpy.context.view_layer.update()
    rx, ry = scene.render.resolution_x, scene.render.resolution_y
    out = {}
    for k, v in pts.items():
        p = world_to_camera_view(scene, cam, Vector(v))
        out[k] = (round(p.x * rx, 1), round((1.0 - p.y) * ry, 1))
    return out
