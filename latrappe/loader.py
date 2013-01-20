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

    def save_city(self, city, filename):
        parser = ConfigParser.ConfigParser()
        for npc in city.npcs:
            parser.add_section(npc.name)
            parser.set(npc.name, 'type', 'npc')
            parser.set(npc.name, 'occupation', type(npc.occupation).__name__)
            parser.set(npc.name, 'home_x', str(npc.home_x))
            parser.set(npc.name, 'home_y', str(npc.home_y))
            parser.set(npc.name, 'x', str(npc.x))
            parser.set(npc.name, 'y', str(npc.y))
            parser.set(npc.name, 'money', str(npc.possession.money))
            parser.set(npc.name, 'strategy', type(npc.strategy).__name__)

        for stock in city.stocks:
            parser.add_section(stock.name)
            parser.set(stock.name, 'type', 'stock')
            parser.set(stock.name, 'x', str(stock.x))
            parser.set(stock.name, 'y', str(stock.y))
            parser.set(stock.name, 'money', str(stock.possession.money))
            
            #Store prices. Get all subclasses of Resource
            #TODO: Now it also saves "grouping" classes like FoodResource
            prices = "\n"
            resource_types = self._itersubclasses(Resource)
            for resource_type in resource_types:
                prices += resource_type.__name__ + ": " + str(stock.get_price(resource_type)) + '\n'
            parser.set(stock.name, 'prices', prices)

            #store stock's resources
            resources = "\n"
            resource_types = stock.possession.get_resource_types()
            for resource_type in resource_types:
                resources += resource_type.__name__ + ": " + str(stock.possession.get_resource_count(resource_type)) + '\n'
            parser.set(stock.name, 'resources', resources)

        with open(filename, 'wb') as configfile:
            parser.write(configfile)

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
        stock.name = stock_section
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
         
    def _itersubclasses(self, cls, _seen=None):
        if not isinstance(cls, type):
            raise TypeError('not a class')
        if _seen is None: _seen = set()
        try:
            subs = cls.__subclasses__()
        except TypeError: # fails only when cls is type
            subs = cls.__subclasses__(cls)
        for sub in subs:    
            if sub not in _seen:
                _seen.add(sub)
                yield sub
                for sub in self._itersubclasses(sub, _seen):
                    yield sub

                
