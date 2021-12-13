
import time

import pygame
import pygame.camera

import neopixel
import board

highlightColor = (255, 128, 0);

pygame.camera.init()
cams = pygame.camera.list_cameras() 
cam = pygame.camera.Camera(cams[0], (1280,720))

leds = neopixel.NeoPixel(board.D18, 50, pixel_order=neopixel.RGB)

for i in range(50):
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

    for x in range(img.get_width()):
        img.set_at((x, roundedBrightestSpot[1]), highlightColor)

    for y in range(img.get_height()):
        img.set_at((roundedBrightestSpot[0], y), highlightColor)

    pygame.image.save(img,"output/led-" + str(i) + "-highlighted.jpg")

    print("Led " + str(i) + " mapped")
