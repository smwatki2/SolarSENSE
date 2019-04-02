import subprocess
import os
import traceback
import sys
import json
import logging
from pathlib import Path
from app import app
from app.forms import HomeForm
from flask import render_template, make_response, request
from flask_jsonpify import jsonify
from flask_cors import cross_origin
from bson.json_util import dumps
from logging.handlers import RotatingFileHandler
import app.modules.trendsModel

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

@app.route('/learn')
def learn():
    return render_template('learn.html')

@app.route('/config')
def config():
    return render_template('config.html')

@app.route('/navigation')
def navigation():
    return render_template('navigation.html')
""" ROUTES END HERE """


""" END POINTS START HERE """


""" END POINTS END HERE """


""" TEST END POINTS START HERE """

''' Test end point for filter sensorDat by Sensor'''
@app.route('/filterBySensor', methods=['GET'])
@cross_origin()
def filterBySensor():
    jsonArray = []
    trendModel = Trends()
    for entry in trendModel.filterBySensor("C4:7C:8D:66:CF:40"):
        print(entry)

    trendModel.close()

    print(make_response(jsonify(jsonArray),200,{
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods' : 'PUT,GET'
        }))
    return make_response(jsonify(jsonArray),200,{
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods' : 'PUT,GET',
        'Access-Control-Allow-Headers' : 'Content-Type, Authorization, Content-Length, X-Requested-With'
        })
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

