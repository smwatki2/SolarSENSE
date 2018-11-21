

import pymongo
import subprocess
import sys
from DBUtility import DBUtility

# Create the client object to connect to the Mongo DB Server

mongoClient = pymongo.MongoClient("mongodb://localhost:27017")

if(len(sys.argv) > 0 and len(sys.argv) == 4):
	dbName = sys.argv[1]
	collection_name = sys.argv[2]
	json_file = sys.argv[3]
else:
	print("Error in Usage!\n USE: python3 cropfactordb.py [dbname] [collection_name] [json_file_name]")
	exit(1)


# Test printing the list of dbs in mongo to console

dblist = mongoClient.database_names()

for db in dblist:
	if dbName == db:
		print("Database Already Exists, exiting script")
		exit(0)
	else:
		print("Creating Database " + dbName + "...")
		dbUtil = DBUtility(mongoClient,dbName,collection_name)
		print("Creating " + collection_name + "...")
		dbUtil.create_database()
		dbUtil.read_json("./DATAFILES/" + json_file)
		exit(0)


