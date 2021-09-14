from http.server import BaseHTTPRequestHandler
from os import path, listdir
import datetime



class Server(BaseHTTPRequestHandler):
    def do_GET(self):
        today = datetime.date.today()
        weekDay = str(int(today.strftime("%w")) - 1)

        if (self.path == "/"):
            self.sendFile(f"index{weekDay}.html", weekDay)

        if (self.path == "/sheet.css"):
            self.sendCss()

        else:
            self.sendFile(self.path[1:], weekDay)

    def sendFile(self, file, weekDay):
        if (not path.exists(f"web/{file}")):
            self.send_error(404,'File Not Found: %s ' % file)
            return

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        with open(f"web/www/{file}", "r", encoding="utf-8") as f:
            content = f.read().replace("$actual$", f"index{weekDay}.html")
            self.wfile.write(bytes(content, "utf-8"))

    def sendCss(self):
        self.send_response(200)
        self.send_header("Content-type", "text/css")
        self.end_headers()

        with open(f"web/sheet.css", "rb") as f:
            self.wfile.write(f.read())

