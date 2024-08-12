import bpy

from roadGridGen.graph_generator import RGG_GraphGenerator


bl_info = {
    "name": "roadGridGen",
    "blender": (3, 6, 12),
    "location": "View3D > Toolbar > roadGridGen",
    "category": "Object",
    "description": "Generate a procedural road grid."
}


# ------------------------------------------------------------------------
#    Integrates implemented road graph generation with Blender.
#    Currently used for testing and visualization purposes only.
# ------------------------------------------------------------------------


class RGG_BasePanel():
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "RoadGridGen"


# ------------------------------------------------------------------------
#    Panel in Object Mode
# ------------------------------------------------------------------------


# Creates panel in the 3D Viewport sidebar (open with 'N' by default).
# Includes button to execute main function and test generation of road graph based on tensor field
# defined manually below.
class RGG_RoadGridPanel(RGG_BasePanel, bpy.types.Panel):
    bl_label = "Road Grid Generator"

    def draw(self, context):
        layout = self.layout
        layout.operator("rgg.generate_grid")


# ------------------------------------------------------------------------
#    Operator
# ------------------------------------------------------------------------


class RGG_GenerateGrid(bpy.types.Operator):
    bl_idname = "rgg.generate_grid"
    bl_label = "Generate"

    def execute(self, context):
        generate()

        return {'FINISHED'}


def generate():
    graph_generator = RGG_GraphGenerator(crossroad_offset=8.0)
    graph_generator.generate_graph()


# ------------------------------------------------------------------------
#    Registration of Operators and Panel
# ------------------------------------------------------------------------


classes = [
    RGG_RoadGridPanel,
    RGG_GenerateGrid
]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
