import subprocess
import os
import traceback
import json
from pathlib import Path
from app import app
from app.forms import HomeForm
from app.modules import SoildDataCollection
from flask import render_template
from flask_jsonpify import jsonify
from bson.json_util import dumps


@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template('index.html')

@app.route('/instant')
def instant():
    return render_template('instant.html')

@app.route('/data', methods=['GET'])
def data():
    jsonArray = []
    sdc = SoildDataCollection()
    for soilObj in sdc.getSoilCollection():
        print(soilObj)
        jsonString = json.dumps(soilObj.getSoilData())
        jsonArray.append(jsonString)
        print(jsonString)
    return jsonify(jsonArray)

@app.route('/scan')
def scan():
    return render_template('scan.html')

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
