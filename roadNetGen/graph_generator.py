import bmesh
import bpy
import math

from mathutils import Vector
from time import time

from .graph import Graph
from .integrator import RK4Integrator
# from .lot_finder import LotFinder
from .streamline_parameters import StreamlineParameters
from .streamlines import StreamlineGenerator
from .tensor_field import TensorField


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
        print("\n\n--- Starting graph generation ---")

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
#    Helper Methods
# ------------------------------------------------------------------------


# def clockwise_angle(point: Vector, reference_vector: Vector):
#     vector = point - reference_vector
#     length = math.sqrt(sum(i**2 for i in vector))

#     # If length of the vector is zero there is no angle.
#     if length == 0:
#         return 0.0

#     vector.normalize()
#     dot = vector[0] * reference_vector[0] + vector[1] * reference_vector[1]
#     diff = vector[0] * reference_vector[1] - vector[1] * reference_vector[0]
#     angle = math.atan2(diff, dot)

#     return angle


# def closest_curve_point(curve: bpy.types.Object, reference_point: Vector):
#     # Get the curve end points in world space.
#     m = curve.matrix_world
#     first_curve_point = curve.data.splines[0].bezier_points[0]
#     last_curve_point = curve.data.splines[0].bezier_points[-1]
#     first_curve_point_co = m @ first_curve_point.co
#     last_curve_point_co = m @ last_curve_point.co

#     point = closest_point([first_curve_point_co, last_curve_point_co], reference_point)

#     return first_curve_point_co if point == first_curve_point_co else last_curve_point_co


# def closest_point(points: list, reference_point: Vector):
#     closest_point = points[0]

#     for i in range(len(points) - 1):
#         point = points[i+1]
#         vector_1 = closest_point - reference_point
#         distance_1 = math.sqrt(sum(i**2 for i in vector_1))
#         vector_2 = point - reference_point
#         distance_2 = math.sqrt(sum(i**2 for i in vector_2))

#         if distance_2 < distance_1:
#             closest_point = point

#     return closest_point


# def intersection_with_circle(first_point: Vector, second_point: Vector, circle_midpoint: Vector, circle_radius: float):
#     vec = second_point - first_point

#     # Coefficients of the quadratic equation for intersection calculation.
#     A = vec[0]**2 + vec[1]**2
#     B = 2 * (vec[0] * (first_point[0] - circle_midpoint[0]) + vec[1] * (first_point[1] - circle_midpoint[1]))
#     C = (first_point[0] - circle_midpoint[0])**2 + (first_point[1] - circle_midpoint[1])**2 - circle_radius**2
#     discriminant = B**2 - 4 * A * C

#     # There are two intersections of a vector with a circle (also with t = (-B - sqrt_discriminant) / (2 * A))
#     # but only the first is relevant.
#     sqrt_discriminant = math.sqrt(discriminant)
#     t = (-B + sqrt_discriminant) / (2 * A)

#     return Vector((first_point[0] + t * vec[0], first_point[1] + t * vec[1], 0.0))


# def mark_nodes_without_neighbor(graph):
#     cube_mesh = bpy.data.meshes.new('Cube_Marker')
#     bm = bmesh.new()
#     bmesh.ops.create_cube(bm, size=5.0)
#     bm.to_mesh(cube_mesh)
#     bm.free()
#     markers = bpy.data.collections.get("Markers")

#     if markers is None:
#         markers = bpy.data.collections.new("Markers")
#         bpy.context.scene.collection.children.link(markers)

#     for node in graph.nodes:
#         if [*node.border_neighbors]:
#             continue

#         if node.curves:
#             marker = bpy.data.objects.new("Marker", cube_mesh)
#             markers.objects.link(marker)
#             marker.location = node.co.to_3d()

#             reference_point = marker.location
#             sorted_curves = sort_curves(node.curves, reference_point)

#             for i, curve in enumerate(sorted_curves):
#                 marker[f"Curve {i+1}"] = curve.name

#             marker["Number of Curves"] = str(len(sorted_curves))


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


# def sort_curves(curves: list, reference_point: Vector):
#     direction_vectors = []
#     # Calculate for each curve a direction vector from curve to reference point.
#     for curve in curves:
#         curve_point = closest_curve_point(curve, reference_point)
#         direction_vector = curve_point - reference_point
#         # Save for each curve its direction vector.
#         direction_vectors.append((curve, direction_vector))

