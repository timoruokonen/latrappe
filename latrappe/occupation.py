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
    POS_X = 0
    POS_Y = 0

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
    DURATION = 7 * 60
    POS_X = 300
    POS_Y = 100

    def __init__(self):
        pass

    def __str__(self):
        return "Farmer"

    def add_default_schedule(self, npc, possession):
        #TODO: only handle one field for now for sake of simplicity...
        field = npc.possession.get_real_property(FieldSquare)
        if field == None:
            print "Farmer has no fields... Cannot add farming action"
            return
                
        if field.status == FieldSquare.STATUS_HARVESTED:    
            npc.schedule.add_action(FieldAction("Ploughing field", npc, field, FieldSquare.STATUS_PLOUGHED))
        elif field.status == FieldSquare.STATUS_PLOUGHED:
            npc.schedule.add_action(FieldAction("Sowing field", npc, field, FieldSquare.STATUS_SOWED))
        elif field.status == FieldSquare.STATUS_SOWED:
            npc.schedule.add_action(Action("Waiting for grain to grow...", Farmer.DURATION))
        elif field.status == FieldSquare.STATUS_READY_TO_BE_HARVESTED:
            npc.schedule.add_action(FieldAction("Harvesting field", npc, field, FieldSquare.STATUS_HARVESTED))

    def get_required_resources(self):
        #farmer needs only inputs when field state is harvested
        #TODO: only handle one field for now for sake of simplicity...
        field = self.npc.possession.get_real_property(FieldSquare)
        if field == None:
            print "Farmer has no fields... "
            return []
        #if field.status == FieldSquare.STATUS_HARVESTED:    
        return FieldSquare.SOWING_INPUTS
        #return []

    def get_resources_to_be_produced(self):
        #farmer only outputs when field state is ready to be harvested
        #TODO: only handle one field for now for sake of simplicity...
        field = self.npc.possession.get_real_property(FieldSquare)
        if field == None:
            print "Farmer has no fields... "
            return []
        #if field.status == FieldSquare.STATUS_READY_TO_BE_HARVESTED:    
        return FieldSquare.HARVEST_OUTPUTS
        #return []


class Hunter(Occupation):
    DURATION = 4 * 60
    POS_X = 650
    POS_Y = 50

    def __init__(self):
        self.inputs = []
        self.outputs = [Meat, Meat]

    def __str__(self):
        return "Hunter"

    def add_default_schedule(self, npc, possession):
        npc.schedule.add_action(ProduceAction("Hunting", self.inputs, self.outputs, Hunter.DURATION, possession))

class Brewer(Occupation):
    DURATION = 7 * 60
    POS_X = 90
    POS_Y = 310

    def __init__(self):
        self.inputs = [Grain, Grain]
        self.outputs = [Beer]

    def __str__(self):
        return "Brewer"

    def add_default_schedule(self, npc, possession):
        kettle = npc.possession.get_real_property(BeerKettle)
        if kettle == None:
            print "Brewer has no beer kettle... Cannot make beer!"
            return
        
        next_status = kettle.next_status()
        if kettle.needs_presence(next_status):
            npc.schedule.add_action(BrewAction(npc, kettle))
        else:
            npc.schedule.add_action(Action("Waiting for " + kettle.name(next_status) + " to finnish...", Brewer.DURATION))
        #npc.schedule.add_action(ProduceAction("Brewing beer", self.inputs, self.outputs, Brewer.DURATION, possession))

    def get_required_resources(self):
        kettle = self.npc.possession.get_real_property(BeerKettle)
        if kettle == None:
            print "Brewer has no beer kettle... Cannot make beer!"
            return []
        return kettle.inputs(kettle.next_status())



    def get_resources_to_be_produced(self):
        kettle = self.npc.possession.get_real_property(BeerKettle)
        if kettle == None:
            print "Brewer has no beer kettle... Cannot make beer!"
            return []

        return kettle.final_outputs()

