from latrappe import *
import unittest 

#Instructions to execute only one tests:
#python -m unittest tests.TestSequenceFunctions.test_simple_npc_strategy_bartender


class TestSequenceFunctions(unittest.TestCase):
    advanceInterval = 1

    def setUp(self):
        self.grainDefaultPrice = 15
        self.meatDefaultPrice = 20
        self.beerDefaultPrice = 50
        self.waterDefaultPrice = 1
        pass

    def AdvanceNpc(self, npc, amount):
        while (amount > 0):
            advanceAmount = min(TestSequenceFunctions.advanceInterval, amount)
            npc.advance(advanceAmount)
            amount -= advanceAmount

    def AdvanceGame(self, npc, amount):
        while (amount > 0):
            advanceAmount = min(TestSequenceFunctions.advanceInterval, amount)
            npc.advance(advanceAmount)
            Scheduler.instance().advance(advanceAmount)
            amount -= advanceAmount
    
    
    def SetDefaultPrices(self, stock):
        stock.set_price(Grain, self.grainDefaultPrice)
        stock.set_price(Meat, self.meatDefaultPrice)
        stock.set_price(Beer, self.beerDefaultPrice)
        stock.set_price(Water, self.waterDefaultPrice) #TODO: Remove water from stock...

    
    def test_farmer_creates_grain(self):
        npc = Npc(Farmer())
        npc.food_consumption = 0 #lets not worry about food in this test
        field = ResourceFactory.create_resource_from_nothing(FieldSquare)
        npc.possession.add_real_property(field)
        npc.possession.add_resource(Grain()) #one grain for sowing
        self.assertEqual(1, len(npc.possession.get_all()))

        #plow field
        self.AdvanceGame(npc, Schedule.MAX_TIME)
        self.assertEqual(FieldSquare.STATUS_PLOUGHED, field.status)        
        self.assertEqual(1, len(npc.possession.get_all()))
        
        #sow field
        self.AdvanceGame(npc, Schedule.MAX_TIME)
        self.assertEqual(FieldSquare.STATUS_SOWED, field.status)        
        self.assertEqual(0, len(npc.possession.get_all()))

        #waiting to grow
        self.AdvanceGame(npc, Schedule.MAX_TIME * 2)
        self.assertEqual(FieldSquare.STATUS_READY_TO_BE_HARVESTED, field.status)        
        self.assertEqual(0, len(npc.possession.get_all()))

        #harvest field
        self.AdvanceGame(npc, Schedule.MAX_TIME)
        self.assertEqual(FieldSquare.STATUS_HARVESTED, field.status)        
        self.assertEqual(3, len(npc.possession.get_all()))
        self.assertTrue(npc.possession.has_resources([Grain, Grain, Grain]))

        #next crop 
        self.AdvanceGame(npc, Schedule.MAX_TIME * 5)
        self.assertEqual(5, len(npc.possession.get_all()))
        self.assertTrue(npc.possession.has_resources([Grain, Grain, Grain, Grain, Grain]))

    def test_hunter_creates_meat(self):
        npc = Npc(Hunter())
        self.assertEqual(0, len(npc.possession.get_all()))
        self.AdvanceNpc(npc, Npc.SLEEP_DURATION) #sleeping time
        self.AdvanceNpc(npc, Hunter.DURATION) #action time
        self.assertEqual(2, len(npc.possession.get_all()))
        self.assertTrue(npc.possession.has_resources([Meat]))
    
    def test_brewer_creates_beer(self):
        npc = Npc(Brewer())
        kettle = ResourceFactory.create_resource_from_nothing(BeerKettle)
        npc.possession.add_real_property(kettle)

        npc.food_consumption = 0 #lets not worry about food in this test
        npc.possession.add_resource(Grain())
        npc.possession.add_resource(Water())
        self.assertEqual(2, len(npc.possession.get_all()))

        #malting
        self.AdvanceGame(npc, Schedule.MAX_TIME)
        self.assertEqual(1, len(npc.possession.get_all()))
        self.assertEqual(BeerKettle.STATUS_MALTED, kettle.status)        

        #mashing
        self.AdvanceGame(npc, Schedule.MAX_TIME)
        self.assertEqual(1, len(npc.possession.get_all()))
        self.assertEqual(BeerKettle.STATUS_MASHED, kettle.status)        

        #boiling
        self.AdvanceGame(npc, Schedule.MAX_TIME)
        self.assertEqual(0, len(npc.possession.get_all()))
        self.assertEqual(BeerKettle.STATUS_BOILED, kettle.status)        

        #fermentation
        self.AdvanceGame(npc, Schedule.MAX_TIME * 2)
        self.assertEqual(0, len(npc.possession.get_all()))
        self.assertEqual(BeerKettle.STATUS_FERMENTED, kettle.status)        

        #conditioning
        self.AdvanceGame(npc, Schedule.MAX_TIME)
        self.assertEqual(0, len(npc.possession.get_all()))
        self.assertEqual(BeerKettle.STATUS_CONDITIONED, kettle.status)        

        #packaging
        self.AdvanceGame(npc, Schedule.MAX_TIME)
        self.assertEqual(BeerKettle.STATUS_PACKAGED, kettle.status)         
        self.assertEqual(len(kettle.outputs(BeerKettle.STATUS_PACKAGED)), npc.possession.get_resource_count(Beer))

        #start next round and give more resources (one extra grain)
        npc.possession.add_resource(Grain())
        npc.possession.add_resource(Water())
        self.AdvanceGame(npc, Schedule.MAX_TIME * 7)
        self.assertEqual(len(kettle.outputs(BeerKettle.STATUS_PACKAGED)) * 2, npc.possession.get_resource_count(Beer))

    
    def test_action_outputs_are_given_after_task_is_fully_done(self):
        npc = Npc(Hunter())
        self.assertEqual(0, len(npc.possession.get_all()))
        self.AdvanceNpc(npc, Npc.SLEEP_DURATION) #sleeping time
        self.AdvanceNpc(npc, Hunter.DURATION / 2) #half of the action time
        self.assertEqual(0, len(npc.possession.get_all()))
        self.AdvanceNpc(npc, Hunter.DURATION / 2) #half of the action time
        self.assertEqual(2, len(npc.possession.get_all()))
        self.assertTrue(npc.possession.has_resources([Meat]))


    def test_brewer_cannot_brew_when_out_of_resources(self):
        npc = Npc(Brewer())
        #brewing needs to grains, only one is given       
        npc.possession.add_resource(Grain())
        self.AdvanceNpc(npc, Npc.SLEEP_DURATION) #sleeping time
        self.AdvanceNpc(npc, Brewer.DURATION) #brewing time
        self.assertEqual(1, len(npc.possession.get_all()))
        self.assertTrue(npc.possession.has_resources([Grain]))

    def test_advance_over_one_action(self):
        npc = Npc(Hunter())
        self.assertEqual(0, len(npc.possession.get_all()))
        #advance one full day, both sleeping and farming should be done       
        self.AdvanceNpc(npc, Schedule.MAX_TIME)
        self.assertEqual(len(npc.occupation.outputs), len(npc.possession.get_all()))
        self.assertTrue(npc.possession.has_resources(npc.occupation.outputs))

    def test_advance_over_day_ending(self):
        npc = Npc(Hunter())
        npc.food_consumption = 0 #lets not worry about food in this test
        self.assertEqual(0, len(npc.possession.get_all()))
        #advance two full days, two sleepings and farmings should be done       
        self.AdvanceNpc(npc, Schedule.MAX_TIME * 2)
        self.assertEqual(len(npc.occupation.outputs) * 2, len(npc.possession.get_all()))
        outputs = []
        outputs.extend(npc.occupation.outputs)
        outputs.extend(npc.occupation.outputs)
        self.assertTrue(npc.possession.has_resources(outputs))

    def test_npc_eats(self):
        npc = Npc(Farmer())
        #npc has food for one day by default
        self.AdvanceNpc(npc, Schedule.MAX_TIME)
        self.assertEqual(0, len(npc.possession.get_all()))
        
        #give foor for the next day and check that it is consumed
        npc.possession.add_resource(Meat())
        self.AdvanceNpc(npc, Schedule.MAX_TIME)
        self.assertEqual(0, len(npc.possession.get_all()))

    def test_npc_dies_with_hunger(self):
        npc = Npc(Farmer())
        #npc has food for one day by default
        self.AdvanceNpc(npc, Schedule.MAX_TIME)
        self.assertEqual(0, len(npc.possession.get_all()))
        self.assertTrue(npc.alive)
        
        #don't give more food so npc should die
        self.AdvanceNpc(npc, Schedule.MAX_TIME)
        self.assertEqual(0, len(npc.possession.get_all())) #couldn't farm anymore
        self.assertFalse(npc.alive)

    def test_npc_produces_the_food_it_needs_next_day(self):
        npc = Npc(Hunter())
        #npc has food for one day by default and produces two foods per day (one day ration)
        #so npc is self contained, advance one week. 
        self.AdvanceNpc(npc, Schedule.MAX_TIME * 7)
        self.assertEqual(8, len(npc.possession.get_all()))
        self.assertTrue(npc.possession.has_resources([Meat]))
        self.assertTrue(npc.alive)
        #starting of next day, npc should have to eat the meat it produced last day       
        self.AdvanceNpc(npc, Schedule.MAX_TIME / 4)
        self.assertEqual(7, len(npc.possession.get_all()))
        self.assertTrue(npc.alive)

    def test_stock_prices(self):
        stock = StockMarket()
        #set/get using class
        stock.set_price(Grain, 20)
        self.assertEqual(20, stock.get_price(Grain))
        #set/get using instances
        stock.set_price(Beer(), 200)
        self.assertEqual(200, stock.get_price(Beer()))
        #set prices again
        stock.set_price(Grain, 15)
        stock.set_price(Beer(), 203)
        self.assertEqual(15, stock.get_price(Grain))
        self.assertEqual(203, stock.get_price(Beer()))

    def test_player_sells_resources(self):
        stock = StockMarket()
        self.SetDefaultPrices(stock)
        npc = Npc(Brewer())
        beer = Beer()
        npc.possession.add_resource(beer)
        self.assertEqual(0, npc.possession.money)
        self.assertEqual(None, stock.find_resource(Beer))
        self.assertTrue(stock.sell_resource(beer, npc.possession)) 
        self.assertEqual(0, len(npc.possession.get_all()))
        self.assertEqual(self.beerDefaultPrice, npc.possession.money) 
        self.assertEqual(1, len(stock.possession.get_all()))
        self.assertTrue(stock.possession.has_resources([Beer]))
        self.assertEqual(beer, stock.find_resource(Beer))

    def test_player_buys_resources(self):
        stock = StockMarket()
        self.SetDefaultPrices(stock)
        stock.possession.add_resource(Meat())
        stock.possession.add_resource(Beer())
        stock.possession.add_resource(Grain())
        
        npc = Npc(Brewer())
        money = 100
        npc.possession._set_money(money)
        self.assertEqual(money, npc.possession.money)
        self.assertEqual(StockMarket.INITIAL_MONEY, stock.possession.money)
        #buy with type
        self.assertTrue(stock.buy_resource(Beer, npc.possession)) 
        self.assertEqual(1, len(npc.possession.get_all()))
        self.assertTrue(npc.possession.has_resources([Beer]))
        self.assertEqual(money - self.beerDefaultPrice, npc.possession.money) 
        self.assertEqual(StockMarket.INITIAL_MONEY + self.beerDefaultPrice, stock.possession.money) 
        self.assertEqual(2, len(stock.possession.get_all()))
        self.assertFalse(stock.possession.has_resources([Beer]))
        self.assertTrue(stock.possession.has_resources([Meat, Grain]))
        #buy with instance
        grain = stock.find_resource(Grain)
        self.assertTrue(stock.buy_resource(grain, npc.possession)) 
        self.assertEqual(2, len(npc.possession.get_all()))
        self.assertTrue(npc.possession.has_resources([Grain, Beer]))
        self.assertEqual(money - self.beerDefaultPrice - self.grainDefaultPrice, npc.possession.money) 
        self.assertEqual(StockMarket.INITIAL_MONEY + self.beerDefaultPrice + self.grainDefaultPrice, stock.possession.money) 
        self.assertEqual(1, len(stock.possession.get_all()))
        self.assertFalse(stock.possession.has_resources([Grain]))
        self.assertTrue(stock.possession.has_resources([Meat]))

    def test_city_with_npcs_and_stock_markets(self):
        city = City()
        self.assertEqual(0, len(city.npcs))
        self.assertEqual(0, len(city.stocks))
        npc1 = Npc(Brewer())
        npc2 = Npc(Farmer())
        stock = StockMarket()
        self.assertEqual(None, npc1.city)
        self.assertEqual(None, npc2.city)
        city.add_npc(npc1)
        city.add_npc(npc2)
        city.add_stock_market(stock)
        self.assertEqual(city, npc1.city)
        self.assertEqual(city, npc2.city)
        self.assertEqual(2, len(city.npcs))
        self.assertEqual(1, len(city.stocks))
        self.assertTrue(npc1 in city.npcs)
        self.assertTrue(npc2 in city.npcs)
        self.assertTrue(stock in city.stocks)
        
    def test_simple_npc_strategy(self):
        #setup city, stock and add some food there
        city = City()
        stock = StockMarket()
        city.add_stock_market(stock)
        self.SetDefaultPrices(stock)
        for i in range(20):
            stock.possession.add_resource(Meat())
            stock.possession.add_resource(Grain())
            stock.possession.add_resource(Water())

        #add simple strategy to npc
        npc = Npc(Brewer())
        kettle = ResourceFactory.create_resource_from_nothing(BeerKettle)
        npc.possession.add_real_property(kettle)
        city.add_npc(npc)
        for i in range(NpcStrategySimpleGreedy.MINIMUM_FOOD):
           npc.possession.add_resource(Meat())
        money = 200
        npc.possession._set_money(money)
        npc.strategy = NpcStrategySimpleGreedy(npc)
        
        #beer making requires currently seven days
        self.AdvanceGame(npc, Schedule.MAX_TIME * 7)
        #brewer should have bought grain, water and food
        money -= self.meatDefaultPrice * 5
        money -= self.grainDefaultPrice
        money -= self.waterDefaultPrice
        self.assertEqual(money, npc.possession.money) 
        self.assertEqual(len(kettle.outputs(BeerKettle.STATUS_PACKAGED)), npc.possession.get_resource_count(Beer))

        #next day brewer should sell beers and buy food and grain (for next round)
        self.AdvanceGame(npc, Schedule.MAX_TIME)
        money -= self.meatDefaultPrice
        money -= self.grainDefaultPrice
        money += self.beerDefaultPrice * len(kettle.outputs(BeerKettle.STATUS_PACKAGED))
        self.assertEqual(money, npc.possession.money) 
        self.assertEqual(0, npc.possession.get_resource_count(Beer))

        #after 6 days (malting already started last day), next beer round should be ready
        self.AdvanceGame(npc, Schedule.MAX_TIME * 6)
        self.assertEqual(len(kettle.outputs(BeerKettle.STATUS_PACKAGED)), npc.possession.get_resource_count(Beer))
        #and after one day it should be sold
        self.AdvanceGame(npc, Schedule.MAX_TIME)
        money -= self.meatDefaultPrice * 7
        money -= self.waterDefaultPrice
        money -= self.grainDefaultPrice
        money += self.beerDefaultPrice * len(kettle.outputs(BeerKettle.STATUS_PACKAGED))
        self.assertEqual(money, npc.possession.money) 
        self.assertEqual(0, npc.possession.get_resource_count(Beer))

    def test_simple_npc_strategy_farmer(self):
        #setup city, stock and add some food there
        city = City()
        stock = StockMarket()
        city.add_stock_market(stock)
        self.SetDefaultPrices(stock)
        for i in range(10):
            stock.possession.add_resource(Meat())
            stock.possession.add_resource(Grain())

        #add simple strategy to npc
        npc = Npc(Farmer())
        field = ResourceFactory.create_resource_from_nothing(FieldSquare) 
        npc.possession.add_real_property(field)
        city.add_npc(npc)
        money = 200
        npc.possession._set_money(money)
        npc.strategy = NpcStrategySimpleGreedy(npc)

        self.AdvanceGame(npc, Schedule.MAX_TIME * 4) #enough for farmer to grow crop but not yet harvest
        #farmer has to buy seeds (once before sowing and after that because inputs are always required) and food 
        money -= self.meatDefaultPrice * 4 + self.grainDefaultPrice * 2
        self.assertEqual(money, npc.possession.money) 

        #farmer should now have first crop ready and harvested
        self.AdvanceGame(npc, Schedule.MAX_TIME)
        money -= self.meatDefaultPrice
        self.assertEqual(money, npc.possession.money) 

        #farmer now has first crop and sell all but one
        self.AdvanceGame(npc, Schedule.MAX_TIME)
        money -= self.meatDefaultPrice
        money += self.grainDefaultPrice * len(field.final_outputs()) #sell whole crop, because inputs has been bought already
        self.assertEqual(money, npc.possession.money) 
        self.assertTrue(npc.possession.has_resources([Grain]))

    def test_simple_npc_strategy_bartender(self):
        #setup city, stock and add some food there
        city = City()
        stock = StockMarket()
        city.add_stock_market(stock)
        self.SetDefaultPrices(stock)
        for i in range(10):
            stock.possession.add_resource(Meat())
            stock.possession.add_resource(Beer())

        #add simple strategy to npc
        npc = Npc(Bartender())
        city.add_npc(npc)
        money = 500
        npc.possession._set_money(money)
        npc.strategy = NpcStrategySimpleGreedy(npc)

        self.AdvanceGame(npc, Schedule.MAX_TIME * 1) #bartender should buy beer so that stock is full
        money -= self.beerDefaultPrice * Bartender.STOCK_SIZE + self.meatDefaultPrice
        self.assertEqual(money, npc.possession.money) 
        self.assertEqual(Bartender.STOCK_SIZE, npc.possession.get_resource_count(Beer))

        #somebody buys a beer from bartender
        customer = Npc(Farmer)
        npc.possession.give_resource(Beer, customer.possession)

        self.AdvanceGame(npc, Schedule.MAX_TIME * 1) #bartender should refill stock
        money -= self.beerDefaultPrice * 1 + self.meatDefaultPrice
        self.assertEqual(money, npc.possession.money) 
        self.assertEqual(Bartender.STOCK_SIZE, npc.possession.get_resource_count(Beer))


    def test_stock_action(self):
        #setup city, stock and add some food there
        city = City()
        stock = StockMarket()
        city.add_stock_market(stock)
        self.SetDefaultPrices(stock)
        stock.possession.add_resource(Meat())
        stock.possession.add_resource(Meat())
        stock.possession.add_resource(Grain())
        stock.possession.add_resource(Grain())

        npc = Npc(Brewer())
        money = 500
        npc.possession._set_money(money)
        npc.possession.add_resource(Beer())
        npc.possession.add_resource(Beer())
        #directly test adding a stock action
        npc.schedule = Schedule()
        npc.schedule.add_action(StockAction("Buying and selling", [Meat, Grain, Grain],
            [Beer, Beer], npc, stock))

        #advance and check that right resources were sold and bought
        self.AdvanceNpc(npc, Schedule.MAX_TIME)
        self.assertTrue(npc.possession.has_resources([Meat, Grain, Grain]))
        self.assertTrue(stock.possession.has_resources([Meat, Beer, Beer]))
        money -= stock.get_price(Grain) * 2 + stock.get_price(Meat)
        money += stock.get_price(Beer) * 2
        self.assertEqual(money, npc.possession.money) 
        
    def test_move_action(self):
        npc = Npc(Brewer())
        x = 50
        y = 60
        npc.x = x
        npc.y = y
        #directly test adding a move action
        target_x = 105
        target_y = 35
        npc.schedule = Schedule()
        npc.schedule.add_action(MoveAction("Moving", npc, target_x, target_y))

        #advance and check that npc moved
        self.AdvanceNpc(npc, Schedule.MAX_TIME)
        self.assertEqual(target_x, npc.x) 
        self.assertEqual(target_y, npc.y) 

    def test_possession_get_resource_and_count(self):
        npc = Npc(Brewer())
        self.assertFalse(npc.possession.get_resource(Beer))
        self.assertFalse(npc.possession.get_resource(Grain))
        self.assertFalse(npc.possession.get_resource(Meat))
        self.assertEqual(0, npc.possession.get_resource_count(Beer))
        self.assertEqual(0, npc.possession.get_resource_count(Grain))
        self.assertEqual(0, npc.possession.get_resource_count(Meat))
        self.assertEqual(0, len(npc.possession.get_resource_types()))

        npc.possession.add_resource(Grain())
        self.assertFalse(npc.possession.get_resource(Beer))
        self.assertTrue(npc.possession.get_resource(Grain))
        self.assertFalse(npc.possession.get_resource(Meat))
        self.assertEqual(0, npc.possession.get_resource_count(Beer))
        self.assertEqual(1, npc.possession.get_resource_count(Grain))
        self.assertEqual(0, npc.possession.get_resource_count(Meat))
        self.assertEqual(1, len(npc.possession.get_resource_types()))
        self.assertTrue(Grain in npc.possession.get_resource_types())
 
        npc.possession.add_resource(Grain())
        npc.possession.add_resource(Beer())
        self.assertTrue(npc.possession.get_resource(Beer))
        self.assertTrue(npc.possession.get_resource(Grain))
        self.assertFalse(npc.possession.get_resource(Meat))
        self.assertEqual(1, npc.possession.get_resource_count(Beer))
        self.assertEqual(2, npc.possession.get_resource_count(Grain))
        self.assertEqual(0, npc.possession.get_resource_count(Meat))
        self.assertEqual(2, len(npc.possession.get_resource_types()))
        self.assertTrue(Grain in npc.possession.get_resource_types())
        self.assertTrue(Beer in npc.possession.get_resource_types())

        npc2 = Npc(Farmer())
        npc.possession.give_resource(Beer, npc2.possession)
        self.assertFalse(npc.possession.get_resource(Beer))
        self.assertTrue(npc.possession.get_resource(Grain))
        self.assertFalse(npc.possession.get_resource(Meat))
        self.assertEqual(0, npc.possession.get_resource_count(Beer))
        self.assertEqual(2, npc.possession.get_resource_count(Grain))
        self.assertEqual(0, npc.possession.get_resource_count(Meat))
        self.assertTrue(npc2.possession.get_resource(Beer))
        self.assertEqual(1, npc2.possession.get_resource_count(Beer))
        self.assertEqual(1, len(npc.possession.get_resource_types()))
        self.assertTrue(Grain in npc.possession.get_resource_types())

    def test_possession_get_missing(self):
        npc = Npc(Brewer())
        missing = npc.possession.get_missing_resources([Beer])
        self.assertEqual(1, len(missing))
        self.assertEqual(Beer, missing[0])

        npc.possession.add_resource(Beer())
        missing = npc.possession.get_missing_resources([Beer])
        self.assertEqual(0, len(missing))

        missing = npc.possession.get_missing_resources([Beer, Grain])
        self.assertEqual(1, len(missing))
        self.assertEqual(Grain, missing[0])

        npc.possession.add_resource(Meat())
        npc.possession.add_resource(Beer())
        missing = npc.possession.get_missing_resources([Beer, Grain])
        self.assertEqual(1, len(missing))
        self.assertEqual(Grain, missing[0])

        npc.possession.add_resource(Grain())
        missing = npc.possession.get_missing_resources([Beer])
        self.assertEqual(0, len(missing))


    def test_resource_heap(self):
        beers = ResourceHeap(Beer)
        self.assertEqual(0, beers.count)
        beer1 = Beer()
        beers.add(beer1)
        self.assertEqual(1, beers.count)
        beer2 = Beer()
        beers.add(beer2)
        self.assertEqual(2, beers.count)
        removed = beers.remove(beer2)
        self.assertEqual(beer2, removed)
        self.assertEqual(1, beers.count)
        #try to remove again the same item
        removed = beers.remove(beer2)
        self.assertEqual(None, removed)
        self.assertEqual(1, beers.count)
        #remove with typr
        beers.remove(Beer)
        self.assertEqual(0, beers.count)

    def test_loader_load_city(self):
        loader = Loader()
        city = loader.load_city('_testcity.txt')
        self._ensure_city_is_testcity(city)


    def test_loader_load_and_save_city(self):
        loader = Loader()
        city = loader.load_city('_testcity.txt')
        loader.save_city(city, '_temptestcity.txt')
        city2 = loader.load_city('_temptestcity.txt')
        self._ensure_city_is_testcity(city2)

    def _ensure_city_is_testcity(self, city):
        #check NPCs
        self.assertEqual(5, len(city.npcs))
        brewer = city.npcs[0]
        self.assertEqual('Mr Trappe', brewer.name)
        self.assertEqual(350, brewer.home_x)
        self.assertEqual(320, brewer.home_y)
        self.assertEqual(150, brewer.x)
        self.assertEqual(275, brewer.y)
        self.assertEqual(24501, brewer.possession.money)
        self.assertEqual(Brewer, type(brewer.occupation))
        self.assertEqual(NpcStrategySimpleGreedy, type(brewer.strategy))
        self.assertEqual(2, len(brewer.possession.get_all()))
        self.assertTrue(brewer.possession.has_resources([Grain, Meat]))

        farmer = city.npcs[1]
        self.assertEqual('Pertti', farmer.name)
        self.assertEqual(510, farmer.home_x)
        self.assertEqual(160, farmer.home_y)
        self.assertEqual(33, farmer.x)
        self.assertEqual(457, farmer.y)
        self.assertEqual(43, farmer.possession.money)
        field = farmer.possession.get_real_property(FieldSquare) 
        self.assertTrue(field != None)
        self.assertEqual(50, field.x)
        self.assertEqual(100, field.y)
        self.assertEqual(Farmer, type(farmer.occupation))
        self.assertEqual(NpcStrategySimpleGreedy, type(farmer.strategy))

        #check stocks:
        self.assertEqual(2, len(city.stocks))
        stock1 = city.stocks[0]
        self.assertEqual(0, stock1.x)
        self.assertEqual(0, stock1.y)
        self.assertEqual(1323, stock1.possession.money)
        self.assertEqual(50, stock1.get_price(Grain))
        self.assertEqual(100, stock1.get_price(Beer))
        self.assertEqual(35, stock1.get_price(Meat))
        self.assertEqual(7, stock1.possession.get_resource_count(Meat))
        self.assertEqual(5, stock1.possession.get_resource_count(Grain))
        self.assertEqual(3, stock1.possession.get_resource_count(Beer))
        
        stock2 = city.stocks[1]
        self.assertEqual(523, stock2.x)
        self.assertEqual(321, stock2.y)
        self.assertEqual(58300, stock2.possession.money)
        self.assertEqual(250, stock2.get_price(Grain))
        self.assertEqual(900, stock2.get_price(Beer))
        self.assertEqual(650, stock2.get_price(Meat))
        self.assertEqual(0, stock2.possession.get_resource_count(Meat))
        self.assertEqual(0, stock2.possession.get_resource_count(Grain))
        self.assertEqual(1, stock2.possession.get_resource_count(Beer))
    
    def test_possession_real_properties(self):
        npc = Npc(Brewer())
        self.assertEqual(None, npc.possession.get_real_property(FieldSquare)) 
        field = ResourceFactory.create_resource_from_nothing(FieldSquare) 
        npc.possession.add_real_property(field)
        self.assertEqual(field, npc.possession.get_real_property(FieldSquare)) 
        self.assertEqual(field, npc.possession.get_real_property(field)) 
        field2 = ResourceFactory.create_resource_from_nothing(FieldSquare) 
        npc.possession.add_real_property(field2)
        self.assertEqual(field, npc.possession.get_real_property(FieldSquare)) 
        self.assertEqual(field2, npc.possession.get_real_property(field2)) 


if __name__ == '__main__':
    unittest.main()

