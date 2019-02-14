'''
   Test Case Module for Back end calculations
   Usage: 

   		Is included to run with the test suite
   	Descritpion: Runs unit tests for the different calculations made on the backend
'''

import unittest
from app import app
from app.modules import SoilAlgorithm

print("Running Backend Calculations Unit Tests")
print("---------------------------------------")

class TestSoilAlgorithm(unittest.TestCase):
	def setUp(self):
		self.soilAlgorithm = SoilAlgorithm()

	def test_getMeanDaylight(self):
		self.assertTrue(self.soilAlgorithm.getMeanDaylight() > 0)

	def test_getMeanTemp(self):
		self.assertTrue(self.soilAlgorithm.getMeanTemp() > 0)

	def test_setConstMeanPercentDayLight(self):
		self.assertTrue(len(self.soilAlgorithm.setConstMeanPercentDayLight()) == 12)

	def test_setMeanDaylight(self):
		light = 81
		self.soilAlgorithm.setMeanDaylight(light)
		assertTrue(self.soilAlgorithm.getMeanDaylight() == light)

	def test_setGoalMeanTemp(self):
		temp = 81
		self.soilAlgorithm.setGoalMeanTemp(temp)
		assertTrue(self.soilAlgorithm.getMeanTemp() == temp)

