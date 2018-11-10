import subprocess
import os
import traceback
from pathlib import Path
from app import app
from app.forms import HomeForm
from app.modules import SoilDataModel
from flask import render_template


@app.route("/", methods=['GET', 'POST'])
def home():
    hello = "Welcome to SolarSENSE!!!"
    form = HomeForm()
    sdm = SoilDataModel()
    if form.validate_on_submit():
        if form.generateData.data:
            obj = sdm.getData()
            return render_template('index.html', hello=hello, form=form, result=obj)

    return render_template('index.html', hello=hello, form=form)

@app.route('/instant')
def instant():
    return render_template('instant.html')

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
