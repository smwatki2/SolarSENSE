# Author: ASU Capstone Team 2018
# Date: 10.25.2018
# Description: A program that subscribes to sensor topic and retrieves data sent
#              by the sensors, and saves the data to a MongoDB database
# SolarSENSE Capstone Project


#Install package as 'pip install paho-mqtt'
import paho.mqtt.client as mqtt 
import pymongo
from pymongo import MongoClient
import json
import datetime
from app.modules import Notifications

# declare mongo client on port 27017
mongoClient = MongoClient('localhost', 27017)
# declare databse object for database 'solarsensereports'
db = mongoClient['solarsensereports']
# access sensor data collection
reports = db.reports

file = open("sensorReportData.txt", "a")

def on_connect(client, data, flags, rc):
    print("Connection to Blocker established "+str(rc))
    client.subscribe("miflora/Flora-care")

def on_message(client, data, message):
    jsonData = message.payload.decode("utf-8", "ignore")
    reading = json.loads(jsonData) 

    # Write Sensor Data and Date to file
    file.write(jsonData+"\n")
    # Save sensor data to database
    result = reports.insert_one(reading)

    # Retrieve current and required water level
    currentWaterLevel = getCurrentWaterLevel()
    requiredWaterLevel = getRequiredWaterLevel()

    # Check if the current condition needs attention and notify farmer
    if (waterIsLow(currentWaterLevel, requiredWaterLevel)):
        notifyFarmer(currentWaterLevel, requiredWaterLevel, reading["timestamp"])

    print("Reading from topic: "+message.topic+"\n")
    print("Moisture: {} \nConductivity {}\nLight: {}\nTemperature: {} \nBattery: {}\n Sensor: {}\n Time: {}\n MAC ADDRESS: {}\n".format(reading["moisture"],reading["conductivity"], reading["light"], reading["temperature"], reading["battery"], reading["name_pretty"], reading["timestamp"], reading["mac"]))

# Method to compare water levels
def waterIsLow(actual, goal):
    if (actual < goal):
        return True
    else:
        return False

# Method to generate and push a notification 
def notifyFarmer(actual, goal, timestamp):
    notifications.saveNewNotification(actual, goal, timestamp)

# Method to calculate actual water level
# Currently a place holder/ Skeleton
def getCurrentWaterLevel():
    return 0

# Method to calculate required water level
# Currently a place holder/ Skeleton
def getRequiredWaterLevel():
    return 0

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost",1883,60)
client.loop_forever()
