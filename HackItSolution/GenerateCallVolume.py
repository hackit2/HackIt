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
testing_data_record_count = 1000

T1, T2 = tl.get_feasible_path_f()

absolute_buffer = (T1 * -1)
max_upper_range = absolute_buffer + T2

final_training_customer_list = cdg.recursive_route_builder_V2(training_data_record_count)
training_data_frame = pd.DataFrame(data=final_training_customer_list)
tessellated_training_data_frame = training_data_frame.T

final_testing_customer_list = cdg.recursive_route_builder_V2(testing_data_record_count)
testing_data_frame = pd.DataFrame(data=final_testing_customer_list)
tessellated_testing_data_frame = testing_data_frame.T

with open('Data/TrainingData.csv', 'w') as file:
    file.write(tessellated_training_data_frame.to_csv(index=True, line_terminator='\n'))

with open('Data/TestingData.csv', 'w') as file:
    file.write(tessellated_testing_data_frame.to_csv(index=True, line_terminator='\n'))
