import pygame
from TileUtils import *
from AnimatedSprite import AnimatedSprite
from latrappe import *
from tmxloader import *

class NpcRenderer:
    def __init__(self, tile_width=32, tile_height=32):
        #self.sprite_layer = sprite_layer
        # FIXME: Just test images for now
        self.MAP_TILE_WIDTH = tile_width
        self.MAP_TILE_HEIGHT = tile_height
        self.font = pygame.font.Font(None, 17)
        self.npc_dead_img = pygame.image.load("monk_dead.png")
        self.npc_alive_img = pygame.image.load("monk.png")
        self.npcimage = self.npc_alive_img
        self.work_animation_images = TileUtils.load_sliced_sprites(32, 32, 'monk_working.png')
        self.sleep_animation_images = TileUtils.load_sliced_sprites(32, 32, 'monk_sleeping.png')
        self.brewing_animation_images = TileUtils.load_sliced_sprites(32, 32, 'monk_brewing.png')
        self.hunting_animation_images = TileUtils.load_sliced_sprites(32, 32, 'monk_hunting.png')

    def get_npc_anim(self, npc):
        # default image
        npcanim = None
        action = npc.schedule.get_current_action()
        if npc.alive:
            if (type(action) == ProduceAction) and (type(npc.occupation) == Hunter):
                npcanim = AnimatedSprite(npc, self.hunting_animation_images, 8)
                #self.surface.blit(self.hunting_animation.image, (npc.x, npc.y))               
            elif (type(action) == ProduceAction) and (type(npc.occupation) == Brewer):
                npcanim = AnimatedSprite(npc, self.brewing_animation_images, 8)
                #self.surface.blit(self.brewing_animation.image, (npc.x, npc.y))
            elif type(action) == ProduceAction:
                npcanim = AnimatedSprite(npc, self.work_animation_images, 30) 
                #self.surface.blit(self.work_animation.image, (npc.x, npc.y))
            elif type(action) == Action and action.name == "Sleep":
                npcanim = AnimatedSprite(npc, self.sleep_animation_images, 30)
                #self.surface.blit(self.sleep_animation.image, (npc.x,npc.y))
            else:
                npcanim = AnimatedSprite(npc, self.sleep_animation_images, 30)

        else:
        # if npc is dead, show dead npc image no matter what
            self.npcimage = self.npc_dead_img
            #self.surface.blit(npcimage, (npc.x, npc.y))
        return npcanim

    def update(self, time):
        self.work_animation.update(time)
        self.brewing_animation.update(time)
        self.sleep_animation.update(time)
        self.hunting_animation.update(time)
