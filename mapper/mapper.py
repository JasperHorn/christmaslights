
import time
import sys
import json
import types
import pathlib

import pygame
import pygame.camera

import neopixel
import board

import config

highlightColor = (255, 128, 0)

outputBaseDir = "output"
outputDir = outputBaseDir

pathlib.Path(outputDir).mkdir(exist_ok = True)
pathlib.Path(outputDir + "/left").mkdir(exist_ok = True)
pathlib.Path(outputDir + "/right").mkdir(exist_ok = True)
pathlib.Path(outputDir + "/front").mkdir(exist_ok = True)
pathlib.Path(outputDir + "/back").mkdir(exist_ok = True)

pygame.camera.init()
cams = pygame.camera.list_cameras() 
cam = pygame.camera.Camera(cams[0], config.cameraResolution)

leds = neopixel.NeoPixel(board.D18, config.numberOfLEDs, pixel_order=neopixel.RGB)

class Mapping:
    def __init__(self, x, y, score):
        self.x = x
        self.y = y
        self.score = score

class Coordinate:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

def mapLED(i):
    leds[i] = (50, 50, 50)

    # Toggling on and off camera each time because otherwise I appear to get old images 
    cam.start()
    # But also throw away the first image because it has a brightness tear
    cam.get_image()
    img = cam.get_image()
    cam.stop()

    pygame.image.save(img, outputDir + "/led-" + str(i) + ".jpg")

    brightestSpot = (0, 0)
    brightestWeight = 0

    for x in range(img.get_width()):
        for y in range(img.get_height()):
            color = img.get_at((x, y))
            brightness = color.r + color.g + color.b

            if color.r > 220 and color.g > 220 and color.b > 220:
                brightestSpot = ((brightestSpot[0] * brightestWeight + x) / (brightestWeight + 1),
                                 (brightestSpot[1] * brightestWeight + y) / (brightestWeight + 1))

                brightestWeight += 1

    leds[i] = (0, 0, 0)

    roundedBrightestSpot = (round(brightestSpot[0]), round(brightestSpot[1]))

    if brightestWeight == 0:
        score = 0
    else:
        color = img.get_at(roundedBrightestSpot)
        score = (color.r + color.g + color.b) * 5 + brightestWeight;

    for x in range(img.get_width()):
        img.set_at((x, roundedBrightestSpot[1]), highlightColor)

    for y in range(img.get_height()):
        img.set_at((roundedBrightestSpot[0], y), highlightColor)

    pygame.image.save(img, outputDir + "/led-" + str(i) + "-highlighted.jpg")
    
    print("Led " + str(i) + " mapped")

    return Mapping(brightestSpot[0], brightestSpot[1], score)

def mapLEDs(targetedLEDs):
    mappings = {}

    for i in targetedLEDs:
        mappings[i] = mapLED(i)

    return mappings

def postProcess(mappings):
    for i in mappings:
        mapping = mappings[i]

        if config.postProcess.flip:
            mapping.x = config.cameraResolution[0] - 1 - mapping.x;
            mapping.y = config.cameraResolution[1] - 1 - mapping.y;

        mapping.x = mapping.x / config.cameraResolution[0] * (config.postProcess.normalize.imageRight - config.postProcess.normalize.imageLeft) + config.postProcess.normalize.imageLeft
        mapping.y = mapping.y / config.cameraResolution[1] * (config.postProcess.normalize.imageTop - config.postProcess.normalize.imageBottom) + config.postProcess.normalize.imageBottom

        if config.postProcess.rotate:
            x = mapping.x
            y = mapping.y
            mapping.x = y
            mapping.y = x

        if config.postProcess.round:
            mapping.x = round(mapping.x)
            mapping.y = round(mapping.y)

def scanSide(targetedLEDs):
    mappings = mapLEDs(targetedLEDs)
    postProcess(mappings)

    return mappings

if len(sys.argv) == 2 and sys.argv[1] == 'fix':
    with open(outputDir + '/faults.json','r') as faultsFile:
        targeted = json.loads(faultsFile.read())
    with open(outputDir + '/coords.txt', 'r') as resultsFile:
        def lineToCoordinate(line):
            l = json.loads(line)
            return Coordinate(l[0], l[1], l[2])

        coordinates = list(map(lineToCoordinate, resultsFile.readlines()))
else:
    targeted = {
        "x": list(range(config.numberOfLEDs)),
        "y": list(range(config.numberOfLEDs)),
        "z": list(range(config.numberOfLEDs))
    }

    coordinates = list(map(lambda i: Coordinate(0, 0, 0), range(config.numberOfLEDs)))

allTargeted = set(targeted["x"] + targeted["y"] + targeted["z"])

input("Press enter to start scanning")
outputDir = outputBaseDir + "/front"
front = scanSide(allTargeted)

input("Rotate tree 90 degrees and then press enter to scan second side")
outputDir = outputBaseDir + "/right"
right = scanSide(allTargeted) # might be the left side in reality, but that doesn't matter

input("Rotate tree 90 degrees and then press enter to scan third side")
outputDir = outputBaseDir + "/back"
back = scanSide(allTargeted)

input("Rotate tree 90 degrees and then press enter to scan fourth side")
outputDir = outputBaseDir + "/left"
left = scanSide(allTargeted)

outputDir = outputBaseDir

shiftHorizontal = config.postProcess.normalize.imageLeft + config.postProcess.normalize.imageRight
shiftVertical = config.postProcess.normalize.imageBottom + config.postProcess.normalize.imageTop

if config.postProcess.rotate:
    hor = shiftHorizontal
    ver = shiftVertical
    shiftHorizontal = ver
    shiftVertical = hor

for i in targeted["x"]:
    if front[i].score > back[i].score:
        coordinates[i].x = front[i].x
    else:
        coordinates[i].x = back[i].x * -1 + shiftHorizontal

for i in targeted["z"]:
    if right[i].score > left[i].score:
        coordinates[i].z = right[i].x
    else:
        coordinates[i].z = left[i].x * -1 + shiftHorizontal

for i in targeted["y"]:
    if front[i].score > right[i].score and front[i].score > back[i].score and front[i].score > left[i].score:
        coordinates[i].y = front[i].y
    elif right[i].score > back[i].score and right[i].score > left[i].score:
        coordinates[i].y = right[i].y
    elif back[i].score > left[i].score:
        coordinates[i].y = back[i].y
    else:
        coordinates[i].y = left[i].y

results = open(outputDir + "/coords.txt", "w")

for coordinate in coordinates:
    results.write("[" + str(coordinate.x) + ", " + str(coordinate.y)  + ", " + str(coordinate.z) + "]\n")

results.close()
