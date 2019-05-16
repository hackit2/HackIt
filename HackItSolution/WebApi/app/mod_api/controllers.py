from flask import Blueprint, request, render_template, flash, \
        g, session, redirect, url_for, current_app as app
from app.mod_api.models import Agent, CallCenter


mod_api = Blueprint('api', __name__, url_prefix='/api')


@mod_api.route('/', methods=['GET'])
def index():
    return 'You have hit the API. You are visitor #{cnt}'


@mod_api.route('/agent/<int:id>', methods=['GET', 'POST'])
def get_agent(id):
    from random import Random
    r = Random()

    chance = app.config['PERCENT_UTILIZATION']
    will_ring = r.randrange(0, 101)

    agent = Agent(id, r.randrange(3, 10))
    if will_ring <= chance:
        agent.ring()

    return str(agent)


def get_neural_cc():
    if 'neural_cc' not in g:
        g.neural_cc = CallCenter()

    return g.neural_cc


def get_classic_cc():
    if 'classic_cc' not in g:
        g.classic_cc = CallCenter()

    return g.classic_cc