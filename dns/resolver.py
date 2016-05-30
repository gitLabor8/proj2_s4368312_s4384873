#!/usr/bin/env python2

""" DNS Resolver

This module contains a class for resolving hostnames. You will have to implement
things in this module. This resolver will be both used by the DNS client and the
DNS server, but with a different list of servers.
"""

import socket

from dns.classes import Class
from dns.types import Type

import dns.cache
import dns.message
import dns.rcodes

class Resolver(object):
    """ DNS resolver """
    
    def __init__(self, caching, ttl):
        """ Initialize the resolver
        
        Args:
            caching (bool): caching is enabled if True
            ttl (int): ttl of cache entries (if > 0)
        """
        self.caching = caching
        self.ttl = ttl

    def lookupAliases(self, dname, cache):
        """ Recursive cache lookup of CNAME resource records to find all
        aliases of a given domain name
        
        Args:
            dname (str): the domain name for which to look up aliases
            cache (RecordCache): the cache to perform the lookup in
        Returns:
            [ResourceRecord]: aliasrrlist
        """
        foundRecords = cache.lookup(dname, Type.CNAME, Class.IN)
        aliasRecords = foundRecords
        for foundRecord in foundRecords:
            aliasRecords.extend(self.lookupAliases(foundRecord.rdata.data, cache))
        return aliasRecords

    def gethostbyname(self, domainname):
        """ Translate a domain name to IPv4 address.

        Currently this method contains an example. You will have to replace
        this example with example with the algorithm described in section
        5.3.3 in RFC 1034.

        Args:
            domainname (str): the domain name to resolve

        Returns:
            (str, [str], [str]): (domainname, aliaslist, ipaddrlist)
        """
        timeout = 2 # the time waited for a response
        found = False
        servername = "8.8.8.8"
        serverport = 53
        searchname = domainname
        aliases = [domainname]
        addresses = []
        hintsStart = ["198.41.0.4","192.228.79.201","192.33.4.12","199.7.91.13","192.203.230.10","192.5.5.241","192.112.36.4","198.97.190.53","192.36.148.17","192.58.128.30","193.0.14.129","199.7.83.42","202.12.27.33"]
        hints = []
        hintdex = 0
        rCache = dns.cache.RecordCache(self.ttl)
        rCache.read_cache_file()
        while not found:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(timeout)
            if self.caching:
                CNrecords = self.lookupAliases(searchname, rCache)
                for CNrecord in CNrecords:
                    aliases.append(CNrecord.rdata.data)
                for alias in aliases:
                    Arecords = rCache.lookup(alias, Type.A, Class.IN)
                    for Arecord in Arecords:
                        addresses.append(Arecord.rdata.data)
                        found = True
                if not found:
                    NSrecords = rCache.lookup(searchname, Type.NS, Class.IN)
                    if not NSrecords == []:
                        NSaddresses = []
                        for NSrecord in NSrecords:
                            NSaddresses.extend(rCache.lookup(NSrecord.rdata.data, Type.A, Class.IN))
                        for NSaddress in NSaddresses:
                            hints.append(NSaddress.rdata.data)
            hints.extend(hintsStart)
            servername = hints[hintdex]
            
            # Create and send query
            question = dns.message.Question(searchname, Type.A, Class.IN)
            header = dns.message.Header(9001, 0, 1, 0, 0, 0)
            header.qr = 0
            header.opcode = 0
            header.rd = 0
            query = dns.message.Message(header, [question])
            sock.sendto(query.to_bytes(), (servername, serverport))
    
            # Receive response
            data = sock.recv(512)
            response = dns.message.Message.from_bytes(data)
    
            # Get data
            if header.rd:
                for additional in response.additionals:
                    if additional.type_ == Type.CNAME:
                        aliases.append(additional.rdata.data)
                        if self.caching:
                            rCache.add_record(additional)
                for answer in response.answers:
                    if answer.type_ == Type.A:
                        addresses.append(answer.rdata.data)
                        found = True
                        if self.caching:
                            rCache.add_record(answer)
            if not found:
                for answer in response.answers:
                    if self.caching:
                        rCache.add_record(answer)
                    if answer.type_ == Type.A:
                        addresses.append(answer.rdata.data)
                        found = True
                    if answer.type_ == Type.CNAME:
                        searchname = answer.rdata.data
                        aliases.append(searchname)
                        for additional in response.additionals:
                            if additional.name == searchname and additional.type_ == Type.A:
                                addresses.append(additional.rdata.data)
                                found = True
                                if self.caching:
                                    rCache.add_record(additional)
                            if additional.name == searchname and additional.type_ == Type.CNAME:
                                aliases.append(additional.rdata.data)
                                if self.caching:
                                    rCache.add_record(additional)
                for authority in response.authorities:
                    if self.caching:
                        rCache.add_record(authority)
                    if authority.type_ == Type.NS:
                        nsName = authority.rdata.data
                        for additional in response.additionals:
                            if additional.name == nsName and additional.type_ == Type.A:
                                hints.insert(hintdex + 1, additional.rdata.data)
                                if self.caching:
                                    rCache.add_record(additional)
                hintdex = hintdex + 1

        rCache.write_cache_file()
        return domainname, aliases, addresses
