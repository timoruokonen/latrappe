import ConfigParser
from city import City
from occupation import *
from npcstrategy import *

class Loader(object):

    def __init__(self):
        pass

    def load_city(self, filename):
        parser = ConfigParser.ConfigParser()
        parser.read(filename)
        city = City()
        
        for section in parser.sections():
            if parser.get(section, 'type') == 'npc':
                city.add_npc(self._create_npc(section, parser))
            elif parser.get(section, 'type') == 'stock':
                city.add_stock_market(self._create_stock(section, parser))
        return city

    def _create_npc(self, npc_section, parser):
        occupation = eval(parser.get(npc_section, 'occupation'))
        home_x = int(parser.get(npc_section, 'home_x'))
        home_y = int(parser.get(npc_section, 'home_y'))
        x = int(parser.get(npc_section, 'x'))
        y = int(parser.get(npc_section, 'y'))
        money = int(parser.get(npc_section, 'money'))
        strategy = eval(parser.get(npc_section, 'strategy'))

        npc = Npc(occupation(), npc_section);
        npc.home_x = home_x
        npc.home_y = home_y
        npc.x = x
        npc.y = y
        npc.possession._set_money(money)
        npc.strategy = strategy(npc)
        return npc
    
    def _create_stock(self, stock_section, parser):
        x = int(parser.get(stock_section, 'x'))
        y = int(parser.get(stock_section, 'y'))
        money = int(parser.get(stock_section, 'money'))

        stock = StockMarket();
        stock.x = x
        stock.y = y
        stock.possession._set_money(money)
        prices = parser.get(stock_section, 'prices').split('\n') 
        for price in prices:
            if not ':' in price:
                continue
            resource_type = eval(price.split(':')[0])
            resource_price = int(price.split(':')[1])
            stock.set_price(resource_type, resource_price)

        resources = parser.get(stock_section, 'resources').split('\n') 
        for resource in resources:
            if not ':' in resource:
                continue
            resource_type = eval(resource.split(':')[0])
            resource_count = int(resource.split(':')[1])
            for i in range(resource_count):
                stock.possession.add_resource(
                    ResourceFactory.create_resource_from_nothing(resource_type, stock.possession))
        return stock
         
                
