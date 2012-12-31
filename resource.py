'''
NOTICE!!

This piece of art is still totally under construction!! Don't look any further. All the classes are 
in the same file and contain whatever shiiiit :)
'''

class City(object):
    def __init__(self):
        self.npcs = []
        self.stocks = []

    def AddNpc(self, npc):
        npc.SetCity(self)
        self.npcs.append(npc)

    def GetNpcs(self):
        return self.npcs
    
    def AddStockMarket(self, stock):
        self.stocks.append(stock)

    def GetStockMarkets(self):
        return self.stocks


'''
Handles ownings of an entity. Contains a list of resources and amount of money.
'''
class Possession(object):
    def __init__(self):
        self.resources = []
        self.money = 0

    def AddResource(self, resource):
        self.resources.append(resource)

    def DestroyResource(self, resource):
        #print "Removing " + str(resource)
        self.resources.remove(resource)

    def GiveResource(self, resource, newOwner):
        self.resources.remove(resource)
        newOwner.resources.append(resource)

    def GetResource(self, resourceType):
        for resource in self.resources:
            if (isinstance(resource, resourceType)):
                return resource
        return None

    def HasResources(self, resources):
        usedResources = []
        for inputResource in resources:
            found = False
            for resource in self.resources:
                if (resource in usedResources):
                    continue
                #print "Comparing " + str(resource) + " to " + str(inputResource)
                if (isinstance(resource, inputResource)):
                    usedResources.append(resource)
                    found = True
                    break;
            if not found:
                return False
        return True

    def GetFoods(self):
        foods = []
        for resource in self.resources:
            if (isinstance(resource, FoodResource)):
                foods.append(resource)
        return foods

    def GetMoney(self):
        return self.money;

    def GiveMoney(self, amount, newOwner):
        if amount > self.money:
            return False
        self.money -= amount
        newOwner.money += amount

'''
Game NPC. Each NPC instance must be advanced when the game is advanced. 
'''
class Npc(object):
    sleepDuration = 7 * 60
    defaultFoodConsumption = 1 #amount of food needed per unit of time (now minute...)

    def __init__(self, occupation):
        self.occupation = occupation
        self.schedule = Schedule()
        #TODO: Cannot think... just advance schedule so that it is already done when Advance is called the first time...
        self.schedule.Advance(Schedule.MaxTime)
        self.possession = Possession()
        self.hungerLevel = 24 * 60 #enough for one day
        self.foodConsumption = Npc.defaultFoodConsumption
        self.alive = True
        self.strategy = None
        self.city = None

    def PrintStatus(self):
        if not self.alive:
            print "Npc is DEAD!"
        print "Npc (" + str(self.occupation) + ") has " + str(self.possession.money) + " money, owns:"
        for pos in self.possession.resources:
            print pos

    def SetCity(self, city):
        self.city = city

    def GetCity(self):
        return self.city

    def SetStrategy(self, strategy):
        self.strategy = strategy

    #TODO: How to handle time advancing. Now advancing goes fine if the time interval is smalles possible.
    #If the interval is increased, first schedule is advanced and then food. This leads to not wanted scenarios
    #where npc can do work without food.
    def Advance(self, time):
        while (time > 0):
            if not self.alive:
                return

            #Day is completed, create new schedule
            if (self.schedule.IsDone()):
                self.CreateSchedule()
            
            timeLeft = self.schedule.Advance(time) 
            self._ConsumeFood(time - timeLeft)
            time = timeLeft

    def IsAlive(self):
        return self.alive;
            
    def CreateSchedule(self):
        self.schedule = Schedule()
        if self.strategy == None:
            self._AddDefaultActions()
            self.occupation.AddDefaultSchedule(self.schedule, self.possession)
        else:
            self._AddDefaultActions()
            self.strategy.CreateSchedule()

    def _ConsumeFood(self, time):
        while (time > 0):
            if (self.hungerLevel <= 0):
                foods = self.possession.GetFoods()
                if len(foods) == 0:
                    self.alive = False
                    print "NPC died from hunger!"
                    return
                #just eat the first thing from the inventory...
                self.possession.DestroyResource(foods[0])
                self.hungerLevel += foods[0].nutritionalValue
            consumedAmount = min(time, self.hungerLevel)
            self.hungerLevel -= consumedAmount * self.foodConsumption            
            time -= consumedAmount

    def _AddDefaultActions(self):
        self.schedule.AddAction(Action("Sleep", [],[], Npc.sleepDuration, self.possession))

