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
        while 1:
            screen.fill((0,0,0))
            self.window.reset()
            self.testText()
            self.testBars()
            self.testNPC()
            self.window.draw()

            msElapsed = clock.tick(30)
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if (event.key == K_ESCAPE):
                        sys.exit()
                        window.reset()

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
        group.addBar("LaTrappea", 200, 400)
        group.addBar("Olutta", self.olutta, 200, (255,64,0))
        group.addBar("Kaljaa", self.kaljaa, 160, (32,255,32))
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