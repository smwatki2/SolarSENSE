import json
import traceback
from pymongo import MongoClient

class SoildDataCollection(object):

    def __init__(self):
        self.soilDataObjects = []
        self.client = MongoClient("mongodb://0.0.0.0:27017")
        # TODO: change to new mongo database/collection
        self.db = self.client.solarsensereports

    def getSoilCollection(self):
        self.getData()
        return self.soilDataObjects

    def getData(self):
        try:
            reports = self.db.reports
            jsonObj = reports.find()
            print("[DEBUG MODULES] ")
            print(jsonObj)
            for obj in jsonObj:
                sdm = SoilDataModel(obj)
                self.soilDataObjects.append(sdm)
        except Exception as e:
            file = open("errorlog.txt", "a")
            file.write(traceback.format_exc())
            file.close()

    def hasDocuments(self, collection):
        if(collection.find() > 0):
            return True
        else:
            return False

    def getLastData(self, number):
        try:
            reports = self.db.reports
            jsonObj = reports.find().sort("_id",-1).limit(number)
            for obj in jsonObj:
                sdm = SoilDataModel(obj)
                self.soilDataObjects.append(sdm)
        except Exception as e:
            file = open("errorlog.txt", "a")
            file.write(traceback.format_exc())
            file.close()
        return self.soilDataObjects

    def close(self):
        self.client.close()


class SoilDataModel(object):

    def __init__(self,dictionary):
        self.__dataValues = {}
        for x,y in dictionary.items():
            if x != '_id':
                self.__dataValues[x] = y
                if(type(y) == datetime.datetime):
                    self.__dataValues[x] = y.isoformat()

    def getSoilData(self):
        return self.__dataValues



