import json

from restaurants.kmp import KMP
from restaurants.buddha import Buddha

class Updater:
    def __init__(self):
        self.services = []
        
        with open("restaurants.json", "r") as f:
            urls = json.loads(f.read())
            
            self.services.append(KMP(urls["kmp"], self))
            self.services.append(Buddha(urls["buddha"], self))

    def updateAll(self):
        for s in self.services:
            s.update()

    def replaceStr(self, string, arrStr):
        for a in arrStr:
            string = string.replace(a, "")
        return string
