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
        
        for npc_section in parser.sections():
            occupation = self._get_occupation_type(parser.get(npc_section, 'occupation'))
            home_x = int(parser.get(npc_section, 'home_x'))
            home_y = int(parser.get(npc_section, 'home_y'))
            x = int(parser.get(npc_section, 'x'))
            y = int(parser.get(npc_section, 'y'))
            money = int(parser.get(npc_section, 'money'))
            strategy = self._get_strategy_type(parser.get(npc_section, 'strategy'))

            npc = Npc(occupation(), npc_section);
            npc.home_x = home_x
            npc.home_y = home_y
            npc.x = x
            npc.y = y
            npc.possession._set_money(money)
            npc.strategy = strategy(npc)

            city.add_npc(npc)

        return city

    def _get_occupation_type(self, occupation_str):
        if (occupation_str == 'Brewer'):
            return Brewer
        if (occupation_str == 'Farmer'):
            return Farmer
        if (occupation_str == 'Hunter'):
            return Hunter

    def _get_strategy_type(self, strategy_str):
        if (strategy_str == 'NpcStrategySimpleGreedy'):
            return NpcStrategySimpleGreedy


            
                
