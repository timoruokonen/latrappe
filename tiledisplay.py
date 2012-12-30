'''
Tile display module
'''
import os, sys
import pygame
from pygame.locals import *
from resource import *

if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'

class TileDisplay:
    def __init__(self, screen, world):
        self.width = screen.get_width()
        self.height = screen.get_height()
        self.screen = screen
        self.font = pygame.font.Font(None, 17)
        self.titleFont = pygame.font.Font(None, 40)
        self.world = world

    def drawMap(self, screen):
    	self.world.draw(screen)

    def draw(self):
    	self.drawMap(self.screen)
        pygame.display.update()

    def reset(self):
    	pass