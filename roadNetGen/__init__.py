import bpy

from .graph_generator import RNG_GraphGenerator


bl_info = {
    "name": "roadNetGen",
    "blender": (3, 6, 12),
    "location": "View3D > Toolbar > RoadNetGen",
    "category": "Object",
    "description": "Generate a procedural road net."
}


# ------------------------------------------------------------------------
#    Integrates implemented road graph generation with Blender.
#    Currently used for testing and visualization purposes only.
# ------------------------------------------------------------------------


class RNG_BasePanel():
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "RoadNetGen"


# ------------------------------------------------------------------------
#    Panel in Object Mode
# ------------------------------------------------------------------------


# Creates panel in the 3D Viewport sidebar (open with 'N' by default).
# Includes button to execute main function and test generation of road graph based on tensor field
# defined manually below.
class RNG_RoadNetPanel(RNG_BasePanel, bpy.types.Panel):
    bl_label = "Road Net Generator"

    def draw(self, context):
        layout = self.layout
        layout.operator("rng.generate_net")


# ------------------------------------------------------------------------
#    Operator
# ------------------------------------------------------------------------


class RNG_GenerateNet(bpy.types.Operator):
    bl_idname = "rng.generate_net"
    bl_label = "Generate"

    def execute(self, context):
        generate()

        return {'FINISHED'}


def generate():
    graph_generator = RNG_GraphGenerator(crossroad_offset=8.0)
    graph_generator.generate_graph()


# ------------------------------------------------------------------------
#    Registration of Operators and Panel
# ------------------------------------------------------------------------


classes = [
    RNG_RoadNetPanel,
    RNG_GenerateNet
]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
