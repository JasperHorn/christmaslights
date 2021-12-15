
import neopixel
import board
import re
import readchar

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

def markLED(ledCoordinates, n):
    for i,ledCoordinate in enumerate(ledCoordinates):
        if i < n:
            leds[ledCoordinate[0]] = beforeColor
        elif i == n:
            leds[ledCoordinate[0]] = currentColor
        else:
            leds[ledCoordinate[0]] = afterColor

def readResultInput():
    while True:
        key = readchar.readkey()

        if key == ' ':
            return True
        elif key == 'x':
            return False

def findFaultyCoordinates(ledCoordinates):
    directionGradient(ledCoordinates)

    input("Press enter to start verifying in the direction from red to blue")

    print()
    print("Press space if the green LED is correct, x if it is not")

    faultyLeds = []

    for i, coordinate in enumerate(ledCoordinates):
        markLED(ledCoordinates, i)

        result = readResultInput()

        if not result:
            faultyLeds.append(coordinate[0])

    return faultyLeds


ledCoordinates = []

for i, coordinate in enumerate(coords):
    ledCoordinates.append((i, coordinate))

print()
print("Now checking x coordinate")
print()

ledCoordinates.sort(key=lambda led: led[1][0])
faultyX = findFaultyCoordinates(ledCoordinates)

print()
print("Now checking y coordinate")
print()

ledCoordinates.sort(key=lambda led: led[1][1])
faultyY = findFaultyCoordinates(ledCoordinates)

print()
print("Now checking z coordinate")
print()

ledCoordinates.sort(key=lambda led: led[1][2])
faultyZ = findFaultyCoordinates(ledCoordinates)

faultsFile = open("output/faults.json", "w")

faultsFile.write("{\n")
faultsFile.write("    \"x\":" + str(faultyX) + ",\n")
faultsFile.write("    \"y\":" + str(faultyY) + ",\n")
faultsFile.write("    \"z\":" + str(faultyZ) + "\n")
faultsFile.write("}\n")

faultsFile.close()
