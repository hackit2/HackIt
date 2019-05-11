import Call_Data_Generator
import Training_Shapes
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf #Tensorflow 2.0
import tensorflow.keras as keras #Tensorflow 2.0
from sklearn.preprocessing import normalize
import tensorflow.keras.callbacks #Tensorflow 2.0
from time import time
import os
import math
import logging as log

# Generate Training and Testing Data
cdg = Call_Data_Generator.CallDataGenerator()
tl = Training_Shapes.TrainingShapes()

training_callers_route_collection = {}
testing_callers_route_collection = {}

training_data_record_count = 1000
testing_data_record_count = 100
nps_range = 10

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

with open('TrainingData.csv', 'w') as file:
    file.write(tessellated_training_data_frame.to_csv(index=True))

with open('TestingData.csv', 'w') as file:
    file.write(tessellated_testing_data_frame.to_csv(index=True))


#cluster by NPS






# Train Neural Network
def plot_history(histories):
    plt.figure(figsize=(12, 8))

    for name, history in histories:
        for HistoryKey in history.history:
            val = plt.plot(history.epoch, history.history[HistoryKey],
                           '--', label=HistoryKey + ' Val')
            plt.plot(history.epoch, history.history[HistoryKey], color=val[0].get_color(),
                     label=HistoryKey + ' Train')

    plt.xlabel('Epochs')
    plt.legend()

    plt.xlim([0, max(history.epoch)])
    #plt.show()




max_depth = tl.get_max_path_depth()

# Pad Data
for customer in training_data_frame:
    training_data_frame[customer][0] = \
        training_data_frame[customer][0] + ['P0'] * (max_depth - len(training_data_frame[customer][0]))

for customer in testing_data_frame:
    testing_data_frame[customer][0] = \
        testing_data_frame[customer][0] + ['P0'] * (max_depth - len(testing_data_frame[customer][0]))

for customer in training_data_frame:
    for x in range(0, len(training_data_frame[customer][0])):
        training_data_frame[customer][0][x] = float(''.join(str(ord(c)) for c in training_data_frame[customer][0][x]))

for customer in testing_data_frame:
    for x in range(0, len(testing_data_frame[customer][0])):
        testing_data_frame[customer][0][x] = float(''.join(str(ord(c)) for c in testing_data_frame[customer][0][x]))

for customer in training_data_frame:
    training_data_frame[customer][0] = \
        [float(i)/sum(training_data_frame[customer][0]) for i in training_data_frame[customer][0]]

for customer in testing_data_frame:
    testing_data_frame[customer][0] = \
        [float(i) / sum(testing_data_frame[customer][0]) for i in testing_data_frame[customer][0]]

training_data = []
training_labels =[]
min_label =999
max_label =-999
for customer in training_data_frame:
    training_data.append(training_data_frame[customer][0])
    if(training_data_frame[customer][1] < min_label):
        min_label = training_data_frame[customer][1]
    if (training_data_frame[customer][1] > max_label):
        max_label = training_data_frame[customer][1]

for customer in training_data_frame:
    result = training_data_frame[customer][1] + abs(min_label)
    training_labels.append(result)

training_data_array = np.empty([training_data_record_count,1,14])

for x in range(training_data_record_count):
    array = np.array(training_data[x])
    training_data_array[x] = array


# Shape DNN
dropout = 0.5
hidden_nodes = int(math.floor(max_depth *.66))
#model = keras.Sequential([
#    keras.layers.Dense(max_depth, kernel_regularizer=keras.regularizers.l2(0.001), activation=tf.nn.relu, input_shape=(1,max_depth)),
#    keras.layers.Dropout(dropout),
#    keras.layers.Dense(nps_range, activation=tf.nn.sigmoid)
#])

model = keras.Sequential([
    keras.layers.Dense(max_depth, kernel_regularizer=keras.regularizers.l2(0.001), activation=tf.nn.relu, input_shape=(1,max_depth)),
    keras.layers.Dropout(dropout),
    keras.layers.Dense(hidden_nodes, activation=tf.nn.relu),
    keras.layers.Dropout(dropout),
    keras.layers.Dense(nps_range, activation=tf.nn.sigmoid)
])

# Compile DNN
model.compile(optimizer=keras.optimizers.Adam(),
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy', 'sparse_categorical_crossentropy', 'kullback_leibler_divergence','categorical_crossentropy', 'cosine_proximity'])

# Tensorboard
tensor_board = tensorflow.keras.callbacks.TensorBoard(log_dir=os.path.realpath('..')+"\\Logs\{}".format(time()))

# Train
model_history = model.fit(training_data_array, training_labels, epochs=10, batch_size=50000, verbose=2, callbacks=[tensor_board])

#plot_history([('Current_Training', model_history)])

testingdata = np.array(training_data_array[x])
Testing_data_array = np.empty([1, 1, 14])
for x in range(9):
    for y in testingdata:
        if y[0] == 'A':
            y = 'A' + str(x)
    Testing_data_array[0] = testingdata
    prediction = np.argmax(model.predict(Testing_data_array))
    print(prediction)


for x in range(100):
    testingdata= np.array(training_data_array[x])
    Testing_data_array = np.empty([1,1,14])
    Testing_data_array[0] = testingdata
    #print(model.predict(Testing_data_array))
    prediction = np.argmax(model.predict(Testing_data_array))
    didPass = 'false'
    if prediction == training_labels[x]:
        didPass = 'true'

    print(didPass + " " + str(prediction) + " and result should have been " + str(training_labels[x]))

# Get Summary
#model.summary()
