# christmaslights

I made a Christmas tree with addressable lights, similar to what Matt Parker
(Stand-up Maths) did. His tree can be vieweed on Youtube:
https://www.youtube.com/watch?v=TvlpIojusBE and his code can be found on Github:
https://github.com/standupmaths/xmastree2020

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

## Interesting files

- onedimensional: several effects that do not require a mapping
  - test.py: contains the effects - all but one are commented out, though
- mapper: generate a 3d mapping
  - config.py: config such as the number of LEDs and camera resolution
  - frame.py: takes a picture, usable to get the tree in frame
- threedimensional: 3d effect
  - coords.txt: copy this file from mapper/output/results.txt
  - test.py: runs a simple changing color in a direction (change file to change direction)
  - off.py: turns all LEDs off
