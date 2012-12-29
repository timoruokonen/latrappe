from resource import *
import unittest

class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        pass

    def test_farmer_creates_grain(self):
        npc = Npc(Farmer())
        self.assertEqual(0, len(npc.possession.resources))
        npc.Advance(Npc.sleepDuration) #sleeping time
        npc.Advance(Farmer.duration) #farming time
        self.assertEqual(1, len(npc.possession.resources))
        self.assertTrue(npc.possession.HasResources([Grain]))

    def test_hunter_creates_meat(self):
        npc = Npc(Hunter())
        self.assertEqual(0, len(npc.possession.resources))
        npc.Advance(Npc.sleepDuration) #sleeping time
        npc.Advance(Hunter.duration) #action time
        self.assertEqual(1, len(npc.possession.resources))
        self.assertTrue(npc.possession.HasResources([Meat]))

    def test_brewer_creates_beer(self):
        npc = Npc(Brewer())
        npc.possession.AddResource(Grain())
        npc.possession.AddResource(Grain())
        self.assertEqual(2, len(npc.possession.resources))
        npc.Advance(Npc.sleepDuration) #sleeping time
        npc.Advance(Brewer.duration) #brewing time
        self.assertEqual(1, len(npc.possession.resources))
        self.assertTrue(npc.possession.HasResources([Beer]))

        #start next day and give more resources (one extra grain)
        npc.possession.AddResource(Grain())
        npc.possession.AddResource(Grain())
        npc.possession.AddResource(Grain())
        npc.Advance(npc.schedule.GetTotalRemainingTime()) #rest of the day
        npc.Advance(Npc.sleepDuration) #sleeping time
        npc.Advance(Brewer.duration) #brewing time
        self.assertEqual(3, len(npc.possession.resources))
        self.assertTrue(npc.possession.HasResources([Beer, Beer, Grain]))

    def test_action_outputs_are_given_after_task_is_fully_done(self):
        npc = Npc(Hunter())
        self.assertEqual(0, len(npc.possession.resources))
        npc.Advance(Npc.sleepDuration) #sleeping time
        npc.Advance(Hunter.duration / 2) #half of the action time
        self.assertEqual(0, len(npc.possession.resources))
        npc.Advance(Hunter.duration / 2) #half of the action time
        self.assertEqual(1, len(npc.possession.resources))
        self.assertTrue(npc.possession.HasResources([Meat]))


    def test_brewer_cannot_brew_when_out_of_resources(self):
        npc = Npc(Brewer())
        #brewing needs to grains, only one is given       
        npc.possession.AddResource(Grain())
        npc.Advance(Npc.sleepDuration) #sleeping time
        npc.Advance(Brewer.duration) #brewing time
        self.assertEqual(1, len(npc.possession.resources))
        self.assertTrue(npc.possession.HasResources([Grain]))

    def test_advance_over_one_action(self):
        npc = Npc(Farmer())
        self.assertEqual(0, len(npc.possession.resources))
        #advance one full day, both sleeping and farming should be done       
        npc.Advance(Schedule.MaxTime)
        self.assertEqual(1, len(npc.possession.resources))
        self.assertTrue(npc.possession.HasResources([Grain]))

    def test_advance_over_day_ending(self):
        npc = Npc(Farmer())
        self.assertEqual(0, len(npc.possession.resources))
        #advance two full days, two sleepings and farmings should be done       
        npc.Advance(Schedule.MaxTime * 2)
        self.assertEqual(2, len(npc.possession.resources))
        self.assertTrue(npc.possession.HasResources([Grain, Grain]))

if __name__ == '__main__':
    unittest.main()

