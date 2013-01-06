from resource import *
from resourcefactory import ResourceFactory

'''
Handles ownings of an entity. Contains a list of resources and amount of money.
'''
class Possession(object):
    def __init__(self):
        self.resources = []
        self._money = 0

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

    def get_resource_types(self):
        types = []
        for res in self.resources:
            if type(res) in types:
                continue
            types.append(type(res))
        return types

    def get_resource(self, resource):
        if type(resource) == type:
            for res in self.resources:
                if (isinstance(res, resource)):
                    return res
        if resource in self.resources:
            return resource
        return None

    def get_resource_count(self, resource):
        count = 0
        for res in self.resources:
            if isinstance(res, resource):
                count += 1
        return count

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
                    break
            if not found:
                return False
        return True

    def get_foods(self):
        foods = []
        for resource in self.resources:
            if (isinstance(resource, FoodResource)):
                foods.append(resource)
        return foods    

    @property
    def money(self):
        return self._money

    @money.setter
    def money(self, value):
        raise Exception("Money setter is not allowed")

    #TODO: Decide how to set money in tests/stock initialization etc. Now direct setter is not allowed
    #but those cases use this private setter...
    def _set_money(self, money):
        self._money = money

    def give_money(self, amount, newOwner):
        if amount > self._money:
            return False
        self._money -= amount
        newOwner._money += amount

