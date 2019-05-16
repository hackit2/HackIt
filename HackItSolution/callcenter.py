#!/usr/bin/env python3
from datetime import datetime
from pymongo import MongoClient
from random import Random
from WebApi import config

STATE = {
    "classic": {
        "averageNps": 0,
        "agents": []
    },
    "neural": {
        "averageNps": 0,
        "agents": []
    },
    "totalCalls": 0,
    "totalNps": 0
}
ID = None
RAND = Random()

# Warm fuzzies
print('Starting backend call center process.')
print('Configuration:')
print(f'      Agents:       {config.AGENT_COUNT}')
print(f'      Utilization:  {config.PERCENT_UTILIZATION}')

# Connect to the database
client = MongoClient('mongodb://localhost:27017')
collection = client.hackit2.state

# Clear previous state
collection.delete_many({})

while True:
    # Ensure we have _a_ document in the database. It's better the
    # frontend receive something empty matching our structure than
    # nothingness/error.
    count = collection.count_documents({})
    if count == 0:
        # Populate agents
        for i in range(1, config.AGENT_COUNT + 1):
            agent = {
                'id': i,
                'busy': False,
                'nps': None,
                '_call_start': None,
                '_call_end': None,
                '_avg_handle_time': RAND.randint(2, 7)
            }
            STATE['classic']['agents'].append(agent)
            STATE['neural']['agents'].append(agent)

        result = collection.insert_one(STATE)
        ID = result.inserted_id

        # from sys import exit
        # from pprint import pprint
        # all = collection.find({})
        # for o in all:
        #     pprint(o)
        # exit(0)

    if ID is not None:
        now = datetime.utcnow()

        # Clear out any agents who have finished their call since
        # our last loop.  TODO

        # Loop through all available agents and determine if they're
        # now on a call. If so, give them a new call within +-1s of
        # their average handle time. For the classic data set, pick
        # a random NPS in [1, 10]. For the neural data set, inference
        # a random route and provide that NPS. Update the average
        # NPS for this particular agent, and increase total NPS/calls
        # for each data set. TODO

        # Loop through both data sets and update average NPS. TODO
        pass
