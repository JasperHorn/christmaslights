
import types

cameraResolution = (1280, 720)
numberOfLEDs = 50

postProcess = types.SimpleNamespace()

postProcess.rotate = True
postProcess.flip = True 
postProcess.round = True

postProcess.normalize = types.SimpleNamespace()

postProcess.normalize.imageLeft = -700
postProcess.normalize.imageRight = 700
postProcess.normalize.imageBottom = -450
postProcess.normalize.imageTop = 450
