This guide outlines the steps needed to setup the MongoDB Connection for storing the sensor data

1. Run the following to install MongoDB on RPI
	
	```
	sudo apt-get update
	sudo apt-get upgrade
	sudo apt-get install mongodb-server
	```

2. To make sure mongodb runs on RPI start up
	
	```sudo service mongodb start```


3. To test that MongoDB has been installed successfully, run 

	```mongo```

	This will run the MongoDB shell where you can issue mongoDB commands


5. Create a new database with name "solarsensereports"
		
		Run: 

		```use solarsensereports```

		after the database has been created, exit the mongodb shell by running: 

		```exit```

5. Install the Python MongoDB driver (PyMongo)

	```python3 -m pip install pymongo==3.4.0```

	Opted to use 3.4.0 because the latest (3.7.2) was having problems connecting with the latest mongo release

6. Copy the modified daemon (located inside folder SensorReader) to /opt/miflora-mqtt-daemon as:

	```sudo cp miflora-mqtt-daemon.py /opt/miflora-mqtt-daemon```

7. Run the python file from folder SensorReader, sensorReader.py, and make sure there is data reported 	at least once so you can test the next step

	**NOTE**: Currently, both sensorReader.py and /opt/miflora-mqtt-daemon/miflora-mqtt-daemon.py have to run 	
	      simultaneously.

8. Sample code to use to test if the daemon is saving to the database:

	```
	mongo
	use solarsensereports
	db.reports.find()```

	If the daemon has saved data at least once, you will see a json object printed on screen with the data

	Run ```exit``` to log out of the mongoDB shell



Glossary:
	RPI : Raspberry Pi


Author: ASU Capstone Team 2018
Date Modified: 10.27.2018
