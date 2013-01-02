from resource import *

class NpcStrategySimpleGreedy(object):
    MINIMUM_FOOD = 2
    MAXIMUM_FOOD = 5

    def __init__(self, npc):
        self.npc = npc

    def to_string(self):
        return str(self.npc.occupation)

    def create_schedule(self):
        #if food is getting low, try to get more
        if len(self.npc.possession.get_foods()) < NpcStrategySimpleGreedy.MINIMUM_FOOD:
            if self._buy_resource(Meat):
                print "Greedy strategy (" + self.to_string() + "): Bought food!"
            else:
                print "Greedy strategy (" + self.to_string() + "): Could not buy food!"
                        
        #try to get ingredients for occupation
        required = self.npc.occupation.get_required_resources()
        if not self.npc.possession.has_resources(required):
            for resourceType in required:
                if self._buy_resource(resourceType):
                    print "Greedy strategy (" + self.to_string() + "): Bought resource (" + str(resourceType) + ")!" 
                else:
                    print "Greedy strategy (" + self.to_string() + "): Could not buy resource (" + str(resourceType) + ")!" 
                    

        #add occupation action
        self.npc.occupation.add_default_schedule(self.npc.schedule, self.npc.possession)

        produced = self.npc.occupation.get_resources_to_be_produced()
        for resourceType in produced:
            resource = self.npc.possession.get_resource(resourceType)
            if resource == None:
                continue

            #sell food away only if npc has enough food for the bad times
            if isinstance(resource, FoodResource) and len(self.npc.possession.get_foods()) < NpcStrategySimpleGreedy.MAXIMUM_FOOD:
                continue

            if self._sell_resource(resource):
                print "Greedy strategy (" + self.to_string() + "): Sold resource! (" + str(resource) + ")"
            else:
                print "Greedy strategy (" + self.to_string() + "): Could not sell resource! (" + str(resource) + ")"
                                                    

    def _buy_resource(self, resourceType):
        stocks = self.npc.get_city().GetStockMarkets()
        if len(stocks) > 0:
            resource = stocks[0].find_resource(resourceType)
            if resource != None:
                return stocks[0].buy_resource(resource, self.npc.possession)
            print "Stock is out of " + str(resourceType) + "!"
            return False
        print "No stock market available!"
        return False

    def _sell_resource(self, resource):
        stocks = self.npc.get_city().GetStockMarkets()
        if len(stocks) > 0:
            return stocks[0].sell_resource(resource, self.npc.possession)
        return False

