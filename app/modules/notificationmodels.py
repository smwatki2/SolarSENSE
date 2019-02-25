import json
from pymongo import MongoClient

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
        self.client = MongoClient("mongodb://0.0.0.0:27017")
        self.db = self.client.solarsensereports

        """ method to get new notifications """
    def getNewNotifications(self):
        self.checkNewNotifications()
        return self.allNotifications

    def checkNewNotifications(self):
        try:
            notifications = self.db.notifications
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
            notifications = self.db.notifications
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
            notifications = self.db.notifications
            query = {'_id': id}
            result = notifications.delete_one(query)

        except Exception as e:
            file = open("errorlog.txt", "a")
            file.write(traceback.format_exc())
            file.close()

    def close(self):
    	self.client.close()