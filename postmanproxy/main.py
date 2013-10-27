from postman.collection import Collection
from postman.collection_creator_proxy import CollectionCreatorProxy
from libmproxy import controller, proxy
from optparse import OptionParser
import signal
import sys

def signal_handler(signal, frame):
    print 'You pressed Ctrl+C!'
    sys.exit(0)

def main():
	print "Hey! This is the Postman proxy!"
	rules = []

	collection = Collection("Postman")
	config = proxy.ProxyConfig()
	server = proxy.ProxyServer(config, 8080)
	m = CollectionCreatorProxy(server, collection, rules)

	# signal.signal(signal.SIGINT, signal_handler)
	# print 'Press Ctrl+C to exit'
	# signal.pause()

	m.run()

if __name__ == "__main__":
    main()