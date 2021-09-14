import json
import requests
import math
from bs4 import BeautifulSoup

class Ganesh:
    def __init__(self, url, parent):
        self.url = url
        self.parent = parent
        self.short = "02ganesh"

    def update(self):
        html = requests.get(self.url).content
        soup = str(BeautifulSoup(html.decode('utf-8','ignore')))

        newUrl = soup.split(";")[0].split(" ")[-1].replace("\"", "")

        html = requests.get(newUrl).content
        soup = BeautifulSoup(html.decode('utf-8','ignore'))

        menu = soup.find_all("div", {"class": "menicko"})[0]
        food = menu.find_all("table", {"class": "menu"})


        jsonData = {}
        jsonData["name"] = "GANESH"
        jsonData["url"] = self.url
        jsonData["short"] = self.short
        jsonData["days"] = []

        for day in food:

            foodJsonData = []

            for food in day.contents[1:]:
                foodJsonData.append((
                    self.parent.replaceStr(str(food.find_all("td", {"class": "jidlo"})[0]), ["<td class=\"jidlo\">", "</td>"]),
                    self.parent.replaceStr(str(food.find_all("td", {"class": "cena"})[0]), ["<td class=\"cena\">", "</td>"])
                ))

            dayJsonData = {}
            dayJsonData["soup"] = self.parent.replaceStr(str(day.contents[0].find_all("td", {"class": "jidlo"})[0]), ["<td class=\"jidlo\">", "</td>"])
            dayJsonData["soupPrice"] = self.parent.replaceStr(str(day.contents[0].find_all("td", {"class": "cena"})[0]), ["<td class=\"cena\">", "</td>"])
            dayJsonData["food"] = foodJsonData

            jsonData["days"].append(dayJsonData)

        with open(f"database/{self.short}.json", "w") as f:
            f.write(json.dumps(jsonData))
     