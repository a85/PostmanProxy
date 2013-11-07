import utils
import uuid
import time
import json

class Collection:
	"""Postman collection class"""

	def __init__(self, name, path):
		self.id = str(uuid.uuid4())
		self.path = path
		self.name = name
		self.order = []
		self.folders = []
		self.timestamp = int(round(time.time()))
		self.synced = False
		self.requests = []

	def get_id(self):
		return self.id

	def is_new_request(self, request):
		for r in self.requests:
			if request.method == r.method and request.dataMode == r.dataMode and  request.data == r.data and request.url == r.url:
				return False

		return True
	def add_request(self, request):
		if self.is_new_request(request):
			self.order.append(request.id)
			self.requests.append(request)
		else:
			print "Duplicate request"

	def get_requests(self):
		r = []
		for request in self.requests:
			r.append(request.get_json())

		return r

	def get_json(self):
		json = {
			'id': self.id,
			'name': self.name,
			'order': self.order,
			'folders': self.folders,
			'timestamp': self.timestamp,
			'synced': self.synced,
			'requests': self.get_requests()
		}
		return json

	def save(self):
		if self.path:
			target = self.path + self.name + ".postman_collection"
		else:
			target = self.name + ".postman_collection"

		data = self.get_json()
		with open(target, 'w') as outfile:
			json.dump(data, outfile)