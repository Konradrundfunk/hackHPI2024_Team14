import numpy as np


class Vertex:
    def __init__(self, vertex_id, coords, is_building=False, building_id=None):
        self.vertex_id = vertex_id
        """Coordinates of the vertex. as numpy array  - 2dimensional"""
        self.coords: np.ndarray = coords
        self.connected_edges: list[Edge] = []
        self.is_building = is_building
        self.building_id = building_id

    def add_edge(self, edge):
        self.connected_edges.append(edge)


class Edge:
    def __init__(self, vertex1, vertex2):
        self.vertex1 = vertex1
        self.vertex2 = vertex2


class Vertices:
    def __init__(self):
        self.vertices = {}

    def add_vertex(self, vertex_id, coords, is_building=False, building_id=None):
        """return reference to inserted vertex"""
        if self.vertices.get(vertex_id) is None:
            self.vertices[vertex_id] = Vertex(
                vertex_id, coords, is_building, building_id
            )
        return self.vertices[vertex_id]

    def get_vertex(self, vertex_id):
        return self.vertices[vertex_id]


#        vertices[vertex_id_1].add_edge(self)
#       vertices[vertex_id_2].add_edge(self)
