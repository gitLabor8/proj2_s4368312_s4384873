#!/usr/bin/env python2

""" A recursive DNS server

This module provides a recursive DNS server. You will have to implement this
server using the algorithm described in section 4.3.2 of RFC 1034.

See RFC 1034 section 3.6 for more information
"""

from socket import AF_INET, SOCK_DGRAM
import socket
from threading import Thread
from dns.resolver import Resolver
import dns.message


class RequestHandler(Thread):
    """ A handler for requests to the DNS server """
# Sources
# http://www.bogotobogo.com/python/Multithread/python_multithreading_subclassing_creating_threads.php
# http://www.binarytides.com/programming-udp-sockets-in-python/

    def __init__(self, requestMessage, clientAddr, caching, ttl):
        """ Initialize the handler thread """
        super(Thread, self).__init__()
        self.requestByte = requestMessage
        self.request = dns.message.Message.from_bytes(self.requestByte)
        self.clientAddr = clientAddr
        self.caching = caching
        self.ttl = ttl
        
    def run(self):
        """ Run the handler thread """
        # Handle DNS request
        resolver = Resolver(self.caching, self.ttl)
        # Works only for ONE question at the time
        hostname = self.request.questions[0].qname
        ip = resolver.gethostbyname(hostname)
        #messageSend = ip 	# TODO Create nice message
        messageSend = "Ack!"
        print "We're through the resolver!"
        # Crafting of the response
        
        respMessage = dns.message.Message(respHeader, [], [], [], [])
        respMessageByte = respMessage.to_bytes()
        self.clientSocket.send(respMessageByte, clientAddr)
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
        self.webSocket = socket.socket(AF_INET, SOCK_DGRAM)
        self.webSocket.bind(('', self.port))
        
    def serve(self):
        """ Start serving request """
        while not self.done:
            # Receive request and open handler
            d = self.webSocket.recvfrom(1024)
            requestMessage = d[0]
            clientAddr = d[1]
            if not requestMessage:
                break
            print "Server.serve, data: " + requestMessage
            reqHandler = RequestHandler(requestMessage, clientAddr, self.caching, self.ttl)
            reqHandler.run()
            
    def shutdown(self):
        """ Shutdown the server """
        self.done = True
        # shutdown socket, neccesairy?
        self.webSocket.close()
