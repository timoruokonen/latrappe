from resource import *
from resourcefactory import ResourceFactory

'''
Handles ownings of an entity. Contains a list of resources and amount of money.
'''
class Possession(object):
    def __init__(self):
        self._resource_heaps = {}
        self._money = 0
        self._real_properties = []

    def add_real_property(self, property):
        self._real_properties.append(property)

    def get_real_property(self, property):
        if type(property) != type:
            if property in self._real_properties:
                return property
            return None
        
        for prop in self._real_properties:
            if type(prop) == property:
                return prop
        return None

    def get_real_properties(self):
        return self._real_properties
            

    def add_resource(self,  resource):
        self._get_resource_heap(resource).add(resource)

    def destroy_resource(self, resource):
        #print "Removing " + str(resource)
        self._get_resource_heap(resource).remove(resource)
        ResourceFactory.on_resource_destroyed(resource)

    def give_resource(self, resource, new_owner):
        #verify that owner has the given instance or resource type
        heap_giver = self._get_resource_heap(resource)
        res = heap_giver.get(resource) 
        if res == None:
            return False

        heap_giver.remove(res)
        new_owner._get_resource_heap(resource).add(res)
        return True

    def get_resource_types(self):
        types = []
        for heap in self._resource_heaps.values():
            if heap.count > 0:
                types.append(heap.resource_type)
        return types

    def get_resource(self, resource):
        heap = self._get_resource_heap(resource) 
        return heap.get(resource)

    def get_resource_count(self, resource):
        return self._get_resource_heap(resource).count

    def has_resources(self, resources):
        handled_res_types = []
        for res_type in resources:
            if res_type in handled_res_types:
                continue

            heap = self._get_resource_heap(res_type) 
            if heap.count < resources.count(res_type):
                return False

            handled_res_types.append(res_type)
        return True

    def get_missing_resources(self, resources):
        missing = []
        handled_res_types = []
        for res_type in resources:
            if res_type in handled_res_types:
                continue
            heap = self._get_resource_heap(res_type) 
            for i in range(max(0, resources.count(res_type) - heap.count)): 
                missing.append(res_type)
            handled_res_types.append(res_type)
        return missing


    def get_foods(self):
        foods = []
        for heap in self._resource_heaps.values():
            if (issubclass(heap.resource_type, FoodResource)):
                foods.extend(heap.get_all())
        return foods    

    def get_all(self):
        resources = []
        for heap in self._resource_heaps.values():
            resources.extend(heap.get_all())
        return resources   

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


    def _get_resource_heap(self, resource):
        if type(resource) != type:
            resource = type(resource)
        if not resource in self._resource_heaps.keys():
            self._resource_heaps[resource] = ResourceHeap(resource)
        return self._resource_heaps[resource]
    

