import logging
import os
from logging.handlers import RotatingFileHandler
#from flask.logging import default_handler
from flask import Flask
from config import Config
from logging.config import dictConfig
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config.from_object(Config)

if not app.debug:
	if not os.path.exists('logs'):
		os.mkdir('logs')
	with open("logs/info.log",'w'):
		pass
	with open("logs/error.log", 'w'):
		pass
	
	file_handler = RotatingFileHandler('logs/info.log',maxBytes=10240,backupCount=10)
	file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
	app.logger.addHandler(file_handler)
	app.logger.setLevel(logging.INFO)
	app.logger.info('SolarSENSE Startup')


from app import routes