class NpcStrategySimpleGreedy(object):
    minimumFood = 2

    def __init__(self, npc):
        self.npc = npc

    def ToString(self):
        return str(self.npc.occupation)

    def CreateSchedule(self):
        #if food is getting low, try to get more
        if len(self.npc.possession.GetFoods()) < NpcStrategySimpleGreedy.minimumFood:
            print "Greedy strategy (" + self.ToString() + "): Trying to buy food!"
            self._BuyResource(Meat)
        
        #try to get ingredients for occupation
        required = self.npc.occupation.GetRequiredResources()
        if not self.npc.possession.HasResources(required):
            print "Greedy strategy: Trying to buy resources!"
            for resourceType in required:
                self._BuyResource(resourceType)

        #add occupation action
        self.npc.occupation.AddDefaultSchedule(self.npc.schedule, self.npc.possession)

        #sell produced goods (if not food, TODO: QUICK FIX FOR HUNTER!!)
        produced = self.npc.occupation.GetResourcesToBeProduced()
        for resourceType in produced:
            resource = self.npc.possession.GetResource(resourceType)
            if resource != None and not isinstance(resource, FoodResource):
                print "Greedy strategy: Sell resources! (" + str(resource) + ")"
                self._SellResource(resource)


    def _BuyResource(self, resourceType):
        stocks = self.npc.GetCity().GetStockMarkets()
        if len(stocks) > 0:
            resource = stocks[0].FindResource(resourceType)
            if resource != None:
                return stocks[0].BuyResource(resource, self.npc.possession)
        return False

    def _SellResource(self, resource):
        stocks = self.npc.GetCity().GetStockMarkets()
        if len(stocks) > 0:
            return stocks[0].SellResource(resource, self.npc.possession)
        return False

'''
Schedule for one day for a NPC. The schedule contains actions and must be advanced when the NPC is advanced.

Scheduled tasks are for now always in a queue. First items are done first. If the day is finished and some
tasks are still unfinished, these should be moved to the next day.
'''
class Schedule(object):
    #Lame, just use minutes now
    MaxTime = 24 * 60

    def __init__(self):
        self.actions = []
        self.totalRemainingTime = Schedule.MaxTime

    def GetTotalRemainingTime(self):
        return self.totalRemainingTime

    def AddAction(self, action):
        self.actions.append(action)

    def Advance(self, time):
        timeToSpend = min(time, self.totalRemainingTime)
        timeLeft = time - timeToSpend
        self.totalRemainingTime -= timeToSpend

        #advance through actions and remove if completed
        while (timeToSpend > 0):
            action = self.GetCurrentAction()
            if (action != None):
                #print "Advancing action " + action.name + ". Time left of day: " + str(self.totalRemainingTime)       
                timeToSpend = action.Advance(timeToSpend)
                if (action.IsDone()):
                    self._RemoveAction(action)
            else:
                #print "Doing nothing..." + ". Time left of day: " + str(self.totalRemainingTime)
                break;
        return timeLeft

    def GetCurrentAction(self):
        if (len(self.actions) > 0):
            return self.actions[0]
        return None

    def GetCurrentActionName(self):
        if (len(self.actions) > 0):
            return self.actions[0].name
        return "Lazing around"

    def IsDone(self):
        return self.totalRemainingTime <= 0

    def GetListOfNotFinishedActions(self):
        return self.actions

    def _RemoveAction(self, action):
        self.actions.remove(action)

'''
General action that requires input resources and produces output resources in given time. 
When the action is started, input resources are removed from the given possession instance.
When the action is finished, created output resources are added to the given possession instance.
'''
class Action(object):
    def __init__(self, name, inputs, outputs, duration, possession):
        self.started = False
        self.name = name
        self.timeLeft = duration
        self.inputs = inputs
        self.outputs = outputs
        self.possession = possession
        self.createdOutputs = []

    def _AddOutputs(self):
        for output in self.createdOutputs:
            self.possession.AddResource(output)

    def Advance(self, time):
        if not self.started:
            self._ReserveResourcesAndCreateOutputs()

        self.timeLeft -= time
        if (self.IsDone()):
            self._AddOutputs()

        if (self.timeLeft < 0):
            #action was completed and some time was left
            return -self.timeLeft
        return 0

    def IsDone(self):
        return self.timeLeft <= 0

    def _ReserveResourcesAndCreateOutputs(self):
        print "Starting action " + self.name       
        self.started = True

        if not self.possession.HasResources(self.inputs):
            print "Not enough resources to start " + self.name + "! Go home..."
            self.timeLeft = 0
            return

        #create the stuff right away, so that resources are "reserved"
        #Don't give the results to the caller until duraton is passed
        for outputResource in self.outputs:
            createdOutput = ResourceFactory.CreateResource(outputResource, self.possession)
            self.createdOutputs.append(createdOutput)

