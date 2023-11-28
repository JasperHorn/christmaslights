
import board
import neopixel
import random
import time
import sys

ledCount = 250

pixel = neopixel.NeoPixel(board.D18, ledCount, pixel_order=neopixel.RGB, auto_write=False)

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


if len(sys.argv) == 2 and sys.argv[1] == 'off':
    pixel.fill((0, 0, 0))
    pixel.show()

elif len(sys.argv) == 2 and sys.argv[1] == 'one':
    ## Single pixel red

    pixel[0] = (255, 0, 0)
    pixel.show()

elif len(sys.argv) == 2 and sys.argv[1] == 'randomize':
    ## Random colors once

    for i in range(pixel.n):
        color = random_color()
        pixel[i] = color
        pixel.show()
        time.sleep(0.05)

elif len(sys.argv) == 2 and sys.argv[1] == 'moving-dot':
    ## Single Dot moving through the wire

    while True:
        color = random_color()

        for i in range(pixel.n):
            pixel[i] = color
            pixel.show()
            time.sleep(0.05)
            pixel[i] = (0, 0, 0)

elif len(sys.argv) == 2 and sys.argv[1] == 'fill':
    ## Single Dot moving through the wire

    while True:
        color = random_color()

        for i in range(pixel.n):
            pixel[i] = color
            pixel.show()
            time.sleep(0.01)

        for i in range(pixel.n):
            pixel[i] = (0, 0, 0)
            pixel.show()
            time.sleep(0.005)

elif len(sys.argv) == 2 and sys.argv[1] == 'gradual':
    ## Gradual changes back and forth

    color1 = random_color()

    while True:
        color2 = different_random_color(color1) 
        color3 = different_random_color(color2)

        for i in range(pixel.n):
            color = mix_colors(color1, color2, i / pixel.n);
            pixel[i] = color
            pixel.show()
            time.sleep(0.005)

        for i in range(pixel.n):
            color = mix_colors(color2, color3, i / pixel.n);
            pixel[pixel.n-1-i] = color
            pixel.show()
            time.sleep(0.1)

        color1 = color3
else:
    print("Usage: ./sudopyton test.py off|one|randomize|moving-dot|fill|gradual")
