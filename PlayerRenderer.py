import pygame
from TileUtils import *
from AnimatedSprite import AnimatedSprite
from latrappe import *

class PlayerRenderer:

    def __init__(self, surface, tile_width=32, tile_height=32):
        self.MAP_TILE_WIDTH = tile_width
        self.MAP_TILE_HEIGHT = tile_height
        # TODO: Change player image
        self.player_img = pygame.image.load("player.png")
        self.surface = surface

    def draw(self, player):
        #print "drawing player"
        self.surface.blit(self.player_img, (player.x, player.y))
