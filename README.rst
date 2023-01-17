Introduction
============


.. image:: https://readthedocs.org/projects/circuitpython-hx1230/badge/?version=latest
    :target: https://circuitpython-hx1230.readthedocs.io/
    :alt: Documentation Status



.. image:: https://img.shields.io/discord/327254708534116352.svg
    :target: https://adafru.it/discord
    :alt: Discord


.. image:: https://github.com/mlg556/CircuitPython_HX1230/workflows/Build%20CI/badge.svg
    :target: https://github.com/mlg556/CircuitPython_HX1230/actions
    :alt: Build Status


.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black
    :alt: Code Style: Black

CircuitPython framebuf driver for HX1230 96x68 monochrome LCD displays using SPI.


Dependencies
=============
This driver depends on:

* `Adafruit CircuitPython <https://github.com/adafruit/circuitpython>`_
* `Bus Device <https://github.com/adafruit/Adafruit_CircuitPython_BusDevice>`_

Please ensure all dependencies are available on the CircuitPython filesystem.
This is easily achieved by downloading
`the Adafruit library and driver bundle <https://circuitpython.org/libraries>`_
or individual libraries can be installed using
`circup <https://github.com/adafruit/circup>`_.

On supported GNU/Linux systems like the Raspberry Pi, you can install the driver locally `from
PyPI <https://pypi.org/project/circuitpython-hx1230/>`_.
To install for current user:

.. code-block:: shell

    pip3 install circuitpython-hx1230

To install system-wide (this may be required in some cases):

.. code-block:: shell

    sudo pip3 install circuitpython-hx1230

To install in a virtual environment in your current project:

.. code-block:: shell

    mkdir project-name && cd project-name
    python3 -m venv .venv
    source .env/bin/activate
    pip3 install circuitpython-hx1230

Installing to a Connected CircuitPython Device with Circup
==========================================================

Make sure that you have ``circup`` installed in your Python environment.
Install it with the following command if necessary:

.. code-block:: shell

    pip3 install circup

With ``circup`` installed and your CircuitPython device connected use the
following command to install:

.. code-block:: shell

    circup install hx1230

Or the following command to update an existing version:

.. code-block:: shell

    circup update

Usage Example
=============

.. code-block:: python
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

Documentation
=============
API documentation for this library can be found on `Read the Docs <https://circuitpython-hx1230.readthedocs.io/>`_.

For information on building library documentation, please check out
`this guide <https://learn.adafruit.com/creating-and-sharing-a-circuitpython-library/sharing-our-docs-on-readthedocs#sphinx-5-1>`_.

Contributing
============

Contributions are welcome! Please read our `Code of Conduct
<https://github.com/mlg556/CircuitPython_HX1230/blob/HEAD/CODE_OF_CONDUCT.md>`_
before contributing to help this project stay welcoming.
