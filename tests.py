from resource import *
import unittest

class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        pass

    def test_farmer_creates_grain(self):
        npc = Npc(Farmer())
        self.assertEqual(0, len(npc.possession.resources))
        npc.Advance(7 * 60) #sleeping time
        npc.Advance(7 * 60) #farming time
        self.assertEqual(1, len(npc.possession.resources))
        self.assertTrue(npc.possession.HasResources([Grain]))


    def test_brewer_creates_beer(self):
        npc = Npc(Brewer())
        npc.possession.AddResource(Grain())
        npc.possession.AddResource(Grain())
        self.assertEqual(2, len(npc.possession.resources))
        npc.Advance(7 * 60) #sleeping time
        npc.Advance(7 * 60) #brewing time
        self.assertEqual(1, len(npc.possession.resources))
        self.assertTrue(npc.possession.HasResources([Beer]))

        #start next day and give more resources (one extra grain)
        npc.possession.AddResource(Grain())
        npc.possession.AddResource(Grain())
        npc.possession.AddResource(Grain())
        npc.Advance(10 * 60) #rest of the day
        npc.Advance(7 * 60) #sleeping time
        npc.Advance(7 * 60) #brewing time
        self.assertEqual(3, len(npc.possession.resources))
        self.assertTrue(npc.possession.HasResources([Beer, Beer, Grain]))

    def test_brewer_cannot_brew_when_out_of_resources(self):
        npc = Npc(Brewer())
        #brewing needs to grains, only one is given       
        npc.possession.AddResource(Grain())
        npc.Advance(7 * 60) #sleeping time
        npc.Advance(7 * 60) #brewing time
        self.assertEqual(1, len(npc.possession.resources))
        self.assertTrue(npc.possession.HasResources([Grain]))




if __name__ == '__main__':
    unittest.main()

