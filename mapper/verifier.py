
import neopixel
import board
import re

beforeColor = (128, 0, 0)
currentColor = (0, 128, 0)
afterColor = (0, 0, 128)

def mix_colors(color1, color2, weight):
    return (color1[0] * (1 - weight) + color2[0] * weight,
            color1[1] * (1 - weight) + color2[1] * weight,
            color1[2] * (1 - weight) + color2[2] * weight)

##
## I straight up copied reading the coordinates from
## https://github.com/standupmaths/xmastree2020
## (which was possible because I used the same format)
##

coordfilename = "output/results.txt"
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

leds = neopixel.NeoPixel(board.D18, PIXEL_COUNT, pixel_order=neopixel.RGB)

##
## own code
##
def directionGradient(ledCoordinates):
    for i,ledCoordinate in enumerate(ledCoordinates):
        leds[ledCoordinate[0]] = mix_colors(beforeColor, afterColor, i / 49)

def findFaultyCoordinates(ledCoordinates):
    directionGradient(ledCoordinates)

    input("Press enter to start verifying in the direction from red to blue")

ledCoordinates = []

for i, coordinate in enumerate(coords):
    ledCoordinates.append((i, coordinate))

ledCoordinates.sort(key=lambda led: led[1][0])

findFaultyCoordinates(ledCoordinates)
