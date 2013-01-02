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
    NUTRITIONAL_VALUE = 24 * 60 #one day energy
    materials = []
    def __init__(self):
        Resource.__init__(self)

class Beer(Resource):
    #NUTRITIONAL_VALUE = 60 #one hour energy
    materials = [Grain(), Grain()]

    def __init__(self):
        Resource.__init__(self) 


