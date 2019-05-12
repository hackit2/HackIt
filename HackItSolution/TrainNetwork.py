import Call_Data_Generator
import Training_Shapes
import pandas as pd
import numpy as np
import tensorflow as tf
import tensorflow.keras as keras #Tensorflow 2.0
import tensorflow.keras.callbacks #Tensorflow 2.0
import math
from time import time
import os

# Train Neural Network
cdg = Call_Data_Generator.CallDataGenerator()
tl = Training_Shapes.TrainingShapes()

training_data_frame = pd.read_csv('Data/TrainingData.csv', header=0, index_col=0).values
testing_data_frame = pd.read_csv('Data/TestingData.csv', header=0, index_col=0).values
nps_range = 5

max_depth = tl.get_max_path_depth()

# Join Data
training_data_frame = np.concatenate((training_data_frame, testing_data_frame), axis=0)

training_data_record_count =training_data_frame.shape[0]

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

# Prep for Network
training_data = []
training_labels =[]
min_label =999
max_label =-999
for customer in training_data_frame:
    training_data.append(customer[0])
    if(customer[1] < min_label):
        min_label = customer[1]
    if (customer[1] > max_label):
        max_label = customer[1]

for customer in training_data_frame:
    result = customer[1] + abs(min_label)
    training_labels.append(result)

training_data_array = np.empty([training_data_record_count,1,max_depth])

for x in range(training_data_record_count):
    array = np.array(training_data[x])
    training_data_array[x] = array

# Shape DNN
dropout = 0.5
hidden_nodes = int(math.floor(max_depth *.3))
print(hidden_nodes)
model = keras.Sequential([
    keras.layers.Dense(max_depth, activation=tf.nn.relu, input_shape=(1, max_depth)),
    keras.layers.Dropout(dropout),
    keras.layers.Dense(5, activation=tf.nn.relu),
    keras.layers.Dropout(dropout),
    keras.layers.Dense(nps_range, activation=tf.nn.softmax)
])

# Compile DNN
model.compile(optimizer=keras.optimizers.Adam(),
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

# Tensorboard
tensor_board = tensorflow.keras.callbacks.TensorBoard(log_dir=os.path.realpath('..')+"\\HackItSolution\\Logs\{}".format(time()))

# Train
model_history = model.fit(training_data_array, training_labels, epochs=1, batch_size=50, verbose=2, callbacks=[tensor_board])

model.save('Networks\\RoutingEngine{}.NN'.format(time()))

scores = []
for x in range(training_data_record_count):
    testingdata= np.array(training_data_array[x])
    Testing_data_array = np.empty([1, 1, max_depth])
    Testing_data_array[0] = testingdata
    #print(model.predict(Testing_data_array))
    prediction = np.argmax(model.predict(Testing_data_array))
    didPass = 'false'
    if prediction == training_labels[x]:
        scores.append(1)
        didPass='true'
    else:
        scores.append(0)

    print(didPass + " " + str(prediction) + " and result should have been " + str(training_labels[x]))
print("Final Score: " + str(sum(scores) / len(scores) ))