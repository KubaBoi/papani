from http.server import BaseHTTPRequestHandler, HTTPServer
import os.path
from os import path, listdir
import pathlib
import datetime
import json



class Server(BaseHTTPRequestHandler):
    def do_GET(self):
        if (self.path == "/"):
            self.sendFile("index.html")

        elif (self.path == "/check"):
            self.check()

        elif (self.path == "/init"):
            self.init()

        elif (self.path.split("?")[0] == "/load"):
            self.sendChat(self.path.split("?")[1])

        else:
            self.sendFile(self.path[1:])

    def do_POST(self):
        if (self.path == "/message"):
            content_len = int(self.headers.get('Content-Length'))
            post_body = self.rfile.read(content_len)
            self.sendMessage(post_body)

    def sendFile(self, file):
        if (not path.exists(f"web/{file}")):
            self.send_response(404)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            return

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        with open(f"web/{file}", "rb") as f:
            self.wfile.write(f.read())

