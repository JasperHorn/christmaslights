
import neopixel
import board
import readchar
import json

beforeColor = (128, 0, 0)
currentColor = (0, 128, 0)
afterColor = (0, 0, 128)

def mix_colors(color1, color2, weight):
    return (color1[0] * (1 - weight) + color2[0] * weight,
            color1[1] * (1 - weight) + color2[1] * weight,
            color1[2] * (1 - weight) + color2[2] * weight)

with open("output/coords.txt",'r') as resultsFile:
    coordinates = list(map(json.loads, resultsFile.readlines()))

numberOfLEDs = len(coordinates)

leds = neopixel.NeoPixel(board.D18, numberOfLEDs, pixel_order=neopixel.RGB)

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

for i, coordinate in enumerate(coordinates):
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
