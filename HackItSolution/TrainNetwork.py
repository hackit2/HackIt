import Call_Data_Generator
import Training_Shapes
import pandas as pd
import csv
import numpy as np
# Train Neural Network
cdg = Call_Data_Generator.CallDataGenerator()
tl = Training_Shapes.TrainingShapes()

training_data_frame = pd.read_csv('Data/TrainingData.csv', header=0, index_col=0).values
testing_data_frame = pd.read_csv('Data/TestingData.csv', header=0, index_col=0).values

max_depth = tl.get_max_path_depth()

# Join Data
training_data_frame = np.concatenate((training_data_frame, testing_data_frame), axis=0)

# Convert and Pad Data
for customer in training_data_frame:
    customer[0] = customer[0].replace('[','').replace(']','').split(',')
    customer[0] = customer[0] + ['P0'] * (max_depth - len(customer[0]))

# Convert Strings to Floats
for customer in training_data_frame:
    for x in range(0, len(customer[0])):
        customer[0][x] = float(''.join(str(ord(c)) for c in customer[0][x]))

# Normalize
for customer in training_data_frame:
    customer[0] = [float(i)/sum(customer[0]) for i in customer[0]]


