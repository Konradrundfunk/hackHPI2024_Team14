from energy_graph import Node, EnergySystemGraph


# Visualizing the graph to check if the building was added

# Assuming the EnergySystemGraph class from the previous example is used to construct the graph

energy_system = EnergySystemGraph()

# Adding generators


# Adding buildings with demands
energy_system.add_node(Node(node_id="S1", node_type="street", lon=1, lat=1))
energy_system.add_node(Node(node_id="S2", node_type="street", lon=3, lat=3))
energy_system.add_node(Node(node_id="S3", node_type="street", lon=5, lat=1))


energy_system.add_node(Node(node_id="B11", lon=1, lat=3, node_type="building"))
energy_system.add_node(
    Node(node_id="B12", lon=2, lat=3, node_type="building")
)  # SHOULD be closest
energy_system.add_node(Node(node_id="B13", lon=1, lat=5, node_type="building"))
energy_system.add_node(Node(node_id="B14", lon=2, lat=5, node_type="building"))


energy_system.add_node(
    Node(node_id="B21", lon=3, lat=4, node_type="building")
)  # SHOULD be closest
energy_system.add_node(Node(node_id="B22", lon=4, lat=4, node_type="building"))
energy_system.add_node(Node(node_id="B23", lon=3, lat=5, node_type="building"))
energy_system.add_node(Node(node_id="B24", lon=4, lat=5, node_type="building"))


# Adding pipelines (edges)
energy_system.add_edge("S1", "S2", length=200, loss=0.1)
energy_system.add_edge("S2", "S3", length=300, loss=0.2)
energy_system.add_edge("S3", "S1", length=300, loss=0.2)
