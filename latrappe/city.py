
class City(object):
    def __init__(self, filename="level.map"):
        self.npcs = []
        self.stocks = []
        self.players = []
        self.filename = filename

    def add_npc(self, npc):
        npc.city = self
        self.npcs.append(npc)
 
    def add_stock_market(self, stock):
        self.stocks.append(stock)

    def add_player(self, player):
    	self.players.append(player)

    # TODO: Rethink this, for now just return always Player 1
    def get_controlled_player(self):
    	if (len(self.players) > 0):
    		return self.players[0]
    	return None


