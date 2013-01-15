import pygame
from TileUtils import *
from AnimatedSprite import AnimatedSprite
from latrappe import *

class NpcRenderer:
    def __init__(self, surface, tile_width=32, tile_height=32):
        self.surface = surface
        # FIXME: Just test images for now
        self.MAP_TILE_WIDTH = tile_width
        self.MAP_TILE_HEIGHT = tile_height
        self.font = pygame.font.Font(None, 17)
        self.npc_dead_img = pygame.image.load("monk_dead.png")
        self.npc_alive_img = pygame.image.load("monk.png")
        self.npcimage = self.npc_alive_img
        self.work_animation_images = TileUtils.load_sliced_sprites(32, 32, 'monk_working.png')
        self.sleep_animation_images = TileUtils.load_sliced_sprites(32, 32, 'monk_sleeping.png')
        self.work_animation = AnimatedSprite(self.work_animation_images, 30)        
        self.sleep_animation = AnimatedSprite(self.sleep_animation_images, 30)

        self.npc_animation = self.work_animation

    def draw_npc(self, npc):
        # default image
        npcimage = self.npc_alive_img
        action = npc.schedule.get_current_action()
        if npc.alive:
            if type(action) == ProduceAction:
                self.npc_animation = self.work_animation
                self.surface.blit(self.work_animation.image, (npc.x, npc.y))
            elif type(action) == Action and action.name == "Sleep":
                self.npc_animation = self.sleep_animation
                self.surface.blit(self.sleep_animation.image, (npc.x,npc.y))
            else:
                self.surface.blit(npcimage, (npc.x, npc.y))

        else:
        # if npc is dead, show dead npc image no matter what
            self.npcimage = self.npc_dead_img
            self.surface.blit(npcimage, (npc.x, npc.y))

        # draw npc name
        text = self.font.render(npc.name, True, (255,255, 255))
        textRect = text.get_rect()
        textRect.left = npc.x - (self.MAP_TILE_WIDTH / 2)
        textRect.top = npc.y + (self.MAP_TILE_HEIGHT)
        self.surface.blit(text, textRect)
