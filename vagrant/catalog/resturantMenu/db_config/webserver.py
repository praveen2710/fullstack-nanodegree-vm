from BaseHTTPServer import BaseHzttrequest, HTTPServer

class webServerHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		try:
			if self.path.endswith

def main():
	try:
		port = 8080
		server = HTTPServer(('',port),webserverHandler)
		print "Web Server running on port %s" % port 
		server.server_forever():


	except KeyboardInterrupt:
		print "^C entered , stopping server..."


if __name__ == '__main__':
	main()


