import json
from pymongo import MongoClient

class FieldSetting(object):

    def __init__(self, settingsDict = None):
        if settingsDict is not None:
            self.fSettings = settingsDict
        self.client = MongoClient("mongodb://0.0.0.0:27017")
        self.settingsDB = self.client["Settings"]

    def getFieldSetting(self):
        settingsCollection = self.settingsDB["FieldSettings"]
        settings = settingsCollection.find({"id":0})[0]
        for x,y in constraint.items():
            if x != '_id':
                settings[x] = y        
        return settings

    def updateSettings(self):
        settingsCollection = self.settingsDB["FieldSettings"]
        query={"id": 0}
        updateValues = {"$set":{"numOfFields" : self.fSettings.get("numOfFields"), "fieldNames": self.fSettings.get("fieldNames")}}

        settingsCollection.update_one(query,updateValues)

    def close(self):
        self.client.close();