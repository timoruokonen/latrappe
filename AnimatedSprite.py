import pygame

class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, npc, images, fps = 10, source_rect=None, flags=0, key=None):
        pygame.sprite.Sprite.__init__(self)
        self._images = images

        # Track the time we started, and the time between updates.
        # Then we can figure out when we have to switch the image.
        self._start = pygame.time.get_ticks()
        self._delay = 1000 / fps
        self._last_update = 0
        self._frame = 0
        self.npc = npc
        
        self.image = self._images[1]
        # TODO: dont use a rect for position
        self.rect = pygame.Rect(npc.x, npc.y, 64, 64) # blit rect
        self.source_rect = source_rect
        self.flags = flags
        self.is_flat = False
        self.z = 0
        self.key = key

        # Call update to set our first image.
        self.update(pygame.time.get_ticks())
        
    def get_x(self):
        return self.npc.x

    def get_y(self):
        return self.npc.y

    def update(self, t):
        self.rect = pygame.Rect(self.npc.x, self.npc.y, 64, 64)
        # Note that this doesn't work if it's been more that self._delay
        # time between calls to update(); we only update the image once
        # then, but it really should be updated twice.

        if t - self._last_update > self._delay:
            self._frame += 1
            #print 'frame: ' + str(self._frame)
            if self._frame >= len(self._images): self._frame = 0
            self.image = self._images[self._frame]
            self._last_update = t
            
    def get_draw_cond(self):
        if self.is_flat:
            return self.rect.top + self.z
        else:
            return self.rect.bottom
