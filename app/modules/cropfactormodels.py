import json
from pymongo import MongoClient


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
        self.client = MongoClient("mongodb://0.0.0.0:27017")
        self.cropFactorDb = client.CropFactor

    """ method to get crop's crop factor """
    def getCropFactor(self):
        self.retrieveCropFactor()
        return self.cropFactors

    def retrieveCropFactor(self):
        try:
            cropFactorCollection = self.cropFactorDb.AZTest
            query = {'CROPNAME': self.crop}
            cropFactors = cropFactorCollection.find(query)
            for cropFactor in cropFactors:
                factors = Factors(cropFactor['CROPID'], cropFactor['CROPNAME'], cropFactor['CROPCO_MID'], cropFactor['CROPCO_G'], cropFactor['CROPCO_HARV'])
                self.cropFactors.append(factors)

        except Exception as e:
            file = open("errorlog.txt", "a")
            file.write(traceback.format_exc())
            file.close()

    def close(self):
        self.client.close()