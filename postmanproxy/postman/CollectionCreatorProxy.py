from libmproxy import controller, proxy
import os

class CollectionCreatorProxy(controller.Master):
	def __init__(self, server):
		controller.Master.__init__(self, server)

	def run(self):
		try:
			return controller.Master.run(self)
		except KeyboardInterrupt:
			self.shutdown()

	def handle_request(self, msg):
		print msg.host
		print msg.port
		print msg.headers
		print msg.content
		# URLEncoded and raw are solved
		# Left with form-data: Can be done by werkzeug?

		print self.__dict__.keys()
		print msg.__dict__.keys()

		msg.reply()

	def handle_response(self, msg):
		msg.reply()