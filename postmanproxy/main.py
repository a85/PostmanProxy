from postman.collection import Collection
from postman.collection_creator_proxy import CollectionCreatorProxy
from postman.header_filter_proxy import HeaderFilterProxy
from libmproxy import controller, proxy
import argparse
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

	if options.restricted_headers == 'false':
		restricted_headers = False
	else:
		restricted_headers = True

	methods = options.methods
	status_codes = ""

	print "Proxy running at %d" % (port)
	print "Press Ctrl+C to stop the proxy"

	rules = {
		'host': host,
		'methods': methods,
		'restricted_headers': restricted_headers
	}

	collection = Collection(name, path)
	config = proxy.ProxyConfig(
		cacert = os.path.expanduser("~/.mitmproxy/mitmproxy-ca.pem")
	)
	server = proxy.ProxyServer(config, port)

	if options.tcp_connection == 'false':
		tcp_connection = False
	else:
		tcp_connection = True

	m = CollectionCreatorProxy(server, collection, rules, tcp_connection=tcp_connection, tcp_host=options.tcp_host, tcp_port=options.tcp_port)

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
	parser = argparse.ArgumentParser(description='PostmanProxy. TODO Add more detailed page')
	parser.add_argument('operation', metavar='Operation', type=str, help='filter or save', default='save')
	parser.add_argument("--name", help="Collection name", default="default")
	parser.add_argument("--port", help="Port for the proxy. Default=8080", default=8080)
	parser.add_argument("--path", help="Target path for saving the collection. Default is current directory", default="")
	parser.add_argument("--host", help="Only allow URLs of this host. Default is all URLs", default="")
	parser.add_argument("--methods", help="Comma separated list of allowed methods. Default is all methods", default="")
	parser.add_argument("--restricted_headers", type=str, help="Enable restricted headers. Default is false.", default='false')
	parser.add_argument("--tcp_connection", type=str, help="Availble for the save option. Set to true to send requests to Postman. Default is False.", default='false')
	parser.add_argument("--tcp_host", help="TCP host to forward to", default="127.0.0.1")
	parser.add_argument("--tcp_port", help="TCP port", default=5005)
	# parser.add_option("-s", "--status_codes", dest="status_codes", help="Comma separated list of allowed status codes. Default is all codes", default=[])

	args = parser.parse_args()

	operation = args.operation

	if operation == "save":
		start_creator_proxy(args)
	elif operation == "filter":
		start_filter_proxy(args)
	else:
		start_creator_proxy(args)

if __name__ == "__main__":
    main()