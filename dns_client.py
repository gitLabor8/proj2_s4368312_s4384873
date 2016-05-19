#!/usr/bin/env python2

""" Simple DNS client

A simple example of a client using the DNS resolver.
"""
import unittest
import logging
import socket
import sys
import time

import dns.resolver

portnr = 8001
timeout = 15

if __name__ == "__main__":
    # Parse arguments
    import argparse
    parser = argparse.ArgumentParser(description="DNS Client")
    parser.add_argument("hostname", help="hostname to resolve")
    parser.add_argument("-c", "--caching", action="store_true",
            help="Enable caching")
    parser.add_argument("-t", "--ttl", metavar="time", type=int, default=0, 
            help="TTL value of cached entries")
    args = parser.parse_args()
    
    # Resolve hostname
	"""Prepare for testing"""
	self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	self.client_socket.connect(("localhost", portnr))
	self.parser = webhttp.parser.ResponseParser()
	
	
	# Send the request
	#header, questions=[], answers=[], authorities=[], additionals=[]):
    header = ""
    questions = ["",""]
    answers = ["",""]
    authorities = ["", ""]
    additionals = ["",""]
    request = Message(header, questions, answers, authorities, additionals)
	self.client_socket.send(request.toBytes)

	# Test response
	byteResponse = self.client_socket.recv(1024)
	response = Message.(byteResponse)
	response.getResources
	# possible asserts
    
    """Clean up after testing"""
	self.client_socket.shutdown(socket.SHUT_RDWR)
	self.client_socket.close()

	## Resolve hostname (Using cheats)
    #resolver = dns.resolver.Resolver(args.caching, args.ttl)
    #hostname, aliases, addresses = resolver.gethostbyname(args.hostname)
    
    # Print output
    print(hostname)
    print(aliases)
    print(addresses)


	
