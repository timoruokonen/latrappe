'''
Game statistics display module
'''
import os, sys
import pygame
from pygame.locals import *
from resource import *

if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'

class Display:
    
    def __init__(self, screen):
        self.width = screen.get_width()
        self.height = screen.get_height()
        self.screen = screen
        self.font = pygame.font.Font(None, 17)
        self.titleFont = pygame.font.Font(None, 40)
        self.textRows = 0
        self.bars = 0
        self.barHeight = 20
        self.beer = 50

    def addTitle(self):
        text = self.titleFont.render("La Trappe stats", True, (255,255,255), (0,0,0))
        textRect = text.get_rect()
        textRect.center = (self.screen.get_width() / 2, self.screen.get_height() - 40)
        self.screen.blit(text, textRect)

    def addText(self, msg):
        text = self.font.render(msg, True, (255,255, 255), (0, 0, 0))

        textRect = text.get_rect()
        textRect.left = 0
        textRect.top = self.textRows * 15
        self.textRows += 1

        self.screen.blit(text, textRect)
    
    # Adds a filled bar, visualizing how many resources there are
    def addBar(self, title, amount, max=100, color=(0,0,255)):
        titleDisplay = title + " (" + str(amount) + "/" + str(max) + ")"
        text = self.font.render(titleDisplay, True, (255,255, 255))

        leftBorder = int(self.screen.get_width() * 0.5)
        rightBorder = self.screen.get_width() - 10
        amountX = int((rightBorder - leftBorder) * (float(amount) / float(max)))

        textRect = text.get_rect()
        textRect.left = leftBorder + 5
        textRect.top = self.bars * self.barHeight + 5

        top_y = self.bars * self.barHeight
        # bar background
        pygame.draw.rect(self.screen, (128,128,128), (leftBorder, top_y, (rightBorder - leftBorder), self.barHeight), 0)
        # bar amount
        pygame.draw.rect(self.screen, color,     (leftBorder, top_y, amountX, self.barHeight ), 0)
        # bar amount borders
        pygame.draw.rect(self.screen, (0,0,0),     (leftBorder, top_y, amountX, self.barHeight ), 2)
        
        self.screen.blit(text, textRect)
        self.bars += 1


    def reset(self):
        self.textRows = 0
        self.bars = 0

    def draw(self):
        self.addTitle()
        pygame.display.update()

    def visualizeNPCs(self, npcs):
        for npc in npcs:
            self.visualizeNPC(npc)

    def visualizeNPC(self, npc):
        self.addText("NPC occupation: " + str(npc.occupation) + " money: " + str(npc.possession.money))
    
