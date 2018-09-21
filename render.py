
from PIL import Image
import webserver
from threading import Thread

class BaseRenderContext():
    def __init__(self, drivername, conf):
        self.width = conf["resolution"]["x"]
        self.height = conf["resolution"]["y"]
        self.fps = conf["maxfps"]
        self.image = Image.new('1', (self.width, self.height), 255)
        self.startWebserver()

    def startWebserver(self):
        self.webserver = webserver.WebServer()
        self.server = Thread(target=self.webserver.run)
        self.server.daemon = True
        self.server.start()

    def display(self):
        pass

    def run(self):
        pass
