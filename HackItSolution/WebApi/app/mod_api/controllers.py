from bson.json_util import dumps
from flask import Blueprint, current_app as app
from flask_cors import cross_origin
from pymongo import MongoClient


mod_api = Blueprint('api', __name__, url_prefix='/api')


@mod_api.route('/', methods=['GET'])
def index():
    return 'Welcome to the API.'


@mod_api.route('/state', methods=['GET', 'POST'])
@cross_origin()
def state():
    client = MongoClient('mongodb://localhost:27017')
    collection = client.hackit2.state
    retrieved_state = collection.find_one()
    return dumps(retrieved_state)


@mod_api.route('/state/reset', methods=['POST'])
def reset_state():
    client = MongoClient('mongodb://localhost:27017')
    collection = client.hackit2.state
    collection.delete_many({})
