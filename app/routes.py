import subprocess
import os
import traceback
import sys
import json
import logging
from pathlib import Path
from app import app
from app.forms import HomeForm
from app.modules.notificationmodels import *
from flask import render_template, make_response, request
from flask_jsonpify import jsonify
from flask_cors import cross_origin
from bson.json_util import dumps
from logging.handlers import RotatingFileHandler

info_file_handler = RotatingFileHandler('logs/info.log',maxBytes=10240,backupCount=10)
info_file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
info_logger = logging.getLogger("app")
info_logger.addHandler(info_file_handler)
info_logger.setLevel(logging.INFO)

error_file_handler = RotatingFileHandler('logs/error.log',maxBytes=10240,backupCount=10)
error_file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
error_logger = logging.getLogger("app")
error_logger.addHandler(error_file_handler)
error_logger.setLevel(logging.WARNING)

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

@app.route('/learn')
def learn():
    return render_template('learn.html')

@app.route('/status')
def status():
    return render_template('status.html')

@app.route('/config')
def config():
    return render_template('config.html')
""" ROUTES END HERE """


""" END POINTS START HERE """
@app.route('/data', methods=['GET'])
@cross_origin()
def data():
    jsonArray = []
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

    notifications.close()

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
    notifications.saveNewNotification(12, 15, '2018-11-16 04:43:59')

    return make_response(jsonify('success'),200,{
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods' : 'PUT,GET',
        'Access-Control-Allow-Headers' : 'Content-Type, Authorization, Content-Length, X-Requested-With'
        })

    ''' End point for testing notification deletion ''' 
@app.route('/deleteNotification/<id>', methods=['GET'])
@cross_origin()
def deleteNotification(id):
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
    error_logger.warning("500 Internal Server Error")
    errorObj = {
        'status': error.code,
        'error' : traceback.format_exc()
    }
    return response(errorObj,error.code)


@app.errorhandler(404)
def resource_not_found(error):
    error_logger.warning("404 Error Resource Not Found")
    errorObj = {
        'status': error.code,
        'error' : traceback.format_exc()
    }
    return response(errorObj, error.code)

@app.errorhandler(405)
def method_not_allowed(error):
    error_logger.warning("405 Error: Method Nnot Allowed")
    errorObj = {
        'status' : error.code,
        'error' : traceback.format_exc()
    }
    return response(errorObj, error.code)

def response(jsonObject, statusCode):
    responseSettingObj = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods' : 'PUT,GET',
        'Access-Control-Allow-Headers' : 'Content-Type, Authorization, Content-Length, X-Requested-With',
        'Cache-Control': 'no-cache, no-store'
    }
    return make_response(jsonify(jsonObject),statusCode,responseSettingObj)

