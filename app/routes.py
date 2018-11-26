import subprocess
import os
import traceback
import json
import time
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
    # subprocess.Popen(['/bin/bash','/usr/local/bin/autofindFlowerCare'])
    #I've been working on this for at least 2 hours today. This is what I've found
        #running the sudo command makes it break
        #the autofindFlowerCare relies on pipes and redirecting stdout to files
        #  apparently Popen does not play well with that, and does not save those files at all.
        # problem is that the lescan only outputs to stdout, and will do so until it is killed
    # So I think it was failing because the lescan output wasn't being captured at all becasue Popen is trying to grab it instead
    # So I'll probably have to run the commands of the autofindFlowerCare script line by line with their own popen lines
    # I was really hoping I would be able to just fork my autofindFlowerCare script in the background and do the webpage stuff while waiting
    # but now I don't know what I'll do
    return render_template('scan.html')

@app.route('/scanScript')
def scanScript():
    file = open("bluetooth_thing.txt", "a")
    # jsonArray = []
    # subprocess.Popen(['hciconfig', 'hci0', 'down'])
    # subprocess.Popen(['hciconfig', 'hci0', 'up'])
    # scan = subprocess.Popen(['hcitool', 'lescan'], stdout=subprocess.PIPE, stdin=subprocess.PIPE)
    os.system("echo $USER > user2.txt")
    os.system("ls > directory2.txt")
    os.system("sudo hcitool lescan > scan2.txt &")
    # scan = subprocess.Popen(['echo $USER'], shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
    # time.sleep(10)
    # scan.kill()
    # scan.wait()
    # output = scan.stdout.readline()
    # result, err = scan.communicate()
    # os.system("hcitool lescan> scan.txt & pkill --signal SIGINT hcitool")
    file.write("Here we go: \n")
    # scan = open("scan.txt", "r")
    # file.write(scan.read())
    # for line in output:
    # file.write(output.decode("utf-8"))
    file.write("ALL DONE\n")
    file.close()

    #jsonArray.append(json.dumps(result))
    #return make_response(jsonify(jsonArray),200,{
    #    'Access-Control-Allow-Origin': '*',
    #    'Access-Control-Allow-Methods' : 'PUT,GET',
    #    'Access-Control-Allow-Headers' : 'Content-Type, Authorization, Content-Length, X-Requested-With'
    #    })

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
