import subprocess
import os
import traceback
import sys
import json
import logging
from pathlib import Path
from app import app
from app.forms import HomeForm
from app.modules.soilalgomodel import *
from app.modules.soilmodels import * 
from app.modules.notificationmodels import *
from app.modules.cropfactormodels import *
from app.modules.historicalmodels import *
from app.modules.constraintmodel import *
from app.modules.regionmodel import *
from app.modules.fieldSettings import *
from app.modules.UtilityModule import Rescan
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


    ''' Enpoint for getting regions '''

@app.route("/getRegions", methods=['GET'])
@cross_origin()
def getRegions():
    regions = []
    regionCollection = RegionCollection()
    for region in regionCollection.getRegions():
        print(region.toString())
        regions.append(region.toString())
    print("Reqest was received")
    regionCollection.close()
    return make_response(jsonify(regions), 200,{
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods' : 'PUT,GET',
        'Access-Control-Allow-Headers' : 'Content-Type, Authorization, Content-Length, X-Requested-With'        
        })   

    ''' Enpoint for saving constraints'''
@app.route('/saveConstraints', methods=['POST'])
@cross_origin()
def saveConstraints():
    constraint = Constraint(request.get_json())
    constraint.updateConstraint()
    print("Save Successful")
    constraint.close()
    return make_response(jsonify("Test Response"), 200,{
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods' : 'PUT,GET',
        'Access-Control-Allow-Headers' : 'Content-Type, Authorization, Content-Length, X-Requested-With'        
        })

@app.route('/getValues', methods=['GET'])
@cross_origin()
def getValues():

    constraint = Constraint()
    soilAlgo = SoilAlgorithm(constraint.getConstraint())
    soilAlgo.setCropStage()
    goalObj = {
        "GoalTempRange" : soilAlgo.goalTempRange(),
        "GoalEvo" : soilAlgo.getGoalEvotransporation()
    }
    actualObj = {
        "WaterActual" : soilAlgo.getEvotransporation(),
        "LightActual" : soilAlgo.getLightMeanActual(),
        "TempActual" : soilAlgo.getTempMeanActual()       
    }
    responseObj = {
        'CropName' : soilAlgo.getCropName(),
        "GoalObj" : goalObj,
        "ActualObj" : actualObj
    }
    constraint.close()
    soilAlgo.close()

    info_logger.info(responseObj)

    return response(responseObj, 200)

@app.route("/changeStage", methods=['POST'])
@cross_origin()
def changeStage():

    stageObj = request.get_json()
    print(stageObj)

    constraint = Constraint()
    soilAlgo = SoilAlgorithm(constraint.getConstraint())
    soilAlgo.setCropStage(stageObj)
    goalObj = {
        "GoalTempRange" : soilAlgo.goalTempRange(),
        "GoalEvo" : soilAlgo.getGoalEvotransporation()
    }
    actualObj = {
        "WaterActual" : soilAlgo.getEvotransporation(),
        "LightActual" : soilAlgo.getLightMeanActual(),
        "TempActual" : soilAlgo.getTempMeanActual()       
    }
    responseObj = {
        'CropName' : soilAlgo.getCropName(),
        "GoalObj" : goalObj,
        "ActualObj" : actualObj
    }
    constraint.close()
    soilAlgo.close()

    return response(responseObj, 200)

''' Given a Region name, return the crops associated with that Region '''
@app.route("/getCrops", methods=['GET'])
@cross_origin()
def getCrops():
    region = request.args.get('region', '')
    client = MongoClient("mongodb://0.0.0.0:27017")
    region_info = client.Regions.RegionInfo.find({"REGION_NAME": region})
    crops = client.CropFactor[region_info[0]['CF_COLLECTION']].find()
    crop_names = []
    for crop in crops:
        crop_names.append(crop['CROPNAME'])
    client.close()
    return make_response(jsonify(crop_names), 200,{
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods' : 'PUT,GET',
        'Access-Control-Allow-Headers' : 'Content-Type, Authorization, Content-Length, X-Requested-With'        
        })
@app.route("/saveFieldSettings", methods=["POST"])
@cross_origin()
def saveFieldSettings():
    setting = FieldSetting(request.get_json())
    setting.updateSettings()
    print("Save Successful")
    setting.close()

    success = {
        "message" : "Save Successful"
    }
    return response(success,200)

@app.route("/scanForSensors", methods=["GET"])
@cross_origin()
def scanForSensors():
    print("Sensors Were Scanned for!")
    rescan = Rescan()
    rescanSucces = rescan.rescan()
    print(type(rescanSucces))
    success = {
        "message" : rescanSucces
    }
    info_logger.info(rescanSucces)
    return response(success,200)
""" END POINTS END HERE """


""" TEST END POINTS START HERE """
    
""" TEST ENDPOINTS END HERE """


""" ERROR HANDLERS START HERE """

@app.errorhandler(500)
def internal_error(error):
    error_logger.warning("500 Internal Server Error")
    errorObj = {
        'status': 500,
        'error' : traceback.format_exc()
    }
    return response(errorObj,500)


@app.errorhandler(404)
def resource_not_found(error):
    error_logger.warning("404 Error Resource Not Found")
    errorObj = {
        'status': 404,
        'error' : traceback.format_exc()
    }
    return response(errorObj, 404)

@app.errorhandler(405)
def method_not_allowed(error):
    error_logger.warning("405 Error: Method Nnot Allowed")
    errorObj = {
        'status' : 405,
        'error' : traceback.format_exc()
    }
    return response(errorObj, 405)

def response(jsonObject, statusCode):
    responseSettingObj = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods' : 'PUT,GET',
        'Access-Control-Allow-Headers' : 'Content-Type, Authorization, Content-Length, X-Requested-With',
        'Cache-Control': 'no-cache, no-store'
    }
    return make_response(jsonify(jsonObject),statusCode,responseSettingObj)

