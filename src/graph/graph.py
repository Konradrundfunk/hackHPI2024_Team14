import json
import numpy as np
from scipy.spatial import KDTree
import matplotlib.pyplot as plt
import networkx as nx
from root_graph import Vertices, Edge


import energy_graph as eg

file_name = "./data/total_Arnis.json"
# file_name = (
#     "D:/_Folders/projects_small/competition/hackHPI2024_Team14/src/data/total_test.json"
# )

with open(file_name, "r") as file:
    data = json.load(file)

highways = data["highways"]

edges = []
"""keys are vertex_ids"""
vertices = Vertices()


def point_to_id(point):
    return f"lat<{point['lat']}>lon<{point['lon']}>"


def coords_to_id(coords):
    return f"lat<{coords[0]}>lon<{coords[1]}>"


# fill vertices and edges
for road in highways.values():
    # add vertices
    for point in road["geometry"]:
        vertex_id = point_to_id(point)
        coords = np.array([point["lat"], point["lon"]])
        vertices.add_vertex(vertex_id, coords)
    # add edges
    for i in range(1, len(road["geometry"])):
        vertex_id_1 = point_to_id(road["geometry"][i - 1])
        vertex_id_2 = point_to_id(road["geometry"][i])
        edge = Edge(vertices.get_vertex(vertex_id_1), vertices.get_vertex(vertex_id_2))
        edges.append(edge)
        vertices.get_vertex(vertex_id_1).add_edge(edge)
        vertices.get_vertex(vertex_id_2).add_edge(edge)


vertex_id_array = np.array(list(vertices.vertices.keys()))
vertex_coords_array = np.array(
    [vertices.get_vertex(vertex_id).coords for vertex_id in vertex_id_array]
)

kdtree = KDTree(vertex_coords_array)


# add buildings
for building_id, building in data["buildings"].items():
    building_points = list(
        map(lambda point: np.array([point["lat"], point["lon"]]), building["geometry"])
    )[1:]
    kd_results = [kdtree.query(point) for point in building_points]
    nearest_building_point_ix = np.argmin(list(map(lambda x: x[0], kd_results)))
    nearest_building_point = building_points[nearest_building_point_ix]
    nearest_vertex_id = vertex_id_array[kd_results[nearest_building_point_ix][1]]
    building_vertex_id = coords_to_id(nearest_building_point)
    # add vertex
    vertices.add_vertex(
        building_vertex_id,
        nearest_building_point,
        is_building=True,
        building_id=building_id,
    )
    # add edge
    edge = Edge(
        vertices.get_vertex(nearest_vertex_id), vertices.get_vertex(building_vertex_id)
    )
    edges.append(edge)
    vertices.get_vertex(nearest_vertex_id).add_edge(edge)
    vertices.get_vertex(building_vertex_id).add_edge(edge)

graph = eg.EnergySystemGraph()

for vertex_id, vertex in vertices.vertices.items():
    if vertex.is_building:
        node = eg.Building(vertex_id, data["buildings"][vertex.building_id])
        graph.add_node(node)
    else:
        node = eg.Traffic(vertex_id)
        graph.add_node(node)
for edge in edges:
    start_node = edge.vertex1.vertex_id
    end_node = edge.vertex2.vertex_id
    street_forward = eg.Street([edge])
    street_backward = eg.Street([edge])
    graph.Streets.append(street_forward)
    graph.Streets.append(street_backward)
    graph.Nodes[start_node].add_out_street(street_forward)
    graph.Nodes[end_node].add_in_street(street_forward)
    graph.Nodes[start_node].add_in_street(street_backward)
    graph.Nodes[end_node].add_out_street(street_backward)
