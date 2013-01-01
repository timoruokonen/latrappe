from resource import *
from resourcefactory import ResourceFactory

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
        ResourceFactory.OnResourceDestroyed(resource)

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

