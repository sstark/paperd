
from PIL import Image, ImageDraw, ImageFont
import webserver
from threading import Thread
import io
import logging
from textlib import WrappedText

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

    def apiSetArea_image(self, a, data):
        x = a["origin"]["x"]
        y = a["origin"]["y"]
        xs = a["size"]["x"]
        xy = a["size"]["y"]
        newimage = Image.open(io.BytesIO(data))
        if a["type"]["overflow"] == "resize":
            newimage = newimage.resize((xs, xy))
        self.paste(newimage, (x, y))

    def apiSetArea_text(self, a, data):
        x = a["origin"]["x"]
        y = a["origin"]["y"]
        xs = a["size"]["x"]
        xy = a["size"]["y"]
        font = a["type"]["font"]
        newimage = Image.new('1', (xs, xy), font["background"])
        newdraw = ImageDraw.Draw(newimage)
        try:
            ttf = ImageFont.truetype(font["face"], font["size"])
        except OSError:
            log.exception("error reading font")
            return "font not found '%s'" % font["face"]
        newtext = data.decode("utf-8")
        wrapped, wrapped_fs = WrappedText(newtext, (xs, xy), ttf, maxlines=2).smartWrapped()

        # unfortunately for single lines we have to do right alignment
        # ourselves:
        shiftx = 0
        if '\n' not in wrapped:
            if font["align"] == "right":
                tw, th = newdraw.textsize(newtext, font=ttf)
                shiftx = xs - tw

        newdraw.multiline_text((shiftx, 0), wrapped, fill=font["color"],
                               font=ttf.font_variant(size=wrapped_fs), align=font["align"])
        self.paste(newimage, (x, y))

    def apiSetArea(self, area, data):
        a = self.getAreaByName(area)
        if not a:
            return "area not found"
        aformat = a["type"]["format"]
        if aformat == "image":
            self.apiSetArea_image(a, data)
        elif aformat == "text":
            self.apiSetArea_text(a, data)
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
