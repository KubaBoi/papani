from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import threading

from server import Server
from updateDatabase import Updater

updateTime = 14400

update = Updater(updateTime)
#update.updateAll()
#update.createHtmls()


hostName = "localhost"
hostPort = 8000

myServer = HTTPServer((hostName, hostPort), Server)
print(time.asctime(), f"Server Starts - {hostName}:{hostPort}")

try:
    updateThread = threading.Thread(target=update.runForever)
    updateThread.start()
    myServer.serve_forever()
except KeyboardInterrupt:
    pass

myServer.server_close()
print(time.asctime(), f"Server Stops - {hostName}:{hostPort}")
