from libmproxy import controller, proxy
from request import Request
from collection import Collection
import os

class HeaderFilterProxy(controller.Master):
	def __init__(self):
		controller.Master.__init__(self, server)

	def run(self):
		try:
			return controller.Master.run(self)
		except KeyboardInterrupt:
			self.shutdown()

	def handle_request(self, msg):
		# Modify outgoing headers here
		msg.reply()

	def handle_response(self, msg):
		# Modify incoming headers
		msg.reply()