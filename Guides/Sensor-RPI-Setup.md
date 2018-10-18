This document outlines the steps needed to **setup communication between Xiaomi Mi Flora sensors and Raspberry Pi 3**

1. **INSTALL the miflora-mqtt-daemon by Thomas Dietrich**
	
	1. Run the following commands in order

		* *`sudo apt install git python3 python3-pip bluetooth bluez`*
		* *`git clone https://github.com/ThomDietrich/miflora-mqtt-daemon.git /opt/miflora-mqtt-daemon`*
		* *`cd /opt/miflora-mqtt-daemon`*
		* *`sudo pip3 install -r requirements.txt`*

	2. Make sure that a tool named **gatttol** has been installed succesfully by running:

		*```gatttool --help```*

		If this returns a unkown command error, restart install from steps 1.1.

2. **INSTALL a MQTT Broker**
	
	An MQTT Broker that is popular and seems to have a long history of support is called the *Mosquitto Broker*, 

	1. Install the Mosquitto MQTT Broker by running: 

		* *```sudo apt update```*
		* *```sudo apt install -y mosquitto mosquitto-clients```* *

	2. To make sure the broker auto starts on start up, run:

		* *```sudo systemctl enable mosquitto.service```* * 

	3. Test if installation was successful by running: 

		* *```mosquitto -v```* *

3. Configure Daemon 

	To get the deamon to connect to our sensors, we will configure properties such as frequency of measurements, Addresses of the sensors, and so forth. To do that we will edit the config file and add our configurations.

	1. Run the following commands to create, open and edit the config file


		* *```cp /opt/miflora-mqtt-daemon/config.{ini.dist,ini}```* *
		* *```vim /opt/miflora-mqtt-daemon/config.ini```*

	2. Replace all the contents with the following (Our minimum settings):

		```
		[General]
		reporting_method = mqtt-json
		adapter = hci0
		[Daemon]
		enabled = true
		period = 300
		[MQTT]
		keepalive = 60
		[Sensors]
		# Here goes sensors in format Sensor name@favorable identifier = MAC ADDRESS
		# For instance the sensor I have is added as FloraCare@Tresor = CA:7C:8D:66:CF:40
		```
	3. To add a sensor, make sure your bluetooth is enabled and run command:

		*`sudo hcitool lescan`*

		This will scan and list all available bluetooth devices. Locate your sensor by looking at its MAC ADDRESS, then add its name and address in the above config file.


4. Test that everything works by running the daemon as:

	*`python3 /opt/miflora-mqtt-daemon/miflora-mqtt-daemon.py`*


	

*Author: Tresor Cyubahiro
Date Modified: 10.17.2018
SolarSENSE Project*