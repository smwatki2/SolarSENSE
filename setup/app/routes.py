'''
    Author: ASU Capstone Team 2018
    Description: Routes and endpoints for the solarsense REST API
'''
import subprocess
import os
import traceback
import json
from pathlib import Path
from app import app
from app.forms import HomeForm
from app.modules import SoildDataCollection
from app.modules import Notifications
from flask import render_template, make_response
from flask_jsonpify import jsonify
from flask_cors import cross_origin
from bson.json_util import dumps


''' =============== ROUTES ================ '''
@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template('index.html')

@app.route('/instant')
def instant():
    return render_template('instant.html')

@app.route('/scan')
def scan():
    return render_template('scan.html')

''' =============== END OF ROUTES ================ '''


''' =============== ENDPOINTS ================ '''
@app.route('/data', methods=['GET'])
@cross_origin()
def data():
    jsonArray = []
    sdc = SoildDataCollection()
    for soilObj in sdc.getSoilCollection():
        print(soilObj)
        jsonString = json.dumps(soilObj.getSoilData())
        jsonArray.append(jsonString)
        print(jsonString)

    print(make_response(jsonify(jsonArray),200,{
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods' : 'PUT,GET'
        }))
    return make_response(jsonify(jsonArray),200,{
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods' : 'PUT,GET',
        'Access-Control-Allow-Headers' : 'Content-Type, Authorization, Content-Length, X-Requested-With'
        })

    
    """ end point for retrieving notifications """
@app.route('/get/notifications', methods=['GET'])
@cross_origin()
def data():
    newNotifications = []
    notifications = Notifications()
    for newNotification in notifications.getNewNotifications():
        toString = json.dumps(newNotification)
        newNotifications.append(toString)

    return make_response(jsonify(newNotifications),200,{
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods' : 'PUT,GET',
        'Access-Control-Allow-Headers' : 'Content-Type, Authorization, Content-Length, X-Requested-With'
        })

''' =============== END OF ENDPOINTS ================ '''



''' =============== TEST END POINTS ================ '''

''' =============== END OF TEST ENDPOINTS ================ '''


''' =============== ERROR HANDLERS ================ '''
@app.errorhandler(500)
def internal_error(error):
    file = open("errorlog.txt", "a")
    file.write(traceback.format_exc())
    file.close()
    return traceback.format_exc()


@app.errorhandler(404)
def resource_not_found(error):
    file = open("errorlog.txt","a")
    file.write(traceback.format_exc())
    file.close()
    return traceback.format_exc()
''' =============== END OF ERROR HANDLERS ================ '''
