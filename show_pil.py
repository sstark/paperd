
from render import BaseRenderContext
from PIL import Image, ImageDraw

class RenderContext(BaseRenderContext):
    def __init__(self, drivername, conf):
        print("init pil output module")
        BaseRenderContext.__init__(self, drivername, conf)

    def display(self):
        self.image.show()

    def run(self):
        print("run pil output module")
        draw = ImageDraw.Draw(self.image)
        draw.rectangle((3, 3, self.width-3, self.height-3), fill = 255, outline = 0)
        self.display()
