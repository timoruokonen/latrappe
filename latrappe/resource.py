class Resource(object):
    def __init__(self):
        self.needs_advancing = False

    def advance(self, time):
        pass

class ResourceHeap(object):
    def __init__(self, resource_type):
        if type(resource_type) != type or not issubclass(resource_type, Resource):
            raise Exception("Resource heap type must be Resource!")

        self.resource_type = resource_type
        self._resources = []

    @property
    def count(self):
        return len(self._resources)
    
    def add(self, resource):
        if not type(resource) == self.resource_type:
            raise Exception("Tried to add a wrong type of resource to a resouce heap. Heap: ", self.resource_type, ", Res: ", resource)
        self._resources.append(resource)

    def remove(self, resource):
        if type(resource) == type:
            if len(self._resources) > 0:
                return self._resources.pop()
        else:
            if resource in self._resources:
                self._resources.remove(resource)
                return resource
        return None

    def get(self, resource):
        if type(resource) == type:
            if resource == self.resource_type and len(self._resources) > 0:
                return self._resources[0]
            return None 
        if resource in self._resources:
            return resource
        return None

    def get_all(self):
        return self._resources
    
class Grain(Resource):
    materials = []
    def __init__(self):
        Resource.__init__(self)

class FoodResource(Resource):
    pass

class Meat(FoodResource):
    NUTRITIONAL_VALUE = 24 * 60 #one day energy
    materials = []
    def __init__(self):
        Resource.__init__(self)

class Beer(Resource):
    #NUTRITIONAL_VALUE = 60 #one hour energy
    materials = [Grain, Grain]

    def __init__(self):
        Resource.__init__(self) 

class ResourceContainer(Resource):
    def __init__(self):
        Resource.__init__(self) 

class FieldSquare(ResourceContainer):
    PLOUGHT_DURATION = 8 * 60
    SOWING_DURATION = 8 * 60
    GROWTH_DURATION = 24 * 60 * 2 #two days 
    HARVEST_DURATION = 8 * 60
        
    STATUS_PLOUGHED = 1
    STATUS_SOWED = 2
    STATUS_READY_TO_BE_HARVESTED = 3
    STATUS_HARVESTED = 4

    SOWING_INPUTS = [Grain]
    HARVEST_OUTPUTS = [Grain, Grain, Grain]

    def __init__(self):
        ResourceContainer.__init__(self)
        self.needs_advancing = True
        self.status = FieldSquare.STATUS_HARVESTED
        self.started = False
        self.remaining_time = 0
        self.x = 0
        self.y = 0

    def get_action_duration(self, target_status):
        if target_status == FieldSquare.STATUS_PLOUGHED:
            return FieldSquare.PLOUGHT_DURATION
        if target_status == FieldSquare.STATUS_SOWED:
            return FieldSquare.SOWING_DURATION
        if target_status == FieldSquare.STATUS_READY_TO_BE_HARVESTED:
            return FieldSquare.GROWTH_DURATION
        if target_status == FieldSquare.STATUS_HARVESTED:
            return FieldSquare.HARVEST_DURATION







