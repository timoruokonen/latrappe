'''
Tile display module
'''
import os, sys
import pygame
from pygame.locals import *
from latrappe import *
import ConfigParser
from AnimatedSprite import AnimatedSprite

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

        # FIXME: Just test images for now
        self.npcimage = pygame.image.load("duff.png").convert()
        self.animation_images = self.load_sliced_sprites(32, 32, 'monk.png')
        self.npc_animated_img = AnimatedSprite(self.animation_images, 30)

        self.MAP_TILE_WIDTH = 32
        self.MAP_TILE_HEIGHT = 32
        self.MAP_CACHE = {
        'tiles.png': self.loadTileTable('tiles.png', self.MAP_TILE_WIDTH, self.MAP_TILE_HEIGHT),
        }
        self.loadFile(city.filename)
        self.camerax = 0
        self.cameray = 0
        self.mapsurface = pygame.Surface((self.mapwidth*self.MAP_TILE_WIDTH, self.mapheight*self.MAP_TILE_HEIGHT))

        self.npc_anim = {}
        self.stock_items_position = { 0:(0,0), 1:(1,0), 2:(0,1), 3:(1,1), 4:(-1,0), 5:(0,-1), 6:(-1,-1) }


    def init_npc_anim(self):
    	npcs = self.city.get_npcs()
    	#for npc in npcs:
    	#	self.npc_anim.append((npc))  	

    def advance(self, time):
    	self.npc_animated_img.update(time)

    def draw_npcs(self):
    	npcs = self.city.get_npcs()
    	for npc in npcs:
            self.mapsurface.blit(self.npc_animated_img.image, (npc.x,npc.y))

    def draw(self):
    	# Draw all the stuff into one big surface buffer
    	self.draw_city()
    	#self.drawNpcs()

    	# Blit visible part of buffer onto screen
    	self.screen.blit(self.mapsurface, (-self.camerax,-self.cameray))

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

    def draw_city(self):
        self.draw_tiles()
        self.draw_npcs()
        self.draw_stocks()

    def draw_stocks(self):
        stocks = self.city.get_stock_markets()
        for stock in stocks:
            possession = stock.possession
            resources = possession.get_resource_types()
            index = 0
            for resource in resources:
                count = possession.get_resource_count(resource)
                x, y = self.get_next_stock_item_pos(stock, index)
                self.draw_stock_item(resource, (x,y), count)
                index += 1


    def get_next_stock_item_pos(self, stock, index):
        x, y = self.stock_items_position[index]
        x *= self.MAP_TILE_WIDTH
        y *= self.MAP_TILE_HEIGHT
        x += stock.x
        y += stock.y
        #print 'Index: ' + str(index) + ' gave coordinates: ' + str(x) + ',' + str(y)
        return x, y

    def draw_stock_item(self, resource, pos, count):
        stock_image = pygame.image.load("default_resource.png")
        if resource == Beer:
            stock_image = pygame.image.load("beerkeg.png")
        if resource == Grain:
            stock_image = pygame.image.load("grain.png")
        if resource == Meat:
            stock_image = pygame.image.load("meat.png")

        self.mapsurface.blit(stock_image, pos)

        text = self.font.render(str(count), True, (255,255, 255))
        textRect = text.get_rect()
        textRect.left = pos[0] + (self.MAP_TILE_WIDTH / 2)
        textRect.top = pos[1] + (self.MAP_TILE_HEIGHT / 2)

        self.mapsurface.blit(text, textRect)


    def draw_tiles(self):
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

    def load_sliced_sprites(self, w, h, filename):
        images = []
        master_image = pygame.image.load(filename).convert_alpha()

        master_width, master_height = master_image.get_size()
        for y in xrange(int(master_height/h)):
            for i in xrange(int(master_width/w)):
    	        images.append(master_image.subsurface(i*w,y*h,w,h))

    	print 'Image count:' + str(len(images))
        return images

        
