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
     
        next_status = field.next_status()
        if field.needs_presence(next_status):
            npc.schedule.add_action(ProductUnitAction(npc, field))
        else:
            npc.schedule.add_action(Action(npc, "Waiting for " + field.name(next_status) + " to finnish...", Farmer.DURATION))

    def get_required_resources(self):
        #farmer needs only inputs when field state is harvested
        #TODO: only handle one field for now for sake of simplicity...
        field = self.npc.possession.get_real_property(FieldSquare)
        if field == None:
            print "Farmer has no fields... "
            return []

        return field.total_inputs()

    def get_resources_to_be_produced(self):
        #farmer only outputs when field state is ready to be harvested
        #TODO: only handle one field for now for sake of simplicity...
        field = self.npc.possession.get_real_property(FieldSquare)
        if field == None:
            print "Farmer has no fields... "
            return []
        return field.final_outputs()



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
        npc.schedule.add_action(ProduceAction(npc, "Hunting", self.inputs, self.outputs, Hunter.DURATION, possession))

class Brewer(Occupation):
    DURATION = 7 * 60

    def __init__(self):
        pass

    def __str__(self):
        return "Brewer"

    def add_default_schedule(self, npc, possession):
        kettle = npc.possession.get_real_property(BeerKettle)
        if kettle == None:
            print "Brewer has no beer kettle... Cannot make beer!"
            return
        
        next_status = kettle.next_status()
        if kettle.needs_presence(next_status):
            npc.schedule.add_action(ProductUnitAction(npc, kettle))
        else:
            npc.schedule.add_action(Action(npc, "Waiting for " + kettle.name(next_status) + " to finnish...", Brewer.DURATION))

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

