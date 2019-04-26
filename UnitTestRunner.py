'''
	Main Test Harness For SolarSENSE
	Usage:
		python3 UnitTestRunner.py
	Description:
	This file will run all unit tests defined by the imported module.
	For example:
		import TestDatabase
	Imports the TestDatabase module and will run any and all test cases found in the
	module
	To add your module (i.e TestModules) to the actual suite you need to add them to the loader
	Example:
		suite.addTests(loader.loadTestsFromModule(YOUR_IMPORTED_MODULE_HERE))
	The unit tests are then run with the usage shown above.
'''

# Main Import to use unit tests
import unittest

# Import Modules Here
#-----------------------------
import FlaskRoutesUnitTests
import FlaskEndpointsUnitTests

#-----------------------------


unit_test_loader = unittest.TestLoader()
unit_test_suite  = unittest.TestSuite()

unit_test_suite.addTests(unit_test_loader.loadTestsFromModule(FlaskRoutesUnitTests))

unit_test_suite.addTests(unit_test_loader.loadTestsFromModule(FlaskEndpointsUnitTests))

unit_test_runner = unittest.TextTestRunner(verbosity=5)
result = unit_test_runner.run(unit_test_suite)