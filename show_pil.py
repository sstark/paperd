
from render import BaseRenderContext
from PIL import Image, ImageDraw
import logging

log = logging.getLogger("paperd.show_pil")

class RenderContext(BaseRenderContext):
    def __init__(self, drivername, conf):
        log.info("init pil output module")
        super().__init__(drivername, conf)

    def display(self):
        self.image.show()

    def run(self):
        log.info("run pil output module")
        draw = ImageDraw.Draw(self.image)
        draw.rectangle((3, 3, self.width-3, self.height-3), fill = 255, outline = 0)
        self.display()
