"""Render one LDraw part with Blender in background mode."""

from __future__ import annotations

import json
import sys
from math import cos, radians, sin
from pathlib import Path

import bpy
from mathutils import Vector


def arguments() -> list[str]:
    return sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []


def argument_value(name: str, default: str | None = None) -> str:
    try:
        return arguments()[arguments().index(name) + 1]
    except (ValueError, IndexError) as error:
        if default is not None:
            return default
        raise SystemExit(f"Missing required argument: {name}") from error


def enable_importer(repository_root: Path) -> None:
    """Load ImportLDraw plus a runtime adapter for Blender 5.2."""
    importer_parent = repository_root / "data" / "tools"
    if not importer_parent.is_dir():
        raise SystemExit(f"ImportLDraw was not found in {importer_parent}")
    sys.path.insert(0, str(importer_parent))
    import ImportLDraw  # pylint: disable=import-outside-toplevel
    from ImportLDraw.loadldraw.loadldraw import (  # pylint: disable=import-outside-toplevel
        BlenderMaterials,
    )

    def set_defaults(
        group: bpy.types.NodeTree, name: str, default: float, _min: float, _max: float
    ) -> None:
        group_input = next(node for node in group.nodes if node.bl_idname == "NodeGroupInput")
        group_input.outputs[name].default_value = default

    BlenderMaterials.setDefaults = staticmethod(set_defaults)
    ImportLDraw.register()


def mesh_bounds() -> tuple[Vector, Vector]:
    points = [
        object_.matrix_world @ Vector(corner)
        for object_ in bpy.context.scene.objects
        if object_.type == "MESH"
        for corner in object_.bound_box
    ]
    if not points:
        raise RuntimeError("The LDraw import produced no mesh objects.")
    return (
        Vector(min(point[axis] for point in points) for axis in range(3)),
        Vector(max(point[axis] for point in points) for axis in range(3)),
    )


def apply_reference_material() -> None:
    material = bpy.data.materials.new("BrickVision Reference Red")
    material.diffuse_color = (0.52, 0.008, 0.01, 1.0)
    material.use_nodes = True
    principled = material.node_tree.nodes.get("Principled BSDF")
    if principled is not None:
        principled.inputs["Base Color"].default_value = material.diffuse_color
        principled.inputs["Roughness"].default_value = 0.3
    for object_ in bpy.context.scene.objects:
        if object_.type == "MESH":
            object_.data.materials.clear()
            object_.data.materials.append(material)


def view_definitions(view_set: str) -> list[dict[str, float | str]]:
    if view_set == "single":
        return [{"name": "view_00", "azimuth": -45.0, "elevation": 28.0}]
    if view_set == "poc-28":
        orbit_views = [
            {
                "name": f"orbit_{azimuth:03d}_{elevation:02d}",
                "azimuth": float(azimuth),
                "elevation": float(elevation),
            }
            for azimuth in range(0, 360, 45)
            for elevation in (20, 45, 70)
        ]
        return orbit_views + [
            {"name": "top", "azimuth": 0.0, "elevation": 88.0},
            {"name": "bottom", "azimuth": 0.0, "elevation": -70.0},
            {"name": "front", "azimuth": 0.0, "elevation": 0.0},
            {"name": "back", "azimuth": 180.0, "elevation": 0.0},
        ]
    raise SystemExit(f"Unknown view set: {view_set}. Use 'single' or 'poc-28'.")


def add_camera(bounds_min: Vector, bounds_max: Vector, azimuth: float, elevation: float) -> None:
    center = (bounds_min + bounds_max) / 2
    radius = max((bounds_max - bounds_min).length / 2, 0.05)
    azimuth_radians = radians(azimuth)
    elevation_radians = radians(elevation)
    position = Vector(
        (
            cos(azimuth_radians) * cos(elevation_radians),
            sin(azimuth_radians) * cos(elevation_radians),
            sin(elevation_radians),
        )
    )
    bpy.ops.object.camera_add(location=center + position * radius * 3.0)
    camera = bpy.context.object
    camera.data.lens = 55
    camera.rotation_euler = (center - camera.location).to_track_quat("-Z", "Y").to_euler()
    bpy.context.scene.camera = camera


def main() -> None:
    repository_root = Path(__file__).resolve().parents[1]
    library = Path(argument_value("--library")).resolve()
    part_name = argument_value("--part")
    output_directory = Path(argument_value("--output")).resolve()
    view_set = argument_value("--view-set", "single")
    part_path = library / "parts" / part_name
    if not part_path.is_file() or not (library / "p").is_dir():
        raise SystemExit(f"Invalid part or LDraw library: {part_path}")

    enable_importer(repository_root)
    bpy.ops.import_scene.importldraw(
        filepath=str(part_path),
        ldrawPath=str(library),
        realScale=1.0,
        look="normal",
        colourScheme="lgeo",
        defaultColour="4",
        addEnvironment=False,
        positionCamera=False,
        useLogoStuds=False,
        useUnofficialParts=False,
        bevelEdges=True,
        bevelWidth=0.5,
    )
    bpy.context.view_layer.update()
    bounds_min, bounds_max = mesh_bounds()
    apply_reference_material()

    scene = bpy.context.scene
    scene.render.engine = "BLENDER_WORKBENCH"
    scene.display.shading.light = "STUDIO"
    scene.display.shading.color_type = "MATERIAL"
    scene.display.shading.background_type = "WORLD"
    scene.display.shading.background_color = (0.04, 0.04, 0.04)
    scene.render.resolution_x = 512
    scene.render.resolution_y = 512
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    output_directory.mkdir(parents=True, exist_ok=True)

    metadata: list[dict[str, float | str]] = []
    for view in view_definitions(view_set):
        add_camera(bounds_min, bounds_max, float(view["azimuth"]), float(view["elevation"]))
        filename = f"{view['name']}.png"
        scene.render.filepath = str(output_directory / filename)
        bpy.ops.render.render(write_still=True)
        bpy.data.objects.remove(scene.camera, do_unlink=True)
        metadata.append({**view, "file": filename})

    (output_directory / "render_metadata.json").write_text(
        json.dumps(
            {"part": part_name, "view_set": view_set, "resolution": [512, 512], "views": metadata},
            indent=2,
        ),
        encoding="utf-8",
    )
    print(f"Rendered {len(metadata)} views of {part_name} to {output_directory}")


if __name__ == "__main__":
    main()
