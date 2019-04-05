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

# declare mongo client on port 27017
mongoClient = MongoClient('localhost', 27017)
# declare databse object for database 'solarsensereports'
db = mongoClient['FarmInfo']
# access sensor data collection
reports = db.sensorData

# frequency by default
reminderFrequency = 8 
# For testing purposes, set the above variable to, say 1 (will be in minutes. See function scheduleReminder), and comment the assignment of this variable in getSetFrequency

#timer (global variable !!) 
startTime = datetime.datetime.now();

file = open("sensorReportData.txt", "a")
config_file = open("/opt/miflora-mqtt-daemon/config.ini", "r")

# Retrieve user set frequency from the database
def getSetFrequency():
    try:
        remindersettings = db.reminderSettings
        result = remindersettings.find()
        if result is not None and result.count() > 0:
            for setting in result:
                reminderFrequency = setting['frequency']['frequency']
                print(str(setting))
                print(str(reminderFrequency))
                break

    except Exception as e:
        file = open("errorlog.txt", "a")
        file.write(traceback.format_exc())
        file.close()
            
getSetFrequency()

def on_connect(client, data, flags, rc):
    print("Connection to Blocker established "+str(rc))
    numOfDevices = config_file.read().count("Flora-care")
    for i in range(numOfDevices):
        topic = "miflora/Flora-care" + str(i)
        client.subscribe(topic)
        print("Subscribed to " + str(topic))

def on_message(client, data, message):
    jsonData = message.payload.decode("utf-8", "ignore")
    reading = json.loads(jsonData) 

    timestamp = reading['timestamp']
    isoTimestamp = datetime.datetime.strptime(timestamp,'%Y-%m-%d %H:%M:%S')
    reading['timestamp'] = isoTimestamp
    # Write Sensor Data and Date to file
    file.write(jsonData+"\n")
    # Save sensor data to database
    result = reports.insert_one(reading)
    scheduleReminder()
    print("Reading from topic: "+message.topic+"\n")
    print("Moisture: {} \nConductivity {}\nLight: {}\nTemperature: {} \nBattery: {}\n Sensor: {}\n Time: {}\n MAC ADDRESS: {}\n".format(reading["moisture"],reading["conductivity"], reading["light"], reading["temperature"], reading["battery"], reading["name_pretty"], reading["timestamp"], reading["mac"]))

# Check if enough time has passed to issue a reminder
def scheduleReminder():
    global startTime
    currentTime = datetime.datetime.now()
    timeDiff = currentTime - startTime
    print(str(currentTime))
    print(str(startTime))
    print(str(timeDiff))
    timeDiffHours = (timeDiff.days) + (timeDiff.seconds) // 3600
    if timeDiffHours > reminderFrequency:
        startTime = datetime.datetime.now()
        sendReminder(startTime)
    # Comment 69 - 77, and uncomment 79 - 83 for testing (time in minutes)
    # timeDiffMinutes = (timeDiff.seconds % 3600) // 60
    # print(str(timeDiffMinutes))
    # if timeDiffMinutes > reminderFrequency:
        # startTime = datetime.datetime.now()
        # sendReminder(startTime)

# Schedule a reminder and save it in database
def sendReminder(time):      
    try:
        reminders = db.reminders
        result = reminders.insert_one({'content': "Water at", 'timestamp': '{0:%Y-%m-%d %H:%M:%S}'.format(time)})
    except Exception as e:
        file = open("errorlog.txt", "a")
        file.write(traceback.format_exc())
        file.close()

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost",1883,60)
client.loop_forever()
