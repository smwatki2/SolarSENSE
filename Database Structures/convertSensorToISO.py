import datetime
import sys
from pymongo import MongoClient

# Converts date to an ISO Object
# This is done to compare dates in Mongo and PyMongo

client = MongoClient("mongodb://0.0.0.0:27017")

if(len(sys.argv) == 2):
	collectionName = sys.argv[1]
else:
	print("Improper Usage:")
	print("This script is mostly with the SolarSenseReports Mongo DB")
	print("This is run by the following commands")
	print("python3 convertHistoricalToISO.py reports")
	client.close()
	exit(0)

db = client.solarsensereports
reports = db['reports']

dateCheck = reports.find_one()

if isinstance(dateCheck['timestamp'],datetime.datetime):
	print("Date is already of ISODate Object")
	client.close()
	exit(0)
else:
	sensorData = reports.find()
	for reading in sensorData:

		origDate = reading['timestamp']
		isodate = datetime.datetime.strptime(reading['timestamp'],'%Y-%m-%d %H:%M:%S')
		query = {'timestamp': origDate}
		update = {'$set': {'timestamp': isodate}}
		reports.update_one(query,update)
	client.close();