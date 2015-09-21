#!/usr/bin/python
# -*- coding: utf-8 -*-

import getopt
import sys
import math
import random
from PIL import Image

# note: Smallest sum of individual (R,G,B) channel differences is
# the closest color match

# generate thumbnails in 3:2 aspect ratio. If the source material is known to be
# in other aspect ratio, this should be probably tweaked to match.
tile_width = 30
tile_height = 20
tile_dir = "thumbnails"

helpmsg = "Syntax: mosaic.py -o <output> input [input, ...] [-h]"


def main():
    outfile = None

    if len(sys.argv) < 2:
        print("Not enough arguments. Try -h for help.")
        sys.exit(1)

    try:
        opts, args = getopt.getopt(sys.argv[1:], "ho:")
    except getopt.GetoptError as err:
        print(str(err))
        print("Help available with '-h'")
        sys.exit(1)

    for o, a in opts:
        if o == "-o":
            outfile = a
        if o == "-h":
            print (helpmsg)
            sys.exit(0)

    if len(args) == 0:
        print("Missing input filename. Try -h for help")
        sys.exit(1)
    infile = args[0]

    if outfile is None:
        print("Missing output filename. Use option -o with argument to specify one.")
        sys.exit(1)

    random.seed()
    mosaic = do_mosaic(infile)

    # todo: use exceptions
    if mosaic == -1:
        print("Can't open " + infile)
        sys.exit(1)
    elif mosaic == -2:
        print("Failed to load tile index file. Please run crtiledb.py to generate one")
        sys.exit(1)

    mosaic.save(outfile, quality=100)


def do_mosaic(filename):
    try:
        img = Image.open(filename)
        # pixbuf = img.load()
    except IOError:
        return -1

    # load tile index
    avg_map = load_tile_avgs(tile_dir + "/" + "tileavg.map")
    if avg_map is None:
        return -2

    output = Image.new("RGB", img.size)
    # outbuf = output.load()

    for y in range(0, img.size[1]-tile_height, tile_height):
        for x in range(0, img.size[0]-tile_width, tile_width):
            sect = img.crop((x, y, x+tile_width, y+tile_height))
            avg = get_pixel_average(list(sect.getdata()))
            write_tile(output, x, y,
                       find_best_tile(avg_map, avg),
                       tile_width, tile_height)
    return output


def load_tile_avgs(mapFile):
    try:
        f = open(mapFile)
    except:
        return None
    avg_map = [map(int, l.split()[1:4]) for l in f.readlines()]
    f.close()

    return avg_map


def write_tile(img, x, y, tilenum, tile_width, tile_height):
    tilefile = open(tile_dir+'/'+str(tilenum), 'rb')
    t = Image.open(tilefile)
    img.paste(t, (x, y, x+tile_width, y+tile_height))
    tilefile.close()


def find_best_tile(rgblist, avg_rgb):
    """ Find closest match for RGB value in a list of values """
    nearest_match = 0  # index of matching tile rgb entry in rgblist
    smallest_dif = 9999999

    matches = []

    for i, v in enumerate(rgblist):
        diff_r, diff_g, diff_b = rgb_difference(avg_rgb, v)
        dif = diff_r+diff_g+diff_b  # combined component difference

        # Keep track of closest match that doesn't pass the threshold
        # of acceptance; for cases where no good enough tiles are found
        # we at least have something to offer in the end
        if dif < smallest_dif:
            smallest_dif = dif
            nearest_match = i

        if diff_r < 15 and diff_g < 15 and diff_b < 15:
            matches.append(i)

    # this happens if there have only been "lousy" matches, i.e. only tiles
    # that don't pass the threshold to be accepted as a potential matching
    # tile
    if len(matches) == 0:
        # print("lousy match")
        return nearest_match

    return random.choice(matches)


def get_pixel_average(rgbdata):
    n = len(rgbdata)

    avg_r = sum(nths(rgbdata, 0)) / n
    avg_g = sum(nths(rgbdata, 1)) / n
    avg_b = sum(nths(rgbdata, 2)) / n

    return (avg_r, avg_g, avg_b)


def nths(x, n):
    """ Given a list of sequences, returns a list of all the Nth elements of
    all the contained sequences
    """
    return [l[n] for l in x]


def rgb_difference(color1, color2):
    diff_r = math.fabs(color1[0] - color2[0])
    diff_g = math.fabs(color1[1] - color2[1])
    diff_b = math.fabs(color1[2] - color2[2])
    return (diff_r, diff_g, diff_b)


if __name__ == "__main__":
    main()
