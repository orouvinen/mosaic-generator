#!/usr/bin/env python

#

import os
import sys
from PIL import Image
from mosaictile import MosaicTile

tile_width = 30
tile_height = 20

def main():
    photoDir = ""           # root dir for photo scan
    tileDir = "thumbnails"  # output dir for generated tiles
    fileNum = 0             # generated thumbnail file names are sequential
    tileAvgMap = tileDir + "/tileavg.map" # thumbnails avg color values output file

    try:
        avgMap = open(tileAvgMap, "w")
    except:
        print "Failed to create a file for writing"
        sys.exit(1)
    
    if len(sys.argv) > 1:
        photoDir = sys.argv[1]
    else:
        photoDir = "./"

    extensions = ["jpg"]
    for root, dirs, files in os.walk(photoDir):
        for f in files:
            ext = f[-3:].lower()
            if ext in extensions:
                print "Generating thumbnail of " + f + " into ", 
                try:
                    tile = MosaicTile()
                    tile.createFrom(root + '/' + f, tile_width, tile_height)
                    tile.save(tileDir + "/" + str(fileNum)) 
                    print str(fileNum)
                    avgColor = tile.getAvgRGB()
                    R, G, B = avgColor[0], avgColor[1], avgColor[2]
                    avgMap.write(str(fileNum) + " {0:d} {1:d} {2:d}\n".format(R,G,B))
                    fileNum += 1
                except KeyboardInterrupt:
                    avgMap.flush()
                    os.fsync(avgMap)
                    sys.exit(1)
                except:
                    print "WARNING: couldn't generate thumbnail for %s" % (f)
                    continue


    avgMap.close()

if __name__ == "__main__":
    main()
    
