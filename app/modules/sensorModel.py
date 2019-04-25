import json
import traceback
from pymongo import MongoClient

class Sensor(object):

    def __init__(self, mac, field):
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
        self.sensorData = self.db.sensorData

    def getSensors(self):
        self.getAll()
        return self.sensorsList

    def getAll(self):
        allSensors = self.collection.find()
        for aSensor in allSensors:
                oneSensor = Sensor(str(aSensor['mac']), aSensor['assigned_field'])
                self.sensorsList.append(oneSensor)

    def updateSensor(self, mac, field):
        query = { "mac" : mac }

        for sensorInfo in self.collection.find(query):
            if sensorInfo['assigned_field'] == field:
                return False
            else:
                updateField = {"$set":{"assigned_field": field}}
                self.collection.update_one(query, updateField)
                # self.filterByMacAndField(query)
                self.deleteByMac(query)
                return True


    def filterByMacAndField(self, query):
        
        for info in self.sensorData.find(query):
            print(info)

    def deleteByMac(self,query):

        self.sensorData.delete_many(query)

    def close(self):
        self.client.close()



