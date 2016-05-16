#!/usr/bin/env python2

""" A recursive DNS server

This module provides a recursive DNS server. You will have to implement this
server using the algorithm described in section 4.3.2 of RFC 1034.
"""

import socket
from socket import AF_INET, SOCK_STREAM
from threading import Thread


class RequestHandler(Thread):
    """ A handler for requests to the DNS server """

    def __init__(self, reqSocket, address):
        """ Initialize the handler thread """
        super().__init__()
        self.daemon = True
        self.socket = reqSocket
        self.address = address
        
    def run(self):
        """ Run the handler thread """
        # TODO: Handle DNS request        
        listServerAdresses 
        FQDNstring = self.socket.recv(1024)
        print "\nFQDNstring: " + FQDNstring + "\n"
        # TODO: remove hardcoded caching, ttl & timeout
        resolver = Resolver(self, 0, 60, 0.5)
        resolver.gethostbyname(FQDNstring)
        pass


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
        # TODO: create socket
        webSocket = socket.socket(AF_INET,SOCK_STREAM)
        webSocket.bind(('',self.port))

    def serve(self):
        """ Start serving request """
        # TODO: start listening
        webSocket.listen(1)
        while not self.done:
            # TODO: receive request and open handler
            (reqSocket, address) = webSocket.accept()
            reqHandler = RequestHandler(reqSocket, address)
            reqHandler.run()
            pass

    def shutdown(self):
        """ Shutdown the server """
        self.done = True
        # TODO: shutdown socket
		
