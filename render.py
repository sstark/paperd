
from PIL import Image

class BaseRenderContext():
    def __init__(self, drivername, conf):
        self.width = conf["resolution"]["x"]
        self.height = conf["resolution"]["y"]
        self.fps = conf["maxfps"]
        self.image = Image.new('1', (self.width, self.height), 255)

    def display(self):
        pass

    def run(self):
        pass
