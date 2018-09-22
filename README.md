
paperd
======

An epaper display server.

So you have your epaper display sucessfully connected to your Raspberry Pi. Now
what do do with it?

paperd will make it easy to push content to your epaper display by letting you
define areas on the display and individually update those areas using a restful
web api.

In the configuration file those areas are defined with their position on the
display and their size. Furthermore it lets you set parameters like how to
handle box overflow or font sizes.

An area can currently be of type "image" or "text". If you push an image
(anything supported by PIL) to an area it will replace the contents of that
area. Likewise, text will be written to a text area in the defined font, size
and alignment.

paperd makes use of the partial update feature of some of the epaper displays
available and can currently only work with those.

Since epaper displays are notoriously slow, you can use a tk based realtime
preview window on your development system.

Requirements
------------

    apt install python3-yaml python3-pil python3-rpi.gpio python3-spidev

for tk output (recommended for preview, not needed on target machine):

    apt python3-pil.imagetk

For updating the epaper display the driver for the Waveshare 2.9" (1-color
version) is included. More drivers will follow.


Configuration
-------------

The configuration file is written in yaml and looks like this:

    paperd:
      v1:
        resolution: {x: &x 296, y: &y 128}
        orientation: 1
        output: epd2in9
        colordepth: 1
        maxfps: 4
        areas:
        - name: background
            type:
            format: image
            overflow: resize
            origin: {x: 0, y: 0}
            size: {x: *x, y: *y}
        - name: title
            type:
            format: text
            overflow: scrolling
            font:
                face: examples/musicplayer/fonts/pf_tempesta_seven_condensed.ttf
                size: 24
                align: left
            origin: {x: 70, y: 0}
            size: {x: 226, y: 64}

See the examples directory for another example. Some of the options in those
examples are not implemented yet: `orientation`, `colordepth`, `scrolling`.

`maxfps` is only partially implemented.

Running
-------

In order to run the included example using the tk preview run this command:

    ./paperd.py -c examples/musicplayer/paperd.yml -o tk

If you have a hidpi display you might want to add the `--scale 2` option to the
command line.

For running the example on your Raspberry Pi with the epd output module, simply
remove the `-o tk` parameter and it will use whichever driver is defined in the
configuration.

Development
-----------

This is an early, but working development version of paperd. Please be kind if
it does weird things and file an issue.

Sice the original waveshare epd2in9 driver is used, and there is no low level
tweaking going on in paperd, it is unlikely this will casuse any damage to your
display or Raspberry Pi.

