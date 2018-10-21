# Author: Tresor Cyubahiro
# Date: 10.20.2018
# Description: A program that subscribes to sensor topic and retrieves data sent
#              by the sensors. All sensors post their data to topic mifora/Flora-care
# SolarSENSE Capstone Project

import paho.mqtt.client as mqtt #Install package as 'pip install paho-mqtt'
import json

def on_connect(client, data, flags, rc):
    print("Connection to Blocker established "+str(rc))
    client.subscribe("miflora/Flora-care")

def on_message(client, data, message):
    jsonData = message.payload.decode("utf-8", "ignore")
    reading = json.loads(jsonData) 

    print("Reading from topic: "+message.topic+"\n")
    print("Moisture: {} \nConductivity {}\nLight: {}\nTemperature: {} \nBattery: {}\n ".format(reading["moisture"], reading["conductivity"], reading["light"], reading["temperature"], reading["battery"]))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost",1883,60)
client.loop_forever()
