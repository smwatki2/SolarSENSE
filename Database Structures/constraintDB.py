import pymongo
from DBUtility import DBUtility

dbName = "Contraint"

mongoClient = pymongo.MongoClient("mongodb://localhost:27017")
dbUtil = DBUtility(mongoClient)

if dbUtil.create_database(dbName):
	print(dbName + " created exiting script")
exit(0)