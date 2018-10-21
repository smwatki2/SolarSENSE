# Author: Tresor Cyubahiro
# Date: 10.19.2018
# Description: A program that subscribes to sensor topic and retrieves data sent#              by the sensors
# SolarSENSE Capstone Project


#Install package as 'pip install paho-mqtt'
import paho.mqtt.client as mqtt 
import json
import datetime

file = open("sensorReportData.txt", "a")

def on_connect(client, data, flags, rc):
    print("Connection to Blocker established "+str(rc))
    client.subscribe("miflora/Flora-care")

def on_message(client, data, message):
    jsonData = message.payload.decode("utf-8", "ignore")
    reading = json.loads(jsonData) 

    date = datetime.datetime.now()

    # Write Sensor Data and Date to file
    file.write("Date: "+str(date)+", Data: "+jsonData+"\n")

    print("Reading from topic: "+message.topic+"\n")
    print("Moisture: {} \nConductivity {}\nLight: {}\nTemperature: {} \nBattery: {}\n ".format(reading["moisture"], reading["conductivity"], reading["light"], reading["temperature"], reading["battery"]))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost",1883,60)
client.loop_forever()
