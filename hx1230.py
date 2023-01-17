# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2023 Mirac Gulgonul
#
# SPDX-License-Identifier: MIT
"""
`hx1230`
================================================================================

CircuitPython framebuf driver for HX1230 96x68 monochrome LCD displays using SPI.


* Author(s): Mirac Gulgonul

Implementation Notes
--------------------

**Hardware:**

.. todo:: Add links to any specific hardware product page(s), or category page(s).
  Use unordered list & hyperlink rST inline format: "* `Link Text <url>`_"

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://circuitpython.org/downloads

.. todo:: Uncomment or remove the Bus Device and/or the Register library dependencies
  based on the library's use of either.

# * Adafruit's Bus Device library: https://github.com/adafruit/Adafruit_CircuitPython_BusDevice
"""

# imports

__version__ = "0.0.0+auto.0"
__repo__ = "https://github.com/mlg556/CircuitPython_HX1230.git"


from time import sleep
from micropython import const
from adafruit_bus_device import spi_device

try:
    import framebuf

    _FRAMEBUF_FORMAT = framebuf.MONO_VLSB
except ImportError:
    import adafruit_framebuf as framebuf

    _FRAMEBUF_FORMAT = framebuf.MVLSB

try:
    # Used only for typing
    from typing import Optional
    import busio
    import digitalio
except ImportError:
    pass


# register definitions
POWER_ON = const(0x2F)  # internal power supply on
POWER_OFF = const(0x28)  # internal power supply off
CONTRAST = const(0x80)  # 0x80 + (0~31)
SEG_NORMAL = const(0xA0)  # SEG remap normal
SEG_REMAP = const(0xA1)  # SEG remap reverse (flip horizontal)
DISPLAY_NORMAL = const(0xA4)  # display ram contents
DISPLAY_TEST = const(0xA5)  # all pixels on
INVERT_OFF = const(0xA6)  # not inverted
INVERT_ON = const(0xA7)  # inverted
DISPLAY_ON = const(0xAF)  # display on
DISPLAY_OFF = const(0xAE)  # display off
SCAN_START_LINE = const(0x40)  # 0x40 + (0~63)
COM_NORMAL = const(0xC0)  # COM remap normal
COM_REMAP = const(0xC8)  # COM remap reverse (flip vertical)
SW_RESET = const(0xE2)  # connect RST pin to GND to rely on software reset
# NOP = const(0xE3) # no operation
DATA = const(0x80)  # the msb in the 9-bit spi mode, command = 0, data = 1
THREE_BITS = const(0x07)  # 0~7
FOUR_BITS = const(0x0F)  # 0~15
FIVE_BITS = const(0x1F)  # 0~31
SIX_BITS = const(0x3F)  # 0~63

# DDRAM addresses
COL_ADDR = const(0x10)  # x pos (0~95)
PAGE_ADDR = const(0xB0)  # y pos, 9 pages of 8 rows (0~8)

# Display dimensions
WIDTH = const(0x60)  # 96 cols
HEIGHT = const(0x44)  # 68 rows
# 9 pages (68 / 8 = 8.5, rounded up to 9) the last page is only half visible
PAGES = const(9)


