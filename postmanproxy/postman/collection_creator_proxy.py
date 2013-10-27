from libmproxy import controller, proxy
from request import Request
from collection import Collection
import os

class CollectionCreatorProxy(controller.Master):
	def __init__(self, server, collection, rules):
		self.collection = collection
		self.rules = rules
		self.host = rules['host']
		self.methods = self.get_methods(rules['methods'])
		self.status_codes = self.get_status_codes(rules['status_codes'])

		print self.host, self.methods, self.status_codes

		controller.Master.__init__(self, server)

	def get_methods(self, methodString):
		m = methodString.split(',')
		methods = []
		for method in m:
			method = method.strip()
			method = method.upper()
			methods.append(method)

		return methods

	def get_status_codes(self, statusCodeString):
		c = statusCodeString.split(',')
		status_codes = []
		for status_code in c:
			status_code = status_code.strip()
			status_codes.append(int(status_code))

		return status_codes

	def run(self):
		try:
			return controller.Master.run(self)
		except KeyboardInterrupt:
			self.shutdown()

	def handle_request(self, msg):
		request = Request(self.collection.id)
		request.init_from_proxy(msg)

		allowed_host = True
		allowed_method = True
		allowed_status_code = True

		if self.host != "":
			if self.host == msg.host:
				allowed_host = True
			else:
				allowed_host = False

		if len(self.methods) > 0:
			if msg.method in self.methods:
				allowed_method = True
			else:
				allowed_method = False

		if allowed_method and allowed_host and allowed_status_code:
			self.collection.add_request(request)

		msg.reply()

	def handle_response(self, msg):
		msg.reply()