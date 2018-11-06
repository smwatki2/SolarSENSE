import subprocess
import os
from app import app
from app.forms import HomeForm
from flask import render_template


@app.route("/", methods=['GET', 'POST'])
def home():
    hello = "Welcome to SolarSENSE!!!"
    form = HomeForm()
    if form.validate_on_submit():
        if form.generateData.data:
            # print(subprocess.check_output(['ehco', 'hello world']))
            os.system('echo "Hello World!"')
            # result = subprocess.run(['python3', '/opt/miflora-mqtt-daemon/miflora-mqtt-daemon.py'], stdout=subprocess.PIPE)
            # cap_obj = result.stdout
            # print("Test Capture Command Result: " + cap_obj)
            return render_template('index.html', hello=hello + "It's pretty cool", form=form)

    return render_template('index.html', hello=hello, form=form)
