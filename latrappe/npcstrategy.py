from resource import *

class NpcStrategySimpleGreedy(object):
    minimumFood = 2

    def __init__(self, npc):
        self.npc = npc

    def ToString(self):
        return str(self.npc.occupation)

    def CreateSchedule(self):
        #if food is getting low, try to get more
        if len(self.npc.possession.GetFoods()) < NpcStrategySimpleGreedy.minimumFood:
            if self._BuyResource(Meat):
                print "Greedy strategy (" + self.ToString() + "): Bought food!"
            else:
                print "Greedy strategy (" + self.ToString() + "): Could not buy food!"
                        
        #try to get ingredients for occupation
        required = self.npc.occupation.GetRequiredResources()
        if not self.npc.possession.HasResources(required):
            for resourceType in required:
                if self._BuyResource(resourceType):
                    print "Greedy strategy (" + self.ToString() + "): Bought resource (" + str(resourceType) + ")!" 
                else:
                    print "Greedy strategy (" + self.ToString() + "): Could not buy resource (" + str(resourceType) + ")!" 
                    

        #add occupation action
        self.npc.occupation.AddDefaultSchedule(self.npc.schedule, self.npc.possession)

        #sell produced goods (if not food, TODO: QUICK FIX FOR HUNTER!!)
        produced = self.npc.occupation.GetResourcesToBeProduced()
        for resourceType in produced:
            resource = self.npc.possession.GetResource(resourceType)
            if resource != None and not isinstance(resource, FoodResource):
                if self._SellResource(resource):
                    print "Greedy strategy (" + self.ToString() + "): Sold resource! (" + str(resource) + ")"
                else:
                    print "Greedy strategy (" + self.ToString() + "): Could not sell resource! (" + str(resource) + ")"
                                                    

    def _BuyResource(self, resourceType):
        stocks = self.npc.GetCity().GetStockMarkets()
        if len(stocks) > 0:
            resource = stocks[0].FindResource(resourceType)
            if resource != None:
                return stocks[0].BuyResource(resource, self.npc.possession)
        print "No stock market available!"
        return False

    def _SellResource(self, resource):
        stocks = self.npc.GetCity().GetStockMarkets()
        if len(stocks) > 0:
            return stocks[0].SellResource(resource, self.npc.possession)
        return False

