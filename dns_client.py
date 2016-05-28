#!/usr/bin/env python2

""" Simple DNS client

A simple example of a client using the DNS resolver.
"""
import unittest
import logging
import socket
import sys
import time
import dns.message
import dns.resolver

portnr = 8001
timeout = 15

website = "google.com"

if __name__ == "__main__":
    # Parse arguments
    import argparse
    parser = argparse.ArgumentParser(description="DNS Client")
    parser.add_argument("hostname", help="hostname to resolve", default="localhost")
    parser.add_argument("-c", "--caching", action="store_true",
            help="Enable caching")
    parser.add_argument("-t", "--ttl", metavar="time", type=int, default=0, 
            help="TTL value of cached entries")
    args = parser.parse_args()
    hostname = args.hostname
    
    # Resolve hostname
    """Prepare for testing"""
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#	self.parser = webhttp.parser.ResponseParser()
	
    # Send the request
    qname = website
    qtype = 255			# request for all records
    qclass = 1		# ANY
    request = dns.message.Question(qname, qtype, qclass)
    requestByte = request.to_bytes()
    client_socket.sendto(requestByte, (hostname, portnr))
#	self.client_socket.send(request.toBytes)

	# Test response
    d = client_socket.recvfrom(1024)
    reply = d[0]
    address = d[1]
    print "reply: " + reply
#	byteResponse = self.client_socket.recv(1024)
#	response = Message.(byteResponse)
#	response.getResources
	# possible asserts
    
	## Resolve hostname (Using cheats)
    #resolver = dns.resolver.Resolver(args.caching, args.ttl)
    #hostname, aliases, addresses = resolver.gethostbyname(args.hostname)
    
    # Print output
#    print(hostname)
 #   print(aliases)
  #  print(addresses)


	
