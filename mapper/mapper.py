
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
    leds[i] = (255, 255, 255)

    # Toggling on and off camera each time because otherwise I appear to get old images 
    cam.start()
    # But also throw away the first image because it has a brightness tear
    cam.get_image()
    img = cam.get_image()
    cam.stop()

    pygame.image.save(img,"output/led-" + str(i) + ".jpg")

    brightest = 0
    brightestSpot = None

    for x in range(img.get_width()):
        for y in range(img.get_height()):
            color = img.get_at((x, y))
            brightness = color.r + color.g + color.b

            if brightness > brightest:
                brightest = brightness
                brightestSpot = (x, y)

    leds[i] = (0, 0, 0)

    for x in range(img.get_width()):
        img.set_at((x, brightestSpot[1]), highlightColor)

    for y in range(img.get_height()):
        img.set_at((brightestSpot[0], y), highlightColor)

    pygame.image.save(img,"output/led-" + str(i) + "-highlighted.jpg")

    print("Led " + str(i) + " mapped")
