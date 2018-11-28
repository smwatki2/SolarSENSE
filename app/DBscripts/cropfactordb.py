

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
    print(
        """Error in Usage!\nUSE:\nIf Creating New DB:\npython3 cropfactordb.py [new db name] [collection_name] [json_file_name]
        \nIf Creating New Collection:\npython3 cropfactordb.py [known db name] [collection_name] [json_file_name]""")
    exit(1)


# Test printing the list of dbs in mongo to console

dblist = mongoClient.database_names()

dbUtil = DBUtility(mongoClient)

if dbName in dblist:
    print("Database Already Exists, Checking collection name")
    db = mongoClient[dbName]

    collectionNames = db.collection_names()
    if collection_name not in collectionNames:
        print("Collection Does not exist. Creating Collection " +
              collection_name + "...")
        dbUtil.create_collection(dbName, collection_name)
        dbUtil.read_json(dbName, collection_name, "./DATAFILES/" +json_file)
    else:
    	 print("Collection Exists, exiting script")
else:
    print("Creating Database " + dbName + "...")
    print("Creating " + collection_name + "...")
    dbUtil.create_database(dbName)
    dbUtil.read_json(dbName, collection_name, "./DATAFILES/" + json_file)

exit(0)
