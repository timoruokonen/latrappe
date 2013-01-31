
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

class Water(Resource):
    def __init__(self):
        Resource.__init__(self) 

class ProduceUnit(Resource):

    def __init__(self):
        Resource.__init__(self)
        self.status = 0
        self.x = 0
        self.y = 0
        self.in_progress = False
        self._states = []
        self._total_inputs = []

    @property
    def states(self):
        return self._states

    @states.setter
    def states(self, value):
        self._states = value
        for state in self._states:
            self._total_inputs.extend(state['inputs'])

    def next_status(self):
        if self.status == len(self._states) - 1:
            return 0
        return self.status + 1

    def name(self, status):
        return self._states[status]['name']

    def duration(self, status):
        return self._states[status]['duration']

    def inputs(self, status):
        return self._states[status]['inputs']

    def outputs(self, status):
        return self._states[status]['outputs']

    def total_inputs(self):
        print str(self._total_inputs) 
        return self._total_inputs

    def final_outputs(self):
        return self._states[len(self._states) - 1]['outputs']

    def needs_presence(self, status):
        return self._states[status]['needs_presence']


class FieldSquare(ProduceUnit): 
    STATUS_PLOUGHED = 0
    STATUS_SOWED = 1
    STATUS_READY_TO_BE_HARVESTED = 2
    STATUS_HARVESTED = 3

    STATES = [
        {'name': 'Plowing',
        'duration': 8 * 60,
        'inputs': [],
        'outputs': [],
        'needs_presence': True
        },
        {'name': 'Sowing',
        'duration': 8 * 60,
        'inputs': [Grain],
        'outputs': [],
        'needs_presence': True
        },
        {'name': 'Growing',
        'duration': 24 * 60 * 2,
        'inputs': [],
        'outputs': [],
        'needs_presence': False
        },
        {'name': 'Harvesting',
        'duration': 8 * 60,
        'inputs': [],
        'outputs': [Grain, Grain, Grain],
        'needs_presence': True
        }]
    
    def __init__(self):
        ProduceUnit.__init__(self)
        self.states = FieldSquare.STATES
        self.status = FieldSquare.STATUS_HARVESTED

class BeerKettle(ProduceUnit):
    STATUS_MALTED = 0
    STATUS_MASHED = 1
    STATUS_BOILED = 2
    STATUS_FERMENTED = 3
    STATUS_CONDITIONED = 4
    STATUS_PACKAGED = 5

    STATES = [
        {'name': 'Malting',
        'duration': 8 * 60,
        'inputs': [Grain],
        'outputs': [],
        'needs_presence': True
        },
        {'name': 'Mashing',
        'duration': 8 * 60,
        'inputs': [],
        'outputs': [],
        'needs_presence': True
        },
        {'name': 'Boiling',
        'duration': 8 * 60,
        'inputs': [Water],
        'outputs': [],
        'needs_presence': True
        },
        {'name': 'Fermentation',
        'duration': 24 * 60 * 2,
        'inputs': [],
        'outputs': [],
        'needs_presence': False
        },
        {'name': 'Conditioning',
        'duration': 8 * 60,
        'inputs': [],
        'outputs': [],
        'needs_presence': True
        },
        {'name': 'Packaging',
        'duration': 8 * 60,
        'inputs': [],
        'outputs': [Beer, Beer, Beer, Beer, Beer, Beer, Beer],
        'needs_presence': True
        },
        ]

    def __init__(self):
        ProduceUnit.__init__(self)
        self.states = BeerKettle.STATES
        self.status = BeerKettle.STATUS_PACKAGED



