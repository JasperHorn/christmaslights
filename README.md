# christmaslights

I made a Christmas tree with addressable lights, similar to what Matt Parker
(Stand-up Maths) did. His tree can be viewed [on Youtube](1)
and his code is [on Github](2) as well.

I was inspired by his code, but I set out to write my own code to map the LEDs
to their 3d coordinates. This repository contains the tools that I wrote to do so,
as well some code for driving the leds.

I documented my progress on my blog: 
http://blog.jasperhorn.nl/search/label/christmas%20tree

## Sub-projects

- onedimensional
  
  Some code that drives the LEDs normally, based on their position
  in the cord

- mapper

  The code I used to assign coordinates to the LEDs

- threedimensional

  Some code that uses the coordinates to drive the LEDs in 3d space

## Installation

Each project contains its own requirements.txt file, which can be used by pip
to install any and all requirements. It is of course advised to do this in a
virtual environment.

Additionally, the mapper project required a non-python dependency (sdl2). It is
listed in nonpython-requirements.txt in the form of an apt-get command which
should work on Raspberry Pi OS.

## Running the code

The library to control the LEDs needs root access. However, python virtual
environments do not work nicely while running as root out of the box. That's
why each of the projects contains a `sudopython` file. You can use this as
you would use `sudo python` (e.g. `./sudopython test.py`). However, it adds
the bits that make it run in the virtual environment you're currently in.

## Usage

### onedimensional

`./sudopython test.py`: run a simple onedimensional effect

(there are several effects in the code, but all but one are commented out)

### mapper
 
`config.py` contains config such as the number of LEDs and camera resolution, so
you should modify this to fit your situation.

`./sudopython frame.py`: takes a picture (saved to `output/photo.jpg`) which you can
use to get the tree nicely in frame

`./sudopython mapper.py`: start the mapping process. It will print out instructions,
so just follow those. For best results, do the mapping in the dark (you can turn on
the lights when it tells you to rotate the tree, as long as you turn them off again
before pressing afterwards)

`./sudopython verifier.py`: start a process to identify LEDs with incorrect coordinates

`./sudopython mapper.py fix`: rescan LEDs with incorrect coordinates (uses the output
from the verifier)

`./sudopython identify.py n: light up the LED with index n up in green and any
following indexes in blue. This can help identify LEDs if you need to map some of them
by hand 

### threedimensional

`coords.txt` is the coordinate mapping and should be copied from `mapper/output/coords.txt`

`./sudopython test.py`: A simple test script that just changes colors in one of the direction
of the y axis

`./sudopython test.pyi x`: Run the test for the x axis

`./sudopython test.py y`: Run the test for the y axis (equivalent to leaving out the y)

`./sudopython test.py z`: Run the test for the z axis

`./sudopython off.py`: turn all LEDs off

[1]: https://www.youtube.com/watch?v=TvlpIojusBE
[2]: https://github.com/standupmaths/xmastree2020
