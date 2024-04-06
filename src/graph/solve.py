import pulp
from energy_graph import Street, Node, Consumer, FlowNode, Producer
from graph import *
from graph import graph
from used_files import total_file, possible_system_file
from potentials import heating_potentials
import json

with open(total_file, "r") as file:
    data = json.load(file)

with open(possible_system_file, "r") as file:
    possible_systems = json.load(file)

problem = pulp.LpProblem("Minimize_BS_Cost", pulp.LpMinimize)

# ---------------- Define variables ----------------#

# street capacities and flows
for street in graph.Streets:
    street.capacity = pulp.LpVariable(
        f"capacity_{street.edges[0].vertex1.vertex_id}_{street.edges[0].vertex2.vertex_id}",
        lowBound=0,
        cat=pulp.LpContinuous,
    )
    for i in range(48):
        street.flows[i] = pulp.LpVariable(
            f"summer_flow_{street.edges[0].vertex1.vertex_id}_{street.edges[0].vertex2.vertex_id}_{i}",
            lowBound=0,
            cat=pulp.LpContinuous,
        )

# # ---------------- Define constraints ----------------#

# Balancing constraints
for node in graph.Nodes.values():
    if isinstance(node, FlowNode):
        for i in range(48):
            left_side = 0
            for in_street in node.in_streets:
                left_side = in_street.flows[i] + left_side
            right_side = 0
            for out_street in node.out_streets:
                right_side = out_street.flows[i] + right_side
            problem += left_side == right_side
    elif isinstance(node, Consumer):
        for i in range(48):
            incoming = 0
            for in_street in node.in_streets:
                incoming = incoming + in_street.flows[i]
            problem += incoming == node.demands[i]
    elif isinstance(node, Producer):
        if node.type == "DistrictHeatingCreator":
            area = data["buildings"][node.supplied_house.vertex.building_id][
                "base_area"
            ]
            total_heat_potentials = heating_potentials * area
            for i in range(48):
                for out_street in node.out_streets:
                    problem += out_street.flows[i] <= total_heat_potentials[i]


# Capacity constraints
for street in graph.Streets:
    for i in range(48):
        problem += street.flows[i] <= street.capacity

# ---------------- cost function ----------------#
cost = 0

# Investment costs
for street in graph.Streets:
    capacity = street.capacity
    price = data[street.type]["invest"] * capacity
    if type == "DistrictHeatingLine (medium)":
        price = street.length * price
    cost += price

# Operating costs
operating_cost = 0
for street in graph.Streets:
    for i in range(48):
        flow = street.flows[i]
        price = data[street.type]["operating_cost"] * flow
        operating_cost += price
    operating_cost = 25 * 365 / 2 * operating_cost
cost = cost + operating_cost

# Electricity costs
electricity_cost = 0
for node in graph.Nodes.values():
    if isinstance(node, Consumer):
        demand = node.energy_demands
        price = demand * 0.43

cost = cost + electricity_cost
solver = pulp.PULP_CBC_CMD()
result = problem.solve(solver)
print(result)
