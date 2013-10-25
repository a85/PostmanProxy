from postman.Collection import Collection
from postman.CollectionCreatorProxy import CollectionCreatorProxy
from libmproxy import controller, proxy

def main():
	print "Hey! This is the Postman proxy!"
	config = proxy.ProxyConfig()
	server = proxy.ProxyServer(config, 8080)
	m = CollectionCreatorProxy(server)
	m.run()


if __name__ == "__main__":
    main()