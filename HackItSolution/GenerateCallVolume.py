import Call_Data_Generator
import Training_Shapes
import pandas as pd
import math

# Generate Training and Testing Data
cdg = Call_Data_Generator.CallDataGenerator()
tl = Training_Shapes.TrainingShapes()

training_callers_route_collection = {}
testing_callers_route_collection = {}

training_data_record_count = 1000000
testing_data_record_count = 100
nps_range = 5

T1, T2 = tl.get_feasible_path_f()

absolute_buffer = (T1 * -1)
max_upper_range = absolute_buffer + T2

for x in range(training_data_record_count):
    caller_route, current_node, final_nps = cdg.recursive_route_builder([], 'N1', 0)
    training_callers_route_collection['Customer ' + str(x)] = [caller_route, int(math.floor(((final_nps + absolute_buffer) * nps_range) / max_upper_range))]

training_data_frame = pd.DataFrame(data=training_callers_route_collection)
tessellated_training_data_frame = training_data_frame.T

for x in range(testing_data_record_count):
    caller_route, current_node, final_nps = cdg.recursive_route_builder([], 'N1', 0)
    testing_callers_route_collection['Customer ' + str(x)] = [caller_route, int(math.floor(((final_nps + absolute_buffer) * nps_range) / max_upper_range))]

testing_data_frame = pd.DataFrame(data=testing_callers_route_collection)
tessellated_testing_data_frame = testing_data_frame.T

with open('Data/TrainingData.csv', 'w') as file:
    file.write(tessellated_training_data_frame.to_csv(index=True, line_terminator='\n'))

with open('Data/TestingData.csv', 'w') as file:
    file.write(tessellated_testing_data_frame.to_csv(index=True, line_terminator='\n'))
