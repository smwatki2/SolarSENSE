import json
import datetime
from pymongo import MongoClient
from calendar import monthrange

'''
Historical Data Object
'''

# client = MongoClient("mongodb://0.0.0.0:27017")
# cropFactorDb = client.CropFactor
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


class HistoricalData(object):
    """docstring for HistoricalData"""
    def __init__(self, country, location, datetime):
        self.country = country
        self.location = location
        self.datetime = datetime
        self.weatherData = []
        self.client = MongoClient("mongodb://0.0.0.0:27017")
        self.historicalDb = self.client.HistoricalClimateData

    """ method to get country's historical data """
    def getHistoricalData(self):
        self.retrieveHistoricalData()
        return self.weatherData

    def retrieveHistoricalData(self):
        try:
            locationDataCollection = self.historicalDb.mesaGatewayClimateData
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

        historyCol = self.historicalDb['mesaGatewayClimateData']
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
        return 0.23

    def close(self):
        self.client.close()




