
import importlib
import sys

class RenderContext():
    def __init__(self, drivername):
        try:
            self.driver = importlib.import_module("epd."+drivername)
        except ModuleNotFoundError as e:
            print("could not load output driver '%s' (or one of its dependencies)" % drivername)
            print(e)
            sys.exit(1)
        print("init epd output module (driver=%s)" % drivername)

    def run(self):
        print("run epd output module")
