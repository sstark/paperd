
#import socket
from http.server import BaseHTTPRequestHandler, HTTPServer

class WebAPI(BaseHTTPRequestHandler):
    
    def do_GET(self):
        self.send_response(200)
        self.wfile.write(bytes("<p>You accessed path: %s</p>" % self.path, "utf-8"))

    def do_PUT(self):
        print("PUT", self.path)
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        self.send_response(200)
        client.close()

class WebServer():
    def __init__(self, hostname="localhost", port=2354):
        self.server = HTTPServer((hostname, port), WebAPI)
        print("starting webserver (%s:%s)" % (hostname, port))

    def run(self):
        self.server.serve_forever()
