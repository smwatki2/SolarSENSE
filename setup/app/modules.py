from pymongo import MongoClient
from pprint import pprint
from bson.json_util import dumps
import json
import traceback


class SoilDataModel(object):

    def __init__(self):
        self.water = ""
        self.temp = ""
        self.light = ""
        self.humidity = ""

    def getData(self):
        try:
            client = MongoClient("mongodb://127.0.0.1:27017")
            db = client.solarsensereports
            reports = db.reports
            jsonObj = dumps(reports.find())
            return jsonObj
        except Exception as exc:
        	file = open("errorlog.txt","a")
        	file.write(traceback.format_exc())
        	file.close()
