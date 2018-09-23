
from PIL import Image, ImageDraw, ImageFont
import webserver
from threading import Thread
import io
import logging

log = logging.getLogger("paperd.render")

class BaseRenderContext():
    def __init__(self, drivername, conf, scale=1):
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

    def paste(self, image, box):
        self.image.paste(image, box)

    def apiGetAreas(self):
        return [ x["name"] for x in self.conf["areas"] ]

    def apiGetArea(self, area):
        return self.getAreaByName(area)

    def apiSetArea(self, area, data):
        a = self.getAreaByName(area)
        if not a:
            return "area not found"

        x = a["origin"]["x"]
        y = a["origin"]["y"]
        xs = a["size"]["x"]
        xy = a["size"]["y"]
        aformat = a["type"]["format"]

        if aformat == "image":
            newimage = Image.open(io.BytesIO(data))
            if a["type"]["overflow"] == "resize":
                newimage = newimage.resize((xs, xy))
            self.paste(newimage, (x, y))
        elif aformat == "text":
            newimage = Image.new('1', (xs, xy), 255)
            newdraw = ImageDraw.Draw(newimage)
            font = a["type"]["font"]
            try:
                ttf = ImageFont.truetype(font["face"], font["size"])
            except OSError:
                log.exception("error reading font")
                return "font not found '%s'" % font["face"]
            newstring = data.decode("utf-8")
            if font["align"] == "right":
                tw, th = newdraw.textsize(newstring, font=ttf)
                shiftx = xs - tw
            else:
                shiftx = 0
            newdraw.text((shiftx, 0), newstring, font=ttf, fill=0)
            self.paste(newimage, (x, y))
        else:
            return "unknown area format '%s'" % aformat
        return None

    def makeRouteMap(self):
        return {
            "getAreas": self.apiGetAreas,
            "getArea": self.apiGetArea,
            "setArea": self.apiSetArea
        }

    def startWebserver(self):
        address = self.conf["listen"]
        self.webserver = webserver.WebServer(self.makeRouteMap(), address)
        self.server = Thread(target=self.webserver.run)
        self.server.daemon = True
        self.server.start()

    def display(self):
        pass

    def run(self):
        pass
