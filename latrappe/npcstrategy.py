from resource import *
from action import *
from occupation import *

class NpcStrategySimpleGreedy(object):
    MINIMUM_FOOD = 2
    MAXIMUM_FOOD = 5

    def __init__(self, npc):
        self.npc = npc

    def to_string(self):
        return str(self.npc.occupation)

    def create_schedule(self):
        to_buy = []
        to_sell = []

        #if food is getting low, try to get more
        if len(self.npc.possession.get_foods()) < NpcStrategySimpleGreedy.MINIMUM_FOOD:
            to_buy.append(Meat)
                        
        #try to get ingredients for occupation
        required = self.npc.occupation.get_required_resources()
        if not self.npc.possession.has_resources(required):
            for resourceType in required:
                to_buy.append(resourceType)
                   
        #sell stuff
        produced = self.npc.occupation.get_resources_to_be_produced()
        handled = []
        for resourceType in produced:
            if resourceType in handled:
                continue
            handled.append(resourceType)
            count = self.npc.possession.get_resource_count(resourceType)
            if count == 0:
                continue
            
            #special case if input contains same types as output
            if resourceType in required:
                count -= required.count(resourceType)
                if count <= 0:
                    continue

            #sell food away only if npc has enough food for the bad times
            if issubclass(resourceType, FoodResource):
                if len(self.npc.possession.get_foods()) < NpcStrategySimpleGreedy.MAXIMUM_FOOD:
                    continue
                count = min(count, len(self.npc.possession.get_foods()) - NpcStrategySimpleGreedy.MAXIMUM_FOOD)
            for _ in range(count):
                to_sell.append(resourceType)
        
        self._add_stock_action(to_buy, to_sell)

        #move to work place TODO: Refactor!!
        if type(self.npc.occupation) == Farmer:
            #go to the first owned field...
            field = self.npc.possession.get_real_property(FieldSquare)
            if field != None:
                self.npc.schedule.add_action(MoveAction("Moving", self.npc, field.x, field.y - 30))
            else:
                #no fields, go home...               
                self.npc.schedule.add_action(MoveAction("Moving", self.npc, self.npc.home_x, self.npc.home_y))
        elif type(self.npc.occupation) == Brewer:
            #go to the first owned beer kettle...
            kettle = self.npc.possession.get_real_property(BeerKettle)
            if kettle != None:
                self.npc.schedule.add_action(MoveAction("Moving", self.npc, kettle.x, kettle.y - 30))
            else:
                self.npc.schedule.add_action(MoveAction("Moving", self.npc, self.npc.home_x, self.npc.home_y))
        else:
            self.npc.schedule.add_action(MoveAction("Moving", self.npc, self.npc.occupation.POS_X, self.npc.occupation.POS_Y))

        #add occupation action
        self.npc.occupation.add_default_schedule(self.npc, self.npc.possession)

        #Go home to sleep
        self.npc.schedule.add_action(MoveAction("Moving", self.npc, self.npc.home_x, self.npc.home_y))

                                                    
    def _add_stock_action(self, to_buy, to_sell):
        if len(to_buy) > 0:
            print "Greedy strategy (" + self.to_string() + "): Adding to buy: " + str(to_buy)
        if len(to_sell) > 0:
            print "Greedy strategy (" + self.to_string() + "): Adding to sell: " + str(to_sell)
        if len(to_sell) == 0 and len(to_buy) == 0:
            return
    
        stocks = self.npc.city.stocks
        if len(stocks) > 0:
            self.npc.schedule.add_action(MoveAction("Moving", self.npc, stocks[0].x, stocks[0].y))
            self.npc.schedule.add_action(StockAction("Stock", to_buy, to_sell, self.npc, stocks[0]))
            return
        print "No stock market available!"

