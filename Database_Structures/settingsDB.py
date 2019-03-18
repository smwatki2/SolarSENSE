import pymongo
from DBUtility import DBUtility

dbName = "Settings"
collectionName = "FieldSettings"

mongoClient = pymongo.MongoClient("mongodb://localhost:27017")
dbUtil = DBUtility(mongoClient)

if dbUtil.create_database(dbName):
	print(dbName + " created.")

if dbUtil.create_collection(dbName, collectionName):
	print(collectionName + " created.")

dbUtil.read_json(dbName,collectionName, "./DATAFILES/DefaultSettings.json")

dbUtil.close_client();
print("Exiting Settings Script")
exit(0)