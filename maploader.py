import os, sys, struct

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


    def load_map(self, filename):
        print "Loading map file: " + filename + ".l1"
        with open(filename + ".l1", 'rb') as f:
            self.mapwidth = struct.unpack('>H', f.read(2))[0]
            self.mapheight = struct.unpack('>H', f.read(2))[0]
            print "Map width: " + str(self.mapwidth) + " height: " + str(self.mapheight)
            map = [[0 for x in xrange(self.mapheight)] for x in xrange(self.mapwidth)] 
            data = f.read()
            print "Loaded map bytes: " + str(len(data))
            data = struct.unpack(str(len(data)) + "B", data)
            #print "Unpacked: " + str(data)
            y = 0
            for x, tile in enumerate(data):
                y = x / self.mapwidth

                if y >= self.mapheight:
                    break

                print "X,Y ",x,y
                map[x % (self.mapwidth)][y] = tile

        print str(map)
        return map