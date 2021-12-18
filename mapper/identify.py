
import sys

import board
import neopixel

pixel = neopixel.NeoPixel(board.D18, 50, pixel_order=neopixel.RGB)

pixel[int(sys.argv[1])] = (0, 128, 0)

for i in range(2, len(sys.argv)):
    pixel[int(sys.argv[i])] = (0, 0, 128)
