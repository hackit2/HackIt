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


max_depth = tl.get_max_path_depth() +1

# Join Data
training_data_frame = np.concatenate((training_data_frame, testing_data_frame), axis=0)

training_data_record_count = training_data_frame.shape[0]
training_labels =[]

# Convert and Pad Data
for customer in training_data_frame:
    customer[2] = customer[2].replace('[','').replace(']','').split(',')
    customer[2] = customer[2] + ['P0'] * (max_depth - len(customer[2]))
    for x in range(len(customer[2])):
        customer[2][x] = int(customer[2][x].replace('N', '').replace('A', '').replace('P', '').replace('\'',''))
    training_labels.append(customer[0])

nps_range = 21

# Convert Strings to Floats
#for customer in training_data_frame:
    #for x in range(len(customer[2])):
        #customer[2][x] = float(''.join(str(ord(c)) for c in customer[2][x]))

# Normalize
training_hot_list = {}
for x in range(training_data_record_count):
    training_hot_list[x] = [x, (([0] * 40), ([0] * 40)), 0]
    pos = training_data_frame[x][2][0] - 1
    training_hot_list[x][1][0][pos] = 1
    pos = training_data_frame[x][2][1] - 1
    training_hot_list[x][1][1][pos] = 1
    training_hot_list[x][2] = training_data_frame[x][0]

training_data_temp = []
training_data_array = np.empty([training_data_record_count, 1, 80])
labels_array = []

for x in range(training_data_record_count):
    training_data_temp.append(np.concatenate((training_hot_list[x][1][0], training_hot_list[x][1][1]), axis=0))
    labels_array.append(training_hot_list[x][2])

training_data_temp = np.array(training_data_temp)
labels_array = np.array(labels_array)


for x in range(training_data_record_count):
    array = np.array(training_data_temp[x])
    training_data_array[x] = array


# Shape DNN
dropout = 0.9
model = keras.Sequential([
    keras.layers.Flatten(input_shape=(1, 80)),
    keras.layers.Dense(20, activation=tf.nn.relu),
    keras.layers.Dropout(dropout),
    keras.layers.Dense(1, activation=tf.nn.sigmoid)
])

# Compile DNN
model.compile(optimizer='adam',
              loss='binary_crossentropy',
              metrics=['accuracy', 'binary_crossentropy'])

# Tensorboard
tensor_board = tensorflow.keras.callbacks.TensorBoard(log_dir=os.path.realpath('..')+"\\HackItSolution\\Logs\{}".format(time()))

# Train
model_history = model.fit(training_data_array, training_labels, epochs=1000, batch_size=50, verbose=2, callbacks=[tensor_board])

model.save('Networks\\RoutingEngine{}.NN'.format(time()))

scores = []
for x in range(10):
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