'''
Tile display module
'''
import os, sys
import pygame
from pygame.locals import *
from latrappe import *
import ConfigParser

if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'

class TileDisplay:
    def __init__(self, screen, city):
        #self.width = screen.get_width()
        #self.height = screen.get_height()
        self.screen = screen
        self.font = pygame.font.Font(None, 17)
        self.titleFont = pygame.font.Font(None, 40)
        self.city = city
        self.npcimage = pygame.image.load("duff.png").convert()
        self.MAP_TILE_WIDTH = 32
        self.MAP_TILE_HEIGHT = 32
        self.MAP_CACHE = {
        'tiles.png': self.loadTileTable('tiles.png', self.MAP_TILE_WIDTH, self.MAP_TILE_HEIGHT),
        }
        self.loadFile(city.filename)
        self.camerax = 0
        self.cameray = 0
        self.mapsurface = pygame.Surface((self.mapwidth*self.MAP_TILE_WIDTH, self.mapheight*self.MAP_TILE_HEIGHT))

    def drawNpcs(self):
    	npcs = self.city.GetNpcs()
    	for npc in npcs:
            self.mapsurface.blit(self.npcimage, (npc.x,npc.y))

    def draw(self):
    	self.drawCity()
    	self.drawNpcs()
    	self.screen.blit(self.mapsurface, (-self.camerax,-self.cameray))
        pygame.display.update()

    def reset(self):
    	pass

    def loadTileTable(self, filename, width, height):
        image = pygame.image.load(filename).convert()
        image_width, image_height = image.get_size()
        tile_table = []
        for tile_x in range(0, image_width/width):
            line = []
            tile_table.append(line)
            for tile_y in range(0, image_height/height):
                rect = (tile_x*width, tile_y*height, width, height)
                line.append(image.subsurface(rect))
        return tile_table

    def loadFile(self, filename="level.map"):
        self.map = []
        self.key = {}
        parser = ConfigParser.ConfigParser()
        parser.read(filename)
        self.tileset = parser.get("level", "tileset")
        self.map = parser.get("level", "map").split("\n")
        for section in parser.sections():
            if len(section) == 1:
                desc = dict(parser.items(section))
                self.key[section] = desc

        self.mapwidth = len(self.map[0]) 
        self.mapheight = len(self.map)

    def drawCity(self):
        tiles = self.MAP_CACHE[self.tileset]
        #print 'Tiles length' + str(len(tiles))
        for map_y, line in enumerate(self.map):
            for map_x, c in enumerate(line):
                try:
                    tile = self.key[c]['tile'].split(',')
                    tile = int(tile[0]), int(tile[1])
                except (ValueError, KeyError):
                    # Default to ground tile
                    print 'Tile key error, using default tile'
                    tile = 0, 3

                #print 'tile: ' + str(tile[0]) + ',' + str(tile[1])
                tile_image = tiles[tile[0]][tile[1]]
                self.mapsurface.blit(tile_image, (map_x*self.MAP_TILE_WIDTH, map_y*self.MAP_TILE_HEIGHT))

        
