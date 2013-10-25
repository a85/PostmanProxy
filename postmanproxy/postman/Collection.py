class Collection:
	"""Postman collection class"""

	def __init__(self):
		self.name = "Test"

	def test(self):
		print "It worked! %s" % self.name