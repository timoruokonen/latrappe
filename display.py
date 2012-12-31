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
        self.barGroups= []

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

    def addBarGroup(self, barGroup):
        self.barGroups.append(barGroup)
    
    def reset(self):
        self.textRows = 0

    def draw(self):
        self.addTitle()
        for group in self.barGroups:
            group.draw(self.screen)

        pygame.display.update()

    def visualizeNPCs(self, npcs):
        for npc in npcs:
            self.visualizeNPC(npc)

    def visualizeNPC(self, npc):
        if (npc.IsAlive()):
            self.addText("NPC occupation: " + str(npc.occupation) + " money: " + str(npc.possession.money) + " action: " + str(npc.schedule.GetCurrentActionName()))
        else:
            self.addText("NPC DEAD occupation: " + str(npc.occupation) + " money: " + str(npc.possession.money))
    
class BarGroup:
    def __init__(self, x, y, maxwidth=300, barHeight=20):
        self.numBars = 0
        self.bars = []
        self.barHeight = barHeight
        self.x = x
        self.y = y
        self.maxwidth = maxwidth
        self.font = pygame.font.Font(None, 17)

    def addBar(self, title, amount, max=100, color=(0,0,255)):
        self.bars.append(Bar(title, amount, max, color))

    def draw(self, screen):
        for bar in self.bars:
            titleDisplay = bar.title + " (" + str(bar.amount) + "/" + str(bar.max) + ")"
            text = self.font.render(titleDisplay, True, (255,255, 255))

            leftBorder = self.x
            rightBorder = self.x + self.maxwidth
            amountX = int((rightBorder - leftBorder) * (float(bar.amount) / float(bar.max)))

            textRect = text.get_rect()
            textRect.left = leftBorder + 5
            textRect.top = self.y + self.bars.index(bar) * self.barHeight + 5

            top_y = self.y + self.bars.index(bar) * self.barHeight
            # bar backgroun
            pygame.draw.rect(screen, (128,128,128), (leftBorder, top_y, (rightBorder - leftBorder), self.barHeight), 0)
            # bar amount
            pygame.draw.rect(screen, bar.color,     (leftBorder, top_y, amountX, self.barHeight ), 0)
            # bar amount borders
            pygame.draw.rect(screen, (0,0,0),     (leftBorder, top_y, amountX, self.barHeight ), 2)
        
            screen.blit(text, textRect)        

class Bar:
    def __init__(self, title, amount, max=100, color=(0,0,255)):
        self.title = title
        self.amount = amount
        self.max = max
        self.color = color
