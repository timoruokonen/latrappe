'''
Tile display module
'''
import os, sys
import struct
import pygame
from tmxloader import *
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
    def __init__(self, screen, city, map, sprite_layers):
        # renderer
        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = 600

        self.renderer = helperspygame.RendererPygame()

        # cam_offset is for scrolling
        self.camerax = 400
        self.cameray = 300

        # set initial cam position and size
        self.renderer.set_camera_position_and_size(self.camerax, self.cameray, self.SCREEN_WIDTH, self.SCREEN_HEIGHT)

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
        self.tileset = "tiles.png"
        self.sprite_layers = sprite_layers
        self.map = map
        #self.loadFile(city.filename)
        
        self.stock_items_position = { 0:(0,0), 1:(1,0), 2:(0,1), 3:(1,1), 4:(-1,0), 5:(0,-1), 6:(-1,-1) }
        #w = len(map)
        #h = len(map[0])
        #self.mapsurface = pygame.Surface((self.MAP_TILE_WIDTH*w, self.MAP_TILE_HEIGHT*h))
        self.npc_renderer = NpcRenderer()
        #self.player_renderer = PlayerRenderer(self.mapsurface)
        #self.animal_renderer = AnimalRenderer(self.mapsurface)
        # Camera margin from edge of screen (pixels)
        self.CAMERA_MARGIN = 100
        self.init_npcs()
        

    def change_map(self, map):
        self.map = map 

    def advance(self, time):
        #self.npc_renderer.update(time)
        pass
    
    def init_npcs(self):
        for npc in self.city.npcs:
            print "Adding npc " + str(npc)
            anim = self.npc_renderer.get_npc_anim(npc)
            self.sprite_layers[0].add_sprite(anim)

    def draw_npcs(self):
        pass

    def draw_players(self):
        pass
        #for player in self.city.players:
        #    self.player_renderer.draw(player)

    def draw_animals(self):
        pass
        #for animal in self.city.animals:
        #    self.animal_renderer.draw(animal)

    def draw_properties(self):
        pass
        #for property in self.city.real_properties:
        #    self.draw_property_item(property)

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
        self.renderer.set_camera_position(self.camerax, self.cameray)
        # Draw all the stuff into one big surface buffer
        self.draw_city()
        #self.drawNpcs()

        # Blit visible part of buffer onto screen
        #self.screen.blit(self.mapsurface, (-self.camerax,-self.cameray))

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


    def draw_city(self):
        self.draw_tiles()
        #self.draw_properties()
        #self.draw_npcs()
        #self.draw_stocks()
        #self.draw_animals()
        #self.draw_players()

    def draw_stocks(self):
        return 
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
        # render the map
        for sprite_layer in self.sprite_layers:
            if sprite_layer.is_object_group:
                # we dont draw the object group layers
                # you should filter them out if not needed
                continue
            else:
                self.renderer.render_layer(self.screen, sprite_layer)


        
