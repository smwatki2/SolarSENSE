import datetime

file = open("./DATAFILES/sensorDataTest.json", "a")
temp = 21.0
light = 1000
moisture = 50
date = 1551978253
conduct = 1000
for day in range(7):
  for half_hour in range(48):
    file.write('{{"temperature": {0}, "battery": 100, "light": {1}, "mac": "C4:7C:8D:66:CF:40", "moisture": {2}, "timestamp": {{"$date": {3}}}, "name_pretty": "Flora-care0", "conductivity": {4}}}'.format(temp, int(light), int(moisture), datetime.datetime.fromtimestamp(date/1e3).isoformat(), conduct))
    if (half_hour < 12): 
      temp += 0
      light += 10
      moisture -= 0.5
      conduct += 0
    elif (half_hour >= 12 and half_hour < 32):
      temp += .3
      light += 20
      moisture -= 2
      conduct -= 20
    else:
      temp -= 0.4
      light -= 33
      moisture += 2.9
      conduct += 30
    date += 1800
    if ((day*half_hour != 282)):
      file.write(',\n')
