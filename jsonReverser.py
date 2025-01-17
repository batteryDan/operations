# -*- coding: utf-8 -*-
"""
Created on Tue Nov  5 15:43:38 2024

@author: DanielDomikaitis
"""

import json

# Load the existing JSON file
with open(r'\\ZMUDOWSKI\doheny\telemetryTemps\logWarehouse.json', 'r') as file:
    data = json.load(file)

# Reverse the data order (assuming each entry has a chronological order based on position)
data.reverse()

# Save the reversed data to a new JSON file
with open(r'\\ZMUDOWSKI\doheny\telemetryTemps\logWarehouseRev.json', 'w') as file:
    json.dump(data, file, indent=4)

print("Data has been reversed and saved to 'output_reversed.json'")
