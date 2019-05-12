import json
import sys
import random


class CallDataGenerator:
    def __init__(self):
        sys.setrecursionlimit(10000)
        self.route_config = {}
        with open('RouteConfig.json') as json_file:
            self.route_config = json.load(json_file)

    def recursive_route_builder(self, caller_route, current_node, running_nps):
        next_node = ''
        next_nps = 0
        if current_node != 'SY':
            if self.route_config[current_node]['Description'] == 'Action':
                next_node = self.route_config[current_node]['Targets'][0]
                random_nps = random.randint(self.route_config[current_node]['F'] - 1,
                                            self.route_config[current_node]['F'] + 1)
                next_nps = running_nps + random_nps
                caller_route.append(next_node)
            else:
                targets_length = len(self.route_config[current_node]['Targets'])
                random_target = random.randint(1, targets_length) - 1
                next_node = self.route_config[current_node]['Targets'][random_target]
                random_nps = random.randint(self.route_config[current_node]['F'] - 1,
                                            self.route_config[current_node]['F'] + 1)
                next_nps = running_nps + random_nps
                caller_route.append(next_node)
            return self.recursive_route_builder(caller_route, next_node, next_nps)
        else:
            return caller_route, current_node, running_nps

