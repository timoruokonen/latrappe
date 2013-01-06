
class City(object):
    def __init__(self, filename="level.map"):
        self.npcs = []
        self.stocks = []
        self.filename = filename

    def add_npc(self, npc):
        npc.city = self
        self.npcs.append(npc)

    def get_npcs(self):
        return self.npcs
    
    def add_stock_market(self, stock):
        self.stocks.append(stock)

    def get_stock_markets(self):
        return self.stocks


