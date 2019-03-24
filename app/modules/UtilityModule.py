import json
import subprocess
from pymongo import MongoClient

class Rescan(object):

	def rescan(self):
		# processMsg = subprocess.check_output(['python3','test.py']).decode('utf-8').split("\n")
		# print(processMsg)
		# print("THis is a test of the scan feature to be implemented")
		# print(psutil.process_iter())
		# for proc in psutil.process_iter():
		# 	print(proc)
		# return processMsg
		subprocess.run(['python3','/opt/miflora-mqtt-daemon/miflora-mqtt-daemon.py'])
