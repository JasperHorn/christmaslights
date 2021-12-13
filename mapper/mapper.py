import pygame
import pygame.camera

pygame.camera.init()
cams = pygame.camera.list_cameras() 
cam = pygame.camera.Camera(cams[0], (1280,720))

cam.start()

img = cam.get_image()
pygame.image.save(img,"photo.jpg")
