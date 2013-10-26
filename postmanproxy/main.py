from postman.collection import Collection
from postman.collection_creator_proxy import CollectionCreatorProxy
from libmproxy import controller, proxy
from optparse import OptionParser

def main():
	print "Hey! This is the Postman proxy!"
	rules = []

	collection = Collection("Postman")
	config = proxy.ProxyConfig()
	server = proxy.ProxyServer(config, 8080)
	m = CollectionCreatorProxy(server, collection, rules)
	m.run()

if __name__ == "__main__":
    main()