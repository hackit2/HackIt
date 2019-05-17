#!/usr/bin/env python3
from datetime import datetime, timedelta
from pymongo import MongoClient
from random import Random
from WebApi import config

# TODO: daemonize. Perhaps https://github.com/thesharp/daemonize

STATE_NAMES = ['classic', 'neural']
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
                '_average_nps': 0,
                '_total_nps': 0,
                '_call_count': 0,
                '_call_start': None,
                '_call_end': None,
                '_avg_handle_time': RAND.randint(2, 7)
            }
            for dataset in STATE_NAMES:
                STATE[dataset]['agents'].append(agent)

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

        # Update the state and stats for each individual agent.
        for dataset in STATE_NAMES:
            for agent in STATE[dataset]['agents']:
                if agent['busy'] and now >= agent['_call_end']:
                    agent['busy'] = False

                if not agent['busy']:
                    # Check to see if the agent got a new call
                    r = RAND.randint(0, 101)
                    if r <= config.PERCENT_UTILIZATION:
                        time_modifier = RAND.randint(-1, 2)
                        call_time = agent['_avg_handle_time'] + time_modifier

                        agent['busy'] = True
                        agent['_call_count'] += 1
                        agent['_call_start'] = now
                        agent['_call_end'] = now + timedelta(seconds=call_time)

                        if dataset == 'neural':
                            # TODO: generate random route (or read one from test data)
                            # TODO: inference
                            pass
                        else:
                            new_nps = RAND.randint(1, 11)

                            agent['nps'] = new_nps
                            agent['_total_nps'] += new_nps
                            agent['_average_nps'] = agent['_total_nps'] / agent['_call_count']

        # Calculate averages for each data set.
        for dataset in STATE_NAMES:
            combined_nps = 0
            total_calls = 0

            for agent in STATE[dataset]['agents']:
                if agent['busy'] and agent['nps'] is not None:
                    combined_nps += agent['nps']
                    total_calls += agent['_call_count']

            if total_calls > 0:
                STATE[dataset]['totalCalls'] = total_calls
                STATE[dataset]['averageNps'] = combined_nps / total_calls

        # Update the state in the database
        result = collection.replace_one({'_id': ID}, STATE, True)
        if result.upserted_id is not None:
            ID = result.upserted_id

    # TODO: Remove
    if RAND.randint(0, 100) <= 10:
        retrieved_state = collection.find_one()
        from pprint import pprint
        pprint(retrieved_state)
    from time import sleep
    sleep(1)
