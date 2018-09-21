
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

    def getAreaByName(self, area):
        areas = [ x for x in self.conf["areas"] if x["name"] == area ]
        if areas:
            return areas[0]
        else:
            return {}

    def apiGetAreas(self):
        return [ x["name"] for x in self.conf["areas"] ]

    def apiGetArea(self, area):
        return self.getAreaByName(area)

    def apiSetArea(self, area, data):
        a = self.getAreaByName(area)
        if not a: return "area not found"
        x = a["origin"]["x"]
        y = a["origin"]["y"]
        xs = a["size"]["x"]
        xy = a["size"]["y"]
        newimage = Image.open(io.BytesIO(data))
        if a["type"]["overflow"] == "resize":
            newimage = newimage.resize((xs, xy))
        self.image.paste(newimage, (x, y))
        return None

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
