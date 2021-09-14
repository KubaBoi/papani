from http.server import BaseHTTPRequestHandler, HTTPServer
import time

from server import Server
from updateDatabase import Updater

update = Updater()
update.updateAll()
update.createHtmls()


hostName = "localhost"
hostPort = 8000

myServer = HTTPServer((hostName, hostPort), Server)
print(time.asctime(), f"Server Starts - {hostName}:{hostPort}")

try:
    myServer.serve_forever()
except KeyboardInterrupt:
    pass

myServer.server_close()
print(time.asctime(), f"Server Stops - {hostName}:{hostPort}")
