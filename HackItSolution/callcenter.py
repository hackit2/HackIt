#!/usr/bin/env python3
import Inferencing
from datetime import datetime, timedelta
from operator import itemgetter
from pymongo import MongoClient
from random import Random, shuffle
from WebApi import config

STATE_NAMES = ['classic', 'neural']
STATE = {
    "classic": {
        "agents": {},
        "averageNps": 0,
        "totalCalls": 0,
        "totalNps": 0
    },
    "neural": {
        "agents": {},
        "averageNps": 0,
        "totalCalls": 0,
        "totalNps": 0
    }
}
RAND = Random()

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


def get_agent_index(agent, cc):
    g = (i for i, e in enumerate(cc['agents']) if e['id'] == agent['id'])
    return next(g)


def generate_calls(now, cc, cc_name):
    busy_agents = [a for a in cc['agents'] if a['busy']]
    busy_agent_count = len(busy_agents)
    expected_busy_agents = int((config.PERCENT_UTILIZATION / 100) * len(cc['agents']))
    needed_agents = expected_busy_agents - busy_agent_count

    if needed_agents > 0:
        if cc_name is 'neural':
            dnn = Inferencing.Inferencing()
            ivr_endpoint = RAND.randint(1, config.IVR_NODE_COUNT)

            for i in range(needed_agents):
                inferences = dnn.get_agent_predictions(f'N{str(ivr_endpoint)}')
                sorted(inferences)

                busy_agents = [a for a in cc['agents'] if a['busy']]
                for agent in busy_agents:
                    del inferences[agent['id']]

                sorted_inferences = sorted(inferences.items(), key=itemgetter(1))
                best_agent = sorted_inferences[0][0]
                new_nps = inferences[best_agent]

                time_modifier = RAND.randint(-1, 1)
                call_time = cc['agents'][best_agent]['_avg_handle_time'] + time_modifier

                cc['agents'][best_agent]['busy'] = True
                cc['agents'][best_agent]['_call_count'] += 1
                cc['agents'][best_agent]['_call_start'] = now
                cc['agents'][best_agent]['_call_end'] = now + timedelta(seconds=call_time)
                cc['agents'][best_agent]['_call_duration'] = call_time

                cc['agents'][best_agent]['nps'] = new_nps
                cc['agents'][best_agent]['_total_nps'] += new_nps
                cc['agents'][best_agent]['_average_nps'] = cc['agents'][best_agent]['_total_nps'] / cc['agents'][best_agent]['_call_count']
        else:
            shuffled_agents = cc['agents']
            shuffle(shuffled_agents)

            free_agents = [a for a in shuffled_agents if not a['busy']]
            new_agents = free_agents[:needed_agents]

            for new_agent in new_agents:
                new_nps = RAND.randint(1, 10)
                time_modifier = RAND.randint(-1, 1)
                call_time = new_agent['_avg_handle_time'] + time_modifier

                new_agent['busy'] = True
                new_agent['_call_count'] += 1
                new_agent['_call_start'] = now
                new_agent['_call_end'] = now + timedelta(seconds=call_time)
                new_agent['_call_duration'] = call_time

                new_agent['nps'] = new_nps
                new_agent['_total_nps'] += new_nps
                new_agent['_average_nps'] = new_agent['_total_nps'] / new_agent['_call_count']

                # We've been working out of shuffled_agents, so no changes have made
                # their way back into STATE. Fix that.
                cc['agents'][new_agent['id']] = new_agent

    return cc


def main():
    mongo_id = None
    cnt = 0
    while cnt < 1000:
        cnt += 1
    # while True:
        # Ensure we have _a_ document in the database. It's better the
        # frontend receive something empty matching our structure than
        # nothingness/error.
        count = collection.count_documents({})
        if count == 0:
            # Populate agents
            for i in range(1, config.AGENT_COUNT):
                agent = {
                    'id': f'A{str(i).zfill(2)}',
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
                    STATE[dataset]['agents'][agent['id']] = agent

            result = collection.insert_one(STATE)
            mongo_id = result.inserted_id

        if mongo_id is not None:
            for dataset in STATE_NAMES:
                now = datetime.utcnow()

                #print(STATE[dataset]['agents'])  # TODO
                # Free up agents who are no longer on a call
                for idx, agent in enumerate(STATE[dataset]['agents']):
                    # If an agent's call has ended, mark them as free
                    if agent['busy'] and now >= agent['_call_end']:
                        agent['busy'] = False
                        agent['_call_start'] = None
                        agent['_call_end'] = None
                        agent['_call_duration'] = None

                # Update the state and stats for each individual agent.
                STATE[dataset] = generate_calls(now, STATE[dataset], dataset)

                # Calculate averages for each data set.
                total_nps = 0
                total_calls = 0

                for idx, agent in enumerate(STATE[dataset]['agents']):
                    if agent['busy'] and agent['nps'] is not None:
                        total_nps += int(agent['_total_nps'])
                        total_calls += int(agent['_call_count'])

                if total_calls > 0:
                    STATE[dataset]['totalCalls'] = total_calls
                    STATE[dataset]['totalNps'] = total_nps
                    STATE[dataset]['averageNps'] = int(total_nps) / int(total_calls)

            # Update the state in the database
            result = collection.replace_one({'_id': mongo_id}, STATE, True)
            if result.upserted_id is not None:
                mongo_id = result.upserted_id


main()

print(STATE)
