'''
Author: ASU Capstone Team 2018 - 2019
Date: 26/03/2019
Description: Class for managing weekly data and derive weekly trends
'''
import json
import traceback
from datetime import datetime, timedelta
from pymongo import MongoClient

class ReportEntry(object):
    """docstring for ReportEntry"""
    def __init__(self, mac, name, timestamp, temperature, moisture, light, conductivity, battery):
        self.mac = mac
        self.name = name
        self.timestamp = timestamp
        self.temperature = temperature
        self.moisture = moisture
        self.light = light
        self.conductivity = conductivity
        self.battery = battery
    def toString(self):
        return json.dumps(self.__dict__)

class Trends(object):

    def __init__(self):
        self.todayDate = datetime.now()
        self.pastWeekStartDate = self.todayDate  - timedelta(6)
        self.weekData = []
        self.client = MongoClient("mongodb://0.0.0.0:27017")
        self.db = self.client.FarmInfo
        self.collection = self.db.sensorData

    def toString(self):
        return json.dumps(self.__dict__, default=json_util.default)

    def getData(self):
        dataset = self.collection.find()
        for entry in dataset:
                self.weekData.append(entry)

    ''' Function to return a sensor's data for the entire week'''
    def filterBySensor(self, sensorMac):
        #query = {"mac": sensorMac, "$date": {'$lte': self.todayDate.isoformat(), '$gte': self.pastWeekStartDate.isoformat()}}
        query = {"mac": sensorMac}
        sensorData = []
        result = self.collection.find(query)
        for entry in result:
            entry['_id'] = str(entry['_id'])
            parsedEntry = ReportEntry(entry['mac'], entry['name_pretty'], entry['timestamp'], entry['temperature'], entry['moisture'], entry['light'], entry['conductivity'], entry['battery'])
            file = open("debug.txt", "a")
            file.write(parsedEntry.toString())
            file.close()
            sensorData.append(parsedEntry)
        return sensorData

        ''' Function to return a sensor's data for the entire week'''
    def filterByField(self, field):
        query = {"field": field, "$date": {'$lte': self.todayDate.isoformat(), '$gte': self.pastWeekStartDate.isoformat()}}
        sensorData = []
        result = self.collection.find(query)
        for entry in result:
            entry['_id'] = str(entry['_id'])
            parsedEntry = ReportEntry(entry['mac'], entry['name_pretty'], entry['timestamp'], entry['temperature'], entry['moisture'], entry['light'], entry['conductivity'], entry['battery'])
            sensorData.append(parsedEntry)
        return sensorData


    def close(self):
        self.client.close()

