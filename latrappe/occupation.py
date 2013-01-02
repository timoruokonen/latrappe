from action import *
from city import City
from npc import Npc
from npcstrategy import *
from occupation import *
from possession import Possession
from resource import *
from resourcefactory import ResourceFactory
from schedule import Schedule
from stockmarket import StockMarket

'''
Occupation for a NPC. Can be used to generate the default action for the occupation to a schedule.
'''
class Occupation(object):
    def __init__(self):
        self.inputs = []
        self.outputs = []

    def __str__(self):
        return "Nothing"

    def add_default_schedule(self, schedule, possession):
        pass

    def get_required_resources(self):
        return self.inputs

    def get_resources_to_be_produced(self):
        return self.outputs

class Farmer(Occupation):
    duration = 7 * 60

    def __init__(self):
        self.inputs = []
        self.outputs = [Grain]

    def __str__(self):
        return "Farmer"

    def add_default_schedule(self, schedule, possession):
        schedule.AddAction(ProduceAction("Farming", self.inputs, self.outputs, Farmer.duration, possession))

class Hunter(Occupation):
    duration = 4 * 60

    def __init__(self):
        self.inputs = []
        self.outputs = [Meat, Meat]

    def __str__(self):
        return "Hunter"

    def add_default_schedule(self, schedule, possession):
        schedule.AddAction(ProduceAction("Hunting", self.inputs, self.outputs, Hunter.duration, possession))

class Brewer(Occupation):
    duration = 7 * 60

    def __init__(self):
        self.inputs = [Grain, Grain]
        self.outputs = [Beer]

    def __str__(self):
        return "Brewer"

    def add_default_schedule(self, schedule, possession):
        schedule.AddAction(ProduceAction("Brewing beer", self.inputs, self.outputs, Brewer.duration, possession))

