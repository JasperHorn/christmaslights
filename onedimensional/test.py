
import board
import neopixel
import random
import time
import sys

print('Argumehts: ', sys.argv)

pixel = neopixel.NeoPixel(board.D18, 50, pixel_order=neopixel.RGB)

def mix_colors(color1, color2, weight):
    return (color1[0] * (1 - weight) + color2[0] * weight,
            color1[1] * (1 - weight) + color2[1] * weight,
            color1[2] * (1 - weight) + color2[2] * weight)

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

## Single pixel red

#pixel[0] = (255, 0, 0)

## Random colors once

#for i in range(50):
#    color = random_color() 
#    pixel[i] = color
#    time.sleep(0.2)

## Single Dot moving through the wire

#while True:
#    color = random_color() 
#
#    for i in range(50):
#        pixel[i] = color 
#
#        time.sleep(0.01)
#
#    for i in range(50):
#        pixel[i] = (0, 0, 0) 
#        
#        time.sleep(0.005)

## Gradual changes back and forth

color1 = random_color()

while True:
    color2 = different_random_color(color1) 
    color3 = different_random_color(color2)

    for i in range(50):
        color = mix_colors(color1, color2, i / 50);
        pixel[i] = color
        time.sleep(0.1)

    for i in range(50):
        color = mix_colors(color2, color3, i / 50);
        pixel[50-1-i] = color
        time.sleep(0.1)

    color1 = color3

