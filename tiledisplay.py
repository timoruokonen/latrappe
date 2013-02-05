'''
Tile display module
'''
import os, sys
import struct
import pygame
from pygame.locals import *
from latrappe import *
import ConfigParser
from AnimatedSprite import AnimatedSprite
from npcrenderer import NpcRenderer
from PlayerRenderer import PlayerRenderer
from AnimalRenderer import AnimalRenderer

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

        self.MAP_TILE_WIDTH = 32
        self.MAP_TILE_HEIGHT = 32
        self.MAP_CACHE = {
        'tiles.png': self.loadTileTable('tiles.png', self.MAP_TILE_WIDTH, self.MAP_TILE_HEIGHT),
        }
        self.mapfile = "level.l1"
        self.map = []
        self.loadMap()
        #self.loadFile(city.filename)
        self.camerax = 0
        self.cameray = 0
        

        self.stock_items_position = { 0:(0,0), 1:(1,0), 2:(0,1), 3:(1,1), 4:(-1,0), 5:(0,-1), 6:(-1,-1) }

        self.npc_renderer = NpcRenderer(self.mapsurface)
        self.player_renderer = PlayerRenderer(self.mapsurface)
        self.animal_renderer = AnimalRenderer(self.mapsurface)
        # Camera margin from edge of screen (pixels)
        self.CAMERA_MARGIN = 100
        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = 600

    def change_map(self, map):
        self.map = map

    def init_npc_anim(self):
        npcs = self.city.npcs
        #for npc in npcs:
        #   self.npc_anim.append((npc))     

    def advance(self, time):
        self.npc_renderer.update(time)

    def draw_npcs(self):
        for npc in self.city.npcs:
            self.npc_renderer.draw_npc(npc)
            # Npc image

    def draw_players(self):
        for player in self.city.players:
            self.player_renderer.draw(player)

    def draw_animals(self):
        for animal in self.city.animals:
            self.animal_renderer.draw(animal)

    def draw_properties(self):
        for property in self.city.real_properties:
            self.draw_property_item(property)

    def draw_property_item(self, property):
        if type(property) == FieldSquare:
            status = property.status
            if property.in_progress:
                status = property.next_status()
            if status == FieldSquare.STATUS_PLOUGHED:
                image = pygame.image.load("field_plowed.png")
            elif status == FieldSquare.STATUS_SOWED:
                image = pygame.image.load("field_sowed.png")
            elif status == FieldSquare.STATUS_READY_TO_BE_HARVESTED:
                image = pygame.image.load("field_ready_harvest.png")
            elif status == FieldSquare.STATUS_HARVESTED:
                image = pygame.image.load("field_harvested.png")
            self.mapsurface.blit(image, [property.x, property.y])
        elif type(property) == BeerKettle:
            status = property.status
            if property.in_progress:
                status = property.next_status()
            if status == BeerKettle.STATUS_MALTED:
                image = pygame.image.load("brew_malted.png")
            elif status == BeerKettle.STATUS_MASHED:
                image = pygame.image.load("brew_mashed.png")
            elif status == BeerKettle.STATUS_BOILED:
                image = pygame.image.load("brew_boiled.png")
            elif status == BeerKettle.STATUS_FERMENTED:
                image = pygame.image.load("brew_fermented.png")
            elif status == BeerKettle.STATUS_CONDITIONED:
                image = pygame.image.load("brew_conditioned.png")
            elif status == BeerKettle.STATUS_PACKAGED:
                image = pygame.image.load("brew_packaged.png")
            self.mapsurface.blit(image, [property.x, property.y])

    def draw(self):
        self.adjust_camera()
        # Draw all the stuff into one big surface buffer
        self.draw_city()
        #self.drawNpcs()

        # Blit visible part of buffer onto screen
        self.screen.blit(self.mapsurface, (-self.camerax,-self.cameray))

    def move_camera(self, x, y):
        self.camerax += x
        self.cameray += y

    def adjust_camera(self):
        player = self.city.get_controlled_player()
        if player == None:
            return
            
        camera_speed = abs(player.speed_x + player.speed_y)
        if player.x > (self.camerax + self.SCREEN_WIDTH - self.CAMERA_MARGIN):
            self.camerax += camera_speed

        if (player.x < (self.camerax + 0 + self.CAMERA_MARGIN)):
            self.camerax -= camera_speed

        if player.y > (self.cameray + self.SCREEN_HEIGHT - self.CAMERA_MARGIN):
            self.cameray += camera_speed

        if (player.y < (self.cameray + 0 + self.CAMERA_MARGIN)):
            self.cameray -= camera_speed


    def reset(self):
        pass

    def loadTileTable(self, filename, width, height):
        image = pygame.image.load(filename).convert()
        image_width, image_height = image.get_size()
        tile_table = []
        for tile_x in range(0, image_width/width):
            #line = []
            #tile_table.append(line)
            for tile_y in range(0, image_height/height):
                rect = (tile_x*width, tile_y*height, width, height)
                tile_table.append(image.subsurface(rect))
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

    def loadMap(self):
        self.tileset = "tiles.png"
        print "Loading map file: " + self.mapfile
        with open(self.mapfile, 'rb') as f:
            self.mapwidth = struct.unpack('>H', f.read(2))[0]
            self.mapheight = struct.unpack('>H', f.read(2))[0]
            print "Map width: " + str(self.mapwidth) + " height: " + str(self.mapheight)
            self.map = [[0 for x in xrange(self.mapheight)] for x in xrange(self.mapwidth)] 
            data = f.read()
            print "Loaded map bytes: " + str(len(data))
            data = struct.unpack(str(len(data)) + "B", data)
            #print "Unpacked: " + str(data)
            y = 0
            for x, tile in enumerate(data):
                y = x / self.mapwidth

                if y >= self.mapheight:
                    break

                print "X,Y ",x,y
                self.map[x % (self.mapwidth)][y] = tile

        print str(self.map)
        self.mapsurface = pygame.Surface((800,600))

    def draw_city(self):
        self.draw_tiles()
        self.draw_properties()
        self.draw_npcs()
        self.draw_stocks()
        self.draw_animals()
        self.draw_players()

    def draw_stocks(self):
        for stock in self.city.stocks:
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

    def get_tile(self, x, y):
        """Tell what's at the specified position of the map."""

        try:
            char = self.map[y][x]
        except IndexError:
            return {}
        try:
            return self.key[char]
        except KeyError:
            return {}

    def get_bool(self, x, y, name):
        """Tell if the specified flag is set for position on the map."""

        value = self.get_tile(x, y).get(name)
        return value in (True, 1, 'true', 'yes', 'True', 'Yes', '1', 'on', 'On')

    def is_wall(self, x, y):
        """Is there a wall?"""

        return self.get_bool(x, y, 'wall')

    def is_blocking(self, x, y):
        """Is this place blocking movement?"""

        if not 0 <= x < self.width or not 0 <= y < self.height:
            return True
        return self.get_bool(x, y, 'block')

    def draw_tiles(self):
        #print "Drawing screen"
        tiles = self.MAP_CACHE[self.tileset]
        for x, line in enumerate(self.map):
            for y, tile in enumerate(line):
            #print "Tile: " + str(tile)
                self.mapsurface.blit(tiles[tile], (x*self.MAP_TILE_WIDTH, y*self.MAP_TILE_HEIGHT))


    def draw_tiles_old(self):
        tiles = self.MAP_CACHE[self.tileset]
        wall = self.is_wall
        #print 'Tiles length' + str(len(tiles))
        for map_y, line in enumerate(self.map):
            for map_x, c in enumerate(line):
                try:
                    tile = self.key[c]['tile'].split(',')
                    tile = int(tile[0]), int(tile[1])
                    #print str(tile)
                    if wall(map_x, map_y):
                        #print "Wall!"
                        if not wall(map_x, map_y-1):
                            if not wall(map_x-1, map_y):
                                tile = int(tile[0])+1, int(tile[1])
                            elif not wall(map_x+1, map_y):
                                tile = int(tile[0])+2, int(tile[1])
                        elif not wall(map_x, map_y+1):
                            if not wall(map_x-1, map_y):
                                tile = int(tile[0])+3, int(tile[1])
                            elif not wall(map_x+1, map_y):
                                tile = int(tile[0])+4, int(tile[1])
                    else:
                        #print "Not a Wall!"
                        # Normal tile
                        tile = int(tile[0]), int(tile[1])
                except (ValueError, KeyError):
                    # Default to ground tile
                    print 'Tile key error, using default tile'
                    tile = 0, 3

                #print 'tile: ' + str(tile[0]) + ',' + str(tile[1])
                tile_image = tiles[tile[0]][tile[1]]
                self.mapsurface.blit(tile_image, (map_x*self.MAP_TILE_WIDTH, map_y*self.MAP_TILE_HEIGHT))



        
