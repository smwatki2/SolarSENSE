from pymongo import MongoClient
from pprint import pprint
from bson.json_util import dumps
from flask import url_for
from calendar import monthrange
import json
import traceback
import datetime


client = MongoClient("mongodb://0.0.0.0:27017")
#client = MongoClient("mongodb://localhost:27017")
db = client.solarsensereports
historicalDb = client.HistoricalClimateData
cropFactorDb = client.CropFactor
constraintsDb = client.Constraint
regionDB = client.Regions

class SoildDataCollection(object):

    def __init__(self):
        self.soilDataObjects = []

    def getSoilCollection(self):
        self.getData()
        return self.soilDataObjects

    def getData(self):
        try:
            reports = db.reports
            jsonObj = reports.find()
            print("[DEBUG MODULES] ")
            print(jsonObj)
            for obj in jsonObj:
                sdm = SoilDataModel(obj)
                self.soilDataObjects.append(sdm)
        except Exception as e:
            file = open("errorlog.txt", "a")
            file.write(traceback.format_exc())
            file.close()

    def hasDocuments(self, collection):
        if(collection.find() > 0):
            return True
        else:
            return False

    def getLastData(self, number):
        try:
            reports = db.reports
            jsonObj = reports.find().sort("_id",-1).limit(number)
            for obj in jsonObj:
                sdm = SoilDataModel(obj)
                self.soilDataObjects.append(sdm)
        except Exception as e:
            file = open("errorlog.txt", "a")
            file.write(traceback.format_exc())
            file.close()
        return self.soilDataObjects


class SoilDataModel(object):

    def __init__(self,dictionary):
        self.__dataValues = {}
        for x,y in dictionary.items():
            if x != '_id':
                self.__dataValues[x] = y

    def getSoilData(self):
        return self.__dataValues

'''
Notifications class
'''
class Notification(object):
    """ This is a class for a notification """
    def __init__(self, current, goal, timestamp):
        self.current = current
        self.goal = goal
        self.timestamp = timestamp

    def __init__(self, id, current, goal, timestamp):
        self.id = id
        self.current = current
        self.goal = goal
        self.timestamp = timestamp
    
    def toString(self):
        return json.dumps(self.__dict__)


class Notifications(object):
    """This is a class for all app's instance Notifications"""
    def __init__(self):
        self.allNotifications = []

        """ method to get new notifications """
    def getNewNotifications(self):
        self.checkNewNotifications()
        return self.allNotifications

    def checkNewNotifications(self):
        try:
            notifications = db.notifications
            newNotifications = notifications.find()
            for newNotification in newNotifications:
                newNotification['_id'] = str(newNotification['_id'])
                notif = Notification(newNotification['_id'], newNotification['current'], newNotification['goal'], newNotification['timestamp'])
                self.allNotifications.append(notif)
        except Exception as e:
            file = open("errorlog.txt", "a")
            file.write(traceback.format_exc())
            file.close()

        """ method to save a new notification """
    def saveNewNotification(self, current, goal, timestamp):
        try:
            notifications = db.notifications
            #newNotification = Notification(current, goal, timestamp)
            #toJson = json.loads(newNotification.toString()) 
            result = notifications.insert_one({'timestamp': timestamp, 'current': current, 'goal': goal})

        except Exception as e:
            file = open("errorlog.txt", "a")
            file.write(traceback.format_exc())
            file.close()
        """ method to delete a notification """
    def deleteNotification(self, id):
        try:
            notifications = db.notifications
            query = {'_id': id}
            result = notifications.delete_one(query)

        except Exception as e:
            file = open("errorlog.txt", "a")
            file.write(traceback.format_exc())
            file.close()


'''
Factors class
'''
class Factors(object):
    """ This is a class for a crop's factors """
    def __init__(self, cropid, name, mid, germination, harvest):
        self.cropid = cropid
        self.name = name
        self.mid = mid
        self.germination = germination
        self.harvest = harvest
    
    def toString(self):
        return json.dumps(self.__dict__)

