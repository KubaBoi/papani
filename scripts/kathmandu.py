import json
import requests
from bs4 import BeautifulSoup

class Kathmandu:
    def __init__(self, url, parent):
        self.url = url
        self.parent = parent
        self.short = "05kathmandu"

        self.soupPrice = "14 Kč"

    def update(self):
        html = requests.get(self.url).text
        
        soup = BeautifulSoup(html)
        tabs = soup.find_all("li", {"data-mce-word-list": "1"})
        soups = soup.find_all("p")
        onlySoups = []
        for s in soups:
            if (s.text.find("polévka") != -1):
                onlySoups.append(s)

        jsonData = {}
        jsonData["name"] = "Kathmandu"
        jsonData["url"] = self.url
        jsonData["short"] = self.short
        jsonData["days"] = []

        # soups
        for i in range(5):

            startIndex = i * 2

            dayJsonData = {}

            firstSoup = onlySoups[startIndex].text.replace("Polévka/Soup:\xa0", "").strip()
            secondSoup = onlySoups[startIndex + 1].text.strip()

            dayJsonData["soup"] = f"{firstSoup} {secondSoup}"
            dayJsonData["soupPrice"] = self.soupPrice

            dayJsonData["food"] = []
            for f in range(4):
                index = i * 4 + f
                nameArrayTemp = tabs[index].text.split("\xa0")
                nameArray = []
                for n in nameArrayTemp:
                    if (n != " "): nameArray.append(n)

                name = nameArray[0]
                price = nameArray[1]
                
                dayJsonData["food"].append((name, price)) 

            jsonData["days"].append(dayJsonData)

        with open(f"database/{self.short}.json", "w") as f:
            f.write(json.dumps(jsonData))     