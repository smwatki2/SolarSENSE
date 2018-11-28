import pymongo
import json
import csv

class DBUtility(object):
	
	def __init__(self, clientConnection):
		self.mongoClient = clientConnection

	def create_database(self, dbName):

		# A dummy object is used to create the intial database and collection
		# This is done because a DB MUST have at least one Collection and that
		# Collection MUST have at least one Document
		dummyObject = { "id": 0,  "initialObj": "intial object ignore"}
		dbNames = self.mongoClient.database_names()
		if dbName in dbNames:
			print(dbName + ' already exists')
			return False #returns false if the db exists and the operation was not successful
		else:
			newDB = self.mongoClient[dbName]
			newCol = newDB['dummyCollection']
			newCol.insert_one(dummyObject)

	def create_collection(self, dbName, collectionName):
		db = self.mongoClient[dbName]
		if collectionName in db.collection_names():
			print('### ' + collectionName + ' already exists ###')
			return False
		else:
			dummyObject = { "id": 0,  "initialObj": "intial object ignore"}
			newCol = db[collectionName]
			newCol.insert_one(dummyObject)
			return True

	def read_json(self, dbName, collectionName, jsonFilePath):
		db = self.mongoClient[dbName]
		col = db[collectionName]
		with open(jsonFilePath) as jsonFile:
			jsonObj = json.load(jsonFile)
		for (k,v) in jsonObj.items():
			for crop in v:
				col.insert_one(crop)
		col.delete_one({"id" : 0}) # Removes dummy value from the collection
		
	def read_csv(self, dbName, collectionName, csvFilePath):
		db = self.mongoClient[dbName]
		col = db[collectionName]
		csvFile = open(csvFilePath, 'r')
		reader = csv.DictReader(csvFile)
		for row in reader:
			col.insert_one(row)
		col.delete_one({"id" : 0}) # Removes dummy value from the collection

