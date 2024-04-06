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
