import pulp
from energy_graph import Street, Node, Building
from graph import *
from graph import graph

problem = pulp.LpProblem("Minimize_BS_Cost", pulp.LpMinimize)

# ---------------- Define variables ----------------#

# street capacities and flows
for street in graph.Streets:
    street.capacity = pulp.LpVariable(
        f"capacity_{street.edges[0].vertex1.vertex_id}_{street.edges[0].vertex2.vertex_id}",
        lowBound=0,
        cat=pulp.LpContinuous,
    )
    for i in range(24):
        street.summer_flows[i] = pulp.LpVariable(
            f"summer_flow_{street.edges[0].vertex1.vertex_id}_{street.edges[0].vertex2.vertex_id}_{i}",
            lowBound=0,
            cat=pulp.LpContinuous,
        )
        street.winter_flows[i] = pulp.LpVariable(
            f"winter_flow_{street.edges[0].vertex1.vertex_id}_{street.edges[0].vertex2.vertex_id}_{i}",
            lowBound=0,
            cat=pulp.LpContinuous,
        )

for node in graph.Nodes.values():
    # if isinstance(node, Building):
    #     node.generators = pulp.LpVariable(
    #         f"Generators_{node.vertex_id}",
    #         lowBound=0,
    #         cat=pulp.LpInteger,
    #     )
    #     if node.json_obj["type"] not in ["industrial", "free_field"]:
    #         for i in range(24):
    #             node.heat_pump_draws_summer[i] = pulp.LpVariable(
    #                 f"heat_pump_draws_summer_{node.vertex_id}_{i}",
    #                 lowBound=0,
    #                 cat=pulp.LpContinuous,
    #             )
    #             node.heat_pump_draws_winter[i] = pulp.LpVariable(
    #                 f"heat_pump_draws_winter_{node.vertex_id}_{i}",
    #                 lowBound=0,
    #                 cat=pulp.LpContinuous,
    #             )
    if "DistrictHeatingCreator" in node.possible_systems:
        node.district_heating_creators = pulp.LpVariable(
            f"DistrictHeatingCreator_{node.vertex_id}",
            lowBound=0,
            cat=pulp.LpInteger,
        )


# ---------------- Define constraints ----------------#
for street in graph.streets:
    for i in range(24):
        problem += street.summer_flows[i] <= street.capacity
        problem += street.winter_flows[i] <= street.capacity
for node in graph.Nodes:
    if isinstance(node, Building) and node.json_obj["type"] == "industrial":
        output_of_one_heat_generator = 1000

# ---------------- Define objective ----------------#


# ---------------- Solve the problem ----------------#


# ---------------- Visualize the results as SVGs ----------------#
