
import importlib
import sys
from render import BaseRenderContext
import time

class RenderContext(BaseRenderContext):
    def __init__(self, drivername, conf, scale=1):
        try:
            self.driver = importlib.import_module("epd."+drivername)
        except ModuleNotFoundError as e:
            print("could not load output driver '%s' (or one of its dependencies)" % drivername)
            print(e)
            sys.exit(1)
        print("init epd output module (driver=%s)" % drivername)
        super().__init__(drivername, conf, scale)
        self.delay = 1000//self.fps
        self.epd = self.driver.EPD()
        self.epd.init(self.epd.lut_partial_update)
        self.clearPaper()

    def clearPaper(self):
        self.epd.clear_frame_memory(0x00)
        self.epd.display_frame()
        self.epd.clear_frame_memory(0xFF)
        self.epd.display_frame()

    def display(self):
        self.epd.set_frame_memory(self.image.rotate(270, expand=1), 0, 0)
        self.epd.display_frame()

    def run(self):
        print("run epd output module")
        try:
            while True:
                self.display()
                time.sleep(2)
        except KeyboardInterrupt:
            pass

