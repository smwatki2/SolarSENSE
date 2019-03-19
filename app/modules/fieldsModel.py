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
        self.db = self.client.solarsensereports

    def getFields(self):
        self.getAll()
        return self.fieldsList

    def getAll(self):
        for i in range(4):
            oneField = Field(i, 'Field_' + str(i))
            self.fieldsList.append(oneField)

    def close(self):
        self.client.close()



