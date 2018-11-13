from pymongo import MongoClient
from pprint import pprint
from bson.json_util import dumps
from flask import url_for
import json
import traceback


class SoildDataCollection(object):

    def __init__(self):
        self.soilDataObjects = []

    def getSoilCollection(self):
        self.getData()
        return self.soilDataObjects

    def getData(self):
        try:
            client = MongoClient("mongodb://0.0.0.0:27017")
            #client = MongoClient("mongodb://localhost:27017")
            db = client.solarsensereports
            reports = db.reports
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


class SoilDataModel(object):

    def __init__(self,dictionary):
        self.__dataValues = {}
        for x,y in dictionary.items():
            if x != '_id':
                self.__dataValues[x] = y

    def getSoilData(self):
        return self.__dataValues

