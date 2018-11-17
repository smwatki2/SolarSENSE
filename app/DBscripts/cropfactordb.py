

import pymongo
import subprocess

# Create the client object to connect to the Mongo DB Server

mongoClient = pymongo.MongoClient("mongodb://localhost:27017")

# Test printing the list of dbs in mongo to console

dblist = mongoClient.database_names()

# if "test" in dblist:
# 	print("Yay its there")
# else:
# 	print("sorry not there yet")
# 	print("We'll get that db working right now")

for db in dblist:
	if "test" == db:
		print("Yay test was found")
		break
	else:
		print("You have no idea what you are doing do you?")
