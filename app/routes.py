import subprocess
import os
import traceback
import json
from pathlib import Path
from app import app
from app.forms import HomeForm
from app.modules import SoildDataCollection
from flask import render_template, make_response
from flask_jsonpify import jsonify
from flask_cors import cross_origin
from bson.json_util import dumps


@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template('index.html')

@app.route('/instant')
def instant():
    return render_template('instant.html')

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

@app.route('/scan')
def scan():
    return render_template('scan.html')

@app.route('/scanFind')
def scanFind()
    result = subprocess.run(['sudo', '/usr/local/bin/autofindFlowerCare'], stdout=subprocess.PIPE).stdout.decode('utf-8')
    return render_template('scanFinished.html', scanResults = result)

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