'''
Occupation for a NPC. Can be used to generate the default action for the occupation to a schedule.
'''
class Occupation(object):
    def __init__(self):
        self.inputs = []
        self.outputs = []

    def __str__(self):
        return "Nothing"

    def AddDefaultSchedule(self, schedule, possession):
        pass

    def GetRequiredResources(self):
        return self.inputs

    def GetResourcesToBeProduced(self):
        return self.outputs

class Farmer(Occupation):
    duration = 7 * 60

    def __init__(self):
        self.inputs = []
        self.outputs = [Grain]

    def __str__(self):
        return "Farmer"

    def AddDefaultSchedule(self, schedule, possession):
        schedule.AddAction(Action("Farming", self.inputs, self.outputs, Farmer.duration, possession))

class Hunter(Occupation):
    duration = 4 * 60

    def __init__(self):
        self.inputs = []
        self.outputs = [Meat]

    def __str__(self):
        return "Hunter"

    def AddDefaultSchedule(self, schedule, possession):
        schedule.AddAction(Action("Hunting", self.inputs, self.outputs, Hunter.duration, possession))

class Brewer(Occupation):
    duration = 7 * 60

    def __init__(self):
        self.inputs = [Grain, Grain]
        self.outputs = [Beer]

    def __str__(self):
        return "Brewer"

    def AddDefaultSchedule(self, schedule, possession):
        schedule.AddAction(Action("Brewing beer", self.inputs, self.outputs, Brewer.duration, possession))

'''
Resource factory. All resources should be created through this factory class! Has a static method for
creating resources. When a resource is created, all the possible input resources are reduced from the
possession instance of the entity that is creating a new resource.
'''
class ResourceFactory(object):
    resourceCreatedSubscribers = []
    resourceDestroyedSubscribers = []

    def __init__(self):
        pass

    @staticmethod
    def CreateResource(target, possession):
        copyPossession = possession
        for resource in target.materials:
            found = False
            for posResource in possession.resources:
                if (isinstance(resource, type(posResource))):
                    possession.DestroyResource(posResource)
                    found = True
                    break;
            if not found:
                raise Exception("Could not create " + str(target) + ", not enough resources!!")
        print "New " + str(target) + " was created!"
        createdResource = target()
        ResourceFactory.OnResourceCreated(createdResource)
        return createdResource

    @staticmethod
    def DestroyResource(resource):
        ResourceFactory.OnResourceDestroyed(resource)

    @staticmethod
    def OnResourceCreated(resource):
        for subscriber in ResourceFactory.resourceCreatedSubscribers:
            subscriber.OnResourceCreated(resource)
    
    @staticmethod
    def OnResourceDestroyed(resource):
        for subscriber in ResourceFactory.resourceDestroyedSubscribers:
            subscriber.OnResourceDestroyed(resource)

class StockMarket(object):
    defaultPrice = 5
    initialMoney = 500

    def __init__(self):
        self.possession = Possession()
        self.prices = {}

        #get some initial cash from loan sharks :D
        self.LoanMoney(StockMarket.initialMoney)

    def LoanMoney(self, amount):
        #TODO: How the hell make this loan system...
        loanShark = Possession()
        loanShark.money = amount
        loanShark.GiveMoney(amount, self.possession)


    def GetPrice(self, resource):
        if type(resource) != type:
            resource = type(resource)
        if not resource in self.prices:
            self.prices[resource] = StockMarket.defaultPrice            
        return self.prices[resource]

    def SetPrice(self, resource, price):
        if type(resource) == type:
            self.prices[resource] = price
        else:
            self.prices[type(resource)] = price

    def FindResource(self, resourceType):
        return self.possession.GetResource(resourceType)

    def SellResource(self, resource, seller):
        if self.possession.GetMoney() < self.GetPrice(resource):
            return False
        seller.GiveResource(resource, self.possession)
        self.possession.GiveMoney(self.GetPrice(resource), seller)
        return True

    def BuyResource(self, resource, buyer):
        if buyer.GetMoney() < self.GetPrice(resource):
            return False
        if type(resource) == type:
            resource = self.FindResource(resource)
            if resource == None:
                return False
        self.possession.GiveResource(resource, buyer)
        buyer.GiveMoney(self.GetPrice(resource), self.possession)
        return True
                             

class Resource(object):
    def __init__(self):
        pass

class Grain(Resource):
    materials = []
    def __init__(self):
        Resource.__init__(self)

class FoodResource(Resource):
    pass

class Meat(FoodResource):
    nutritionalValue = 24 * 60 #one day energy
    materials = []
    def __init__(self):
        Resource.__init__(self)

class Beer(Resource):
    #nutritionalValue = 60 #one hour energy
    materials = [Grain(), Grain()]

    def __init__(self):
        Resource.__init__(self) 


