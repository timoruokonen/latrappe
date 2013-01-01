import ConfigParser
import pygame
import pygame.locals

class City(object):
    def __init__(self, filename="level.map"):
        self.npcs = []
        self.stocks = []
        self.MAP_TILE_WIDTH = 32
        self.MAP_TILE_HEIGHT = 32
        self.MAP_CACHE = {
        'tiles.png': self.load_tile_table('tiles.png', self.MAP_TILE_WIDTH, self.MAP_TILE_HEIGHT),
        }
        self.load_file()

    def AddNpc(self, npc):
        npc.SetCity(self)
        self.npcs.append(npc)

    def GetNpcs(self):
        return self.npcs
    
    def AddStockMarket(self, stock):
        self.stocks.append(stock)

    def GetStockMarkets(self):
        return self.stocks

    def load_tile_table(self, filename, width, height):
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

    def load_file(self, filename="level.map"):
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

        self.width = len(self.map[0])
        self.height = len(self.map)

    def draw(self, screen):
        tiles = self.MAP_CACHE[self.tileset]
        #print 'Tiles length' + str(len(tiles))
        image = pygame.Surface((self.width*self.MAP_TILE_WIDTH, self.height*self.MAP_TILE_HEIGHT))
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
                image.blit(tile_image, (map_x*self.MAP_TILE_WIDTH, map_y*self.MAP_TILE_HEIGHT))

        screen.blit(image, (0,0))

