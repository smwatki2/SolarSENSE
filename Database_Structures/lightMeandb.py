import pymongo
from DBUtility import DBUtility

dbName = "MeanLightValues";
dbCollectionName="NorthSouthLatValues"

mongoClient = pymongo.MongoClient("mongodb://localhost:27017")
dbUtil = DBUtility(mongoClient)

if dbUtil.create_database(dbName):
	print(dbName + " created.")

if dbUtil.create_collection(dbName,dbCollectionName):
	print(dbCollectionName + " created.")

dbUtil.read_json(dbName, dbCollectionName, "./DATAFILES/LightMeanValues.json")
print("Exiting LightMeanValues Script")
exit(0)