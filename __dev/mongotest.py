from pprint import pprint
from pymongo import MongoClient

print('Connecting...')
client = MongoClient('mongodb://localhost:27017')
collection = client.hackit2.state

state = {
    "classic": {
        "averageNps": 3.2,
        "agents": [
            {"id": 1, "nps": None, "busy": False},
            {"id": 2, "nps": 2, "busy": True}
        ]
    },
    "neural": {
        "averageNps": 8.5,
        "agents": [
            {"id": 1, "nps": None, "busy": False},
            {"id": 2, "nps": 2, "busy": True}
        ]
    },
    "totalCalls": 10,
    "totalNps": 6
}

print('Clearing database...')
collection.delete_many({})

print('Inserting...')
result = collection.insert_one(state)
print(f'ID: {result.inserted_id}')

print('Retrieving...')
retrieved_state = collection.find_one()
pprint(retrieved_state)

print('Replacing...')
retrieved_state['totalNps'] = 7
result = collection.replace_one({'_id': retrieved_state['_id']}, retrieved_state)
print(f'ID: {result.upserted_id}')

print('Retrieving...')
retrieved_state = collection.find_one()
pprint(retrieved_state)

print('\n\n\n')
print('All objects:')
all = collection.find({})
for o in all:
    pprint(o)
