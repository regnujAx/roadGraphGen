import bmesh
import bpy
import math

from mathutils import Vector
from time import time

from roadNetGen.roadNetGen.graph import Graph
from roadNetGen.roadNetGen.integrator import RK4Integrator
# from roadNetGen.roadNetGen.lot_finder import LotFinder
from roadNetGen.roadNetGen.streamline_parameters import StreamlineParameters
from roadNetGen.roadNetGen.streamlines import StreamlineGenerator
from roadNetGen.roadNetGen.tensor_field import TensorField


class RNG_GraphGenerator():
    def __init__(self, width: int = 100, height: int = 100, seed: int = None):
        # Create new global TensorField
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

    def generate(self):
        print(f"\n\n--- Starting graph generation with seed {self.generator.seed} ---")

        # Add two grid and one radial basis field to the global field.
        self.field.add_grid(Vector((1381, 788)), 1500, 35, 1.983775)
        self.field.add_grid(Vector((1181, 988)), 1500, 35, -1.283775)
        self.field.add_radial(Vector((800, 888)), 750, 55)

        # Generate all streamlines.
        print("\n- Starting generation of streamlines -")

        t = time()

        self.generator.create_all_streamlines()

        print(f"Streamlines generation completed in {time() - t:.2f}s")

        # Generate graph from generated streamlines.
        print("\n- Starting generation of graph -")

        t = time()

        self.graph = Graph(self.generator)

        print(f"Graph generation completed in {time() - t:.2f}s")

        # # Visualize graph in Blender.
        # t = time()

        # visualize_edges(self.graph)
        # mark_nodes_without_neighbor(self.graph)

        # print(f"placed graph in {time() - t:.2f}s")

        # poly = LotFinder(graph)
        # poly.find_lots()
        # place_polygons(poly)


# ------------------------------------------------------------------------
#    Helper Method
# ------------------------------------------------------------------------


# def place_polygons(poly_generator: LotFinder):
#     try:
#         lots = bpy.data.collections["lots"]
#         bpy.ops.object.select_all(action='DESELECT')
#         for obj in lots.objects:
#             obj.select_set(True)
#         bpy.ops.object.delete()
#     except Exception:
#         lots = bpy.data.collections.new("lots")
#         bpy.context.scene.collection.children.link(lots)

#     for lot in poly_generator.lots:
#         if len(lot) < 3:
#             continue
#         bm = bmesh.new()
#         mesh = bpy.data.meshes.new('lot')
#         bm.from_mesh(mesh)
#         verts = []
#         for point in lot:
#             verts.append(bm.verts.new(point.to_3d().to_tuple()))
#         bm.faces.new(verts)
#         bm.to_mesh(mesh)
#         obj = bpy.data.objects.new('lot', mesh)
#         lots.objects.link(obj)
