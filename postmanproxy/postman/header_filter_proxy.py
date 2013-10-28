from libmproxy import controller, proxy
from request import Request
from collection import Collection
import os
import logging

class HeaderFilterProxy(controller.Master):
	def __init__(self, server):
		self.restricted_headers = [
		    'accept-charset',
		    'accept-encoding',
		    'access-control-request-headers',
		    'access-control-request-method',
		    'connection',
		    'content-length',
		    'cookie',
		    'cookie2',
		    'content-transfer-encoding',
		    'date',
		    'expect',
		    'host',
		    'keep-alive',
		    'origin',
		    'referer',
		    'te',
		    'trailer',
		    'transfer-encoding',
		    'upgrade',
		    'user-agent',
		    'via'
		    ]

		controller.Master.__init__(self, server)

	def run(self):
		try:
			return controller.Master.run(self)
		except KeyboardInterrupt:
			self.shutdown()

	def handle_request(self, msg):
		try:
			# Modify outgoing headers here
			outgoing_headers = msg.headers.copy()
			prefix = "postman-"
			l = len(prefix)
			for k, v in outgoing_headers:
				key = k.lower()
				if key.find(prefix) == 0 and key != "postman-content-length":
					print "Found %s" % (key)
					target_header = key[l:]
					msg.headers[target_header] = [v]
					del msg.headers[key]

		except Exception as ex:
			logging.exception("Something awful happened!")

		msg.reply()

	def handle_response(self, msg):
		# Modify incoming headers
		incoming_headers = msg.headers

		print "###Incoming headers###"

		for k, v in incoming_headers:
			key = k.lower()
			if key == "location":
				msg.headers["Postman-Location"] = [v]
				del msg.headers[key]

		print msg.headers
		# If location header exists, remove it and call it postman-location
		msg.reply()