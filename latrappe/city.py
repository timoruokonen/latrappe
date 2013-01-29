
class City(object):
    def __init__(self, filename="level.map"):
        self.npcs = []
        self.stocks = []
        self.players = []
        self.animals = []
        self.filename = filename
        self.real_properties = []

    def add_npc(self, npc):
        npc.city = self
        self.npcs.append(npc)
        
        #TODO: add static real properties for now.
        for prop in npc.possession.get_real_properties():
            self.real_properties.append(prop)
 
    def add_stock_market(self, stock):
        self.stocks.append(stock)

    def add_player(self, player):
    	self.players.append(player)

    def add_animal(self, animal):
    	self.animals.append(animal)

    # TODO: Rethink this, for now just return always Player 1
    def get_controlled_player(self):
    	if (len(self.players) > 0):
    		return self.players[0]
    	return None


