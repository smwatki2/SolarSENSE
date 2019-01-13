import pymongo
import sys
from DBUtility import DBUtility

dbName = "Regions"
collectionName = "RegionInfo"

mongoClient = pymongo.MongoClient("mongodb://localhost:27017")
dbUtil = DBUtility(mongoClient)

if dbUtil.create_database(dbName):
	print(dbName + " created.")

if dbUtil.create_collection(dbName, collectionName):
	print(collectionName + " created.")

dbUtil.read_json(dbName, collectionName,"./DATAFILES/Regions.json")

dbUtil.close_client()
print("Exiting Region Script")
exit(0)