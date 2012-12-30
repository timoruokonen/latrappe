from resource import *
import unittest

class TestSequenceFunctions(unittest.TestCase):
    advanceInterval = 1

    def setUp(self):
        self.grainDefaultPrice = 20
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
        self.assertEqual(1, len(npc.possession.resources))
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
        self.assertEqual(1, len(npc.possession.resources))
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
        #npc has food for one day by default and produces one food per day (one day ration)
        #so npc is self contained, advance one week. 
        self.AdvanceNpc(npc, Schedule.MaxTime * 7)
        self.assertEqual(1, len(npc.possession.resources))
        self.assertTrue(npc.possession.HasResources([Meat]))
        self.assertTrue(npc.IsAlive())
        #starting of next day, npc should have to eat the meat it produced last day       
        self.AdvanceNpc(npc, Schedule.MaxTime / 4)
        self.assertEqual(0, len(npc.possession.resources))
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
        self.assertTrue(stock.SellResource(beer, npc.possession)) 
        self.assertEqual(0, len(npc.possession.resources))
        self.assertEqual(self.beerDefaultPrice, npc.possession.GetMoney()) 
        self.assertEqual(1, len(stock.possession.resources))
        self.assertTrue(stock.possession.HasResources([Beer]))


if __name__ == '__main__':
    unittest.main()

