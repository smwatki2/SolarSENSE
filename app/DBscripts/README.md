# Mongodb Database Scripts

These scripts are meant to be run on the initial startup of the Rasperry Pi system.

**NOTE:** You can run these scripts as a quick test to verify they are working
through a Python environment and with the Mongo Daemon running.

### Usage

To run this script use the following command:

`sudo python3 cropfactordb.py [database name] [collection name] [json filename]`

Example:

`sudo python3 cropfactordb.py CropFactor CropFactors Crops.json`

The above will create the CropFactor database with a generalized list of all Crop Factors in a CropFactors
collection. This collection is found in the Crops.json.

To add another collection run the same script with the existing database name and add the new collection
name and the file supporting it.

Example:

`sudo python3 cropfactordb.py CropFactor AZCrops AZCrops.json`

This command will use the already existing CropFactor database and add a new collection with the following
json file.



