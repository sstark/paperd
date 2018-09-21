
from http.server import BaseHTTPRequestHandler, HTTPServer
from functools import partial
import json

class WebAPI(BaseHTTPRequestHandler):

    def __init__(self, routeMap, *args, **kwargs):
        self.apiFuncs = routeMap
        self.urlsGET = {
            "/v1/areas": self.getApiFunc("getAreas")
        }
        super().__init__(*args, **kwargs)

    def unknownApiFunc(self):
        print("unknown API function requested")

    def getApiFunc(self, name):
        return self.apiFuncs.get(name, self.unknownApiFunc)

    def matchUrl(self, routes):
        return routes.get(self.path, None)

    def do_GET(self):
        func = self.matchUrl(self.urlsGET)
        if func:
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