class HX1230(framebuf.FrameBuffer):
    """
    Main class for HX1230 display driver.

    :param spi: the SPI peripheral to use
    :param cs: the chip-select pin to use
    :param reset: the reset pin to use
    :param baudrate: baudrate, maximum 4_000_000
    """

    def __init__(
        self,
        spi: busio.SPI,
        cs: digitalio.DigitalInOut,
        reset: Optional[digitalio.DigitalInOut],
        baudrate=2_000_000,
    ):
        self.spi_device = spi_device.SPIDevice(
            spi=spi, chip_select=cs, baudrate=baudrate, polarity=0, phase=0
        )
        self.width = WIDTH
        self.height = HEIGHT
        self.reset_pin = reset
        self.cs_pin = cs
        self.framebuffer = bytearray(PAGES * WIDTH)  # initialize framebuffer
        if self.reset_pin:
            self.reset_pin.switch_to_output(value=True)
        super().__init__(self.framebuffer, WIDTH, HEIGHT, _FRAMEBUF_FORMAT)
        self._power = False
        # Let's get moving!
        self.init_display()

    def init_display(self) -> None:
        """Initialize the display"""
        self.reset()
        self.power_on()
        self.contrast(31)  # maximum contrast
        self.invert(False)
        self.test(False)
        self.flip_horizontal(False)  # no rotation
        self.flip_vertical(False)
        self.display(True)  # switch on
        self.start_line(0)  # set line to 0
        self.clear()  # clear
        self.show()

    def reset(self) -> None:
        """Reset the display"""
        if self.reset_pin:
            self.reset_pin.value = False
            sleep(0.05)  # 50ms, recommended is between 10 and 100 ms
            self.reset_pin.value = True
            sleep(0.05)

    def power_on(self) -> None:
        """Turn the display ON"""
        self.write_command(POWER_ON)

    def power_off(self) -> None:
        """Turn the display OFF"""
        self.write_command(POWER_OFF)

    def contrast(self, contrast: int) -> None:
        """Adjust the contrast, a value between 0~31"""
        self.write_command(CONTRAST | (contrast & FIVE_BITS))

    def invert(self, invert=True) -> None:
        """Invert all pixels on the display"""
        self.write_command(INVERT_ON if invert else INVERT_OFF)

    def display(self, on=True) -> None:
        """Set the display on"""
        self.write_command(DISPLAY_ON if on else DISPLAY_OFF)

    def test(self, on=True) -> None:
        """Display test pattern"""
        self.write_command(DISPLAY_TEST if on else DISPLAY_NORMAL)

    def flip_horizontal(self, flip: bool) -> None:
        """Flips the screen horizontally, call with False to flip, True to reset"""
        self.write_command(COM_REMAP if flip else COM_NORMAL)

    def flip_vertical(self, flip: bool) -> None:
        """Flips the screen vertically, call with False to flip, True to reset"""
        # doesn't work for some reason...
        self.write_command(SEG_REMAP if flip else SEG_NORMAL)

    def position(self, x: int, y: int) -> None:
        """Position the cursor, x between 0~95 and y between 0~9"""
        self.write_command(PAGE_ADDR | y)  # set y pos (0~8)
        self.write_command(COL_ADDR | ((x >> 4) & THREE_BITS))  # set x pos high 3 bits
        self.write_command(x & FOUR_BITS)  # set x pos low 4 bits

    def start_line(self, line=0) -> None:
        """Set the start line, between 0~63"""
        self.write_command(SCAN_START_LINE + (line & SIX_BITS))

    def clear(self) -> None:
        """Clear the display"""
        self.fill(0)
        self.show()

    def show(self) -> None:
        """Update the display"""
        self.position(0, 0)  # why 0,0?
        self.write_framebuf()

    def write_command(self, command: int) -> None:
        """Sends a single command"""
        # allocate 9 bits to be sent
        # 9-bit SPI, MSB = D/C, 8 data bits, 7 padding bits
        command_array = bytearray(2)
        # send 2 bytes left aligned with padding bits
        command_array[0] = 0  # MSB is D/C, in this case C(control)
        command_array[0] |= command >> 1  # high 7 bits of value
        command_array[1] = (command & 1) << 7  # low 1 bit of value
        self.cs_pin.value = False
        with self.spi_device as spi:
            spi.write(command_array)
        self.cs_pin.value = True

    def write_framebuf(self) -> None:
        """Sends the framebuffer via SPI"""
        # for each 8 bytes of the framebuffer,
        # send 9 bytes (include a DC bit for each chunk)
        for i in range(0, PAGES * WIDTH, 8):
            chunk = self.framebuffer[i : i + 8]
            command = bytearray(9)
            for j in range(8):
                command[j] |= 1 << (7 - j)  # DC bit
                if j == 7:
                    # DC on prev 7th byte means this one is no change
                    command[j + 1] = chunk[j]
                else:
                    command[j] |= chunk[j] >> (j + 1)
                    command[j + 1] |= (chunk[j] << (7 - j)) & 0xFF
            self.cs_pin.value = False
            with self.spi_device as spi:
                spi.write(command)
            self.cs_pin.value = True
