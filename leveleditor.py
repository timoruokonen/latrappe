'''
Level editor
'''
import os, sys
import pygame
import math
import random
import struct
import pygame.mouse
from latrappe import *
from tiledisplay import *
from pygame.locals import *
from display import *
from latrappe.player import Player
from latrappe.animal import Animal

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

CURSOR_COLOR = (255, 255, 255)

class LevelEditor:

    editmodes = ["ADD_TILE", "ADD_OBJECT", "CURSOR"]
    
    def start(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        icon = pygame.image.load("icon.png").convert()
        pygame.display.set_icon(icon)
        pygame.display.set_caption("La Trappe - Level editor")
        self.TILE_WIDTH = 32
        self.TILE_HEIGHT = 32
        self.selectedTile = 1
        self.filename = "level.l1"
        #self.city = City()
        loader = Loader()
        self.city = loader.load_city('city.txt')
        self.display = TileDisplay(self.screen, self.city)
        self.cursor = (0, 0)
        self.map = self.display.map
        #print str(self.map)

        self.editmode = "CURSOR"
        while 1:
            self.screen.fill((0,0,0))

            for event in pygame.event.get():
                # Keyboard handling
                if event.type == KEYDOWN:
                    if (event.key == K_ESCAPE):
                        pygame.quit()
                        sys.exit()
                    if (event.key == K_1):
                        pass
                    if (event.key == K_2):
                        pass
                    if (event.key == K_RIGHT):
                        self.display.move_camera(192,0)

                    if (event.key == K_LEFT):
                        self.display.move_camera(-192,0)

                    if (event.key == K_UP):
                        self.display.move_camera(0,-192)

                    if (event.key == K_DOWN):
                        self.display.move_camera(0,192)

                    if (event.key == K_SPACE):
                        self.do_action()

                    if (event.key == K_t):
                        print "Add tile mode"
                        self.editmode = "ADD_TILE"
                        self.choose_tile()

                    if (event.key == K_s):
                        print "Saving map"
                        self.save_map()

                    if (event.key == K_PAGEUP):
                        #print "Selecting next tile"
                        tiles = self.display.MAP_CACHE[self.display.tileset]
                        tile = self.selectedTile + 1
                        if tile > (len(tiles) - 1):
                            tile = 0

                        self.selectedTile = tile
                        print "Selected tile: " + str(tile)

                    if (event.key == K_PAGEDOWN):
                        #print "Selecting next tile"
                        tiles = self.display.MAP_CACHE[self.display.tileset]
                        tile = self.selectedTile - 1
                        if tile < 0:
                            tile = len(tiles) - 1

                        self.selectedTile = tile
                        print "Selected tile: " + str(tile)

                # Mouse handling
                elif event.type == MOUSEBUTTONUP:
                    mousex, mousey = pygame.mouse.get_pos()
                    print "Mouse clicked: " + str(mousex) + "," + str(mousey)
                    self.do_action()


            self.display.draw()
            self.draw_overlays()
            pygame.display.update()

    def draw_overlays(self):
        # Draw cursor
        pygame.draw.rect(self.screen, CURSOR_COLOR, Rect(self.cursor, (self.TILE_WIDTH, self.TILE_HEIGHT)), 1)

        # Draw current tile
        tiles = self.display.MAP_CACHE[self.display.tileset]
        tile_image = tiles[self.selectedTile]
        self.screen.blit(tile_image, (0, 0))
        pygame.draw.rect(self.screen, CURSOR_COLOR, Rect((0,0), (self.TILE_WIDTH, self.TILE_HEIGHT)), 1)

    def do_action(self):
        print "Doing action: " + self.editmode
        if self.editmode == "CURSOR":
            self.select()

        elif self.editmode == "ADD_TILE":
            self.add_tile()

    def save_map(self):
        f = open(self.filename, 'wb')
        print "Writing map width: " + str(self.display.mapwidth) + " height: " + str(self.display.mapheight)
        width = struct.pack('>h', self.display.mapwidth)
        height = struct.pack('>h', self.display.mapwidth)
        f.write(width)
        f.write(height)
        for y in xrange(self.display.mapheight):
            print "Y is " + str(y)
            for line in self.display.map:
                tilepacked = struct.pack('B', line[y])
                print "line[y]: " + str(line[y])
                f.write(tilepacked)
            

        f.close()

    def choose_tile(self):
        pass

    def add_tile(self):
        self.select()
        tilex, tiley = self.get_nearest_tile(self.cursor[0], self.cursor[1])
        self.map[tilex][tiley] = self.selectedTile
        #print str(self.map[tiley])
        #self.map[tiley] = self.map[tiley][:tilex] + "w" + self.map[tiley][tilex+1:]

    def select(self):
        mousex, mousey = pygame.mouse.get_pos()
        tilex, tiley = self.get_nearest_tile(mousex, mousey)
        self.cursor = (tilex * self.TILE_WIDTH, tiley * self.TILE_HEIGHT)

    def get_nearest_tile(self, x, y):
        x = x / self.TILE_WIDTH
        y = y / self.TILE_HEIGHT
        return (x, y)

if __name__ == "__main__":
    editor = LevelEditor()
    editor.start()