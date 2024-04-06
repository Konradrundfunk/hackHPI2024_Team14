from used_files import winter_potentials, summer_potentials
import json
import numpy as np

with open(winter_potentials, "r") as file:
    winter_potentials = json.load(file)
with open(summer_potentials, "r") as file:
    summer_potentials = json.load(file)

heating_potentials = np.array(
    winter_potentials["districtHeatingPotential"]
    + summer_potentials["districtHeatingPotential"]
)
