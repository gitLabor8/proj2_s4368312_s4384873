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

website = "www.google.com"

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
    client_socket.settimeout(2)
#	self.parser = webhttp.parser.ResponseParser()
	
    # Send the request
    header = dns.message.Header(37, 0, 1, 0, 0, 0)
    header.qr = 0
    header.opcode = 0
    header.aa = 0
    header.tc = 0
    header.rd = 1
    header.ra = 0
    header.z = 0
    header.rcode = 0
    
    qname = website
    qtype = 255			# request for all records
    qclass = 1			# ANY
    question = dns.message.Question(qname, qtype, qclass)
    request = dns.message.Message(header, [question], [], [], [])
    requestByte = request.to_bytes()
    client_socket.sendto(requestByte, (hostname, portnr))
    client_socket.sendto(requestByte, (hostname, portnr))
    client_socket.sendto(requestByte, (hostname, portnr))
    client_socket.sendto(requestByte, (hostname, portnr))
    client_socket.sendto(requestByte, (hostname, portnr))
    client_socket.sendto(requestByte, (hostname, portnr))
    client_socket.sendto(requestByte, (hostname, portnr))
    client_socket.sendto(requestByte, (hostname, portnr))
#	self.client_socket.send(request.toBytes)

	# Test response
    responseData = client_socket.recv(512)
    response = dns.message.Message.from_bytes(responseData)
    
    everything = ""
    for resource in response.resources:
        everything = everything + (resource.to_string()) + "\n"
    print "response:\n" + everything
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


	
