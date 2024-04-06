from gurobipy import Model, GRB
from energy_graph import EnergySystemGraph

####################### START - BY IMPORTING THE SYSTEMS #####################
import json

# Assuming `usage.json` is your JSON file
with open("usage.json", "r") as file:
    data = json.load(file)

# Example of accessing commercial demands
commercial_demands = data["commercial"]["demands"]
print(commercial_demands)

# Hypothetical total demands for illustration
# total_elektro_demand = sum([demand["demand"][0] for sector in data.values() for demand in sector["demands"] if demand["name"] == "Elektro (Allgemeinstrom)"])
# total_waerme_demand = sum([demand["demand"][0] for sector in data.values() for demand in sector["demands"] if demand["name"] == "Wärme (Hochtemperatur)"])


# Assuming the JSON data is stored in `energy_data.json`
with open("../data/systems.json", "r") as file:
    energy_data = json.load(file)

# Example parsing
demands = energy_data["commercial"]["demands"][0]["demand"]
# Accessing demand for demonstration
suppliers = energy_data["supplier"]
storages = energy_data["storages"]
lines = energy_data["line"]

################# Initialize the Gurobi model ################
model = Model("Minimize_BS_Cost")

# Define variables
gen_costs = {}
smallPV = {}
bigPV = {}

energy_system = EnergySystemGraph()


# Define variables for supplier output per hour
# Assuming 'pv_potential' is an array with 24 elements representing hourly potential
pv_output_vars = [model.addVar(name=f"PV_Output_Hour_{hour}") for hour in range(24)]

# Similarly, for other suppliers and storages, define variables per hour
for hour in range(24):
    for attr in suppliers:
        model.addConstr(
            sum(pv_output_vars[hour] * attr["output"]["factor"]) >= demands[hour],
            name=f"Demand_Meeting_Hour_{hour}",
        )
        # sum(pv_output_vars[hour] * suppliers['Photovoltaics']['output']['factor']) >= demands[hour],

# edge traversal
for u, v, data in energy_system.graph.edges(data=True):
    test = 1
    #
    # constraints


cost_vars = []
##################### OBJECTIVES ####################
for supplier, attributes in suppliers.items():
    output_var = model.addVar(name=f"{supplier}_output")
    cost_vars.append(output_var * attributes["operatingCost"] + attributes["invest"])

co2_weight = 0.5  # Example weight
cost_weight = 0.5  # Example weight
# model.setObjective(co2_weight * sum(co2_emission_vars) + cost_weight * sum(cost_vars), GRB.MINIMIZE)
model.setObjective(sum(cost_vars, GRB.MINIMIZE))

# Optimize the model
model.optimize()

if model.status == GRB.OPTIMAL:
    print(f"Optimal Objective: {model.ObjVal}")
    for var in model.getVars():
        print(f"{var.varName} = {var.x}")

else:
    print("Optimal solution was not found.")
