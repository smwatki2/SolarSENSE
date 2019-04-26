import unittest
import json
import ast
from app import app

from app.modules.sensorModel import *
from app.modules.fieldsModel import *
from flask_jsonpify import jsonify


class EndpointsUnitTest(unittest.TestCase):

	def setUp(self):
		self.app = app.test_client()
		self.app.testing = True

	def test_get_sensors(self):

		response = self.app.get("/getSensors")
		responseDict = ast.literal_eval(json.loads(response.data)[0])
		self.assertIsNotNone(responseDict)

	def test_for_sensor_mac(self):

		response = self.app.get("/getSensors")
		responseDict = ast.literal_eval(json.loads(response.data)[0])
		self.assertIsNot(responseDict['mac'],"")

	def test_edit_sensor(self):

		testSensorData = {"mac":"AA:AA:AA:AA:AA:AA","field":"UNIT_TEST"}
		postResponse = self.app.post("/editSensor", data=json.dumps(testSensorData),content_type='application/json')
		self.assertTrue(postResponse.status_code,200)

	def test_get_fields(self):

		response = self.app.get("/getFields")
		responseDict = ast.literal_eval(json.loads(response.data)[0])
		self.assertIsNotNone(responseDict)

	def test_set_fields(self):

		testFieldNames = {"fieldNames" : [{"fieldName" : "UNIT_TEST_1"},{"fieldName" : "UNIT_TEST_2"}]}
		postResponse = self.app.post("/setFields", data=json.dumps(testFieldNames), content_type='application/json')
		self.assertTrue(postResponse.status_code, 200)