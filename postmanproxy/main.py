from postman.collection import Collection
from postman.collection_creator_proxy import CollectionCreatorProxy
from postman.header_filter_proxy import HeaderFilterProxy
from libmproxy import controller, proxy
from optparse import OptionParser
import signal
import sys
import os

collection = False

def signal_handler(signal, frame):
	global collection
	print 'You pressed Ctrl+C! Here is the collection file'
	print collection.save()
	sys.exit(0)

def start_creator_proxy(options):
	global collection

	port = int(options.port)
	name = options.name
	path = options.path
	host = options.host
	methods = options.methods
	status_codes = ""

	print "Proxy running at %d" % (port)
	print "Press Ctrl+C to stop the proxy"

	rules = {
		'host': host,
		'methods': methods
	}

	print "Rules are", rules

	collection = Collection(name, path)
	config = proxy.ProxyConfig(
		cacert = os.path.expanduser("~/.mitmproxy/mitmproxy-ca.pem")
	)
	server = proxy.ProxyServer(config, port)
	m = CollectionCreatorProxy(server, collection, rules)

	m.run()

	signal.signal(signal.SIGINT, signal_handler)
	print 'Press Ctrl+C again to save the collection'
	signal.pause()

def start_filter_proxy(options):
	print "Press Ctrl+C to stop the proxy"
	port = int(options.port)
	config = proxy.ProxyConfig(
		cacert = os.path.expanduser("~/.mitmproxy/mitmproxy-ca.pem")
	)
	server = proxy.ProxyServer(config, port)
	m = HeaderFilterProxy(server)
	m.run()

def main():
	parser = OptionParser(usage="Usage: %prog [options] filename")
	parser.add_option("-o", "--operation", dest="operation", help="1. Filter requests (filter)\n 2. Save request to a collection (save)\n (Default is save)", default="save")
	parser.add_option("-n", "--name", dest="name", help="Collection name", default="default")
	parser.add_option("-r", "--port", dest="port", help="Port for the proxy", default=8080)
	parser.add_option("-p", "--path", dest="path", help="Target path for saving the collection", default="")
	parser.add_option("-t", "--host", dest="host", help="Only allow URLs of this host", default="")
	parser.add_option("-m", "--methods", dest="methods", help="Comma separated list of allowed methods. Default is all methods", default="")
	# parser.add_option("-s", "--status_codes", dest="status_codes", help="Comma separated list of allowed status codes. Default is all codes", default=[])

	(options, args) = parser.parse_args()

	if options.operation == "save":
		start_creator_proxy(options)
	elif options.operation == "filter":
		start_filter_proxy(options)
	else:
		start_creator_proxy(options)



if __name__ == "__main__":
    main()