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

""" ROUTES START HERE"""
@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template('index.html')

@app.route('/instant')
def instant():
    return render_template('instant.html')

@app.route('/scan')
def scan():
    return render_template('scan.html')
""" ROUTES END HERE """


""" END POINTS START HERE """
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

    ''' End point for retrieving current notifications ''' 
@app.route('/notifications', methods=['GET'])
@cross_origin()
def notifications():
    newNotifications = []
    notifications = Notifications()
    for newNotification in notifications.getNewNotifications():
        newNotifications.append(newNotification.toString())

    return make_response(jsonify(newNotifications),200,{
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods' : 'PUT,GET',
        'Access-Control-Allow-Headers' : 'Content-Type, Authorization, Content-Length, X-Requested-With'
        })

    ''' End point for testing saving a notification ''' 
@app.route('/notificationSave', methods=['GET'])
@cross_origin()
def notificationSave():
    notifications = Notifications()
    notifications.saveNewNotification("{'water': 12, 'goal': 15}", 0, '2018-11-16 04:43:59')

    return make_response(jsonify('success'),200,{
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods' : 'PUT,GET',
        'Access-Control-Allow-Headers' : 'Content-Type, Authorization, Content-Length, X-Requested-With'
        })

    ''' End point for testing notification deletion ''' 
@app.route('/deleteNotification/<id>', methods=['GET'])
@cross_origin()
def notificationSave():
    notifications = Notifications()
    notifications.deleteNotification(id)

    return make_response(jsonify('success'),200,{
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods' : 'PUT,GET',
        'Access-Control-Allow-Headers' : 'Content-Type, Authorization, Content-Length, X-Requested-With'
        })

""" END POINTS END HERE """


""" TEST END POINTS START HERE """
    
""" TEST ENDPOINTS END HERE """


""" ERROR HANDLERS START HERE """
@app.errorhandler(500)
def internal_error(error):
    file = open("errorlog.txt", "a")
    file.write(traceback.format_exc())
    file.close()
    #return traceback.format_exc()
    return make_response(jsonify({'error': error}),500,{
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods' : 'GET',
        'Access-Control-Allow-Headers' : 'Content-Type, Authorization, Content-Length, X-Requested-With'
        })


@app.errorhandler(404)
def resource_not_found(error):
    file = open("errorlog.txt","a")
    file.write(traceback.format_exc())
    file.close()
    return traceback.format_exc()
