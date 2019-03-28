import unittest
from app import app

class RoutesUnitTest(unittest.TestCase):

	def setUp(self):
		self.app = app.test_client()
		self.app.testing = True

	def test_home_request(self):
		response = self.app.get("/")
		self.assertTrue(response.mimetype == 'text/html' and response.data is not None)

	def test_home_response_code(self):
		# We want to verify we are receiving a 200 response code
		response = self.app.get("/")
		self.assertEquals(response.status_code,200,'Received 200 as Response Code')

	def test_learn_request(self):

		response = self.app.get("/learn")
		self.assertTrue(response.mimetype == 'text/html' and response.data is not None)

	def test_learn_response_code(self):
		response = self.app.get("/learn")
		self.assertEquals(response.status_code, 200)

	def test_config_request(self):

		response = self.app.get("/config")
		self.assertFalse(response.mimetype == 'application/json' and response.data is None)

	def test_config_response_code(self):

		response = self.app.get("/config")
		self.assertNotEquals(response.status_code, 404)