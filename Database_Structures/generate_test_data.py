import datetime
import random
import sys
from dateutil.tz import tzlocal

#This is the default mac address
macAddresses = []
mac = "C4:7C:8D:66:D1:98"

macAddresses.append(mac)

if len(sys.argv) > 1:
  macAddresses.append(sys.argv[1])
  macAddresses.append(sys.argv[2])
  macAddresses.append(sys.argv[3])
  print(macAddresses)

for address in macAddresses:
  print(address)
  file = open("./DATAFILES/sensorDataTest.json", "a")
  temp = random.randint(21,30)
  light = random.randint(500,1000)
  moisture = random.randint(50,75)
  date = 1555632000 + 25200
  conduct = 1000
  for day in range(7):
    for half_hour in range(48):
      file.write('{{"temperature": {0}, "battery": 100, "light": {1}, "mac": \"{2}\", "moisture": {3}, "timestamp": {{"$date": \"{4}\"}}, "name_pretty": "Flora-care0", "conductivity": {5}}}'.format(temp, int(light), address ,int(moisture), datetime.datetime.fromtimestamp(date,tzlocal()).isoformat(), conduct))
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
        file.write('\n')