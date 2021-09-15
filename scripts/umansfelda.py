import json
import requests
from bs4 import BeautifulSoup

class Umansfelda:
    def __init__(self, url, parent):
        self.url = url
        self.parent = parent
        self.short = "05umansfelda"

    def update(self):
        html = requests.get(self.url).text
        
        soup = BeautifulSoup(html)
        menuTemp = soup.find_all("div", {"class": "menu"})[0].contents
        menu = []

        for m in menuTemp[1:]:
            if (m != "\n"):
                if (m.name == "article"):
                    menu.append(m)

        jsonData = {}
        jsonData["name"] = "U Mansfelda"
        jsonData["url"] = self.url
        jsonData["short"] = self.short
        jsonData["days"] = []

        for i in range(5):

            startIndex = i * 3

            dayJsonData = {}

            attribute = menu[startIndex].contents[1]

            dayJsonData["soup"] = attribute.contents[1].text.strip()
            dayJsonData["soupPrice"] = attribute.contents[3].text.strip()

            dayJsonData["food"] = []
            for f in range(1, 3):
                attribute = menu[startIndex + f]

                name = attribute.contents[1].contents[1].contents[0]
                price = attribute.contents[1].contents[3].contents[0]
                
                dayJsonData["food"].append((name, price)) 

            jsonData["days"].append(dayJsonData)

        with open(f"database/{self.short}.json", "w") as f:
            f.write(json.dumps(jsonData))     