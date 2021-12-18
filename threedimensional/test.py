
##
## This is a really quick sample to see that my mapping is working
##

import sys
import time
import board
import neopixel
import json
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
## read the axis from the arguments
##

if len(sys.argv) == 1:
    axis = 1
elif sys.argv[1] == 'x':
    axis = 0
elif sys.argv[1] == 'y':
    axis = 1
elif sys.argv[1] == 'z':
    axis = 2
else:
    raise Exception("If an argument is provided, it should be x, y or z")

with open("coords.txt",'r') as coordinatesFile:
    coordinates = list(map(json.loads, coordinatesFile.readlines()))

pixelCount = len(coordinates)
    
pixels = neopixel.NeoPixel(board.D18, pixelCount, auto_write=False)

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

    for i, coordinate in enumerate(coordinates):
        if coordinate[axis] < h:
            pixels[i] = color

    pixels.show()

