import utils
import time

class Request:
	def __init__(self, collectionId):
		self.id = uuid.uuid4()
		self.collectionId = collectionId
		self.name = ""
		self.description = ""
		self.method = ""
		self.headers = []
		self.data = []
		self.dataMode = "params"
		self.responses = []
		self.version = 2
		self.timestamp = time.time()

