import pygame
import pygame.camera
import time

pygame.camera.init()
cams = pygame.camera.list_cameras() 
cam = pygame.camera.Camera(cams[0], (1280,720))

cam.start()

# First image often contains a weird brightness tear, so we discard it
cam.get_image()

img = cam.get_image()

pygame.image.save(img,"photo.jpg")

brightest = 0
brightestSpot = None

for x in range(img.get_width()):
    for y in range(img.get_height()):
        color = img.get_at((x, y))
        brightness = color.r + color.g + color.b

        if brightness > brightest:
            brightest = brightness
            brightestSpot = (x, y)

print(brightestSpot)
print(brightness)

highlightColor = (255, 128, 0);

for x in range(img.get_width()):
    img.set_at((x, brightestSpot[1]), highlightColor)

for y in range(img.get_height()):
    img.set_at((brightestSpot[0], y), highlightColor)

pygame.image.save(img,"photo-highlighted.jpg")
