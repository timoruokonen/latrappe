'''
Tile display module
'''
import os, sys
import pygame
from pygame.locals import *
from latrappe import *

if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'

class TileDisplay:
    def __init__(self, screen, city):
        self.width = screen.get_width()
        self.height = screen.get_height()
        self.screen = screen
        self.font = pygame.font.Font(None, 17)
        self.titleFont = pygame.font.Font(None, 40)
        self.city = city

    def drawCity(self, screen):
    	self.city.draw(screen)

    def drawNpcs(self, screen):
    	npcs = self.city.GetNpcs()
    	for npc in npcs:
    		npc.draw(screen)

    def draw(self):
    	self.drawCity(self.screen)
    	self.drawNpcs(self.screen)
        pygame.display.update()

    def reset(self):
    	pass