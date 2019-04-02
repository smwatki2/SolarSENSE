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
        self.conductivity
        self.battery
    def toString(self):
        return json.dumps(self.__dict__)

class Trends(object):

    def __init__(self):
        self.todayDate = datetime.now()
        self.weekData = []
        self.client = MongoClient("mongodb://0.0.0.0:27017")
        self.db = self.client.FarmInfo
        self.collection = self.db.sensorData

    def toString(self):
        return json.dumps(self.__dict__)

    def getData(self):
        dataset = self.collection.find()
        for entry in dataset:
                self.weekData.append(entry)

    ''' Function to return a sensor's data for the entire week'''
    def filterBySensor(self, sensorMac):
        pastWeekStartDate = self.todayDate  - timedelta(6)
        print(self.todayDate);
        print(pastWeekStartDate);
        query = {"mac": sensorMac, "$date": {'$lte': self.todayDate.isoformat(), '$gte': pastWeekStartDate.isoformat()}}
        #query = {"mac": sensorMac}
        sensorData = []
        result = self.collection.find(query)
        for entry in result:
            sensorData.append(entry)
        return sensorData


    def close(self):
        self.client.close()

