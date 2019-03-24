import json
import subprocess
import psutil
from pymongo import MongoClient

class Rescan(object):

	def rescan(self):
		# processMsg = subprocess.check_output(['ls','-l']).decode('utf-8').split("\n")
		# print(processMsg)
		# print("THis is a test of the scan feature to be implemented")
		# print(psutil.process_iter())
		for proc in psutil.process_iter():
			print(proc)
		return psutil.Process().cmdline()