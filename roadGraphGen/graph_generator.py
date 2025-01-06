import bmesh
import bpy

from mathutils import Vector
from time import time

from roadGraphGen.roadGraphGen.graph import Graph
from roadGraphGen.roadGraphGen.integrator import RK4Integrator
from roadGraphGen.roadGraphGen.streamline_parameters import StreamlineParameters
from roadGraphGen.roadGraphGen.streamlines import StreamlineGenerator
from roadGraphGen.roadGraphGen.tensor_field import TensorField


class RGG_GraphGenerator():
    def __init__(self, width: int = 100, height: int = 100, seed: int = None):
        # Create new global TensorField.
        self.field = TensorField()

        # Create new StreamlineParameters. Values used here are derived from testing and seem like a good baseline.
        self.parameters = StreamlineParameters(
            dsep=100,
            dtest=30,
            dstep=1,
            dcirclejoin=5,
            dlookahead=200,
            joinangle=0.1,
            path_iterations=1500,
            seed_tries=500,
            simplify_tolerance=0.01,
            collide_early=0,
        )

        # Create new RK4Integrator with tensor field and parameters as input.
        self.integrator = RK4Integrator(
            self.field,
            self.parameters
        )

        # Create new StreamlineGenerator with integrator, parameters, and origin + world dimensions as input variables.
        # Current testing shows that integer values based on common screen sizes work well.
        self.generator = StreamlineGenerator(
            integrator=self.integrator,
            origin=Vector((519, 249)),
            world_dimensions=Vector((width, height)),
            parameters=self.parameters,
            seed=seed
        )

    def generate(self, with_visualization: bool = True):
        print(f"\n\n--- Starting graph generation of size {int(self.generator.world_dimensions[0])} x "
              f"{int(self.generator.world_dimensions[1])} with seed {self.generator.seed} ---")

        # Add two grid and one radial basis field to the global field.
        self.field.add_grid(Vector((1381, 788)), 1500, 35, 1.983775)
        self.field.add_grid(Vector((1181, 988)), 1500, 35, -1.283775)
        self.field.add_radial(Vector((800, 888)), 750, 55)

        # Generate all streamlines.
        print("\n- Starting generation of streamlines -")

        t = time()

        self.generator.create_all_streamlines()

        print(f"Generation of streamlines completed in {time() - t:.2f}s")

        # Generate graph from generated streamlines.
        print("\n- Starting generation of graph -")

        t = time()

        self.graph = Graph(self.generator)

        print(f"Generation of graph completed in {time() - t:.2f}s")

        if with_visualization:
            print("\n- Starting visualization of graph -")

            t = time()

            self.visualize_edges()
            self.visualize_nodes()

            print(f"Visualization of graph completed in {time() - t:.2f}s")

    # Turn streamline sections of the graph into curves to visualize in Blender.
    def visualize_edges(self, prefix=''):
        try:
            grid = bpy.data.collections[prefix + "grid"]
            bpy.ops.object.select_all(action='DESELECT')

            for child in grid.children:
                for obj in child.objects:
                    obj.select_set(True)

            for obj in grid.objects:
                obj.select_set(True)

            bpy.ops.object.delete()

            for child in grid.children:
                bpy.data.collections.remove(child)
        except Exception:
            grid = bpy.data.collections.new(prefix + "grid")
            bpy.context.scene.collection.children.link(grid)

        for streamline in self.graph.streamline_sections:
            sl = bpy.data.collections.new("streamline")
            grid.children.link(sl)

            for section in streamline:
                curve = bpy.data.curves.new("section", 'CURVE')
                curve.splines.new('BEZIER')
                curve.splines.active.bezier_points.add(len(section) - 1)
                obj = bpy.data.objects.new("section", curve)
                sl.objects.link(obj)

                for i in range(len(section)):
                    curve.splines.active.bezier_points[i].co = section[i].to_3d()
                    curve.splines.active.bezier_points[i].handle_right_type = 'VECTOR'
                    curve.splines.active.bezier_points[i].handle_left_type = 'VECTOR'

    # Place cubes at node points of the generated graph.
    def visualize_nodes(self, prefix=''):
        try:
            nodes = bpy.data.collections[prefix + "nodes"]
            bpy.ops.object.select_all(action='DESELECT')
            for obj in nodes.objects:
                obj.select_set(True)
            bpy.ops.object.delete()
        except Exception:
            nodes = bpy.data.collections.new(prefix + "nodes")
            bpy.context.scene.collection.children.link(nodes)

        cube_mesh = bpy.data.meshes.new("Basic_Cube")
        bm = bmesh.new()
        bmesh.ops.create_cube(bm, size=1.5)
        bm.to_mesh(cube_mesh)
        bm.free()

        for graph_node in self.graph.nodes:
            if not [*graph_node.neighbors]:
                # Ignore the node if it has no neigbors
                continue

            node = bpy.data.objects.new("Node", cube_mesh)
            nodes.objects.link(node)
            node.location = graph_node.co.to_3d()
