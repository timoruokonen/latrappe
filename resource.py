'''
NOTICE!!

This piece of art is still totally under construction!! Don't look any further. All the classes are 
in the same file and contain whatever shiiiit :)
'''


'''
Handles ownings of an entity. Contains a list of resources and amount of money.
'''
class Possession(object):
    def __init__(self):
        self.resources = []
        self.money = 0

    def AddResource(self, resource):
        self.resources.append(resource)

    def RemoveResource(self, resource):
        #print "Removing " + str(resource)
        self.resources.remove(resource)

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


'''
Game NPC. Each NPC instance must be advanced when the game is advanced. 
'''
class Npc(object):
    def __init__(self, occupation):
        self.occupation = occupation
        self.schedule = Schedule()
        #TODO: Cannot think... just advance schedule so that it is already done when Advance is called the first time...
        self.schedule.Advance(Schedule.MaxTime)
        self.possession = Possession()
        self.hungerLevel = 100

    def printStatus(self):
        print "Npc (" + str(self.occupation) + ") has " + str(self.possession.money) + " money, owns:"
        for pos in self.possession.resources:
            print pos

    def Advance(self, time):
        if (self.schedule.IsDone()):
            #Day is completed, create new schedule
            self.CreateSchedule()
        self.schedule.Advance(time)

    def CreateSchedule(self):
        self.schedule = Schedule()
        self._AddDefaultActions()
        self.occupation.AddDefaultSchedule(self.schedule, self.possession)

    def _AddDefaultActions(self):
        self.schedule.AddAction(Action("Sleep", [],[], 7 * 60, self.possession))

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
        #TODO: Handle case where time goes beyond remaining time
        timeToSpend = min(time, self.totalRemainingTime)
        self.totalRemainingTime -= timeToSpend

        #advance current action and remove if completed
        action = self.GetCurrentAction()
        if (action != None):
            print "Advancing action " + action.name + ". Time left of day: " + str(self.totalRemainingTime)       
            action.Advance(timeToSpend)
            if (action.IsDone()):
                self._RemoveAction(action)
        else:
            print "Doing nothing..." + ". Time left of day: " + str(self.totalRemainingTime)

    def GetCurrentAction(self):
        if (len(self.actions) > 0):
            return self.actions[0]
        return None

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

    def IsDone(self):
        return self.timeLeft <= 0

    def _ReserveResourcesAndCreateOutputs(self):
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

class Farmer(Occupation):
    def __init__(self):
        self.inputs = []
        self.outputs = [Grain]

    def __str__(self):
        return "Farmer"

    def AddDefaultSchedule(self, schedule, possession):
        schedule.AddAction(Action("Farming", [],[Grain], 7 * 60, possession))

class Brewer(Occupation):
    def __init__(self):
        self.inputs = [Grain, Grain]
        self.outputs = [Beer]

    def __str__(self):
        return "Brewer"

    def AddDefaultSchedule(self, schedule, possession):
        schedule.AddAction(Action("Brewing beer", self.inputs, self.outputs, 7 * 60, possession))

'''
Resource factory. All resources should be created through this factory class! Has a static method for
creating resources. When a resource is created, all the possible input resources are reduced from the
possession instance of the entity that is creating a new resource.
'''
class ResourceFactory(object):
    def __init__(self):
        pass

    @staticmethod
    def CreateResource(target, possession):
        copyPossession = possession
        for resource in target.materials:
            found = False
            for posResource in possession.resources:
                if (isinstance(resource, type(posResource))):
                    possession.RemoveResource(posResource)
                    found = True
                    break;
            if not found:
                raise Exception("Could not create " + str(target) + ", not enough resources!!")
        print "New " + str(target) + " was created!"
        return target()
                     

class Resource(object):
    def __init__(self):
        pass

class Grain(Resource):
    materials = []
    def __init__(self):
        Resource.__init__(self)

class Meat(Resource):
    materials = []
    def __init__(self):
        Resource.__init__(self)

class Beer(Resource):
    materials = [Grain(), Grain()]

    def __init__(self):
        Resource.__init__(self) 


