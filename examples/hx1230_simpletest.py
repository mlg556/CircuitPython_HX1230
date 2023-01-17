# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2023 Mirac Gulgonul
#
# SPDX-License-Identifier: Unlicense

# simple example showing the capabilities of HX1230 with framebuffer
# adapted from https://github.com/adafruit/Adafruit_CircuitPython_SSD1306/blob/main/examples/ssd1306_framebuftest.py

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
# choose a backlight pin, this is also optional
backlight = digitalio.DigitalInOut(board.GP16)
# turn on the backlight
backlight.switch_to_output(True)
backlight.value = True

# create the HX1230 class
display = hx1230.HX1230(spi=spi, cs=cs, reset=reset)

# press ctrl-c to exit
while True:
    display.clear()  # clear the display

    # Set a pixel in the origin 0,0 position.
    display.pixel(0, 0, 1)
    # Set a pixel in the middle position.
    display.pixel(display.width // 2, display.height // 2, 1)
    # Set a pixel in the opposite corner position.
    display.pixel(display.width - 1, display.height - 1, 1)
    # don't forget to call show!
    display.show()
    time.sleep(2)

    print("Lines test")
    # we'll draw from corner to corner, lets define all the pair coordinates here
    corners = (
        (0, 0),
        (0, display.height - 1),
        (display.width - 1, 0),
        (display.width - 1, display.height - 1),
    )

    display.fill(0)
    for corner_from in corners:
        for corner_to in corners:
            display.line(corner_from[0], corner_from[1], corner_to[0], corner_to[1], 1)
    display.show()
    time.sleep(2)

    print("Rectangle test")
    display.fill(0)
    w_delta = display.width / 10
    h_delta = display.height / 10
    for i in range(11):
        display.rect(0, 0, int(w_delta * i), int(h_delta * i), 1)
    display.show()
    time.sleep(2)

    print("Text test")
    display.fill(0)
    try:
        display.text("hello world", 0, 0, 1)
        display.show()
        time.sleep(1)
        display.clear()  # clear the display
        # lets print all the characters from the font5x8.bin font
        char_width = 5
        char_height = 8
        total_lines = display.height // char_height  # 8 lines
        chars_per_line = display.width // char_width  # 19 chars per line
        x, y, i = 0, 0, 0
        for line in range(total_lines):
            for char in range(chars_per_line):
                display.text(chr(i), x, y, 1)
                x += char_width  # increment x
                i += 1  # increment char index
            x = 0  # reset x
            y += char_height  # increment y
        display.show()
    except OSError:
        print(
            "To test the framebuf font setup, you'll need the font5x8.bin file from "
            + "https://github.com/adafruit/Adafruit_CircuitPython_framebuf/blob/main/examples/"
            + " in the same directory as this script"
        )
    time.sleep(2)
    # repeat
