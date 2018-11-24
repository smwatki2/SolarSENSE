import pymongo
import subprocess
import sys
import os
from DBUtility import DBUtility

# Create the client object to connect to the Mongo DB Server
dbName = 'HistoricalClimateData'

mongoClient = pymongo.MongoClient("mongodb://localhost:27017")
dbUtil = DBUtility(mongoClient)
dbUtil.create_database('HistoricalClimateData') #creates the db whether it exists or not

#create collections for all of the csv files
files = os.listdir('./DATAFILES')
for elem in files:
	if elem.lower().endswith('.csv'):
		collection_name = elem[0].lower() + elem[1:len(elem)-4]
		if (dbUtil.create_collection('HistoricalClimateData', collection_name)):
			print('### reading in ' + elem + ' ###')
			dbUtil.read_csv('HistoricalClimateData', collection_name, "./DATAFILES/" + elem)
			print('### done reading in ' + elem + ' ###')
		else:
			print('### not reading in '+elem+' ###')

exit(0)
