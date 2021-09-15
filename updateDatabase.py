import json
import os
import datetime

from scripts.kmp import KMP
from scripts.buddha import Buddha
from scripts.ganesh import Ganesh
from scripts.martinska import Martinska

class Updater:
    def __init__(self):
        self.services = []
        
        with open("./restaurants.json", "r") as f:
            urls = json.loads(f.read())
            
            self.services.append(KMP(urls["kmp"], self))
            self.services.append(Buddha(urls["buddha"], self))
            self.services.append(Ganesh(urls["ganesh"], self))
            self.services.append(Martinska(urls["martinska"], self))

        self.loadTemplates()

    def updateAll(self):
        for s in self.services:
            s.update()

    def createHtmls(self):
        print("Creating htmls")
        path = "./database"
        for root, dirs, files in os.walk(path, topdown=False):
            for name in files:
                file = f"{path}/{name}"
                data = self.getJson(file)
                if (data == ""): continue
                self.createHtml(data)

        self.createIndexes()
        self.createIndex()

    #vytvori index
    def createIndex(self):
        today = datetime.date.today()
        actualWeekDay = str(int(today.strftime("%w")) - 1)
        html = f"<head></head><body><script>window.location.href = \"web/index{actualWeekDay}.html\";</script></body>"

        with open("index.html", "w") as f:
            f.write(html)

    #vytvori index (jeden den pro vsechny restaurace)
    def createIndexes(self):
        today = datetime.date.today()
        dates = [today + datetime.timedelta(days=i) for i in range(0 - today.weekday(), 5 - today.weekday())]

        for date in dates:
            
            weekDay = int(date.strftime("%w")) - 1
            fileName = "index" + str(weekDay)
            with open(f"web/{fileName}.html", "w", encoding="utf-8") as f:
                index = self.indexTemp

                today = datetime.date.today()
                actualWeekDay = str(int(today.strftime("%w")) - 1)
                index = index.replace("$actual$", f"index{actualWeekDay}.html")

                index = index.replace(f"$active{weekDay}$", "active")
                for i in range(5):
                    index = index.replace(f"$active{i}$", "unactive")

                path = "./database"
                for root, dirs, files in os.walk(path, topdown=False):

                    content = ""

                    for name in files:
                        file = f"{path}/{name}"
                        data = self.getJson(file)
                        if (data == ""): continue

                        rest = self.restTemp.replace("$name$", data["name"])
                        rest = rest.replace("$url$", data["url"])
                        rest = rest.replace("$rest$", data["short"] + ".html")

                        day = data["days"][weekDay]

                        rest = rest.replace("$soup$", day["soup"])
                        rest = rest.replace("$soupPrice$", day["soupPrice"])

                        lines = ""

                        for food in day["food"]:
                            line = self.lineTemp.replace("$name$", food[0])
                            line = line.replace("$price$", food[1])
                            lines += line

                        rest = rest.replace("$table$", lines)

                        content += rest
                    index = index.replace("$content$", content)
                f.write(index)

    #vytvori html pro cely tyden pro jednu restauraci
    def createHtml(self, data):
        short = data["short"]
        with open(f"web/{short}.html", "w", encoding="utf-8") as f:

            html = self.oneRestTemp.replace("$name$", data["name"])
            html = html.replace("$url$", data["url"])

            today = datetime.date.today()
            actualWeekDay = str(int(today.strftime("%w")) - 1)
            html = html.replace("$actual$", f"index{actualWeekDay}.html")

            today = datetime.date.today()
            dates = [today + datetime.timedelta(days=i) for i in range(0 - today.weekday(), 5 - today.weekday())]

            content = ""

            for day, date in zip(data["days"], dates):
                line = ""
                for l in day["food"]:
                    line += self.lineTemp.replace("$name$", l[0]).replace("$price$", l[1])

                dt = date.strftime("%A - %d.%m.%Y")

                table = self.tableTemp.replace("$soup$", day["soup"])
                table = table.replace("$soupPrice$", day["soupPrice"])
                table = table.replace("$day$", dt)
                table = table.replace("$table$", line)

                content += table

            html = html.replace("$content$", content)
            f.write(html)

    def loadTemplates(self):
        with open("templates/oneRestaurantTemplate.html", "r", encoding="utf-8") as f:
            self.oneRestTemp = f.read()

        with open("templates/tableTemplate.html", "r", encoding="utf-8") as f:
            self.tableTemp = f.read()

        with open("templates/lineTemplate.html", "r", encoding="utf-8") as f:
            self.lineTemp = f.read()

        with open("templates/indexTemplate.html", "r", encoding="utf-8") as f:
            self.indexTemp = f.read()

        with open("templates/restaurantTemplate.html", "r", encoding="utf-8") as f:
            self.restTemp = f.read()

    def getJson(self, path):
        if (path.find(".gitkeep") != -1):
            return ""

        with open(path, "r") as f:
            return json.loads(f.read())

    def removeStr(self, string, arrStr):
        for a in arrStr:
            string = string.replace(a, "")
        return string