'''
Crop Factor Class
'''       
class CropFactor(object):
    """docstring for CropFactor"""
    def __init__(self, crop):
        self.crop = crop
        self.cropFactors = []

    """ method to get crop's crop factor """
    def getCropFactor(self):
        self.retrieveCropFactor()
        return self.cropFactors

    def retrieveCropFactor(self):
        try:
            cropFactorCollection = cropFactorDb.AZTest
            query = {'CROPNAME': self.crop}
            cropFactors = cropFactorCollection.find(query)
            for cropFactor in cropFactors:
                factors = Factors(cropFactor['CROPID'], cropFactor['CROPNAME'], cropFactor['CROPCO_MID'], cropFactor['CROPCO_G'], cropFactor['CROPCO_HARV'])
                self.cropFactors.append(factors)

        except Exception as e:
            file = open("errorlog.txt", "a")
            file.write(traceback.format_exc())
            file.close()

'''
Historical Data Object
'''
class HistoricalReport(object):
    """ This is a class for Historical Data Object """
    def __init__(self, hourlyDewPointTemp, locationID, hourlyWindSpeed, hourlyDryBulbTemp, hourlyRelHumidity, hourlyPrecip, date, sublocationID, hourlyWindDirection):
        self.hourlyDewPointTemp = hourlyDewPointTemp
        self.locationID = locationID
        self.hourlyWindSpeed = hourlyWindSpeed
        self.hourlyDryBulbTemp = hourlyDryBulbTemp
        self.hourlyRelHumidity = hourlyRelHumidity
        self.hourlyPrecip = hourlyPrecip
        self.date = date
        self.sublocationID = sublocationID
        self.hourlyWindDirection = hourlyWindDirection
    
    def toString(self):
        return json.dumps(self.__dict__)
            
'''
Historical Data Class
'''       
class HistoricalData(object):
    """docstring for HistoricalData"""
    def __init__(self, country, location, datetime):
        self.country = country
        self.location = location
        self.datetime = datetime
        self.weatherData = []

    """ method to get country's historical data """
    def getHistoricalData(self):
        self.retrieveHistoricalData()
        return self.weatherData

    def retrieveHistoricalData(self):
        try:
            locationDataCollection = historicalDb.mesaGatewayClimateData
            query = {'location_id': self.country, 'sublocation_id': self.location, 'date': self.datetime}
            allData = locationDataCollection.find(query)
            for data in allData:
                report = HistoricalReport(data['hourly_dew_point_temp'], data['location_id'], data['hourly_wind_speed'], data['hourly_drybulb_temp'], data['hourly_rel_humidity'], data['hourly_precip'], data['date'], data['sublocation_id'], data['hourly_wind_direction'])
                self.weatherData.append(report)

        except Exception as e:
            file = open("errorlog.txt", "a")
            file.write(traceback.format_exc())
            file.close()

    def monthlyAverageTemperature(self):
        date = datetime.datetime.today()
        monthInt = date.month
        daysInMonth = monthrange(2017, monthInt)[1]

        historyCol = historicalDb['mesaGatewayClimateData']
        maxTemp = []
        minTemp = []

        for x in range(daysInMonth):
            tempArray = []
            histByDay = historyCol.find({'date':{'$gte':datetime.datetime(2017,monthInt,x + 1,0,0,0),'$lt':datetime.datetime(2017,monthInt,x + 1,23,59,59)}})
            for item in histByDay:
                if item['hourly_drybulb_temp'] == '':
                    continue
                tempArray.append(int(item['hourly_drybulb_temp']))
            maxTemp.append(max(tempArray))
            minTemp.append(min(tempArray))
            tempArray.clear()

        meanMaxTemp = sum(maxTemp) / daysInMonth
        meanMinTemp = sum(minTemp) / daysInMonth

        meanTemp = (meanMaxTemp + meanMinTemp) / 2
        return meanTemp

    def monthlyAverageSunlight(self):
        date = datetime.datetime.today()
        monthInt = date.month
        yearInt = date.year
        daysInMonth = monthrange(yearInt, monthInt)[1]

        # historyCol = historicalDb['mesaGatewayClimateData']
        reportsCol = db['reports']
        maxLight = []
        minLight = []
        for x in range(daysInMonth):
            tempArray = []
            histByDay = reportsCol.find({'timestamp':{'$gte':datetime.datetime(yearInt,monthInt,x + 1,0,0,0),'$lt':datetime.datetime(yearInt,monthInt,x + 1,23,59,59)}})
            if(histByDay.count() == 0):
                continue
            for item in histByDay:
                tempArray.append(item['light'])
            maxLight.append(max(tempArray))
            minLight.append(min(tempArray))
            tempArray.clear()

        meanMaxLight = sum(maxLight) / daysInMonth
        meanMinLight = sum(minLight) / daysInMonth

        meanLight = (meanMaxLight + meanMinLight) / 2
        return meanLight

