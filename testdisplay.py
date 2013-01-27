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
from latrappe.player import Player
from latrappe.animal import Animal


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
        self.initStatDisplay(self.statdisplay)
        self.window = self.statdisplay
        #self.camera_movement = (0,0)
        self.time = 0
        self.player = self.city.get_controlled_player()

        Npc.defaultFoodConsumption = 0 #no food problems :)
        #self.testBars()
        while 1:
            screen.fill((0,0,0))
            self.window.reset()
            self.testText()
            
            #self.testNPC()
            self.statdisplay.visualizeNPCs(self.city.npcs)

            #self.UpdateVillage()
            self.moveNpcs()
            for npc in self.city.npcs:
                npc.advance(5)

            for player in self.city.players:
                player.advance(5)

            for animal in self.city.animals:
                animal.advance(5)

            #self.moveCamera()
            self.window.advance(self.time)
            self.window.draw()
            pygame.display.update()

            msElapsed = clock.tick(30)
            self.time += 30
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if (event.key == K_ESCAPE):
                        pygame.quit()
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
                        self.player.move(2, 0)

                    if (event.key == K_LEFT):
                        self.player.move(-2, 0)

                    if (event.key == K_UP):
                        self.player.move(0, -2)

                    if (event.key == K_DOWN):
                        self.player.move(0, 2)

    def CreateTestVillage(self):
        loader = Loader()
        self.city = loader.load_city('city.txt')
        self.city.add_player(Player())
        self.city.add_animal(Animal(200, 200))
        self.city.add_animal(Animal(200, 240))
        self.city.add_animal(Animal(245, 205))
        return self.city

    def initStatDisplay(self, disp):
        for stock in self.city.stocks:
            disp.addStock(stock)

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
        return
        for npc in self.city.npcs:
            x_movement = random.randint(-1, 1)
            y_movement = random.randint(-1, 1)
            npc.x += x_movement
            npc.y += y_movement

    #def moveCamera(self):
        #self.tiledisplay.camerax += self.camera_movement[0]
        #self.tiledisplay.cameray += self.camera_movement[1]

    def randomizeNpcLocations(self):
        for npc in self.city.npcs:
            npc.x = random.randint(0, SCREEN_WIDTH)
            npc.y = random.randint(0, SCREEN_HEIGHT)       

if __name__ == "__main__":
    test = TestDisplay()
    test.run()
