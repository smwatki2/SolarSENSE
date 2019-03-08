import json
import datetime
import traceback
from app.modules.historicalmodels import *
from app.modules.soilmodels import *
from pymongo import MongoClient
from calendar import monthrange


class SoilAlgorithm(object):
    """
    My thinking is to leave this as generic as possible in case we switch to a more
    complicated Algorith which may or may not still use some of these variables
    """

    def __init__(self,cropFactorCollection = None):

        self.client = MongoClient("mongodb://0.0.0.0:27017")
        self.cropFactorDb = self.client.CropFactor
        self.constraintsDb = self.client.Constraint
        # This value is a test value based in AZ, others will be added as a constraint
        # TODO: Add a property to constraint or to Region db for lat value.
        self.historical = HistoricalData('USA', 'AZ', datetime.datetime.today())

        # This value is derived from a table based on lat and lon, not calculated
        self.dPercentofDaylight = 0.23

        """ Let's figure out how to get the constaints that the user set"""
        constrainCollection = self.constraintsDb.SolarSENSEConstraint
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

        # Default stage for crop factor
        self.cropStage = ""

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
        regionCrops = self.cropFactorDb[self.cfCollection["CF_COLLECTION"]]
        cropFactors = self.cropFactorDb.CropFactors

        crops = regionCrops.find()

        for crop in crops:
            if crop['CROPNAME'] == self.cfCollection['CROPNAME']:
                cropID = crop['CROPID']
        file = open("errorthing.txt", "a")
        file.write(str(cropID))

        cfactors = cropFactors.find_one({'CROPID': cropID})

        file.write(str(cfactors))
        file.close()
        for x, y in cfactors.items():
            if x != '_id':
                self.cropFactors[x] = y;

    def setCropStage(self,stageObj = None):

        if stageObj is not None:
            stageName = stageObj['stage']

            switcher = {
                'midSeason' : 'CROPCO_MID',
                'harvest' : 'CROPCO_HARV'
            }

            self.cropStage = switcher.get(stageName, "CROPCO_G")

        else:
            self.cropStage = 'CROPCO_G'

        print("[DEBUG] SoilAlgorithm: " + self.cropStage)

    def getCropFactors(self):
        return self.cropFactors

    def getCropName(self):
        return self.cfCollection['CROPNAME']

    def goalTempRange(self):
        tempRange = [20,25]
        return tempRange;

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
        sensorData.close()

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
        self.goalevotransporation = self.cropFactors[self.cropStage] * evoReference
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
        self.evotransporation = self.cropFactors[self.cropStage] * evoReference
        print(self.evotransporation)
        return self.evotransporation

    def close(self):
        self.client.close()
