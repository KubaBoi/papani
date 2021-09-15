from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import threading

from server import Server
from updateDatabase import Updater

updateTime = 14400

update = Updater(updateTime)
update.updateAll()
update.createHtmls()
