from latrappe import *
import unittest 

class TestSequenceFunctions(unittest.TestCase):
    advanceInterval = 1

    def setUp(self):
        self.grainDefaultPrice = 15
        self.meatDefaultPrice = 20
        self.beerDefaultPrice = 50
        pass

    def AdvanceNpc(self, npc, amount):
        while (amount > 0):
            advanceAmount = min(TestSequenceFunctions.advanceInterval, amount)
            npc.advance(advanceAmount)
            amount -= advanceAmount
    
    
    def SetDefaultPrices(self, stock):
        stock.set_price(Grain, self.grainDefaultPrice)
        stock.set_price(Meat, self.meatDefaultPrice)
        stock.set_price(Beer, self.beerDefaultPrice)

    
    def test_farmer_creates_grain(self):
        npc = Npc(Farmer())
        self.assertEqual(0, len(npc.possession.get_all()))
        self.AdvanceNpc(npc, Npc.SLEEP_DURATION) #sleeping time
        self.AdvanceNpc(npc, Farmer.DURATION) #farming time
        self.assertEqual(1, len(npc.possession.get_all()))
        self.assertTrue(npc.possession.has_resources([Grain]))

    def test_hunter_creates_meat(self):
        npc = Npc(Hunter())
        self.assertEqual(0, len(npc.possession.get_all()))
        self.AdvanceNpc(npc, Npc.SLEEP_DURATION) #sleeping time
        self.AdvanceNpc(npc, Hunter.DURATION) #action time
        self.assertEqual(2, len(npc.possession.get_all()))
        self.assertTrue(npc.possession.has_resources([Meat]))
    
    def test_brewer_creates_beer(self):
        npc = Npc(Brewer())
        npc.food_consumption = 0 #lets not worry about food in this test
        npc.possession.add_resource(Grain())
        npc.possession.add_resource(Grain())
        self.assertEqual(2, len(npc.possession.get_all()))
        self.AdvanceNpc(npc, Npc.SLEEP_DURATION) #sleeping time
        self.AdvanceNpc(npc, Brewer.DURATION) #brewing time
        self.assertEqual(1, len(npc.possession.get_all()))
        self.assertTrue(npc.possession.has_resources([Beer]))

        #start next day and give more resources (one extra grain)
        npc.possession.add_resource(Grain())
        npc.possession.add_resource(Grain())
        npc.possession.add_resource(Grain())
        self.AdvanceNpc(npc, npc.schedule.get_total_remaining_time()) #rest of the day
        self.AdvanceNpc(npc, Npc.SLEEP_DURATION) #sleeping time
        self.AdvanceNpc(npc, Brewer.DURATION) #brewing time
        self.assertEqual(3, len(npc.possession.get_all()))
        self.assertTrue(npc.possession.has_resources([Beer, Beer, Grain]))

    
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
        npc = Npc(Farmer())
        self.assertEqual(0, len(npc.possession.get_all()))
        #advance one full day, both sleeping and farming should be done       
        self.AdvanceNpc(npc, Schedule.MAX_TIME)
        self.assertEqual(1, len(npc.possession.get_all()))
        self.assertTrue(npc.possession.has_resources([Grain]))

    def test_advance_over_day_ending(self):
        npc = Npc(Farmer())
        npc.food_consumption = 0 #lets not worry about food in this test
        self.assertEqual(0, len(npc.possession.get_all()))
        #advance two full days, two sleepings and farmings should be done       
        self.AdvanceNpc(npc, Schedule.MAX_TIME * 2)
        self.assertEqual(2, len(npc.possession.get_all()))
        self.assertTrue(npc.possession.has_resources([Grain, Grain]))

    def test_npc_eats(self):
        npc = Npc(Farmer())
        #npc has food for one day by default
        self.AdvanceNpc(npc, Schedule.MAX_TIME)
        self.assertEqual(1, len(npc.possession.get_all()))
        self.assertTrue(npc.possession.has_resources([Grain]))
        
        #give foor for the next day and check that it is consumed
        npc.possession.add_resource(Meat())
        self.AdvanceNpc(npc, Schedule.MAX_TIME)
        self.assertEqual(2, len(npc.possession.get_all()))
        self.assertTrue(npc.possession.has_resources([Grain, Grain]))

    def test_npc_dies_with_hunger(self):
        npc = Npc(Farmer())
        #npc has food for one day by default
        self.AdvanceNpc(npc, Schedule.MAX_TIME)
        self.assertEqual(1, len(npc.possession.get_all()))
        self.assertTrue(npc.possession.has_resources([Grain]))
        self.assertTrue(npc.alive)
        
        #don't give more food so npc should die
        self.AdvanceNpc(npc, Schedule.MAX_TIME)
        self.assertEqual(1, len(npc.possession.get_all())) #couldn't farm anymore
        self.assertTrue(npc.possession.has_resources([Grain]))
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
        self.assertEqual(0, len(city.get_npcs()))
        self.assertEqual(0, len(city.get_stock_markets()))
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
        self.assertEqual(2, len(city.get_npcs()))
        self.assertEqual(1, len(city.get_stock_markets()))
        self.assertTrue(npc1 in city.get_npcs())
        self.assertTrue(npc2 in city.get_npcs())
        self.assertTrue(stock in city.get_stock_markets())
        
    def test_simple_npc_strategy(self):
        #setup city, stock and add some food there
        city = City()
        stock = StockMarket()
        city.add_stock_market(stock)
        self.SetDefaultPrices(stock)
        stock.possession.add_resource(Meat())
        stock.possession.add_resource(Meat())
        stock.possession.add_resource(Meat())

        #add simple strategy to npc
        npc = Npc(Brewer())
        city.add_npc(npc)
        for i in range(NpcStrategySimpleGreedy.MINIMUM_FOOD):
           npc.possession.add_resource(Meat())
        money = 200
        npc.possession._set_money(money)
        npc.strategy = NpcStrategySimpleGreedy(npc)
        self.AdvanceNpc(npc, Schedule.MAX_TIME * 2)

        #npc should have spend one food and have now less food than minimum and buy more
        self.AdvanceNpc(npc, Schedule.MAX_TIME)
        money -= self.meatDefaultPrice
        self.assertEqual(money, npc.possession.money) 

        #add needed resources to stock so npc should try to buy food and resources
        stock.possession.add_resource(Grain())
        stock.possession.add_resource(Grain())
        self.AdvanceNpc(npc, Schedule.MAX_TIME)
        money -= self.meatDefaultPrice
        money -= self.grainDefaultPrice * 2
        self.assertEqual(money, npc.possession.money) 
        self.assertTrue(npc.possession.has_resources([Beer]))

        #next day, npc should try to buy food and sell beer (there are no resources to buy)
        self.AdvanceNpc(npc, Schedule.MAX_TIME)
        money -= self.meatDefaultPrice
        money += self.beerDefaultPrice
        self.assertEqual(money, npc.possession.money) 
        self.assertFalse(npc.possession.has_resources([Beer]))

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
            [Beer, Beer], npc.possession, stock))

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


if __name__ == '__main__':
    unittest.main()

