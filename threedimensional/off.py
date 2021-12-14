
import board
import neopixel
import random
import time
import sys

pixel = neopixel.NeoPixel(board.D18, 50, pixel_order=neopixel.RGB)

for i in range(50):
    pixel[i] = (0, 0, 0)
