import json
import sys
import random
import math

class CallDataGenerator:
    def __init__(self):
        sys.setrecursionlimit(10000)
        self.route_config = {}
        with open('RouteConfig.json') as json_file:
            self.route_config = json.load(json_file)

    def recursive_route_builder(self, caller_route, current_node, running_nps):
        next_node = ''
        next_nps = 0
        if len(self.route_config[current_node]['Targets']) != 0:
            if self.route_config[current_node]['Description'] == 'Action':
                next_node = self.route_config[current_node]['Targets'][0]
                next_nps = running_nps + self.route_config[current_node]['F']
                caller_route.append(next_node)
            else:
                targets_length = len(self.route_config[current_node]['Targets'])
                random_target = random.randint(1, targets_length) - 1
                next_node = self.route_config[current_node]['Targets'][random_target]
                next_nps = running_nps + self.route_config[current_node]['F']
                caller_route.append(next_node)
            return self.recursive_route_builder(caller_route, next_node, next_nps)
        else:
            running_nps = running_nps + self.route_config[current_node]['F']
            return caller_route, current_node, running_nps

    def recursive_route_builder_V2(self, record_count):
        final_customer_list = {}
        for x in range(record_count):
            this_customer = {}
            this_customer['name'] = 'Customer' + str(x).zfill(2)
            caller_route, current_node, final_nps = self.recursive_route_builder([], 'N00', 0)
            this_customer['path'] = caller_route
            this_customer['label'] = int(math.floor(final_nps/2))
            #this_customer['label'] = (int(final_nps / 2) % 2)
            final_customer_list[this_customer['name']] = this_customer
        return final_customer_list
