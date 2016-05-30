#!/usr/bin/env python2

""" Tests for your DNS resolver and server """

import unittest
import socket
import dns.message
import dns.resolver
import sys
from dns.types import Type
from dns.classes import Class
from random import randint 

# Tests without caching
class TestResolver(unittest.TestCase):
    def setUp(self):
        """Prepare for testing"""
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.client_socket.settimeout(15)
        
    def tearDown(self):
        self.client_socket.close()
       
    def test_single_lookup(self):
        """Ask for a single existing hostname"""
        dnsID = randint(0, 65535)
        header = dns.message.Header(dnsID, 0, 1, 0, 0, 0)
        header.qr = 0
        header.opcode = 0
        header.aa = 0
        header.tc = 0
        header.rd = 1
        header.ra = 0
        header.z = 0
        header.rcode = 0
        qname = "www.funnygames.com"
        qtype = Type.ANY         	# request for all records
        qclass = Class.IN		# ANY
        question = dns.message.Question(qname, qtype, qclass)
        request = dns.message.Message(header, [question], [], [], [])
        requestByte = request.to_bytes()
        self.client_socket.sendto(requestByte, (server, portnr))
        print Type.to_string(question.qtype) + Class.to_string(question.qclass)
        responseData = self.client_socket.recv(512)
        response = dns.message.Message.from_bytes(responseData)
        self.assertTrue(response.answer[0])
        
    def test_single_lookup_fail(self):
        pass
    
# Tests with caching
class TestResolverCache(unittest.TestCase):
    pass


class TestServer(unittest.TestCase):
    pass


if __name__ == "__main__":
    # Parse command line arguments
    import argparse
    parser = argparse.ArgumentParser(description="HTTP Tests")
    parser.add_argument("-s", "--server", type=str, default="localhost")
    parser.add_argument("-p", "--port", type=int, default=8001)
    args, extra = parser.parse_known_args()
    portnr = args.port
    server = args.server
    
    # Pass the extra arguments to unittest
    sys.argv[1:] = extra

    # Start test suite
    unittest.main()
