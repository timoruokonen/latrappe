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


