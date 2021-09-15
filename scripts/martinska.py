import json
import requests
from bs4 import BeautifulSoup

class Martinska:
    def __init__(self, url, parent):
        self.url = url
        self.parent = parent
        self.short = "04martinska"

    def update(self):
        html = requests.get(self.url).text
        
        soup = BeautifulSoup(html)
        tabs = soup.find_all("div", {"class": "tab-content"})[0]

        tds = tabs.find_all("td")

        jsonData = {}
        jsonData["name"] = "Martinská"
        jsonData["url"] = self.url
        jsonData["short"] = self.short
        jsonData["days"] = []

        # gramaz jmeno cena
        for i in range(5):

            startIndex = i * 9

            dayJsonData = {}
            soupPrice = tds[startIndex + 2].text.strip().replace("\xa0", " ")
            dayJsonData["soup"] = (f"{tds[startIndex].text} {tds[startIndex + 1].text}").strip().replace("\xa0", " ")
            dayJsonData["soupPrice"] = soupPrice

            dayJsonData["food"] = []
            for f in range(2):
                index = startIndex + f * 3 + 3
                name = (f"{tds[index].text} {tds[index + 1].text}").strip().replace("\xa0", " ")
                price = tds[index + 2].text.strip().replace("\xa0", " ")
                
                dayJsonData["food"].append((name, price)) 

            jsonData["days"].append(dayJsonData)

        with open(f"database/{self.short}.json", "w") as f:
            f.write(json.dumps(jsonData))     