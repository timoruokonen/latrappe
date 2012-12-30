'''
Test for game statistics display module
'''
import os, sys
import pygame
import math
from pygame.locals import *
from resource import *
from display import *

class TestDisplay:
    def run(self):
        pygame.init()
        screen = pygame.display.set_mode((800, 600))
        clock = pygame.time.Clock()
        self.window = Display(screen)

        self.olutta = 100
        self.kaljaa = 50
        self.meat = 0
        self.grain = 0
        self.beer = 0

        ResourceFactory.resourceCreatedSubscribers.append(self)
        Npc.defaultFoodConsumption = 0 #no food problems :)
        npcs = self.CreateTestVillage()

        while 1:
            screen.fill((0,0,0))
            self.window.reset()
            self.testText()
            self.testBars()
            self.testNPC()

            self.UpdateVillage()
            for npc in npcs:
                npc.Advance(15)

            self.window.draw()

            msElapsed = clock.tick(30)
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if (event.key == K_ESCAPE):
                        sys.exit()
                        window.reset()

    def CreateTestVillage(self):
        npcs = []
        npcHunter = Npc(Hunter())
        npcs.append(npcHunter)
        self.npcFarmer = Npc(Farmer())
        npcs.append(self.npcFarmer)
        self.npcBrewer = Npc(Brewer())
        npcs.append(self.npcBrewer)
        return npcs

    def UpdateVillage(self):
        #farmer gives grain away when he has more than two ready
        if self.npcFarmer.possession.HasResources([Grain, Grain, Grain]):
            grain = self.npcFarmer.possession.GetResource(Grain)
            self.npcFarmer.possession.ChangeResourceOwner(grain, self.npcBrewer.possession)
    
    def OnResourceCreated(self, resource):
        if isinstance(resource, Meat):
            self.meat += 1
        elif isinstance(resource, Grain):
            self.grain += 1
        elif isinstance(resource, Beer):
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
        self.window.addBarGroup(group)

    def testText(self):
        self.window.addText("La Trappen markkinahinta: 12")

    def testNPC(self):
        npc1 = Npc(Farmer())
        npc2 = Npc(Brewer())
        self.window.visualizeNPC(npc1)
        self.window.visualizeNPC(npc2)

if __name__ == "__main__":
    test = TestDisplay()
    test.run()
