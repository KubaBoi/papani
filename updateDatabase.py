import json
import requests
import math
from bs4 import BeautifulSoup

class Updater:
    def __init__(self):
        with open("restaurants.json", "r") as f:
            urls = json.loads(f.read())
            
            self.kmp = urls["kmp"]
            self.buddha = urls["buddha"]

    def updateAll(self):
        self.updateKMP()
        self.updateBuddha()


    def updateKMP(self):
        html = requests.get(self.kmp).text
        
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

    def updateBuddha(self):
        html = requests.get(self.buddha).content

        soup = str(BeautifulSoup(html.decode('utf-8','ignore')))

        data = soup.split("PONDĚLÍ AŽ PÁTEK DO 14:30")[1]
        data = data.split("<big>Indická a nepálská restaurace BUDDHA</big>")[0]

        days = data.split("<br/><b>")[1:]

        jsonData = {}
        weekDays = ["PONDĚLÍ", "ÚTERÝ", "STŘEDA", "ČTVRTEK", "PÁTEK"]

        for i, dayName in enumerate(weekDays):
            index = math.floor(i / 2)
            dayData = days[index]

            print(dayData)

            dayJsonData = {}
            #dayJsonData["soup"] = dayData[1].split("</strong>")[1]


            jsonData[dayName] = dayJsonData

        print(days)
