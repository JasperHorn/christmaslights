import pygame
import pygame.camera

pygame.camera.init()
cams = pygame.camera.list_cameras() 
cam = pygame.camera.Camera(cams[0], (1280,720))

cam.start()

# First image often contains a weird brightness tear, so we discard it
cam.get_image()

img = cam.get_image()

pygame.image.save(img,"output/photo.jpg")
