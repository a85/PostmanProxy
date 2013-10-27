from postman.collection import Collection
from postman.collection_creator_proxy import CollectionCreatorProxy
from libmproxy import controller, proxy
from optparse import OptionParser
import signal
import sys

collection = False

def signal_handler(signal, frame):
	global collection
	print 'You pressed Ctrl+C! Here is the collection file'
	print collection.save()
	sys.exit(0)

def main():
	global collection
	print "Hey! This is the Postman proxy!"
	print "Press Ctrl+C to stop the proxy"
	rules = []

	collection = Collection("Postman")
	config = proxy.ProxyConfig()
	server = proxy.ProxyServer(config, 8080)
	m = CollectionCreatorProxy(server, collection, rules)

	m.run()

	signal.signal(signal.SIGINT, signal_handler)
	print 'Press Ctrl+C again to save the collection'
	signal.pause()

if __name__ == "__main__":
    main()