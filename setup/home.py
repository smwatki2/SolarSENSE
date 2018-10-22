from flask import Flask
from flask import render_template

solarSENSE_app = Flask(__name__)

@solarSENSE_app.route("/")
def basic_test():
    hello = "Welcome to SolarSENSE!!!"
    return render_template('index.html', message=hello) 

if __name__ == "__main__":
 solarSENSE_app.run(host='0.0.0.0')
