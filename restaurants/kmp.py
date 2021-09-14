import json
import requests
from bs4 import BeautifulSoup

class KMP:
    def __init__(self, url, parent):
        self.url = url
        self.parent = parent
        self.short = "00kmp"

    def update(self):
        html = requests.get(self.url).text
        
        soup = BeautifulSoup(html)
        food = str(soup.find_all("div", {"class": "panel panel-default"})[1])

        days = food.split("<p>Rezervace: 725 339 926</p>")[0].split("<p><strong>")[1:]
        jsonData = {}
        jsonData["name"] = "Klub Malých Pivovarů"
        jsonData["url"] = self.url
        jsonData["short"] = self.short
        jsonData["days"] = []

        for day in days:

            dayData = day.replace("<br/>\n", "").replace("\xa0", "").split("<strong>")

            dayJsonData = {}
            soupPrice = dayData[1].split("</strong>")[1].split(" ")[-1]
            dayJsonData["soup"] = dayData[1].split("</strong>")[1].replace(soupPrice, "").strip()
            dayJsonData["soupPrice"] = soupPrice

            dayJsonData["food"] = []
            for f in dayData[2:]:
                name = f.split("</strong>")[1].replace("</p>\n", "")
                price = name.split(" ")[-1]
                name = name.replace(price, "").strip()
                
                dayJsonData["food"].append((name, price)) 

            jsonData["days"].append(dayJsonData)

        with open(f"database/{self.short}.json", "w") as f:
            f.write(json.dumps(jsonData))     