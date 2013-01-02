'''
Test for game statistics display module
'''
import os, sys
import pygame
import math
import random
from latrappe import *
from tiledisplay import *
from pygame.locals import *
from display import *

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

class TestDisplay:
    def run(self):
        pygame.init()
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        icon = pygame.image.load("icon.png").convert()
        pygame.display.set_icon(icon)
        pygame.display.set_caption("La Trappe")
        clock = pygame.time.Clock()

        self.olutta = 100
        self.kaljaa = 50
        self.meat = BarAmount(0)
        self.grain = BarAmount(0)
        self.beer = BarAmount(0)

        ResourceFactory.resource_created_subscribers.append(self)
        ResourceFactory.resource_destroyed_subscribers.append(self)

        self.CreateTestVillage()
        self.randomizeNpcLocations()
        self.tiledisplay = TileDisplay(screen, self.city)
        self.statdisplay = Display(screen)
        self.window = self.statdisplay
        self.camera_movement = (0,0)

        Npc.defaultFoodConsumption = 0 #no food problems :)
        self.testBars()
        while 1:
            screen.fill((0,0,0))
            self.window.reset()
            self.testText()
            
            #self.testNPC()
            self.statdisplay.visualizeNPCs(self.city.GetNpcs())

            #self.UpdateVillage()
            self.moveNpcs()
            for npc in self.city.GetNpcs():
                npc.Advance(15)

            self.moveCamera()
            self.window.draw()

            msElapsed = clock.tick(30)
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if (event.key == K_ESCAPE):
                        sys.exit()
                        window.reset()
                    if (event.key == K_1):
                        print 'Switching to tile display.'
                        self.window = self.tiledisplay
                        # Show tile display
                        pass
                    if (event.key == K_2):
                        print 'Switching to statistics display.'
                        self.window = self.statdisplay
                        # Show statistics display
                        pass
                    if (event.key == K_RIGHT):
                        self.camera_movement = (1,0)

                    if (event.key == K_LEFT):
                        self.camera_movement = (-1,0)

                    if (event.key == K_UP):
                        self.camera_movement = (0,-1)

                    if (event.key == K_DOWN):
                        self.camera_movement = (0,1)

    def CreateTestVillage(self):
        npcs = []
        self.city = City()
        npcs.append(Npc(Farmer()))
        npcs.append(Npc(Farmer()))
        npcs.append(Npc(Farmer()))
        npcs.append(Npc(Hunter()))
        npcs.append(Npc(Brewer()))
        self.stock = StockMarket()

        #set prices
        self.stock.set_price(Grain, 10)
        self.stock.set_price(Meat, 15)
        self.stock.set_price(Beer, 50)
        #add some stuff to stock
        for i in range(50):
            self.stock.possession.add_resource(ResourceFactory.create_resource(Meat, self.stock.possession))
        self.stock.possession.add_resource(ResourceFactory.create_resource(Grain, self.stock.possession))
        self.stock.possession.add_resource(ResourceFactory.create_resource(Grain, self.stock.possession))

        self.city.AddStockMarket(self.stock)
        for n in npcs:
            n.possession.money = 100
            n.SetStrategy(NpcStrategySimpleGreedy(n))
            self.city.AddNpc(n)
        
        return self.city

#    def UpdateVillage(self):
#        #farmer sells grain when he has more than two ready
#        if self.npcFarmer.possession.HasResources([Grain, Grain, Grain]):
#            grain = self.npcFarmer.possession.GetResource(Grain)
#            self.npcFarmer.possession.GiveResource(grain, self.npcBrewer.possession)
#            self.npcBrewer.possession.GiveMoney(self.stock.GetPrice(Grain), self.npcFarmer.possession)
    
    def on_resource_created(self, resource):
        print "created resource " + str(resource)
        if isinstance(resource, Meat):
            self.meat.AddAmount(1)
        elif isinstance(resource, Grain):
            self.grain.AddAmount(1)
        elif isinstance(resource, Beer):
            self.beer.AddAmount(1)

    def on_resource_destroyed(self, resource):
        if isinstance(resource, Meat):
            self.meat.AddAmount(-1)
        elif isinstance(resource, Grain):
            self.grain.AddAmount(-1)
        elif isinstance(resource, Beer):
            self.beer.AddAmount(-1)

    def testBars(self):
        self.olutta += 1
        self.kaljaa -= 1
        if (self.olutta > 200):
            self.olutta = 0

        if (self.kaljaa < 0):
            self.kaljaa = 160
        
        #group2 = BarGroup(int(300), int(300))
        #group2.addBar("Kinkkua", 150, 1000, (128,192,64))        
        #group2.addBar("Viljaa", self.olutta, 2000, (192,225,50))
        #group2.addBar("Toolsseja", self.kaljaa, 200, (64,32,192))
        #self.window.addBarGroup(group2)
        
        group = BarGroup(int(200), int(100))
        group.addBar("Beer", self.beer, 160, (32, 255, 32)) 
        group.addBar("Grain", self.grain, 200, (255, 64, 0))
        group.addBar("Meat", self.meat, 160, (32, 255, 32)) 
        self.statdisplay.addBarGroup(group)

    def testText(self):
        self.statdisplay.addText("La Trappen markkinahinta: 12")

    def moveNpcs(self):
        npcs = self.city.GetNpcs()
        for npc in npcs:
            x_movement = random.randint(-1, 1)
            y_movement = random.randint(-1, 1)
            npc.x += x_movement
            npc.y += y_movement

    def moveCamera(self):
        self.tiledisplay.camerax += self.camera_movement[0]
        self.tiledisplay.cameray += self.camera_movement[1]

    def randomizeNpcLocations(self):
        npcs = self.city.GetNpcs()
        for npc in npcs:
            npc.x = random.randint(0, SCREEN_WIDTH)
            npc.y = random.randint(0, SCREEN_HEIGHT)       

if __name__ == "__main__":
    test = TestDisplay()
    test.run()
