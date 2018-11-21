
import pymongo
import json

class DBUtility(object):
	
	def __init__(self, clientConnection, dbName, collectionName):
		self.mongoClient = clientConnection
		self.dbName = dbName
		self.collectionName = collectionName

	def create_database(self):

		# A dummy object is used to create the intial database and collection
		# This is done because a DB MUST have at least one Collection and that
		# Collection MUST have at least one Document
		dummyObject = { "id": 0,  "initialObj": "intial object ignore"}
		newDB = self.mongoClient[self.dbName]
		newCol = newDB[self.collectionName]
		newCol.insert_one(dummyObject)
		print(self.dbName + " was created with collection " + self.collectionName)

	def read_json(self, jsonFilePath):
		db = self.mongoClient[self.dbName]
		col = db[self.collectionName]
		with open(jsonFilePath) as jsonFile:
			jsonObj = json.load(jsonFile)
		for (k,v) in jsonObj.items():
			for crop in v:
				col.insert_one(crop)
		col.delete_one({"id" : 0}) # Removes dummy value from the collection

