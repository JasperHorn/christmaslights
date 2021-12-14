
##
## This is a really quick sample to see that my mapping is working
##

import time
import board
import neopixel
import re
import random

##
## Some helper functions copied from onedimensional
##

def random_color():
    return (random.randint(0,128),
            random.randint(0,128),
            random.randint(0,128))

def total_difference(color1, color2):
    diff = abs(color1[0] - color2[0])
    diff += abs(color1[1] - color2[1])
    diff += abs(color1[2] - color2[2])

    return diff

def different_random_color(old_color):
    color = random_color()
    
    while total_difference(color, old_color) < 128:
        color = random_color()

    return color

##
## I straight up copied reading the coordinates from
## https://github.com/standupmaths/xmastree2020
## (which was possible because I used the same format)
##

coordfilename = "coords.txt"
	
fin = open(coordfilename,'r')
coords_raw = fin.readlines()
    
coords_bits = [i.split(",") for i in coords_raw]
    
coords = []
    
for slab in coords_bits:
    new_coord = []
    for i in slab:
        new_coord.append(int(re.sub(r'[^-\d]','', i)))
    coords.append(new_coord)

PIXEL_COUNT = len(coords)
    
pixels = neopixel.NeoPixel(board.D18, PIXEL_COUNT, auto_write=False)

##
## Finally, some original code
## (in the sense that I wrote it, just about every game engine looks like
## this, so it's not truly "original")
##

t = time.clock_gettime(time.CLOCK_MONOTONIC)
color = random_color()
h = 0
speed = 300

while True:
    tNew = time.clock_gettime(time.CLOCK_MONOTONIC)
    dt = tNew - t;
    t = tNew;

    h += speed * dt

    if h > 450:
        h = -450
        color = different_random_color(color)

    for i, coordinate in enumerate(coords):
        # Change the 1 here to either 0 or 2 to test different directions
        if coordinate[1] < h:
            pixels[i] = color

    pixels.show()

