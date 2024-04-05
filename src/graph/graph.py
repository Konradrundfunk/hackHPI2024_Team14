import json
import numpy as np
from scipy.spatial import KDTree

# file_name = "./data/total_Arnis.json"
file_name = "D:/_Folders/projects_small/competition/hackHPI2024_Team14/src/data/total_Arnis.json"

with open(file_name, "r") as file:
    data = json.load(file)

highways = data["highways"]

edges = []
vertices = {}


class Vertex:
    def __init__(self, vertex_id, coords):
        self.vertex_id = vertex_id
        self.coords = coords
        self.edges = []


class Edge:
    def __init__(self, vertex_id1, vertex_id2):
        self.vertex_id1 = vertex_id1
        self.vertex_id2 = vertex_id2


def point_to_id(point):
    return f"lat<{point['lat']}>lon<{point['lon']}>"


# fill vertices and edges
for highway in highways.values():
    for point in highway["geometry"]:
        vertex_id = point_to_id(point)
        coords = np.array([point["lat"], point["lon"]])
        vertices[vertex_id] = Vertex(vertex_id, coords)
    for i in range(1, len(highway["geometry"])):
        vertex_1 = point_to_id(highway["geometry"][i - 1])
        vertex_2 = point_to_id(highway["geometry"][i])
        edge = Edge(vertex_1, vertex_2)


vertex_id_array = np.array(list(vertices.keys()))
vertex_coords_array = np.array(
    [vertices[vertex_id].coords for vertex_id in vertex_id_array]
)

kdtree = KDTree(vertex_coords_array)

# add houses
for building in data["buildings"].values():
    building_points = map(
        lambda point: np.array([point["lat"], point["lon"]]), building["geometry"]
    )
    kd_results = [kdtree.query(point) for point in building_points]
