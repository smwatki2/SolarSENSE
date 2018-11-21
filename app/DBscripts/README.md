# Mongodb Database Scripts

These scripts are meant to be run on the initial startup of the Rasperry Pi system.

**NOTE:** You can run these scripts as a quick test to verify they are working
through a Python environment and with the Mongo Daemon running.

### Usage

To run this script use the following command:

`sudo python3 cropfactordb.py [database name] [collection name] [json filename]`

Example:

`sudo python3 cropfactordb.py CropFactor AZTest AZCrops.json`

Right now this script only takes in one name of a collection to add to and one json file
to read data from. This will be fixed later once the different regions have been finalized
and the crops for those regions have been discussed. In the mean time the default script command
would be to execute the example above.



