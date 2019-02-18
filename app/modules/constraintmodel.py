import json
from pymongo import MongoClient


class Constraint(object):

    def __init__(self, constraintDict = None):
        if constraintDict is not None:
            self.constraint = constraintDict
        self.client = MongoClient("mongodb://0.0.0.0:27017")
        self.constraintsDb = self.client.Constraint

    def getConstraint(self):
        constraintCollection = self.constraintsDb.SolarSENSEConstraint
        constraint = constraintCollection.find({"ID":0})[0]
        for x,y in constraint.items():
            if x != '_id':
                constraint[x] = y        
        return constraint

    def updateConstraint(self):
        constrainCollection = self.constraintsDb.SolarSENSEConstraint
        query = { "ID" : 0 }
        updateVals = {"$set":{"REGION": self.constraint.get("region"),"CROPNAME": self.constraint.get('crop'), "SEASON": self.constraint.get('season'), "DATE": self.constraint.get('date'), "CF_COLLECTION": self.constraint.get('cfCollection')}}

        constrainCollection.update_one(query,updateVals)
        for constraint in constrainCollection.find():
            print(constraint)

    def close(self):
        self.client.close()