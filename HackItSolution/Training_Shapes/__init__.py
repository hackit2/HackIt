import json


class TrainingShapes:
    def __init__(self):
        self.route_config = {}
        self.max_depth = 0
        self.min_f = 999
        self.max_f = -999
        with open('RouteConfig.json') as json_file:
            self.route_config = json.load(json_file)

    def get_training_label_ranges(self):
        min_label = 0
        max_label = 0
        for current_node in self.route_config:
            max_label += self.route_config[current_node]['F'] + 1
        for current_node in self.route_config:
            min_label += self.route_config[current_node]['F'] - 1
        return min_label, max_label

    def get_max_path_depth(self):
        return self.recursive_depth_finder('N01', 0)

    def recursive_depth_finder(self, current_node, depth):
        depth += 1
        if current_node in self.route_config:
            for target in self.route_config[current_node]['Targets']:
                self.recursive_depth_finder(target, depth)
                if depth > self.max_depth:
                    self.max_depth = depth
        return self.max_depth

    def get_feasible_path_f(self):
        return self.recursive_feasible_path_f_finder('N01', 0, 0)

    def recursive_feasible_path_f_finder(self, current_node, path_total_pos, path_total_neg):
        path_total_pos += self.route_config[current_node]['F'] + 1
        path_total_neg += self.route_config[current_node]['F'] - 1
        if current_node in self.route_config:
            for target in self.route_config[current_node]['Targets']:
                if path_total_pos > self.max_f:
                    self.max_f = path_total_pos
                if path_total_neg < self.min_f:
                    self.min_f = path_total_neg
                self.recursive_feasible_path_f_finder(target, path_total_pos, path_total_neg)
        return self.min_f, self.max_f
