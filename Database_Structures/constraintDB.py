import pymongo
from DBUtility import DBUtility

# TODO No longer need this file: constraintDB.py
# TODO Remove the constrint DB from Mongo
dbName = "Constraint"
collectionName = "SolarSENSEConstraint"

mongoClient = pymongo.MongoClient("mongodb://localhost:27017")
dbUtil = DBUtility(mongoClient)

if dbUtil.create_database(dbName):
	print(dbName + " created.")

if dbUtil.create_collection(dbName, collectionName):
	print(collectionName + " created.")

dbUtil.read_json(dbName,collectionName, "./DATAFILES/Constraints.json")

dbUtil.close_client();
print("Exiting Constraint Script")
exit(0)
