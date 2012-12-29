'''
Test for game statistics display module
'''
import os, sys
import pygame
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

        self.window.addBar("LaTrappea", 200, 400)
        self.window.addBar("Olutta", self.olutta, 200, (255, 64, 0))
        self.window.addBar("Kaljaa", self.kaljaa, 160, (32, 255, 32)) 

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