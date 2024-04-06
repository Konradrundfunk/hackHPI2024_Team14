import geopy.distance
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from root_graph import Vertex, Edge
import geopy


class Street:
    def __init__(self, edges: list[Edge]):
        self.edges = edges
        self.length = sum(
            geopy.distance.geodesic(edge.vertex1.coords, edge.vertex2.coords).meters
            for edge in edges
        )
        self.capacity = None
        self.summer_flows = [None] * 24
        self.winter_flows = [None] * 24


class Node:
    def __init__(self, vertex_id):
        self.vertex_id = vertex_id
        self.in_streets: list[Street] = []
        self.out_streets: list[Street] = []
        self.generators = None
        self.heat_pump_draws_summer = [None] * 24
        self.heat_pump_draws_winter = [None] * 24

    def add_in_street(self, street: Street):
        self.in_streets.append(street)

    def add_out_street(self, street: Street):
        self.out_streets.append(street)


# class Demands:
#    def __init__(self, w_electro, w_heating, s_electro, s_heating):
#        self.w_electro = w_electro
#        self.w_heating = w_heating
#        self.s_electro = s_electro
#        self.s_heating = s_heating


class Building(Node):
    def __init__(
        self,
        vertex_id,
        json_obj,
    ):
        super().__init__(vertex_id)
        self.json_obj = json_obj


class Traffic(Node):
    def __init__(
        self,
        vertex_id,
    ):
        super().__init__(vertex_id)


class EnergySystemGraph:
    def __init__(self):
        self.Nodes = {}
        self.Streets = []

    def add_node(self, node: Node):
        self.Nodes[node.vertex_id] = node