'''
Constraint class
'''

class Constraint(object):

    def __init__(self, constraintDict = None):
        if constraintDict is not None:
            self.constraint = constraintDict

    def getConstraint(self):
        constraintCollection = constraintsDb.SolarSENSEConstraint
        constraint = constraintCollection.find({"ID":0})[0]
        for x,y in constraint.items():
            if x != '_id':
                constraint[x] = y        
        return constraint

    def updateConstraint(self):
        constrainCollection = constraintsDb.SolarSENSEConstraint
        query = { "ID" : 0 }
        updateVals = {"$set":{"REGION": self.constraint.get("region"),"CROPNAME": self.constraint.get('crop'), "SEASON": self.constraint.get('season'), "DATE": self.constraint.get('date'), "CF_COLLECTION": self.constraint.get('cfCollection')}}

        constrainCollection.update_one(query,updateVals)
        for constraint in constrainCollection.find():
            print(constraint)
        

'''
Region Class
'''

class Region(object):

    def __init__(self, name, cropFactorCollection):
        self.name = name
        self.cfCollection = cropFactorCollection

    def toString(self):
        return json.dumps(self.__dict__)

class RegionCollection(object):

    def __init__(self):
        self.regions = []

    def retrieveRegions(self):
        regionInfoCollection = regionDB.RegionInfo
        regionInfo = regionInfoCollection.find()
        for info in regionInfo:
            rInfo = Region(info['REGION_NAME'],info['CF_COLLECTION'])
            self.regions.append(rInfo)

    def getRegions(self):
        self.retrieveRegions()
        return self.regions

