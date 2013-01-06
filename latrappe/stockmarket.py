from possession import Possession

class StockMarket(object):
    DEFAULT_PRICE = 5
    INITIAL_MONEY = 500

    def __init__(self):
        self.possession = Possession()
        self.prices = {}
        self.x = 0
        self.y = 0

        #get some initial cash from loan sharks :D
        self.loan_money(StockMarket.INITIAL_MONEY)

    def loan_money(self, amount):
        #TODO: How the hell make this loan system...
        loanShark = Possession()
        loanShark.money = amount
        loanShark.give_money(amount, self.possession)

    def get_price(self, resource):
        if type(resource) != type:
            resource = type(resource)
        if not resource in self.prices:
            self.prices[resource] = StockMarket.DEFAULT_PRICE            
        return self.prices[resource]

    def set_price(self, resource, price):
        if type(resource) == type:
            self.prices[resource] = price
        else:
            self.prices[type(resource)] = price

    def find_resource(self, resourceType):
        return self.possession.get_resource(resourceType)

    def sell_resource(self, resource, seller):
        if self.possession.get_money() < self.get_price(resource):
            return False
        seller.give_resource(resource, self.possession)
        self.possession.give_money(self.get_price(resource), seller)
        return True

    def buy_resource(self, resource, buyer):
        if buyer.get_money() < self.get_price(resource):
            print "Buyer has not enough money"
            return False
        if type(resource) == type:
            resource = self.find_resource(resource)
            if resource == None:
                print "Stock has not required resource"
                return False
        self.possession.give_resource(resource, buyer)
        buyer.give_money(self.get_price(resource), self.possession)
        return True

