import pygame
from TileUtils import *
from AnimatedSprite import AnimatedSprite
from latrappe import *

class AnimalRenderer:

    def __init__(self, surface, tile_width=32, tile_height=32):
        self.MAP_TILE_WIDTH = tile_width
        self.MAP_TILE_HEIGHT = tile_height
        # TODO: Change player image
        self.animal_img = pygame.image.load("sheep.png")
        self.surface = surface

    def draw(self, animal):
        #print "drawing player"
        self.surface.blit(self.animal_img, (animal.x, animal.y))
