'''

	Test Case Module for Databases

	Useage:

		Runs with the test suite
		NOTE: To see how to run without test suite visit:
		@ref: https://docs.python.org/3/library/unittest.html

	Description: Runs all Unit Tests for different databases
	When creating a test method YOU MUST begin the method name
	with test_ or else the python unit test interpretor will
	not understand it is a test method
'''

import unittest
import datetime
from pymongo import MongoClient

print("Running Database Unit Tests")
print("---------------------------")

class TestConstraint(unittest.TestCase):

	def setUp(self):
		self.dbClient = MongoClient("mongodb://0.0.0.0:27017")
		self.constraintDB = self.dbClient['Constraint']
		self.constraintCollection = self.constraintDB ['SolarSENSEConstraint']

	def test_collection_exists(self):
		cCollection = 'SolarSENSEConstraint'
		self.assertIn(cCollection, self.constraintDB.collection_names())

	def test_check_collection_count(self):
		self.assertFalse(self.constraintCollection.count() == 0)

	def test_ISODateFormat(self):

		constraintObj = self.constraintCollection.find_one()
		self.assertTrue(type(constraintObj['DATE']) is datetime.datetime)

	def test_HasProperties(self):

		constraintObj = self.constraintCollection.find_one()
		propertyArray = []

	def tearDown(self):
		self.dbClient.close()

class TestHistorical(unittest.TestCase):

	def setUp(self):
		self.dbClient = MongoClient("mongodb://0.0.0.0:27017")
		self.historicalDB = self.dbClient['HistoricalClimateData']

	def test_MesaCollection(self):

		mesaCollection = self.historicalDB['mesaGatewayClimateData']

		self.assertTrue(mesaCollection.count() > 0)

	def test_Mesa_ISODateFormat(self):

		mesaCollection = self.historicalDB['mesaGatewayClimateData']

		for item in mesaCollection.find():
			self.assertTrue(type(item['date']) is datetime.datetime)


	def tearDown(self):
		self.dbClient.close()






