import utils
import uuid
import time
import json

class Collection:
	"""Postman collection class"""

	def __init__(self, name):
		self.id = uuid.uuid4()
		self.name = name
		self.order = []
		self.folders = []
		self.timestamp = time.time()
		self.synced = False
		self.requests = []

	def get_id(self):
		return self.id

	def add_request(self, request):
		self.requests.append(request)

	def test(self):
		print "It worked! %s" % self.name

	def get_json(self):
		json = ""
		return json

	def save(self, target):
		pass