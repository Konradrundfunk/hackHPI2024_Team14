import geopy.distance
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from root_graph import Vertex, Edge
import geopy
import json


class Street:
    def __init__(self, edges: list[Edge], type: str):
        self.edges = edges
        self.length = sum(
            geopy.distance.geodesic(edge.vertex1.coords, edge.vertex2.coords).meters
            for edge in edges
        )
        self.capacity = None
        """summer, winter"""
        self.flows = [None] * 48
        self.type = type


class Node:
    def __init__(self):
        self.in_streets: list[Street] = []
        self.out_streets: list[Street] = []

    def add_in_street(self, street: Street):
        self.in_streets.append(street)

    def add_out_street(self, street: Street):
        self.out_streets.append(street)


class Consumer(Node):
    def __init__(
        self,
        demands,
    ):
        super().__init__()
        self.demands = demands

    # def evaluate_possible_systems(self):
    #     type = self.json_obj["type"]
    #     for system in possible_systems:
    #         if system["canBeUsedBy"].contains(type):
    #             self.possible_systems.append(system)


class Producer(Node):
    def __init__(self, type: str):
        super().__init__()
        self.type = type


class Traffic(Node):
    def __init__(self, vertex):
        super().__init__()
        self.vertex = vertex


class House(Node):
    def __init__(self, vertex, consumer: Consumer, producers: list[Producer]):
        super().__init__()
        self.vertex: Vertex = vertex
        self.consumer = consumer
        self.producers = producers


class EnergySystemGraph:
    def __init__(self):
        self.Nodes = {}
        self.Streets = []

    def add_node(self, node: Node):
        if type(node) == Traffic:
            self.Nodes[node.vertex.vertex_id] = node
        else:
            index = str(np.random.random())
            self.Nodes[index] = node
