
from http.server import BaseHTTPRequestHandler, HTTPServer
from functools import partial
import json
import re

class WebAPI(BaseHTTPRequestHandler):

    def __init__(self, routeMap, *args, **kwargs):
        self.apiFuncs = routeMap
        self.urlsGET = {
            "/v1/areas/(.*)": self.getApiFunc("getArea"),
            "/v1/areas$": self.getApiFunc("getAreas"),
        }
        self.urlsPUT = {
            "/v1/areas/(?P<area>%s)": self.getApiFunc("setArea")
        }
        super().__init__(*args, **kwargs)

    def unknownApiFunc(self):
        print("unknown API function requested")

    def getApiFunc(self, name):
        return self.apiFuncs.get(name, self.unknownApiFunc)

    def matchUrl(self, routes):
        # first return value is actual function to run
        # second return value "name" is set to first match group of the route
        for k in routes:
            m = re.match(k, self.path)
            if m:
                try:
                    name = m.group(1)
                except:
                    name = None
                return routes[k], name
        return None

    def do_GET(self):
        func, name = self.matchUrl(self.urlsGET)
        if func:
            if name:
                out = func(name)
            else:
                out = func()
            self.send_response(200)
        else:
            out = "not found"
            self.send_response(404)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(bytes(json.dumps(out).encode("utf-8")))

    def do_PUT(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        self.send_response(200)
        client.close()

class WebServer():
    def __init__(self, routeMap, hostname="localhost", port=2354):
        requestHandler = partial(WebAPI, routeMap)
        self.server = HTTPServer((hostname, port), requestHandler)
        print("starting webserver (%s:%s)" % (hostname, port))

    def run(self):
        self.server.serve_forever()
