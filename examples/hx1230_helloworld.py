# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2023 Mirac Gulgonul
#
# SPDX-License-Identifier: Unlicense

# simple example printing hello world
# to be able to print text, download the font file font5x8.bin
# from https://github.com/adafruit/Adafruit_CircuitPython_framebuf/blob/main/examples/font5x8.bin
# and put it in the same directory as your code

# import required CircuitPython libraries
import time
import board
import busio
import digitalio

# import the HX1230 module
import hx1230

# create the SPI interface, this part depends on your specific board
# for Raspberry Pico W using SPI0:
spi = busio.SPI(clock=board.GP18, MOSI=board.GP19)
# choose a CS (chip select) pin
cs = digitalio.DigitalInOut(board.GP17)  # Chip select
# choose a reset pin, this part is optional since HX1230 has sofware reset
reset = digitalio.DigitalInOut(board.GP20)
# create the HX1230 class
display = hx1230.HX1230(spi=spi, cs=cs, reset=reset)

# clear the display
display.clear()
# print hello world
display.text("hello world", 0, 0, 1)
# don't forget to call show!
display.show()
