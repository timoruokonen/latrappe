import latrappe
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
        stock.SetPrice(latrappe.Grain, self.grainDefaultPrice)
        stock.SetPrice(latrappe.Meat, self.meatDefaultPrice)
        stock.SetPrice(latrappe.Beer, self.beerDefaultPrice)


    def test_farmer_creates_grain(self):
        npc = latrappe.Npc(latrappe.Farmer())
        self.assertEqual(0, len(npc.possession.resources))
        self.AdvanceNpc(npc, latrappe.Npc.sleepDuration) #sleeping time
        self.AdvanceNpc(npc, latrappe.Farmer.duration) #farming time
        self.assertEqual(1, len(npc.possession.resources))
        self.assertTrue(npc.possession.HasResources([latrappe.Grain]))

    def test_hunter_creates_meat(self):
        npc = latrappe.Npc(latrappe.Hunter())
        self.assertEqual(0, len(npc.possession.resources))
        self.AdvanceNpc(npc, latrappe.Npc.sleepDuration) #sleeping time
        self.AdvanceNpc(npc, latrappe.Hunter.duration) #action time
        self.assertEqual(1, len(npc.possession.resources))
        self.assertTrue(npc.possession.HasResources([latrappe.Meat]))

    def test_brewer_creates_beer(self):
        npc = latrappe.Npc(latrappe.Brewer())
        npc.foodConsumption = 0 #lets not worry about food in this test
        npc.possession.AddResource(latrappe.Grain())
        npc.possession.AddResource(latrappe.Grain())
        self.assertEqual(2, len(npc.possession.resources))
        self.AdvanceNpc(npc, latrappe.Npc.sleepDuration) #sleeping time
        self.AdvanceNpc(npc, latrappe.Brewer.duration) #brewing time
        self.assertEqual(1, len(npc.possession.resources))
        self.assertTrue(npc.possession.HasResources([latrappe.Beer]))

        #start next day and give more resources (one extra grain)
        npc.possession.AddResource(latrappe.Grain())
        npc.possession.AddResource(latrappe.Grain())
        npc.possession.AddResource(latrappe.Grain())
        self.AdvanceNpc(npc, npc.schedule.GetTotalRemainingTime()) #rest of the day
        self.AdvanceNpc(npc, latrappe.Npc.sleepDuration) #sleeping time
        self.AdvanceNpc(npc, latrappe.Brewer.duration) #brewing time
        self.assertEqual(3, len(npc.possession.resources))
        self.assertTrue(npc.possession.HasResources([latrappe.Beer, latrappe.Beer, latrappe.Grain]))

    def test_action_outputs_are_given_after_task_is_fully_done(self):
        npc = latrappe.Npc(latrappe.Hunter())
        self.assertEqual(0, len(npc.possession.resources))
        self.AdvanceNpc(npc, latrappe.Npc.sleepDuration) #sleeping time
        self.AdvanceNpc(npc, latrappe.Hunter.duration / 2) #half of the action time
        self.assertEqual(0, len(npc.possession.resources))
        self.AdvanceNpc(npc, latrappe.Hunter.duration / 2) #half of the action time
        self.assertEqual(1, len(npc.possession.resources))
        self.assertTrue(npc.possession.HasResources([latrappe.Meat]))


    def test_brewer_cannot_brew_when_out_of_resources(self):
        npc = latrappe.Npc(latrappe.Brewer())
        #brewing needs to grains, only one is given       
        npc.possession.AddResource(latrappe.Grain())
        self.AdvanceNpc(npc, latrappe.Npc.sleepDuration) #sleeping time
        self.AdvanceNpc(npc, latrappe.Brewer.duration) #brewing time
        self.assertEqual(1, len(npc.possession.resources))
        self.assertTrue(npc.possession.HasResources([latrappe.Grain]))

    def test_advance_over_one_action(self):
        npc = latrappe.Npc(latrappe.Farmer())
        self.assertEqual(0, len(npc.possession.resources))
        #advance one full day, both sleeping and farming should be done       
        self.AdvanceNpc(npc, latrappe.Schedule.MaxTime)
        self.assertEqual(1, len(npc.possession.resources))
        self.assertTrue(npc.possession.HasResources([latrappe.Grain]))

    def test_advance_over_day_ending(self):
        npc = latrappe.Npc(latrappe.Farmer())
        npc.foodConsumption = 0 #lets not worry about food in this test
        self.assertEqual(0, len(npc.possession.resources))
        #advance two full days, two sleepings and farmings should be done       
        self.AdvanceNpc(npc, latrappe.Schedule.MaxTime * 2)
        self.assertEqual(2, len(npc.possession.resources))
        self.assertTrue(npc.possession.HasResources([latrappe.Grain, latrappe.Grain]))

    def test_npc_eats(self):
        npc = latrappe.Npc(latrappe.Farmer())
        #npc has food for one day by default
        self.AdvanceNpc(npc, latrappe.Schedule.MaxTime)
        self.assertEqual(1, len(npc.possession.resources))
        self.assertTrue(npc.possession.HasResources([latrappe.Grain]))
        
        #give foor for the next day and check that it is consumed
        npc.possession.AddResource(latrappe.Meat())
        self.AdvanceNpc(npc, latrappe.Schedule.MaxTime)
        self.assertEqual(2, len(npc.possession.resources))
        self.assertTrue(npc.possession.HasResources([latrappe.Grain, latrappe.Grain]))

    def test_npc_dies_with_hunger(self):
        npc = latrappe.Npc(latrappe.Farmer())
        #npc has food for one day by default
        self.AdvanceNpc(npc, latrappe.Schedule.MaxTime)
        self.assertEqual(1, len(npc.possession.resources))
        self.assertTrue(npc.possession.HasResources([latrappe.Grain]))
        self.assertTrue(npc.IsAlive())
        
        #don't give more food so npc should die
        self.AdvanceNpc(npc, latrappe.Schedule.MaxTime)
        self.assertEqual(1, len(npc.possession.resources)) #couldn't farm anymore
        self.assertTrue(npc.possession.HasResources([latrappe.Grain]))
        self.assertFalse(npc.IsAlive())

    def test_npc_produces_the_food_it_needs_next_day(self):
        npc = latrappe.Npc(latrappe.Hunter())
        #npc has food for one day by default and produces one food per day (one day ration)
        #so npc is self contained, advance one week. 
        self.AdvanceNpc(npc, latrappe.Schedule.MaxTime * 7)
        self.assertEqual(1, len(npc.possession.resources))
        self.assertTrue(npc.possession.HasResources([latrappe.Meat]))
        self.assertTrue(npc.IsAlive())
        #starting of next day, npc should have to eat the meat it produced last day       
        self.AdvanceNpc(npc, latrappe.Schedule.MaxTime / 4)
        self.assertEqual(0, len(npc.possession.resources))
        self.assertTrue(npc.IsAlive())

    def test_stock_prices(self):
        stock = latrappe.StockMarket()
        #set/get using class
        stock.SetPrice(latrappe.Grain, 20)
        self.assertEqual(20, stock.GetPrice(latrappe.Grain))
        #set/get using instances
        stock.SetPrice(latrappe.Beer(), 200)
        self.assertEqual(200, stock.GetPrice(latrappe.Beer()))
        #set prices again
        stock.SetPrice(latrappe.Grain, 15)
        stock.SetPrice(latrappe.Beer(), 203)
        self.assertEqual(15, stock.GetPrice(latrappe.Grain))
        self.assertEqual(203, stock.GetPrice(latrappe.Beer()))

    def test_player_sells_resources(self):
        stock = latrappe.StockMarket()
        self.SetDefaultPrices(stock)
        npc = latrappe.Npc(latrappe.Brewer())
        beer = latrappe.Beer()
        npc.possession.AddResource(beer)
        self.assertEqual(0, npc.possession.GetMoney())
        self.assertEqual(None, stock.FindResource(latrappe.Beer))
        self.assertTrue(stock.SellResource(beer, npc.possession)) 
        self.assertEqual(0, len(npc.possession.resources))
        self.assertEqual(self.beerDefaultPrice, npc.possession.GetMoney()) 
        self.assertEqual(1, len(stock.possession.resources))
        self.assertTrue(stock.possession.HasResources([latrappe.Beer]))
        self.assertEqual(beer, stock.FindResource(latrappe.Beer))

    def test_player_buys_resources(self):
        stock = latrappe.StockMarket()
        self.SetDefaultPrices(stock)
        stock.possession.AddResource(latrappe.Meat())
        stock.possession.AddResource(latrappe.Beer())
        stock.possession.AddResource(latrappe.Grain())
        
        npc = latrappe.Npc(latrappe.Brewer())
        money = 100
        npc.possession.money = money
        self.assertEqual(money, npc.possession.GetMoney())
        self.assertEqual(latrappe.StockMarket.initialMoney, stock.possession.GetMoney())
        #buy with type
        self.assertTrue(stock.BuyResource(latrappe.Beer, npc.possession)) 
        self.assertEqual(1, len(npc.possession.resources))
        self.assertTrue(npc.possession.HasResources([latrappe.Beer]))
        self.assertEqual(money - self.beerDefaultPrice, npc.possession.GetMoney()) 
        self.assertEqual(latrappe.StockMarket.initialMoney + self.beerDefaultPrice, stock.possession.GetMoney()) 
        self.assertEqual(2, len(stock.possession.resources))
        self.assertFalse(stock.possession.HasResources([latrappe.Beer]))
        self.assertTrue(stock.possession.HasResources([latrappe.Meat, latrappe.Grain]))
        #buy with instance
        grain = stock.FindResource(latrappe.Grain)
        self.assertTrue(stock.BuyResource(grain, npc.possession)) 
        self.assertEqual(2, len(npc.possession.resources))
        self.assertTrue(npc.possession.HasResources([latrappe.Grain, latrappe.Beer]))
        self.assertEqual(money - self.beerDefaultPrice - self.grainDefaultPrice, npc.possession.GetMoney()) 
        self.assertEqual(latrappe.StockMarket.initialMoney + self.beerDefaultPrice + self.grainDefaultPrice, stock.possession.GetMoney()) 
        self.assertEqual(1, len(stock.possession.resources))
        self.assertFalse(stock.possession.HasResources([latrappe.Grain]))
        self.assertTrue(stock.possession.HasResources([latrappe.Meat]))

    def test_city_with_npcs_and_stock_markets(self):
        city = latrappe.City()
        self.assertEqual(0, len(city.GetNpcs()))
        self.assertEqual(0, len(city.GetStockMarkets()))
        npc1 = latrappe.Npc(latrappe.Brewer())
        npc2 = latrappe.Npc(latrappe.Farmer())
        stock = latrappe.StockMarket()
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
        city = latrappe.City()
        stock = latrappe.StockMarket()
        city.AddStockMarket(stock)
        self.SetDefaultPrices(stock)
        stock.possession.AddResource(latrappe.Meat())
        stock.possession.AddResource(latrappe.Meat())
        stock.possession.AddResource(latrappe.Meat())

        #add simple strategy to npc
        npc = latrappe.Npc(latrappe.Brewer())
        city.AddNpc(npc)
        for i in range(latrappe.NpcStrategySimpleGreedy.minimumFood):
           npc.possession.AddResource(latrappe.Meat())
        money = 200
        npc.possession.money = money
        npc.SetStrategy(latrappe.NpcStrategySimpleGreedy(npc))
        self.AdvanceNpc(npc, latrappe.Schedule.MaxTime * 2)

        #npc should have spend one food and have now less food than minimum and buy more
        self.AdvanceNpc(npc, latrappe.Schedule.MaxTime)
        money -= self.meatDefaultPrice
        self.assertEqual(money, npc.possession.GetMoney()) 

        #add needed resources to stock so npc should try to buy food and resources
        stock.possession.AddResource(latrappe.Grain())
        stock.possession.AddResource(latrappe.Grain())
        self.AdvanceNpc(npc, latrappe.Schedule.MaxTime)
        money -= self.meatDefaultPrice
        money -= self.grainDefaultPrice * 2
        self.assertEqual(money, npc.possession.GetMoney()) 
        self.assertTrue(npc.possession.HasResources([latrappe.Beer]))

        #next day, npc should try to buy food and sell beer (there are no resources to buy)
        self.AdvanceNpc(npc, latrappe.Schedule.MaxTime)
        money -= self.meatDefaultPrice
        money += self.beerDefaultPrice
        self.assertEqual(money, npc.possession.GetMoney()) 
        self.assertFalse(npc.possession.HasResources([latrappe.Beer]))



if __name__ == '__main__':
    unittest.main()

