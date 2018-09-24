
import importlib
import sys
from render import BaseRenderContext
import time
import threading
import logging

log = logging.getLogger("paperd.show_epd")

class RenderContext(BaseRenderContext):
    def __init__(self, drivername, conf, scale=1):
        try:
            self.driver = importlib.import_module("epd."+drivername)
        except ModuleNotFoundError:
            log.exception("could not load output driver '%s' (or one of its dependencies)" % drivername)
            sys.exit(1)
        log.info("init epd output module (driver=%s)" % drivername)
        super().__init__(drivername, conf, scale)
        self.delay = 1000//self.fps
        self.screenlock = threading.Lock()
        self.epd = self.driver.EPD()
        self.epd.init(self.epd.lut_partial_update)
        self.clearPaper()

    def clearPaper(self):
        self.screenlock.acquire()
        self.epd.init(self.epd.lut_full_update)
        for blarg in range(2):
            self.epd.clear_frame_memory(0xFF)
            self.epd.display_frame()
        self.epd.init(self.epd.lut_partial_update)
        self.screenlock.release()

    def display(self):
        self.screenlock.acquire()
        self.epd.init(self.epd.lut_full_update)
        for blarg in range(2):
            self.epd.set_frame_memory(self.image, 0, 0)
            self.epd.display_frame()
        self.epd.init(self.epd.lut_partial_update)
        self.screenlock.release()

    def paste(self, image, box):
        # x and y are swapped here because the waveshare displays
        # are in portrait mode
        y, x = box
        xs, ys = image.size
        # because we rotate the sub images we need to adjust x a bit
        realx = self.height-x-ys
        rimg = image.rotate(270, expand=1)
        # store image to self for full redraws
        self.image.paste(rimg, (realx, y))
        # the epd has two screen buffers and for now we simply update
        # both each time. This could be improved.
        self.screenlock.acquire()
        for blarg in range(2):
            self.epd.set_frame_memory(rimg, realx, y)
            self.epd.display_frame()
        self.screenlock.release()

    def run(self):
        log.info("run epd output module")
        while True:
            time.sleep(10)
            # at this point we could do regular full redraws
            # to repair messed up parts of the display
            #log.info("epd full redraw")
            #self.display()
