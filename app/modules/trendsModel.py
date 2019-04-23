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
    def __init__(self, light, temperature, moisture, mac, field):
        self.light = light
        self.temperature = temperature
        self.moisture = moisture
        self.mac = mac
        self.field = field
    def toString(self):
        return json.dumps(self.__dict__) 

class Averages(object):
    """docstring for Averages"""
    def __init__(self, light, temperature, moisture, field):
        self.light = light
        self.temperature = temperature
        self.moisture = moisture
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
            sensorData.append(entry)
        return sensorData
        '''Function to extract data for one value from the a sensor data'''
    def generateDataForOneValue(self, data, value):
        extractData = []
        for entry in data:
            extractData.append(entry[value])
        return extractData

        '''Function to get the three slopes for values in a field for a specific sensor in that field'''
    def getSlopesFromSensorData(self, data, mac, field):
        lightData = self.generateDataForOneValue(data, 'light')
        tempData = self.generateDataForOneValue(data, 'temperature')
        moistureData = self.generateDataForOneValue(data, 'moisture')
        timestampData = self.generateDataForOneValue(data, 'timestamp')

        light = self.calculateSlope(timestampData, lightData)
        temperature = self.calculateSlope(timestampData, tempData)
        moisture = self.calculateSlope(timestampData, moistureData)
        slopes = Slope(light, temperature, moisture, mac, field)

        '''
        UNCOMMENT BELOW TO TEST THAT DATA AND CALCULATIONS ARE RIGHT
        file = open("debug.txt", "w")
        file.write("\nFIELD:" + field)
        file.write("\n\n")
        file.write("\n\nLIGHT DATA\n")
        file.write(str(lightData))
        file.write("\n\nTEMP DATA\n\n")
        file.write(str(tempData))
        file.write("\n\nMOISTURE DATA\n\n")
        file.write(str(moistureData))
        file.write("\n\nTIMESTAMP DATA\n\n")
        file.write(str(timestampData))
        file.write("\n\nLIGHT SLOPE:")
        file.write(str(light))
        file.write("\n\nTEMPERATURE SLOPE:")
        file.write(str(temperature))
        file.write("\n\nMOISTURE SLOPE:")
        file.write(str(moisture))
        file.close()
        '''
        return slopes

        '''Function to generate slope from a dataset'''
    def calculateSlope(self, timeData, valueData):
        xaxis = np.array(timeData, dtype=np.float64)
        yaxis = np.array(valueData, dtype=np.float64)
        slope = (((mean(xaxis) * mean(yaxis)) - mean(xaxis*yaxis)) / ((mean(xaxis)**2) - mean(xaxis**2)))
        return slope

        ''' Function to return averages for sensors in a field for the entire week'''
    def filterByField(self, field):
        allSensorQuery = {"assigned_field": field}
        fieldSlopes = []
        result = self.sensorsCollection.find(allSensorQuery)
        for entry in result:
            oneSlope = self.getSlopesFromSensorData(self.filterBySensor(entry['mac']), entry['mac'], field)
            fieldSlopes.append(oneSlope)
        return self.getFieldAverages(fieldSlopes, field)

        '''Function to make averages for data by sensors in a field using slopes generated for each sensor'''
    def getFieldAverages(self, slopes, field):
        lightAverage = 0
        tempAverage = 0
        moistureAverage = 0
        for slope in slopes:
            lightAverage += slope.light
            tempAverage += slope.temperature
            moistureAverage += slope.moisture
        if len(slopes) > 0:
            lightAverage = lightAverage / len(slopes)
            tempAverage = tempAverage / len(slopes)
            moistureAverage = moistureAverage / len(slopes)
        slopeAverages = Averages(lightAverage, tempAverage, moistureAverage, field)
        return slopeAverages.toString()

    def close(self):
        self.client.close()

