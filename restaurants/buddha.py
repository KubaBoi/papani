import json
import requests
import math
from bs4 import BeautifulSoup

class Buddha:
    def __init__(self, url, parent):
        self.url = url
        self.parent = parent
        self.price = 100

    def update(self):
        html = requests.get(self.url).content

        soup = str(BeautifulSoup(html.decode('utf-8','ignore')))

        data = soup.split("PONDĚLÍ AŽ PÁTEK DO 14:30")[1]
        data = data.split("<big>Indická a nepálská restaurace BUDDHA</big>")[0]

        days = data.split("<br/><b>")[1:]

        jsonData = {}
        weekDays = ["PONDĚLÍ", "ÚTERÝ", "STŘEDA", "ČTVRTEK", "PÁTEK"]

        for i, dayName in enumerate(weekDays):
            index = math.floor(i / 2)
            dayData = self.parent.replaceStr(days[index], ["\r", "\n", "<i>", "</i>", "<b>", "</b>"])
            dayData = dayData.replace("\xa0", " ")

            foods = dayData.split("</table>")[0].split(".")[1:]
            foodJsonData = []
            veg = False

            for food in foods:
                vFood = food

                food = food.replace("<br/>", "(", 1)
                food = food.split(">")[0]
                food = food.replace("<br/", ")", 1).strip()

                if (not veg):
                    foodJsonData.append((food, self.price))
                else:
                    foodJsonData.append((food + " - VEGETARIÁNSKÉ", self.price))

                if (vFood.find("Zeleninové menu:") != -1):
                    veg = True

            dayJsonData = {}
            dayJsonData["food"] = foodJsonData
            dayJsonData["soup"] = "to tam není :("

            jsonData[dayName] = dayJsonData

        with open("database/buddha.json", "w") as f:
            f.write(json.dumps(jsonData))
     