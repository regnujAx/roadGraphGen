import bpy

from roadGraphGen.roadGraphGen.graph_generator import RGG_GraphGenerator


bl_info = {
    "name": "roadGraphGen",
    "blender": (3, 6, 12),
    "location": "View3D > Toolbar > RoadGraphGen",
    "category": "Object",
    "description": "Generate a procedural road graph."
}


# ------------------------------------------------------------------------
#    Integrates implemented road graph generation with Blender.
#    Currently used for testing and visualization purposes only.
# ------------------------------------------------------------------------


class RGG_BasePanel():
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "RoadGraphGen"


# ------------------------------------------------------------------------
#    Panel in Object Mode
# ------------------------------------------------------------------------


# Creates panel in the 3D Viewport sidebar (open with 'N' by default).
# Includes button to execute main function and test generation of road graph based on tensor field
# defined manually below.
class RGG_RoadGraphGenPanel(RGG_BasePanel, bpy.types.Panel):
    bl_label = "Road Graph Generator"
    bl_idname = "OBJECT_PT_roadGraphGen_panel"

    def draw(self, context):
        layout = self.layout
        layout.operator("rgg.generate_graph")


# ------------------------------------------------------------------------
#    Operator
# ------------------------------------------------------------------------


class RGG_GenerateGraph(bpy.types.Operator):
    bl_idname = "rgg.generate_graph"
    bl_label = "Generate"

    def execute(self, context):
        graph_generator = RGG_GraphGenerator()
        graph_generator.generate()

        return {'FINISHED'}


# ------------------------------------------------------------------------
#    Registration of Panel and Operator
# ------------------------------------------------------------------------


classes = [
    RGG_RoadGraphGenPanel,
    RGG_GenerateGraph
]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
