
import board
import neopixel
import random
import time
import sys
import math

ledCount = 250

leds = neopixel.NeoPixel(board.D18, ledCount, pixel_order=neopixel.RGB, auto_write=False)

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
    leds.fill((0, 0, 0))
    leds.show()

elif len(sys.argv) == 2 and sys.argv[1] == 'one':
    ## Single pixel red

    leds[0] = (255, 0, 0)
    leds.show()

elif len(sys.argv) == 2 and sys.argv[1] == 'randomize':
    ## Random colors once

    for i in range(leds.n):
        color = random_color()
        leds[i] = color
        leds.show()
        time.sleep(0.05)

elif len(sys.argv) == 2 and sys.argv[1] == 'moving-dot':
    ## Single Dot moving through the wire

    while True:
        color = random_color()

        for i in range(leds.n):
            leds[i] = color
            leds.show()
            time.sleep(0.05)
            leds[i] = (0, 0, 0)

elif len(sys.argv) == 2 and sys.argv[1] == 'fill':
    ## Single Dot moving through the wire

    while True:
        color = random_color()

        for i in range(leds.n):
            leds[i] = color
            leds.show()
            time.sleep(0.01)

        for i in range(leds.n):
            leds[i] = (0, 0, 0)
            leds.show()
            time.sleep(0.005)

elif len(sys.argv) == 2 and sys.argv[1] == 'gradual':
    ## Gradual changes back and forth

    color1 = random_color()

    while True:
        color2 = different_random_color(color1) 
        color3 = different_random_color(color2)

        for i in range(leds.n):
            color = mix_colors(color1, color2, i / leds.n);
            leds[i] = color
            leds.show()
            time.sleep(0.005)

        for i in range(leds.n):
            color = mix_colors(color2, color3, i / leds.n);
            leds[leds.n-1-i] = color
            leds.show()
            time.sleep(0.1)

        color1 = color3

elif len(sys.argv) == 2 and sys.argv[1] == 'rainbow':
    ## A raibow moving through the leds

    colors = [
        (128, 0, 0),
        (128, 32, 0),
        (128, 128, 0),
        (0, 128, 0),
        (0, 0, 128),
        (32, 0, 128)
    ]

    offset = 0;

    colorDistance = leds.n / len(colors)

    while True:
        for i in range(leds.n):
            n = (i + offset) % leds.n

            colorIndex = math.floor(n / colorDistance)
            color1 = colors[colorIndex]
            color2 = colors[(colorIndex + 1) % len(colors)]

            mixFactor = (n % colorDistance) / colorDistance;

            color = mix_colors(color1, color2, mixFactor);

            leds[i] = color

        leds.show()
        offset = (offset + 1) % leds.n
elif len(sys.argv) == 2 and sys.argv[1] == 'white':
    leds.fill((64, 64, 64))
    leds.show()

elif len(sys.argv) == 2 and sys.argv[1] == 'repeat-white':
    while True:
        leds.fill((64, 64, 64))
        leds.show()

else:
    print("Usage: ./sudopyton main.py off|one|randomize|moving-dot|fill|gradual|rainbow|white|repeat-white")
