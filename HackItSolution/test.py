import json
import random
import sys

route_config = {}

with open('RouteConfig.json') as json_file:
    route_config = json.load(json_file)

total = 0

for current_node in route_config:
    total += route_config[current_node]['F'] + 1

print(total)