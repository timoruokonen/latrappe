from schedule import Schedule
from possession import Possession
from action import *
import pygame

'''
Game NPC. Each NPC instance must be advanced when the game is advanced. 
'''
class Npc(object):
    sleepDuration = 7 * 60
    defaultFoodConsumption = 1 #amount of food needed per unit of time (now minute...)

    def __init__(self, occupation):
        self.occupation = occupation
        self.schedule = Schedule()
        #TODO: Cannot think... just advance schedule so that it is already done when Advance is called the first time...
        self.schedule.Advance(Schedule.MaxTime)
        self.possession = Possession()
        self.hungerLevel = 24 * 60 #enough for one day
        self.foodConsumption = Npc.defaultFoodConsumption
        self.alive = True
        self.strategy = None
        self.city = None
        self.x = 100
        self.y = 100
        self.image = pygame.image.load("duff.png").convert()

    def PrintStatus(self):
        if not self.alive:
            print "Npc is DEAD!"
        print "Npc (" + str(self.occupation) + ") has " + str(self.possession.money) + " money, owns:"
        for pos in self.possession.resources:
            print pos

    def SetCity(self, city):
        self.city = city

    def GetCity(self):
        return self.city

    def SetStrategy(self, strategy):
        self.strategy = strategy

    #TODO: How to handle time advancing. Now advancing goes fine if the time interval is smalles possible.
    #If the interval is increased, first schedule is advanced and then food. This leads to not wanted scenarios
    #where npc can do work without food.
    def Advance(self, time):
        while (time > 0):
            if not self.alive:
                return

            #Day is completed, create new schedule
            if (self.schedule.IsDone()):
                self.CreateSchedule()
            
            timeLeft = self.schedule.Advance(time) 
            self._ConsumeFood(time - timeLeft)
            time = timeLeft

    def IsAlive(self):
        return self.alive;
            
    def CreateSchedule(self):
        self.schedule = Schedule()
        if self.strategy == None:
            self._AddMandatoryActions()
            self.occupation.AddDefaultSchedule(self.schedule, self.possession)
        else:
            self._AddMandatoryActions()
            self.strategy.CreateSchedule()

    def _ConsumeFood(self, time):
        while (time > 0):
            if (self.hungerLevel <= 0):
                foods = self.possession.GetFoods()
                if len(foods) == 0:
                    self.alive = False
                    print "NPC (" + str(self.occupation) + ") died from hunger!"
                    return
                #just eat the first thing from the inventory...
                self.possession.DestroyResource(foods[0])
                self.hungerLevel += foods[0].nutritionalValue
            consumedAmount = min(time, self.hungerLevel)
            self.hungerLevel -= consumedAmount * self.foodConsumption            
            time -= consumedAmount

    def _AddMandatoryActions(self):
        self.schedule.AddAction(ProduceAction("Sleep", [],[], Npc.sleepDuration, self.possession))

    def draw(self, screen):
        screen.blit(self.image, (self.x,self.y))


