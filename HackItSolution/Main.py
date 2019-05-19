import Inferencing
import random
import operator

I = Inferencing.Inferencing()

routing_collection = []
for x in range(1, 1000):
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

average_nps_classic_routing = 0
average_nps_nn_routing = 0

for call in routing_collection:
    average_nps_classic_routing += call['ClassicRoutingNPS']

average_nps_classic_routing = round(average_nps_classic_routing / len(routing_collection), 2)

for call in routing_collection:
    average_nps_nn_routing += call['NNRoutingNPS']

average_nps_nn_routing = round(average_nps_nn_routing / len(routing_collection), 2)

print('For 1000 random calls, Average NN Routing NPS is {} and Classic Routing NPS is {}'.format(average_nps_nn_routing, average_nps_classic_routing))