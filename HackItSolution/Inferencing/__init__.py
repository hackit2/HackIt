import tensorflow as tf
import tensorflow.keras as keras #Tensorflow 2.0
import tensorflow.keras.callbacks #Tensorflow 2.0
import numpy as np


class Inferencing:
    def __init__(self):
        self.model = keras.models.load_model('Networks/RoutingEngine1Mrecords25epoch96percent.NN')

    def get_agent_predictions(self, ivr_node):
        predictions = {}

        ivr_node = int(ivr_node.replace('N', ''))

        for x in range(1, 41):
            training_hot_list = (([0] * 40), ([0] * 40))
            training_hot_list[0][ivr_node-1] = 1
            training_hot_list[1][x-1] = 1
            testing_record = []
            testing_record.append(np.concatenate((training_hot_list[0], training_hot_list[1]), axis=0))

            testingdata = np.array(testing_record[0])
            Testing_data_array = np.empty([1, 1, 80])
            Testing_data_array[0] = testingdata
            # print(model.predict(Testing_data_array))
            results = self.model.predict(Testing_data_array)
            predictions['A'+str(x).zfill(2)] = np.argmax(results)
        return predictions



