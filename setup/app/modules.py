from pymongo import MongoClient
from pprint import pprint
from bson.json_util import dumps
import json

class SoilDataModel(object):

	def __init__(self):
		self.water = ""
		self.temp = ""
		self.light = ""
		self.humidity = ""

	def getData(self):
		client = MongoClient("mongodb://127.0.0.1:27017")
		db = client.solarsensereports
		reports = db.reports
		print(dumps(reports.find()))
		jsonObj = dumps(reports.find())
		return jsonObj


		