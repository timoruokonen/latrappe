'''
Game statistics display module
'''
import os, sys
import pygame
from pygame.locals import *
from latrappe import *

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
        self.barGroups = []
        self.stockBarGroups = []

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

    def addStock(self, stock, x=100, y=300):
        self.stockBarGroups.append(StockBarGroup(x, y, stock))
    
    def reset(self):
        self.textRows = 0

    def advance(self, time):
        pass

    def draw(self):
        self.addTitle()
        for group in self.barGroups:
            group.draw(self.screen)

        for stockGroup in self.stockBarGroups:
            stockGroup.updateValues()
            stockGroup.draw(self.screen)


    def visualizeNPCs(self, npcs):
        for npc in npcs:
            self.visualizeNPC(npc)

    def visualizeNPC(self, npc):
        if (npc.is_alive()):
            self.addText("NPC " + str(npc.name) + " occupation: " + str(npc.occupation) + " money: " + str(npc.possession.money) + " action: " + str(npc.schedule.get_current_action_name()))
        else:
            self.addText("*DEAD* NPC " + str(npc.name) + " occupation: " + str(npc.occupation) + " money: " + str(npc.possession.money))



    
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
            titleDisplay = bar.title + " (" + str(bar.amount.GetAmount()) + "/" + str(bar.max) + ")"
            text = self.font.render(titleDisplay, True, (255,255, 255))

            leftBorder = self.x
            rightBorder = self.x + self.maxwidth
            fillRate = float(bar.amount.GetAmount()) / float(bar.max)
            if fillRate > 1.0:
                fillRate = 1.0
            amountX = int((rightBorder - leftBorder) * fillRate)

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

class BarAmount:
    def __init__(self, amount):
        self.amount = amount

    def SetAmount(self, amount):
        self.amount = amount

    def AddAmount(self, amount):
        self.amount += amount

    def GetAmount(self):
        return self.amount

class StockBarGroup(BarGroup):
    def __init__(self, x, y, stock, maxwidth=300, barHeight=20):
        BarGroup.__init__(self, x, y, maxwidth, barHeight)
        self.stock = stock
        self.beer = BarAmount(stock.possession.get_resource_count(Beer))
        self.meat = BarAmount(stock.possession.get_resource_count(Meat))
        self.grain = BarAmount(stock.possession.get_resource_count(Grain))
        self.addBar("Beer", self.beer, 160, (32, 255, 32)) 
        self.addBar("Grain", self.grain, 200, (255, 64, 0))
        self.addBar("Meat", self.meat, 160, (32, 255, 32)) 

    def updateValues(self):
        self.beer.SetAmount(self.stock.possession.get_resource_count(Beer))
        self.meat.SetAmount(self.stock.possession.get_resource_count(Meat))
        self.grain.SetAmount(self.stock.possession.get_resource_count(Grain))

