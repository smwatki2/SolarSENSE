import pymongo
from DBUtility import DBUtility

dbName = "FarmInfo";
dbCollectionName="fields"

mongoClient = pymongo.MongoClient("mongodb://localhost:27017")
dbUtil = DBUtility(mongoClient)

if dbUtil.create_database(dbName):
	print(dbName + " created.")

if dbUtil.create_collection(dbName,dbCollectionName):
	print(dbCollectionName + " created.")

dbUtil.read_json(dbName, dbCollectionName, "./DATAFILES/fields.json")
print("Exiting fields Script")
exit(0)
