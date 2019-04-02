import json
import traceback
from pymongo import MongoClient

class Sensor(object):

    def __init__(self, id, mac):
        self.id = id
        self.mac = mac

    def toString(self):
        return json.dumps(self.__dict__)

class SensorsCollection(object):

    def __init__(self):
        self.sensorsList = []
        self.client = MongoClient("mongodb://0.0.0.0:27017")
        self.db = self.client.solarsensereports

    def getSensors(self):
        self.getAll()
        return self.sensorsList

    def getAll(self):
        for i in range(4):
            oneSensor = Sensor(i, 'AD:GF:HD:JD:23')
            self.sensorsList.append(oneSensor)

    def close(self):
        self.client.close()



