from random import Random
from datetime import datetime, timedelta


RANDOM = Random()


class Agent:
    def __init__(self, id, average_call_duration):
        self.id = id
        self.on_call = False
        self.call_start = None
        self.call_end = None
        self.average_call_duration = average_call_duration

    def __str__(self):
        return f'Agent&lt;id={self.id}&gt;[on_call={self.on_call},' + \
                f'call_start={self.call_start},call_end={self.call_end}]'

    def ring(self):
        if not self.on_call:
            self.on_call = True

            lower_bound = self.average_call_duration - 1
            upper_bound = self.average_call_duration + 1
            call_length = RANDOM.randrange(lower_bound, upper_bound + 1)

            self.call_start = datetime.utcnow()
            self.call_end = self.call_start + timedelta(seconds=call_length)


class CallCenter:
    def __init__(self):
        self.agents = []

    def add_agent(self, agent):
        self.agents.append(agent)
