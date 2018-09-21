
from PIL import Image
import webserver
from threading import Thread
import io

class BaseRenderContext():
    def __init__(self, drivername, conf):
        self.conf = conf
        self.width = conf["resolution"]["x"]
        self.height = conf["resolution"]["y"]
        self.fps = conf["maxfps"]
        self.image = Image.new('1', (self.width, self.height), 255)
        self.startWebserver()

    def apiGetAreas(self):
        return [ x["name"] for x in self.conf["areas"] ]

    def apiGetArea(self, area):
        return [ x for x in self.conf["areas"] if x["name"] == area ]

    def apiSetArea(self, area, data):
        newimage = Image.open(io.BytesIO(data))
        self.image.paste(newimage)

    def makeRouteMap(self):
        return {
            "getAreas": self.apiGetAreas,
            "getArea": self.apiGetArea,
            "setArea": self.apiSetArea
        }

    def startWebserver(self):
        self.webserver = webserver.WebServer(self.makeRouteMap())
        self.server = Thread(target=self.webserver.run)
        self.server.daemon = True
        self.server.start()

    def display(self):
        pass

    def run(self):
        pass