#     reference_vector = direction_vectors[0][1]
#     angles = []
#     # Calculate the clockwise angle for each direction vector (the first direction vector is the origin/start).
#     for vector in direction_vectors:
#         angle = clockwise_angle(vector[1], reference_vector)
#         angles.append(angle)

#     # Check whether the lines cross straight and swap the order (set one angle to -1) if they do.
#     if len(angles) == 2 and round(angles[1], 2) == 3.14:
#         angles[1] = -1

#     vectors_and_angles = []
#     for vector, angle in zip(direction_vectors, angles):
#         vectors_and_angles.append((vector[0], angle))

#     # Sort the direction vectors according to angle and extract the corresponding curves.
#     vectors_and_angles.sort(key=lambda x: x[1])
#     sorted_curves = [curve for curve, _ in vectors_and_angles]

#     return sorted_curves


# def visualize_edges(graph: Graph, crossroad_offset: float = 0.0):
#     undirected_edges = [*graph.edges].copy()
#     curves = {}
#     try:
#         edges = bpy.data.collections["Edges"]
#         bpy.ops.object.select_all(action='DESELECT')
#         for obj in edges.objects:
#             obj.select_set(True)
#         bpy.ops.object.delete()
#     except Exception:
#         edges = bpy.data.collections.new("Edges")
#         bpy.context.scene.collection.children.link(edges)

#     idx = 0
#     for node in graph.nodes:
#         for edge in node.edges:
#             if edge in undirected_edges:
#                 undirected_edges.remove(edge)

#                 edge_points = edge.connection
#                 edge_points_copy = edge_points.copy()

#                 curve = bpy.data.curves.new("Edge", 'CURVE')
#                 curve.splines.new('BEZIER')
#                 curve_spline = curve.splines.active

#                 first_point = edge_points[0].to_3d()
#                 last_point = edge_points[-1].to_3d()

#                 vec = last_point - first_point
#                 distance = math.sqrt(sum(i**2 for i in vec))

#                 # Skip edges that are too small.
#                 if distance < crossroad_offset * 2:
#                     continue

#                 if len(edge_points) == 2:
#                     # If there are only two points, we can simply adjust the points.
#                     unit_vec = vec / distance
#                     edge_points_copy[0] = first_point + unit_vec * crossroad_offset
#                     edge_points_copy[1] = last_point - unit_vec * crossroad_offset
#                 else:
#                     # If there are more than two points, we have to iterate from the begin and the end
#                     # and check whether we need to remove points or can adjust them.
#                     for x in range(2):
#                         point = first_point if x == 0 else last_point
#                         previous_edge_point = point

#                         for i in range(len(edge_points)):
#                             index = i if x == 0 else -i - 1
#                             edge_point = edge_points[index].to_3d()
#                             vec = edge_point - point
#                             distance = math.sqrt(sum(i**2 for i in vec))

#                             if distance < crossroad_offset:
#                                 previous_edge_point = edge_point
#                                 # Remove the point if it is too close to begin/end point.
#                                 edge_points_copy.popleft() if x == 0 else edge_points_copy.pop()
#                                 continue
#                             else:
#                                 # Add a new point with updated coordinates
#                                 # when a point is reached that is far enough away from the begin/end point.
#                                 new_co = intersection_with_circle(previous_edge_point, edge_point, point, crossroad_offset)
#                                 edge_points_copy.appendleft(new_co) if x == 0 else edge_points_copy.append(new_co)
#                                 break

#                 # Skip edges with less than two points.
#                 if len(edge_points_copy) < 2:
#                     continue

#                 curve_spline.bezier_points.add(len(edge_points_copy) - 1)
#                 obj = bpy.data.objects.new(f"Edge_{str(idx).zfill(3)}", curve)
#                 idx += 1
#                 edges.objects.link(obj)

#                 for i in range(len(edge_points_copy)):
#                     curve_spline.bezier_points[i].co = edge_points_copy[i].to_3d()
#                     curve_spline.bezier_points[i].handle_right_type = 'VECTOR'
#                     curve_spline.bezier_points[i].handle_left_type = 'VECTOR'

#                 # Update the origin.
#                 obj.select_set(True)
#                 bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
#                 obj.select_set(False)

#                 curves[edge] = obj

#             curve = curves.get(edge)

#             if curve:
#                 node.curves.append(curve)
