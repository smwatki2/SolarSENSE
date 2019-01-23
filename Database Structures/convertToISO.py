
import datetime
import sys
from pymongo import MongoClient

# Converts date to an ISO Object
# This is done to compare dates in Mongo and PyMongo

client = MongoClient("mongodb://0.0.0.0:27017")

if(len(sys.argv) == 2):
	collectionName = sys.argv[1]
	print(collectionName)
else:
	print("Improper Usage:")
	print("This script is mostly with the HistoricalClimateData Mongo DB")
	print("This is run by the following commands")
	print("python3 convertToISO.py [collection_name")
	client.close()
	exit(0)

historydb = client['HistoricalClimateData']
historyCollection = historydb[collectionName]

dateCheck = historyCollection.find_one()

if isinstance(dateCheck['date'],datetime.datetime):
	print("Date is already of ISODate Object")
	client.close()
	exit(0)
else:
	history = historyCollection.find()
	print("Running...")
	for item in history:
		origDate = item['date']
		date = origDate.split(" ")
		dateArray = date[0].split("/")
		timeArray = date[1].split(":")
		isoDate = datetime.datetime(int(dateArray[2]), int(dateArray[0]), int(dateArray[1]), int(timeArray[0]), int(timeArray[1]))
		query = {'date': origDate}
		update = {'$set' : {'date' : isoDate}}
		historyCollection.update_one(query, update)
	client.close()