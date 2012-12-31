from possession import Possession

class StockMarket(object):
    defaultPrice = 5
    initialMoney = 500

    def __init__(self):
        self.possession = Possession()
        self.prices = {}

        #get some initial cash from loan sharks :D
        self.LoanMoney(StockMarket.initialMoney)

    def LoanMoney(self, amount):
        #TODO: How the hell make this loan system...
        loanShark = Possession()
        loanShark.money = amount
        loanShark.GiveMoney(amount, self.possession)


    def GetPrice(self, resource):
        if type(resource) != type:
            resource = type(resource)
        if not resource in self.prices:
            self.prices[resource] = StockMarket.defaultPrice            
        return self.prices[resource]

    def SetPrice(self, resource, price):
        if type(resource) == type:
            self.prices[resource] = price
        else:
            self.prices[type(resource)] = price

    def FindResource(self, resourceType):
        return self.possession.GetResource(resourceType)

    def SellResource(self, resource, seller):
        if self.possession.GetMoney() < self.GetPrice(resource):
            return False
        seller.GiveResource(resource, self.possession)
        self.possession.GiveMoney(self.GetPrice(resource), seller)
        return True

    def BuyResource(self, resource, buyer):
        if buyer.GetMoney() < self.GetPrice(resource):
            print "Buyer has not enough money"
            return False
        if type(resource) == type:
            resource = self.FindResource(resource)
            if resource == None:
                print "Stock has not required resource"
                return False
        self.possession.GiveResource(resource, buyer)
        buyer.GiveMoney(self.GetPrice(resource), self.possession)
        return True

