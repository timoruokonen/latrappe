import os, sys, struct
from tmxloader import *

class MapLoader:

    def save_map(self, map, filename, width, height):
        f = open(filename + ".l1", 'wb')
        print "Writing map width: " + str(width) + " height: " + str(height)
        w = struct.pack('>h', width)
        h = struct.pack('>h', height)
        f.write(w)
        f.write(h)
        for y in xrange(height):
            #print "Y is " + str(y)
            for line in map:
                tilepacked = struct.pack('B', line[y])
                #print "line[y]: " + str(line[y])
                f.write(tilepacked)
            
        print "Map " + filename + " saved."
        f.close()


    def init_map(self, filename):
        print "Loading map file: " + filename
        self.world_map = tmxreader.TileMapParser().parse_decode(filename)
        resources = helperspygame.ResourceLoaderPygame()
        resources.load(self.world_map)
        self.sprite_layers = helperspygame.get_layers_from_map(resources)

    def get_map(self):
        return self.world_map
        
    def get_sprite_layers(self):
        return self.sprite_layers