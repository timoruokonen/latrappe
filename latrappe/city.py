
class City(object):
    def __init__(self, filename="level.map"):
        self.npcs = []
        self.stocks = []
        self.filename = filename

    def AddNpc(self, npc):
        npc.SetCity(self)
        self.npcs.append(npc)

    def GetNpcs(self):
        return self.npcs
    
    def AddStockMarket(self, stock):
        self.stocks.append(stock)

    def GetStockMarkets(self):
        return self.stocks


