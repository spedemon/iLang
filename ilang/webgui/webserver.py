
# ilang - Inference Language 
# Stefano Pedemonte
# Aalto University, School of Science, Helsinki
# Oct 2013, Helsinki 


import sys
import BaseHTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler

def serve(address,port):
    HandlerClass = SimpleHTTPRequestHandler
    ServerClass  = BaseHTTPServer.HTTPServer
    Protocol     = "HTTP/1.0"

    HandlerClass.protocol_version = Protocol
    httpd = ServerClass((address,port), HandlerClass)

    sa = httpd.socket.getsockname()
    print "Serving HTTP on", sa[0], "port", sa[1], "..."
    httpd.serve_forever()

if __name__ == "__main__": 
    serve()
