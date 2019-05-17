from flask import Blueprint, current_app as app
from pymongo import MongoClient
import json


mod_api = Blueprint('api', __name__, url_prefix='/api')


@mod_api.route('/', methods=['GET'])
def index():
    return 'Welcome to the API.'


@mod_api.route('/state', methods=['GET', 'POST'])
def state():
    client = MongoClient('mongodb://localhost:27017')
    collection = client.hackit2.state
    retrieved_state = collection.find_one()
    return json.dumps(retrieved_state)


@mod_api.route('/state/reset', methods=['POST'])
def reset_state():
    client = MongoClient('mongodb://localhost:27017')
    collection = client.hackit2.state
    collection.delete_many({})
