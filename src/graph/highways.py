import json


class Highway:
    def __init__(
        self,
        highway_id,
        highway_type,
        geometry,
        is_open=True,
        base_area=None,
        levels=None,
        area=None,
    ):
        self.highway_id = highway_id
        self.highway_type = highway_type
        self.geometry = geometry  # Expected to be a list of (lat, lon) tuples
        self.is_open = is_open
        self.base_area = base_area
        self.levels = levels
        self.area = area


def parse_highways(json_data):
    highways = []
    for highway_id, highway_info in json_data["highways"].items():
        # Basic highway information
        highway_type = highway_info["type"]
        highway_geo = highway_info["geometry"]
        # print(highway_geo)
        geometry = [(geo["lat"], geo["lon"]) for geo in highway_geo]

        # Optional attributes with default values if not present
        is_open = highway_info.get("open", True)
        base_area = highway_info.get("base_area")
        levels = highway_info.get("levels")
        area = highway_info.get("area")

        # Create and append the Highway object
        highway = Highway(
            highway_id, highway_type, geometry, is_open, base_area, levels, area
        )
        highways.append(highway)

    return highways


# Assuming `usage.json` is your JSON file
with open("./data/total_Freyburg (Unstrut).json", "r") as file:
    citydata = json.load(file)

print(citydata["highways"].keys())
# Assuming `json_data` is your loaded JSON containing highways
highways = parse_highways(citydata)
print("###### total_Freyburg .json or other city #####")
print(highways)

####################### START - BY IMPORTING THE SYSTEMS #####################
import json

# Assuming `usage.json` is your JSON file
with open("./data/usage copy.json", "r") as file:
    data = json.load(file)

# Example of accessing commercial demands
print("######## usage.json ######")
print(data)
commercial_demands = data["residential"]["demands"]
print(commercial_demands)

# Hypothetical total demands for illustration
# total_elektro_demand = sum([demand["demand"][0] for sector in data.values() for demand in sector["demands"] if demand["name"] == "Elektro (Allgemeinstrom)"])
# total_waerme_demand = sum([demand["demand"][0] for sector in data.values() for demand in sector["demands"] if demand["name"] == "Wärme (Hochtemperatur)"])


# Assuming the JSON data is stored in `energy_data.json`
with open("./data/systems.json", "r") as file:
    energy_data = json.load(file)


# {key: {length}[]}
# {supplier: {12}}
class supplyInterface:
    example = {
        "name": "SolarThermal",
        "area": 1,
        "invest": 250,
        "operatingCost": 0.003,
        "co2": 0.004,
        "input": {"energy": "pv_potential"},
        "output": {"energy": "DistrictHeating (Transport)", "factor": 0.5},
        "canBeUsedBy": ["free_field"],
    }


# {lines: {4}}
print("###### systems.json #####")
# Example parsing
# demands = data['commercial']['demands'][0]#['demand']  # Accessing demand for demonstration

print(energy_data["line"])
suppliers = energy_data["supplier"]
# storages = energy_data['storages']
lines = energy_data["line"]

energy_system = EnergySystemGraph()

# Add each highway to the graph
for highway in highways:
    energy_system.add_highway(highway)
