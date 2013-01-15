import pygame

class TileUtils:
    @staticmethod
    def load_sliced_sprites(w, h, filename):
        images = []
        master_image = pygame.image.load(filename).convert_alpha()

        master_width, master_height = master_image.get_size()
        for y in xrange(int(master_height/h)):
            for i in xrange(int(master_width/w)):
                images.append(master_image.subsurface(i*w,y*h,w,h))

        print 'Image count:' + str(len(images))
        return images