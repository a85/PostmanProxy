from libmproxy import controller, proxy
from request import Request
from collection import Collection
import os
import socket
import json
import logging

class CollectionCreatorProxy(controller.Master):
	def __init__(self, server, collection, rules, tcp_connection=False, tcp_host="127.0.0.1", tcp_port=5005):
		self.collection = collection
		self.rules = rules
		self.host = rules['host']
		self.methods = self.get_methods(rules['methods'])
		self.tcp_connection = tcp_connection
		self.tcp_host = tcp_host
		self.tcp_port = tcp_port
		# self.status_codes = self.get_status_codes(rules['status_codes'])

		controller.Master.__init__(self, server)

	def send_to_postman(self, request):
		try:
			TCP_IP = self.tcp_host
			TCP_PORT = self.tcp_port
			BUFFER_SIZE = 1024
			MESSAGE = json.dumps(request.get_json())

			print MESSAGE

			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s.connect((TCP_IP, TCP_PORT))
			s.send(MESSAGE)
			data = s.recv(BUFFER_SIZE)
			s.close()

			print "received data:", data
		except Exception as ex:
			logging.exception("Something awful happened!")


	def get_methods(self, methodString):
		if methodString == '':
			return []

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

			if status_code != "":
				status_codes.append(int(status_code))

		return status_codes

	def run(self):
		try:
			return controller.Master.run(self)
		except KeyboardInterrupt:
			self.shutdown()

	def handle_request(self, msg):
		try:
			request = Request(self.collection.id)
			request.init_from_proxy(msg)

			allowed_host = True
			allowed_method = True
			allowed_status_code = True

			if not self.host == '':
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

				if self.tcp_connection:
					print "Send to Postman"
					self.send_to_postman(request)
		except Exception as ex:
			logging.exception("Something awful happened!")

		msg.reply()

	def handle_response(self, msg):
		msg.reply()