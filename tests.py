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
            npc.Advance(advanceAmount)
            amount -= advanceAmount
    
    
    def SetDefaultPrices(self, stock):
        stock.SetPrice(Grain, self.grainDefaultPrice)
        stock.SetPrice(Meat, self.meatDefaultPrice)
        stock.SetPrice(Beer, self.beerDefaultPrice)


    def test_farmer_creates_grain(self):
        npc = Npc(Farmer())
        self.assertEqual(0, len(npc.possession.resources))
        self.AdvanceNpc(npc, Npc.sleepDuration) #sleeping time
        self.AdvanceNpc(npc, Farmer.duration) #farming time
        self.assertEqual(1, len(npc.possession.resources))
        self.assertTrue(npc.possession.HasResources([Grain]))

    def test_hunter_creates_meat(self):
        npc = Npc(Hunter())
        self.assertEqual(0, len(npc.possession.resources))
        self.AdvanceNpc(npc, Npc.sleepDuration) #sleeping time
        self.AdvanceNpc(npc, Hunter.duration) #action time
        self.assertEqual(2, len(npc.possession.resources))
        self.assertTrue(npc.possession.HasResources([Meat]))

    def test_brewer_creates_beer(self):
        npc = Npc(Brewer())
        npc.foodConsumption = 0 #lets not worry about food in this test
        npc.possession.AddResource(Grain())
        npc.possession.AddResource(Grain())
        self.assertEqual(2, len(npc.possession.resources))
        self.AdvanceNpc(npc, Npc.sleepDuration) #sleeping time
        self.AdvanceNpc(npc, Brewer.duration) #brewing time
        self.assertEqual(1, len(npc.possession.resources))
        self.assertTrue(npc.possession.HasResources([Beer]))

        #start next day and give more resources (one extra grain)
        npc.possession.AddResource(Grain())
        npc.possession.AddResource(Grain())
        npc.possession.AddResource(Grain())
        self.AdvanceNpc(npc, npc.schedule.GetTotalRemainingTime()) #rest of the day
        self.AdvanceNpc(npc, Npc.sleepDuration) #sleeping time
        self.AdvanceNpc(npc, Brewer.duration) #brewing time
        self.assertEqual(3, len(npc.possession.resources))
        self.assertTrue(npc.possession.HasResources([Beer, Beer, Grain]))

    def test_action_outputs_are_given_after_task_is_fully_done(self):
        npc = Npc(Hunter())
        self.assertEqual(0, len(npc.possession.resources))
        self.AdvanceNpc(npc, Npc.sleepDuration) #sleeping time
        self.AdvanceNpc(npc, Hunter.duration / 2) #half of the action time
        self.assertEqual(0, len(npc.possession.resources))
        self.AdvanceNpc(npc, Hunter.duration / 2) #half of the action time
        self.assertEqual(2, len(npc.possession.resources))
        self.assertTrue(npc.possession.HasResources([Meat]))


    def test_brewer_cannot_brew_when_out_of_resources(self):
        npc = Npc(Brewer())
        #brewing needs to grains, only one is given       
        npc.possession.AddResource(Grain())
        self.AdvanceNpc(npc, Npc.sleepDuration) #sleeping time
        self.AdvanceNpc(npc, Brewer.duration) #brewing time
        self.assertEqual(1, len(npc.possession.resources))
        self.assertTrue(npc.possession.HasResources([Grain]))

    def test_advance_over_one_action(self):
        npc = Npc(Farmer())
        self.assertEqual(0, len(npc.possession.resources))
        #advance one full day, both sleeping and farming should be done       
        self.AdvanceNpc(npc, Schedule.MaxTime)
        self.assertEqual(1, len(npc.possession.resources))
        self.assertTrue(npc.possession.HasResources([Grain]))

    def test_advance_over_day_ending(self):
        npc = Npc(Farmer())
        npc.foodConsumption = 0 #lets not worry about food in this test
        self.assertEqual(0, len(npc.possession.resources))
        #advance two full days, two sleepings and farmings should be done       
        self.AdvanceNpc(npc, Schedule.MaxTime * 2)
        self.assertEqual(2, len(npc.possession.resources))
        self.assertTrue(npc.possession.HasResources([Grain, Grain]))

    def test_npc_eats(self):
        npc = Npc(Farmer())
        #npc has food for one day by default
        self.AdvanceNpc(npc, Schedule.MaxTime)
        self.assertEqual(1, len(npc.possession.resources))
        self.assertTrue(npc.possession.HasResources([Grain]))
        
        #give foor for the next day and check that it is consumed
        npc.possession.AddResource(Meat())
        self.AdvanceNpc(npc, Schedule.MaxTime)
        self.assertEqual(2, len(npc.possession.resources))
        self.assertTrue(npc.possession.HasResources([Grain, Grain]))

    def test_npc_dies_with_hunger(self):
        npc = Npc(Farmer())
        #npc has food for one day by default
        self.AdvanceNpc(npc, Schedule.MaxTime)
        self.assertEqual(1, len(npc.possession.resources))
        self.assertTrue(npc.possession.HasResources([Grain]))
        self.assertTrue(npc.IsAlive())
        
        #don't give more food so npc should die
        self.AdvanceNpc(npc, Schedule.MaxTime)
        self.assertEqual(1, len(npc.possession.resources)) #couldn't farm anymore
        self.assertTrue(npc.possession.HasResources([Grain]))
        self.assertFalse(npc.IsAlive())

    def test_npc_produces_the_food_it_needs_next_day(self):
        npc = Npc(Hunter())
        #npc has food for one day by default and produces two foods per day (one day ration)
        #so npc is self contained, advance one week. 
        self.AdvanceNpc(npc, Schedule.MaxTime * 7)
        self.assertEqual(8, len(npc.possession.resources))
        self.assertTrue(npc.possession.HasResources([Meat]))
        self.assertTrue(npc.IsAlive())
        #starting of next day, npc should have to eat the meat it produced last day       
        self.AdvanceNpc(npc, Schedule.MaxTime / 4)
        self.assertEqual(7, len(npc.possession.resources))
        self.assertTrue(npc.IsAlive())

    def test_stock_prices(self):
        stock = StockMarket()
        #set/get using class
        stock.SetPrice(Grain, 20)
        self.assertEqual(20, stock.GetPrice(Grain))
        #set/get using instances
        stock.SetPrice(Beer(), 200)
        self.assertEqual(200, stock.GetPrice(Beer()))
        #set prices again
        stock.SetPrice(Grain, 15)
        stock.SetPrice(Beer(), 203)
        self.assertEqual(15, stock.GetPrice(Grain))
        self.assertEqual(203, stock.GetPrice(Beer()))

    def test_player_sells_resources(self):
        stock = StockMarket()
        self.SetDefaultPrices(stock)
        npc = Npc(Brewer())
        beer = Beer()
        npc.possession.AddResource(beer)
        self.assertEqual(0, npc.possession.GetMoney())
        self.assertEqual(None, stock.FindResource(Beer))
        self.assertTrue(stock.SellResource(beer, npc.possession)) 
        self.assertEqual(0, len(npc.possession.resources))
        self.assertEqual(self.beerDefaultPrice, npc.possession.GetMoney()) 
        self.assertEqual(1, len(stock.possession.resources))
        self.assertTrue(stock.possession.HasResources([Beer]))
        self.assertEqual(beer, stock.FindResource(Beer))

    def test_player_buys_resources(self):
        stock = StockMarket()
        self.SetDefaultPrices(stock)
        stock.possession.AddResource(Meat())
        stock.possession.AddResource(Beer())
        stock.possession.AddResource(Grain())
        
        npc = Npc(Brewer())
        money = 100
        npc.possession.money = money
        self.assertEqual(money, npc.possession.GetMoney())
        self.assertEqual(StockMarket.initialMoney, stock.possession.GetMoney())
        #buy with type
        self.assertTrue(stock.BuyResource(Beer, npc.possession)) 
        self.assertEqual(1, len(npc.possession.resources))
        self.assertTrue(npc.possession.HasResources([Beer]))
        self.assertEqual(money - self.beerDefaultPrice, npc.possession.GetMoney()) 
        self.assertEqual(StockMarket.initialMoney + self.beerDefaultPrice, stock.possession.GetMoney()) 
        self.assertEqual(2, len(stock.possession.resources))
        self.assertFalse(stock.possession.HasResources([Beer]))
        self.assertTrue(stock.possession.HasResources([Meat, Grain]))
        #buy with instance
        grain = stock.FindResource(Grain)
        self.assertTrue(stock.BuyResource(grain, npc.possession)) 
        self.assertEqual(2, len(npc.possession.resources))
        self.assertTrue(npc.possession.HasResources([Grain, Beer]))
        self.assertEqual(money - self.beerDefaultPrice - self.grainDefaultPrice, npc.possession.GetMoney()) 
        self.assertEqual(StockMarket.initialMoney + self.beerDefaultPrice + self.grainDefaultPrice, stock.possession.GetMoney()) 
        self.assertEqual(1, len(stock.possession.resources))
        self.assertFalse(stock.possession.HasResources([Grain]))
        self.assertTrue(stock.possession.HasResources([Meat]))

    def test_city_with_npcs_and_stock_markets(self):
        city = City()
        self.assertEqual(0, len(city.GetNpcs()))
        self.assertEqual(0, len(city.GetStockMarkets()))
        npc1 = Npc(Brewer())
        npc2 = Npc(Farmer())
        stock = StockMarket()
        self.assertEqual(None, npc1.GetCity())
        self.assertEqual(None, npc2.GetCity())
        city.AddNpc(npc1)
        city.AddNpc(npc2)
        city.AddStockMarket(stock)
        self.assertEqual(city, npc1.GetCity())
        self.assertEqual(city, npc2.GetCity())
        self.assertEqual(2, len(city.GetNpcs()))
        self.assertEqual(1, len(city.GetStockMarkets()))
        self.assertTrue(npc1 in city.GetNpcs())
        self.assertTrue(npc2 in city.GetNpcs())
        self.assertTrue(stock in city.GetStockMarkets())
        
    def test_simple_npc_strategy(self):
        #setup city, stock and add some food there
        city = City()
        stock = StockMarket()
        city.AddStockMarket(stock)
        self.SetDefaultPrices(stock)
        stock.possession.AddResource(Meat())
        stock.possession.AddResource(Meat())
        stock.possession.AddResource(Meat())

        #add simple strategy to npc
        npc = Npc(Brewer())
        city.AddNpc(npc)
        for i in range(NpcStrategySimpleGreedy.minimumFood):
           npc.possession.AddResource(Meat())
        money = 200
        npc.possession.money = money
        npc.SetStrategy(NpcStrategySimpleGreedy(npc))
        self.AdvanceNpc(npc, Schedule.MaxTime * 2)

        #npc should have spend one food and have now less food than minimum and buy more
        self.AdvanceNpc(npc, Schedule.MaxTime)
        money -= self.meatDefaultPrice
        self.assertEqual(money, npc.possession.GetMoney()) 

        #add needed resources to stock so npc should try to buy food and resources
        stock.possession.AddResource(Grain())
        stock.possession.AddResource(Grain())
        self.AdvanceNpc(npc, Schedule.MaxTime)
        money -= self.meatDefaultPrice
        money -= self.grainDefaultPrice * 2
        self.assertEqual(money, npc.possession.GetMoney()) 
        self.assertTrue(npc.possession.HasResources([Beer]))

        #next day, npc should try to buy food and sell beer (there are no resources to buy)
        self.AdvanceNpc(npc, Schedule.MaxTime)
        money -= self.meatDefaultPrice
        money += self.beerDefaultPrice
        self.assertEqual(money, npc.possession.GetMoney()) 
        self.assertFalse(npc.possession.HasResources([Beer]))



if __name__ == '__main__':
    unittest.main()

