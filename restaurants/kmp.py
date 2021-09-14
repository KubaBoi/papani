import json
import requests
from bs4 import BeautifulSoup

class KMP:
    def __init__(self, url, parent):
        self.url = url
        self.parent = parent

    def update(self):
        html = requests.get(self.url).text
        
        soup = BeautifulSoup(html)
        food = str(soup.find_all("div", {"class": "panel panel-default"})[1])

        days = food.split("<p>Rezervace: 725 339 926</p>")[0].split("<p><strong>")[1:]
        jsonData = {}

        for day in days:

            dayData = day.replace("<br/>\n", "").replace("\xa0", "").split("<strong>")

            dayJsonData = {}
            dayJsonData["soup"] = dayData[1].split("</strong>")[1]

            dayJsonData["food"] = []
            for f in dayData[2:]:
                name = f.split("</strong>")[1].replace("</p>\n", "")
                price = name.split(" ")[-1]
                name = name.replace(price, "").strip()
                
                dayJsonData["food"].append((name, price)) 


            dayName = day.split(":")[0]
            jsonData[dayName] = dayJsonData

        with open("database/kmp.json", "w") as f:
            f.write(json.dumps(jsonData))     