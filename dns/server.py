#!/usr/bin/env python2

""" A recursive DNS server

This module provides a recursive DNS server. You will have to implement this
server using the algorithm described in section 4.3.2 of RFC 1034.

See RFC 1034 section 3.6 for more information
"""

from socket import AF_INET, SOCK_STREAM
import socket
from threading import Thread


class RequestHandler(Thread):
    """ A handler for requests to the DNS server """

    def __init__(self, clientSocket, caching, ttl):
        """ Initialize the handler thread """
        super().__init__()
        self.daemon = True
        self.clientSocket = clientSocket
        
    def run(self):
        """ Run the handler thread """
        # Handle DNS request
        resolver = Resolver(caching, ttl)
        messageReceived = self.clientSocket.recv(1024)
        hostname = message 	# TODO Parse input
        ip = resolver.gethostbyname(hostname)
        messageSend = ip 	# TODO Create nice message
        self.clientSocket.send(messageSend)
        self.clientSocket.close()


class Server(object):
    """ A recursive DNS server """

    def __init__(self, port, caching, ttl):
        """ Initialize the server
        
        Args:
            port (int): port that server is listening on
            caching (bool): server uses resolver with caching if true
            ttl (int): ttl for records (if > 0) of cache
        """
        self.caching = caching
        self.ttl = ttl
        self.port = port
        self.done = False
        # Create socket
        self.webSocket = socket.socket(AF_INET, SOCK_STREAM)
        self.webSocket.bind(('', self.port))
        
    def serve(self):
        """ Start serving request """
        # Start listening
        self.webSocket.listen(1)
        while not self.done:
            # Receive request and open handler
            (reqSocket, address) = self.webSocket.accept()
            reqHandler = RequestHandler(reqSocket, caching, ttl)
            
    def shutdown(self):
        """ Shutdown the server """
        self.done = True
        # shutdown socket
		self.webSocket.close()
