import bpy

from roadGraphGen.roadGraphGen.graph_generator import RGG_GraphGenerator


bl_info = {
    "name": "roadGraphGen",
    "blender": (3, 6, 12),
    "location": "View3D > Toolbar > RoadNetGen",
    "category": "Object",
    "description": "Generate a procedural road net."
}


# ------------------------------------------------------------------------
#    Integrates implemented road graph generation with Blender.
#    Currently used for testing and visualization purposes only.
# ------------------------------------------------------------------------


class RGG_BasePanel():
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "RoadNetGen"


# ------------------------------------------------------------------------
#    Panel in Object Mode
# ------------------------------------------------------------------------


# Creates panel in the 3D Viewport sidebar (open with 'N' by default).
# Includes button to execute main function and test generation of road graph based on tensor field
# defined manually below.
class RGG_RoadNetPanel(RGG_BasePanel, bpy.types.Panel):
    bl_label = "Road Net Generator"

    def draw(self, context):
        layout = self.layout
        layout.operator("rng.generate_net")


# ------------------------------------------------------------------------
#    Operator
# ------------------------------------------------------------------------


class RGG_GenerateNet(bpy.types.Operator):
    bl_idname = "rng.generate_net"
    bl_label = "Generate"

    def execute(self, context):
        graph_generator = RGG_GraphGenerator()
        graph_generator.generate()

        return {'FINISHED'}


# ------------------------------------------------------------------------
#    Registration of Operators and Panel
# ------------------------------------------------------------------------


classes = [
    RGG_RoadNetPanel,
    RGG_GenerateNet
]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
