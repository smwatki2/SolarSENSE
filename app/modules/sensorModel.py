import json
import traceback
from pymongo import MongoClient

class Sensor(object):

    def __init__(self, id, mac, field):
        self.id = id
        self.mac = mac
        self.field = field

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
            oneSensor = Sensor(i, 'AD:GF:HD:JD:2' + str(i), 'Field_' + str(i))
            self.sensorsList.append(oneSensor)

    def close(self):
        self.client.close()



