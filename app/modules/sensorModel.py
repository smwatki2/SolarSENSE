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
        self.db = self.client.FarmInfo
        self.collection = self.db.sensors

    def getSensors(self):
        self.getAll()
        return self.sensorsList

    def getAll(self):
        allSensors = self.collection.find()
        for aSensor in allSensors:
                oneSensor = Sensor(str(aSensor['_id']), str(aSensor['mac']), aSensor['assigned_field'])
                self.sensorsList.append(oneSensor)

    def updateSensor(self, mac, field):
        query = { "mac" : mac }
        updateField = {"$set":{"assigned_field": field}}
        self.collection.update_one(query, updateField)

    def close(self):
        self.client.close()



