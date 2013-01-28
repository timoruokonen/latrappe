import ConfigParser
from city import City
from occupation import *
from npcstrategy import *

'''
Loader for the LaTrappe. Can be used to save and load game state.
Currently implements serialization and deserialization by using Python's config files.
'''
class Loader(object):

    def __init__(self):
        pass

    '''
    Loads a city instance from the given filename.
    '''
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

    '''
    Saves the given city instance to the given file.
    '''
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
            #store npc's resources
            self._add_resources_option(npc.possession, npc.name, parser)
            self._add_real_properties_option(npc.possession, npc.name, parser)
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
            self._add_resources_option(stock.possession, stock.name, parser)

        with open(filename, 'wb') as configfile:
            parser.write(configfile)

    def _add_resources_option(self, possession, section, parser):
        resources = "\n"
        resource_types = possession.get_resource_types()
        if len(resource_types) == 0:
            return
        for resource_type in resource_types:
            resources += resource_type.__name__ + ": " + str(possession.get_resource_count(resource_type)) + '\n'
        parser.set(section, 'resources', resources)

    def _add_real_properties_option(self, possession, section, parser):
        properties = "\n"
        for prop in possession.get_real_properties():
            #TODO: real properties now stored as invidual lines
            properties += type(prop).__name__ + ': ' + str(prop.x) + ': ' + str(prop.y) + '\n'
        parser.set(section, 'real_properties', properties)

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
        self._add_resources(npc.possession, npc_section, parser)
        self._add_real_properties(npc.possession, npc_section, parser)
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

        self._add_resources(stock.possession, stock_section, parser)
        return stock
        
    def _add_resources(self, possession, section, parser):
        if not parser.has_option(section, 'resources'):
            return 

        resources = parser.get(section, 'resources').split('\n') 
        for resource in resources:
            if not ':' in resource:
                continue
            resource_type = eval(resource.split(':')[0])
            resource_count = int(resource.split(':')[1])
            for i in range(resource_count):
                possession.add_resource(
                    ResourceFactory.create_resource_from_nothing(resource_type))
         
    def _add_real_properties(self, possession, section, parser):
        if not parser.has_option(section, 'real_properties'):
            return 

        properties = parser.get(section, 'real_properties').split('\n') 
        for property in properties:
            if not ':' in property:
                continue
            property_type = eval(property.split(':')[0])
            x = int(property.split(':')[1])
            y = int(property.split(':')[2])
            prop = ResourceFactory.create_resource_from_nothing(property_type)
            prop.x = x
            prop.y = y
            possession.add_real_property(prop)

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

                
