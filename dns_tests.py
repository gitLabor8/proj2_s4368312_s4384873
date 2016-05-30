#!/usr/bin/env python2

""" Tests for your DNS resolver and server """

import unittest
import socket
import dns.message
import dns.resolver
import sys
from dns.types import Type
from dns.classes import Class

portnr = 8001
server = "localhost"

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
        header = dns.message.Header(37, 0, 1, 0, 0, 0)
        header.qr = 0
        header.opcode = 0
        header.aa = 0
        header.tc = 0
        header.rd = 1
        header.ra = 0
        header.z = 0
        header.rcode = 0
        qname = "www.funnygames.com"
        qtype = 255			# request for all records
        qclass = 1			# ANY
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
    parser.add_argument("-p", "--port", type=int, default=5001)
    args, extra = parser.parse_known_args()
    portnr = args.port
    server = args.server
    
    # Pass the extra arguments to unittest
    sys.argv[1:] = extra

    # Start test suite
    unittest.main()
