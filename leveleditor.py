'''
Level editor
'''
import os, sys
import pygame
import math
import random
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
        self.selectedTile = (0, 0)

        #self.city = City()
        loader = Loader()
        self.city = loader.load_city('city.txt')
        self.display = TileDisplay(self.screen, self.city)
        self.cursor = (0, 0)
        self.map = self.display.map
        print str(self.map)

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
                        pass

                    if (event.key == K_LEFT):
                        pass

                    if (event.key == K_UP):
                        pass

                    if (event.key == K_DOWN):
                        pass

                    if (event.key == K_SPACE):
                        self.do_action()

                    if (event.key == K_t):
                        print "Add tile mode"
                        self.editmode = "ADD_TILE"
                        self.choose_tile()

                    if (event.key == K_PAGEUP):
                        #print "Selecting next tile"
                        tile = (self.selectedTile[0]+1, self.selectedTile[1])
                        tiles = self.display.MAP_CACHE[self.display.tileset]
                        print "len: " + str(len(tiles))
                        if (tile[0] > len(tiles) - 1):
                            tile = (0, self.selectedTile[1]+1)
                            if (tile[1] > len(tiles[0]) - 1):
                                tile = (0, 0)

                        self.selectedTile = tile
                        print "Selected tile: " + str(tile)

                    if (event.key == K_PAGEDOWN):
                        #print "Selecting next tile"
                        tile = (self.selectedTile[0]-1, self.selectedTile[1])
                        tiles = self.display.MAP_CACHE[self.display.tileset]
                        print "len: " + str(len(tiles))
                        if (tile[0] < 0):
                            tile = (len(tiles) - 1, self.selectedTile[1]-1)
                            if (tile[1] < 0):
                                tile = (0, 0)

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
        tile_image = tiles[self.selectedTile[0]][self.selectedTile[1]]
        self.screen.blit(tile_image, (0, 0))
        pygame.draw.rect(self.screen, CURSOR_COLOR, Rect((0,0), (self.TILE_WIDTH, self.TILE_HEIGHT)), 1)

    def do_action(self):
        print "Doing action: " + self.editmode
        if self.editmode == "CURSOR":
            self.select()

        elif self.editmode == "ADD_TILE":
            self.add_tile()

    def choose_tile(self):
        pass

    def add_tile(self):
        self.select()
        tilex, tiley = self.get_nearest_tile(self.cursor[0], self.cursor[1])
        print str(self.map[tiley])
        self.map[tiley] = self.map[tiley][:tilex] + "w" + self.map[tiley][tilex+1:]

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