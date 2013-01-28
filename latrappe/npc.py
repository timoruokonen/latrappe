from schedule import Schedule
from possession import Possession
from action import *

'''
Game NPC. Each NPC instance must be advanced when the game is advanced. 
'''
class Npc(object):
    SLEEP_DURATION = 7 * 60
    DEFAULT_FOOD_CONSUMPTION = 1 #amount of food needed per unit of time (now minute...)

    def __init__(self, occupation, name="Unknown"):
        self.occupation = occupation
        self.occupation.npc = self
        self.schedule = Schedule()
        #TODO: Cannot think... just advance schedule so that it is already done when Advance is called the first time...
        self.schedule.advance(Schedule.MAX_TIME)
        self.possession = Possession()
        self.hungerLevel = 24 * 60 #enough for one day
        self.food_consumption = Npc.DEFAULT_FOOD_CONSUMPTION
        self.alive = True
        self.strategy = None
        self.city = None
        self.x = 100
        self.y = 100
        self.home_x = 0
        self.home_y = 0
        self.name = name

    def print_status(self):
        if not self.alive:
            print "Npc is DEAD!"
        print "Npc (" + str(self.occupation) + ") has " + str(self.possession.money) + " money, owns:"
        for pos in self.possession.resources:
            print pos

    #TODO: How to handle time advancing. Now advancing goes fine if the time interval is smalles possible.
    #If the interval is increased, first schedule is advanced and then food. This leads to not wanted scenarios
    #where npc can do work without food.
    def advance(self, time):
        while (time > 0):
            if not self.alive:
                return

            #Day is completed, create new schedule
            if (self.schedule.is_done()):
                self.create_schedule()
            
            timeLeft = self.schedule.advance(time) 
            self._consume_food(time - timeLeft)
            time = timeLeft
 
    def create_schedule(self):
        self.schedule = Schedule()
        if self.strategy == None:
            self._add_mandatory_actions()
            self.occupation.add_default_schedule(self, self.possession)
        else:
            self._add_mandatory_actions()
            self.strategy.create_schedule()

    def _consume_food(self, time):
        while (time > 0):
            if (self.hungerLevel <= 0):
                foods = self.possession.get_foods()
                if len(foods) == 0:
                    self.alive = False
                    print "NPC (" + str(self.occupation) + ") died from hunger!"
                    return
                #just eat the first thing from the inventory...
                self.possession.destroy_resource(foods[0])
                self.hungerLevel += foods[0].NUTRITIONAL_VALUE
            consumedAmount = min(time, self.hungerLevel)
            self.hungerLevel -= consumedAmount * self.food_consumption            
            time -= consumedAmount

    def _add_mandatory_actions(self):
        self.schedule.add_action(Action("Sleep", Npc.SLEEP_DURATION))




