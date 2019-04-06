'''
Author: ASU Capstone Team 2018 - 2019
Date: 26/03/2019
Description: Class for managing weekly data and derive weekly trends
'''
import json
import traceback
from datetime import datetime, timedelta
from pymongo import MongoClient
import numpy as np
from statistics import mean

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

class Slope(object):
    """docstring for Slope"""
    def __init__(self, valueType, value, mac, field):
        self.valueType = valueType
        self.value = value
        self.mac = mac
        self.field = field
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
        self.sensorsCollection = self.db.sensors

    def toString(self):
        return json.dumps(self.__dict__, default=json_util.default)

    def getData(self):
        dataset = self.collection.find()
        for entry in dataset:
                self.weekData.append(entry)

    ''' Function to return a sensor's data for the entire week sorted by timestamp in ascending order'''
    def filterBySensor(self, sensorMac):
        query = {"mac": sensorMac, "timestamp": {"$lt": self.todayDate, "$gte": self.pastWeekStartDate}}
        sensorData = []
        result = self.collection.find(query).sort([('timestamp', 1)])
        for entry in result:
            entry['_id'] = str(entry['_id'])
            entry['timestamp'] = entry['timestamp'].timestamp()
            parsedEntry = ReportEntry(entry['mac'], entry['name_pretty'], entry['timestamp'], entry['temperature'], entry['moisture'], entry['light'], entry['conductivity'], entry['battery'])
            sensorData.append(parsedEntry)
        return sensorData

        '''Function to get the three slopes for values in a field for a specific sensor in that field'''
    def getSlopesFromSensorData(self, data):

        '''Function to generate slope from a dataset'''
    def calculateSlope(self, timeData, valueData):
        xaxis = np.array(timeData, dtype=np.float64)
        yaxis = np.array(valueData, dtype=np.float64)
        slope = (((mean(xaxis) * mean(yaxis)) - mean(xaxis*yaxis)) / ((mean(xaxis)**2) - mean(xaxis**2)))
        return slope
        ''' Function to return a sensor's data for the entire week'''
    def filterByField(self, field):
        allSensorQuery = {"assigned_field": field}
        fieldData = []
        result = self.sensorsCollection.find(allSensorQuery)
        for entry in result:
            fieldData = fieldData + self.filterBySensor(entry['mac'])
        return fieldData


    def close(self):
        self.client.close()

