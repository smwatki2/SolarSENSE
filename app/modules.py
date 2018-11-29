from pymongo import MongoClient
from pprint import pprint
from bson.json_util import dumps
from flask import url_for
import json
import traceback

client = MongoClient("mongodb://0.0.0.0:27017")
#client = MongoClient("mongodb://localhost:27017")
db = client.solarsensereports
historicalDb = client.HistoricalClimateData
cropFactorDb = client.CropFactor
constraintsDb = client.Constraints

class SoildDataCollection(object):

    def __init__(self):
        self.soilDataObjects = []

    def getSoilCollection(self):
        self.getData()
        return self.soilDataObjects

    def getData(self):
        try:
            #client = MongoClient("mongodb://0.0.0.0:27017")
            #client = MongoClient("mongodb://localhost:27017")
            #db = client.solarsensereports
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

'''
Constraint class
'''
class Constraint(object):
    """ This is a class for Constraint """
    def __init__(self, region, crop, date):
        self.region = region
        self.crop = crop
        self.date = date
    
    def toString(self):
        return json.dumps(self.__dict__)

'''
Constraints Class
'''       
class Constraints(object):
    """docstring for Constraints"""
    def __init__(self, region, crop,  date):
        self.region = region
        self.crop = crop
        self.date = date
        self.constraints = []

    """ method to get current constraints """
    def getConstraints(self):
        self.retrieveConstraints()
        return self.constraints

    def retrieveConstraints(self):
        try:
            farmConstraintsCollection = constraintsDb.constraints
            query = {'CROPNAME': self.crop}
            farmConstraints = farmConstraintsCollection.find(query)
            for farmConstraint in farmConstraints:
                currentConstraint = Constraint(currentConstraint['region'], currentConstraint['crop'], currentConstraint['date'])
                self.constraints.append(currentConstraint)

        except Exception as e:
            file = open("errorlog.txt", "a")
            file.write(traceback.format_exc())
            file.close()

    """ method to set constraints """
    def setConstraints(self):
        try:
            farmConstraintsCollection = constraintsDb.constraints
            query = {'crop': self.crop}
            if farmConstraintsCollection.find(query).count() > 0:
                newConstraints = {'$set': {'region': self.region, 'date': self.date}}
                farmConstraintsCollection.update_one(query, newConstraints)
            else:
                newConstraints = {{'region': self.region, 'crop': self.crop, 'date': self.date}}
                farmConstraintsCollection.insert_one(newConstraints)

        except Exception as e:
            file = open("errorlog.txt", "a")
            file.write(traceback.format_exc())
            file.close()
        




