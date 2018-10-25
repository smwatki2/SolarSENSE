import json
from flask import url_for

class Questions(object):

	def __init__(self):
		self.questions = None

	def read_questions(self, url):
		with open(url, 'r') as f:
			self.questions = json.load(f)

	def get_questions(self):
		self.read_questions()
		return self.questions