import Inferencing
from collections import OrderedDict
from datetime import datetime, timedelta
from operator import itemgetter
from pymongo import MongoClient
from random import Random, shuffle
from time import sleep
from WebApi import config
import operator


STATE_NAMES = ['classic', 'neural']
STATE = {
    "classic": {
        "agents": [],
        "averageNps": 0,
        "totalCalls": 0,
        "totalNps": 0
    },
    "neural": {
        "agents": [],
        "averageNps": 0,
        "totalCalls": 0,
        "totalNps": 0
    }
}
random = Random()

# Warm fuzzies
print('Starting call centers.')
print('Configuration:')
print(f'      Agents:       {config.AGENT_COUNT}')
print(f'      IVR Nodes:    {config.IVR_NODE_COUNT}')
print(f'      Utilization:  {config.PERCENT_UTILIZATION}%')

# Connect to the database
client = MongoClient('mongodb://localhost:27017')
collection = client.hackit2.state

# Clear previous state
collection.delete_many({})

I = Inferencing.Inferencing()
total_calls = 0
classic_total_nps = 0
neural_total_nps = 0
while True:
    try:
        total_calls = STATE['classic']['totalCalls']
        classic_total_nps = STATE['classic']['totalNps']
        neural_total_nps = STATE['neural']['totalNps']
        STATE = {
            "classic": {
                "agents": [],
                "averageNps": 0,
                "totalCalls": 0,
                "totalNps": 0
            },
            "neural": {
                "agents": [],
                "averageNps": 0,
                "totalCalls": 0,
                "totalNps": 0
            }
        }


        routing_collection = []
        sleep(1)
        for x in range(1, 41):
            random_routed_call = {}
            random_routed_call['IVRNode'] = random_ivr_node = random.randint(1, 40)
            inference_results = I.get_agent_predictions('N' + str(random_ivr_node))
            # Random Routing
            random_routed_call['ClassicRoutingAgent'] = random_agent = random.randint(1, 40)
            random_routed_call['ClassicRoutingNPS'] = inference_results['A' + str(random_agent).zfill(2)]
            # NN Routing
            random_routed_call['NNRoutingAgent'] = max(inference_results.items(), key=operator.itemgetter(1))[0]
            random_routed_call['NNRoutingNPS'] = inference_results[random_routed_call['NNRoutingAgent']]
            routing_collection.append(random_routed_call)

        x=0
        for call in routing_collection:
            STATE['classic']['agents'].append({ 'id':int(x),'nps':int(call['ClassicRoutingNPS']),'busy':True })
            STATE['neural']['agents'].append({ 'id':int(x),'nps':int(call['NNRoutingNPS']),'busy':True  })
            x=x+1

        average_nps_classic_routing = 0
        average_nps_nn_routing = 0

        for call in routing_collection:
            average_nps_classic_routing += call['ClassicRoutingNPS']

        STATE['classic']['totalNps'] = int(classic_total_nps + average_nps_classic_routing)
        average_nps_classic_routing = round(average_nps_classic_routing / len(routing_collection), 2)
        STATE['classic']['averageNps'] = round(average_nps_classic_routing,2)
        for call in routing_collection:
            average_nps_nn_routing += call['NNRoutingNPS']

        STATE['neural']['totalNps'] = int(neural_total_nps + average_nps_nn_routing)
        average_nps_nn_routing = round(average_nps_nn_routing / len(routing_collection), 2)
        STATE['neural']['averageNps'] = round(average_nps_nn_routing,2)

        STATE['classic']['totalCalls'] = int(total_calls + 40)
        STATE['neural']['totalCalls'] = int(total_calls + 40)
        count = collection.count_documents({})
        if count == 0:
            result = collection.insert_one(STATE)
            mongo_id = result.inserted_id
        else:
            result = collection.replace_one({'_id': mongo_id}, STATE, True)

        if(STATE['classic']['totalCalls']>=1000):
            STATE['classic']['totalCalls'] = 0
            STATE['neural']['totalCalls'] = 0
            STATE['neural']['totalNps'] = 0
            STATE['neural']['averageNps'] = 0
            STATE['classic']['totalNps'] = 0
            STATE['classic']['averageNps'] = 0
    except Exception as e:
        print(e)


