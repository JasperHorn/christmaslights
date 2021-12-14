
import time

import pygame
import pygame.camera

import neopixel
import board

import config

highlightColor = (255, 128, 0);

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

    pygame.image.save(img,"output/led-" + str(i) + ".jpg")

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

    pygame.image.save(img,"output/led-" + str(i) + "-highlighted.jpg")
    
    print("Led " + str(i) + " mapped")

    return Mapping(brightestSpot[0], brightestSpot[1], score)

def mapLEDs():
    mappings = []

    for i in range(config.numberOfLEDs):
        mappings.append(mapLED(i))

    return mappings

def postProcess(mappings):
    for mapping in mappings:
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

def scanSide():
    mappings = mapLEDs()
    postProcess(mappings)

    return mappings

input("Press enter to start scanning")
front = scanSide()

input("Rotate tree 90 degrees and then press enter to scan second side")
right = scanSide() # might be the left side in reality, but that doesn't matter

input("Rotate tree 90 degrees and then press enter to scan third side")
back = scanSide()

input("Rotate tree 90 degrees and then press enter to scan fourth side")
left = scanSide()

coordinates = []

shiftHorizontal = config.postProcess.normalize.imageLeft + config.postProcess.normalize.imageRight
shiftVertical = config.postProcess.normalize.imageBottom + config.postProcess.normalize.imageTop

if config.postProcess.rotate:
    hor = shiftHorizontal
    ver = shiftVertical
    shiftHorizontal = ver
    shiftVertical = hor

for i in range(config.numberOfLEDs):
    if front[i].score > back[i].score:
        x = front[i].x
    else:
        x = back[i].x * -1 + shiftHorizontal

    if right[i].score > left[i].score:
        z = right[i].x
    else:
        z = left[i].x * -1 + shiftHorizontal

    if front[i].score > right[i].score and front[i].score > back[i].score and front[i].score > left[i].score:
        y = front[i].y
    elif right[i].score > back[i].score and right[i].score > left[i].score:
        y = right[i].y
    elif back[i].score > left[i].score:
        y = back[i].y
    else:
        y = left[i].y

    coordinates.append(Coordinate(x, y, z))


results = open("output/results.txt", "w")

for coordinate in coordinates:
    results.write("[" + str(coordinate.x) + ", " + str(coordinate.y)  + ", " + str(coordinate.z) + "]\n")

results.close()