class SoilAlgorithm(object):
    """
    My thinking is to leave this as generic as possible in case we switch to a more
    complicated Algorith which may or may not still use some of these variables
    """

    def __init__(self,cropFactorCollection = None):

        # This value is a test value based in AZ, others will be added as a constraint
        # TODO: Add a property to constraint or to Region db for lat value.
        self.historical = HistoricalData('USA', 'AZ', datetime.datetime.today())

        # This value is derived from a table based on lat and lon, not calculated
        self.dPercentofDaylight = 0.23

        """ Let's figure out how to get the constaints that the user set"""
        constrainCollection = constraintsDb.SolarSENSEConstraint
        if cropFactorCollection is not None:
            self.cfCollection = cropFactorCollection

        self.cropFactors = {};

        # grab historical data right away, in case sensor data is unavailable
        # I'm not sure how to get the historical data quite yet, so I'll leave in 0s for now.
        self.mean_daily_percentage_daylight = 0 #percentage between 0 and 1 (ex: 25% == 0.25)
        self.goal_mean_temp = 0
        self.mean_temp = 0 # In degrees celcius

        # self.evotransporation = self.mean_daily_percentage_daylight * (0.457 * self.mean_temp + 8.128) # mm per day
        self.goalevotransporation = 0
        self.evotransporation = 0

    def getMeanDaylight(self):
        return self.mean_daily_percentage_daylight

    def getMeanTemp(self):
        return self.mean_temp

    def setMeanDaylight(self, light):
        self.mean_daily_percentage_daylight = light

    def setGoalMeanTemp(self):

        meanTemp = self.historical.monthlyAverageTemperature()
        self.goal_mean_temp = meanTemp    

    def setCropFactors(self):
        cropID = ""
        regionCrops = cropFactorDb[self.cfCollection["CF_COLLECTION"]]
        cropFactors = cropFactorDb.CropFactors

        crops = regionCrops.find()

        for crop in crops:
            if crop['CROPNAME'] == self.cfCollection['CROPNAME']:
                cropID = crop['CROPID']

        cfactors = cropFactors.find_one({'CROPID': cropID})

        for x, y in cfactors.items():
            if x != '_id':
                self.cropFactors[x] = y;

    def getCropFactors(self):
        return self.cropFactors

    def getCropName(self):
        return self.cfCollection['CROPNAME']

    def getTempMeanActual(self):
        return self.mean_temp

    def getLightMeanActual(self):
        return self.historical.monthlyAverageSunlight()

    # def setMeanTemp(self,temp):
    #     self.mean_temp = temp

    def setMeanActual(self):
        sensorData = SoildDataCollection()
        numberOfReadings = 24 #Maybe if we collect once every hour, we get the last day of readings
        dataCollection = sensorData.getLastData(numberOfReadings)
        temp = 0
        inSunLight = 0
        for dataPoint in dataCollection:
            temp += dataPoint.getSoilData()['temperature']
            if dataPoint.getSoilData()['light'] > 100:
                inSunLight += 1
        self.mean_temp = temp / numberOfReadings
        self.mean_daily_percentage_daylight = inSunLight / numberOfReadings

    def getGoalEvotransporation(self):
        #recalculate the evotransporation, assuming 
        # BLANEY-CRIDDLE equation comes from https://en.wikipedia.org/wiki/Blaney%E2%80%93Criddle_equation
        # ET0 - Reference Crop Evapotraspiration
        # For determining crop water need we use ET = Kc x ETo, where Kc is the crop factor and ET is the amount of water needed in (mm/day)
        # @ref: http://www.fao.org/docrep/s2022e/s2022e07.htm#3.1.4%20calculation%20example%20blaney%20criddle
        # TODO: Need to Create mean daily percentage table from @ref site
        # evoReference = self.mean_daily_percentage_daylight * (0.457 * self.mean_temp + 8.128)

        self.setCropFactors()
        self.setGoalMeanTemp()

        # Test Values: Not real values
        evoReference = self.dPercentofDaylight * (0.46 * self.goal_mean_temp + 8)
        self.goalevotransporation = self.cropFactors['CROPCO_G'] * evoReference
        return self.goalevotransporation    

    def getEvotransporation(self):
        #recalculate the evotransporation, assuming 
        # BLANEY-CRIDDLE equation comes from https://en.wikipedia.org/wiki/Blaney%E2%80%93Criddle_equation
        # ET0 - Reference Crop Evapotraspiration
        # For determining crop water need we use ET = Kc x ETo, where Kc is the crop factor and ET is the amount of water needed in (mm/day)
        # @ref: http://www.fao.org/docrep/s2022e/s2022e07.htm#3.1.4%20calculation%20example%20blaney%20criddle
        # TODO: Need to Create mean daily percentage table from @ref site
        # evoReference = self.mean_daily_percentage_daylight * (0.457 * self.mean_temp + 8.128)

        self.setCropFactors()
        self.setMeanActual()

        # Test Values: Not real values
        evoReference = self.dPercentofDaylight * (0.46 * self.mean_temp + 8)
        self.evotransporation = self.cropFactors['CROPCO_G'] * evoReference
        print(self.evotransporation)
        return self.evotransporation
