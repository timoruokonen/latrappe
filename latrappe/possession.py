from resource import *
from resourcefactory import ResourceFactory

'''
Handles ownings of an entity. Contains a list of resources and amount of money.
'''
class Possession(object):
    def __init__(self):
        self.resources = []
        self.money = 0

    def add_resource(self, resource):
        self.resources.append(resource)

    def destroy_resource(self, resource):
        #print "Removing " + str(resource)
        self.resources.remove(resource)
        ResourceFactory.on_resource_destroyed(resource)

    def give_resource(self, resource, new_owner):
        #verify that owner has the given instance or resource type 
        res = self.get_resource(resource)
        if res == None:
            return False

        self.resources.remove(res)
        new_owner.resources.append(res)
        return True

    def get_resource(self, resource):
        if type(resource) == type:
            for res in self.resources:
                if (isinstance(res, resource)):
                    return res
        if resource in self.resources:
            return resource
        return None

    def has_resources(self, resources):
        used_resources = []
        for input_resource in resources:
            found = False
            for resource in self.resources:
                if (resource in used_resources):
                    continue
                if (isinstance(resource, input_resource)):
                    used_resources.append(resource)
                    found = True
                    break;
            if not found:
                return False
        return True

    def get_foods(self):
        foods = []
        for resource in self.resources:
            if (isinstance(resource, FoodResource)):
                foods.append(resource)
        return foods

    def get_money(self):
        return self.money;

    def give_money(self, amount, newOwner):
        if amount > self.money:
            return False
        self.money -= amount
        newOwner.money += amount

