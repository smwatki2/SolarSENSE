from pymongo import MongoClient
from pprint import pprint
from bson.json_util import dumps
from flask import url_for
import json
import traceback

client = MongoClient("mongodb://0.0.0.0:27017")
#client = MongoClient("mongodb://localhost:27017")
db = client.solarsensereports

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
Reminder class
'''
class Reminder(object):
    """ This is a class for a reminder """
    def __init__(self, id, timestamp, type):
        self.id = id
        self.timestamp = timestamp
        self.type = type
    
    def toString(self):
        return json.dumps(self.__dict__)

'''
Reminders class
'''
class Reminders(object):
    """ This is a class for a reminders """
    def __init__(self):
        self.allReminders = []

    def __init__(self, frequency):
        self.frequency = frequency
        self.allReminders = []
    
    def toString(self):
        return json.dumps(self.__dict__)

    """ method to get new reminders """
    def getReminders(self):
        self.checkReminders()
        return self.allReminders

    def checkNewReminders(self):
        try:
            reminders = db.reminders
            newReminders = reminders.find()
            for newReminder in newReminders:
                newReminder['_id'] = str(newReminder['_id'])
                remind = Reminder(newReminder['_id'], newReminder['timestamp'], newReminder['type'])
                self.allReminders.append(remind)
        except Exception as e:
            file = open("errorlog.txt", "a")
            file.write(traceback.format_exc())
            file.close()

    def editSettings(self, frequency):
        try:
            remindersettings = db.reminderSettings
            result = remindersettings.find()
            if result is not None and result.count() > 0:
                for setting in result:
                    query = {'_id': setting['_id']}
                    remindersettings.update(query, {"$set": {"frequency": frequency}}, upsert=False, multi=False)
            else:
                remindersettings.insert_one({"frequency": frequency})
        except Exception as e:
            file = open("errorlog.txt", "a")
            file.write(traceback.format_exc())
            file.close()

    """ method to save a new notification """
    def saveNewReminder(self, content, timestamp):
        try:
            reminders = db.reminders
            result = reminders.insert_one({'content': content, 'timestamp': timestamp})

        except Exception as e:
            file = open("errorlog.txt", "a")
            file.write(traceback.format_exc())
            file.close()

    """ method to delete a reminder """
    def deleteReminder(self, id):
        try:
            reminders = db.reminders
            query = {'_id': id}
            result = reminders.delete_one(query)

        except Exception as e:
            file = open("errorlog.txt", "a")
            file.write(traceback.format_exc())
            file.close()
            


