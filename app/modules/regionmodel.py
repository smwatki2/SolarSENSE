import json
from pymongo import MongoClient


class Region(object):

    def __init__(self, name, cropFactorCollection):
        self.name = name
        self.cfCollection = cropFactorCollection

    def toString(self):
        return json.dumps(self.__dict__)

class RegionCollection(object):

    def __init__(self):
        self.regions = []
        self.client = MongoClient("mongodb://0.0.0.0:27017")
        self.regionDB = self.client.Regions

    def retrieveRegions(self):
        regionInfoCollection = self.regionDB.RegionInfo
        regionInfo = regionInfoCollection.find()
        for info in regionInfo:
            rInfo = Region(info['REGION_NAME'],info['CF_COLLECTION'])
            self.regions.append(rInfo)

    def getRegions(self):
        self.retrieveRegions()
        return self.regions

    def close(self):
        self.client.close()