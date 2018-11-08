import subprocess
import os
from pathlib import Path
from app import app
from app.forms import HomeForm
from flask import render_template
from app.modules import SoilDataModel


@app.route("/", methods=['GET', 'POST'])
def home():
    hello = "Welcome to SolarSENSE!!!"
    form = HomeForm()
    sdm = SoilDataModel()
    if form.validate_on_submit():
        if form.generateData.data:
            obj = sdm.getData()
            # print(subprocess.check_output(['ehco', 'hello world']))
            # file = Path("./app/static/log.txt")
            # if file.exists():
            #     print("File exists")
            #     log = open("./app/static/log.txt","w")
            # else:
            #     print("File does not exist")
            #     log = open("./app/static/log.txt","a")
            # # with open('/static/log.txt','a') as log:
            #     subprocess.call(['echo', 'Hello World'], stdout=log)
            #     log.close()
            # print(os.getcwd())
            # result = subprocess.run(['python3', '/opt/miflora-mqtt-daemon/miflora-mqtt-daemon.py'], stdout=subprocess.PIPE)
            # cap_obj = result.stdout
            # print("Test Capture Command Result: " + cap_obj)
            return render_template('index.html', hello=hello, form=form, result=obj)

    return render_template('index.html', hello=hello, form=form)
