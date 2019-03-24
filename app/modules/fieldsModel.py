import json
import traceback
from pymongo import MongoClient

class Field(object):

    def __init__(self, id, name):
        self.id = id
        self.name = name

    def toString(self):
        return json.dumps(self.__dict__)

class FieldsCollection(object):

    def __init__(self):
        self.fieldsList = []
        self.client = MongoClient("mongodb://0.0.0.0:27017")
        self.db = self.client.FarmInfo
        self.collection = self.db.fields

    def getFields(self):
        self.getAll()
        return self.fieldsList

    def getAll(self):
        allFields = self.collection.find()
        for aField in allFields:
                oneField = Field(str(aField['_id']), str(aField['name']))
                self.fieldsList.append(oneField)

    def close(self):
        self.client.close()



