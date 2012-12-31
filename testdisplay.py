'''
Test for game statistics display module
'''
import os, sys
import pygame
import math
import latrappe
from tiledisplay import *
from pygame.locals import *
from display import *
from world import *

class TestDisplay:
    def run(self):
        pygame.init()
        screen = pygame.display.set_mode((800, 600))
        clock = pygame.time.Clock()
        self.world = World()
        self.world.load_file("level.map")

        self.statdisplay = Display(screen)
        self.tiledisplay = TileDisplay(screen, self.world)
        self.window = self.statdisplay

        self.olutta = 100
        self.kaljaa = 50
        self.meat = 0
        self.grain = 0
        self.beer = 0

        latrappe.ResourceFactory.resourceCreatedSubscribers.append(self)
        self.CreateTestVillage()
        latrappe.Npc.defaultFoodConsumption = 0 #no food problems :)
        self.testBars()
        while 1:
            screen.fill((0,0,0))
            self.window.reset()
            self.testText()
            
            #self.testNPC()
            self.statdisplay.visualizeNPCs(self.city.GetNpcs())

            #self.UpdateVillage()
            for npc in self.city.GetNpcs():
                npc.Advance(15)

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

    def CreateTestVillage(self):
        npcs = []
        self.city = latrappe.City()
        npcHunter = latrappe.Npc(latrappe.Hunter())
        npcs.append(npcHunter)
        self.npcFarmer = latrappe.Npc(latrappe.Farmer())
        npcs.append(self.npcFarmer)
        self.npcBrewer = latrappe.Npc(latrappe.Brewer())
        npcs.append(self.npcBrewer)
        self.stock = latrappe.StockMarket()

        #set prices
        self.stock.SetPrice(latrappe.Grain, 10)
        self.stock.SetPrice(latrappe.Meat, 15)
        self.stock.SetPrice(latrappe.Beer, 50)
        #add some stuff to stock
        for i in range(50):
            self.stock.possession.AddResource(latrappe.Meat())
        self.stock.possession.AddResource(latrappe.Grain())
        self.stock.possession.AddResource(latrappe.Grain())
        self.stock.possession.AddResource(latrappe.Grain())
        self.stock.possession.AddResource(latrappe.Grain())

        self.city.AddStockMarket(self.stock)
        for n in npcs:
            n.possession.money = 100
            n.SetStrategy(latrappe.NpcStrategySimpleGreedy(n))
            self.city.AddNpc(n)
        

#    def UpdateVillage(self):
#        #farmer sells grain when he has more than two ready
#        if self.npcFarmer.possession.HasResources([latrappe.Grain, latrappe.Grain, latrappe.Grain]):
#            grain = self.npcFarmer.possession.GetResource(latrappe.Grain)
#            self.npcFarmer.possession.GiveResource(grain, self.npcBrewer.possession)
#            self.npcBrewer.possession.GiveMoney(self.stock.GetPrice(latrappe.Grain), self.npcFarmer.possession)
    
    def OnResourceCreated(self, resource):
        print "Resource created!"
        if isinstance(resource, latrappe.Meat):
            self.meat += 1
        elif isinstance(resource, latrappe.Grain):
            self.grain += 1
        elif isinstance(resource, latrappe.Beer):
            self.beer += 1

    def testBars(self):
        self.olutta += 1
        self.kaljaa -= 1
        if (self.olutta > 200):
            self.olutta = 0

        if (self.kaljaa < 0):
            self.kaljaa = 160
        
        group2 = BarGroup(int(300), int(300))
        group2.addBar("Kinkkua", 150, 1000, (128,192,64))        
        group2.addBar("Viljaa", self.olutta, 2000, (192,225,50))
        group2.addBar("Toolsseja", self.kaljaa, 200, (64,32,192))
        self.window.addBarGroup(group2)
        
        group = BarGroup(int(200), int(100))
        group.addBar("Beer", self.beer, 160, (32, 255, 32)) 
        group.addBar("Grain", self.grain, 200, (255, 64, 0))
        group.addBar("Meat", self.meat, 160, (32, 255, 32)) 
        self.statdisplay.addBarGroup(group)

    def testText(self):
        self.statdisplay.addText("La Trappen markkinahinta: 12")

if __name__ == "__main__":
    test = TestDisplay()
    test.run()
