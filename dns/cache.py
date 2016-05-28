#!/usr/bin/env python2

"""A cache for resource records

This module contains a class which implements a cache for DNS resource records,
you still have to do most of the implementation. The module also provides a
class and a function for converting ResourceRecords from and to JSON strings.
It is highly recommended to use these.
"""

import json
import time

from dns.resource import ResourceRecord, RecordData
from dns.types import Type
from dns.classes import Class


class ResourceEncoder(json.JSONEncoder):
    """ Conver ResourceRecord to JSON
    
    Usage:
        string = json.dumps(records, cls=ResourceEncoder, indent=4)
    """
    def default(self, obj):
        if isinstance(obj, ResourceRecord):
            return {
                "name": obj.name,
                "type": Type.to_string(obj.type_),
                "class": Class.to_string(obj.class_),
                "ttl": obj.ttl,
                "rdata": obj.rdata.data
            }
        return json.JSONEncoder.default(self, obj)


def resource_from_json(dct):
    """ Convert JSON object to ResourceRecord
    
    Usage:
        records = json.loads(string, object_hook=resource_from_json)
    """
    name = dct["name"]
    type_ = Type.from_string(dct["type"])
    class_ = Class.from_string(dct["class"])
    ttl = dct["ttl"]
    rdata = RecordData.create(type_, dct["rdata"])
    return ResourceRecord(name, type_, class_, ttl, rdata)


class RecordCache(object):
    """ Cache for ResourceRecords """

    def __init__(self, ttl):
        """ Initialize the RecordCache
        
        Args:
            ttl (int): TTL of cached entries (if > 0)
        """
        self.records = []
        self.ttl = ttl

    def lookup(self, dname, type_, class_):
        """ Lookup resource records in cache

        Lookup for the resource records for a domain name with a specific type
        and class.
        
        Args:
            dname (str): domain name
            type_ (Type): type
            class_ (Class): class
        """
        found = []
        for (record, stamp) in self.records:
            if time.time() > time.mktime(stamp) + record.ttl:
                self.records.remove((record, stamp))
            else:
                if record.name == dname and record.type_ == type_ and record.class_ == class_:
                    found.append(record)
        return found
    
    def add_record(self, record):
        """ Add a new Record to the cache
        
        Args:
            record (ResourceRecord): the record added to the cache
        """
        if self.ttl > 0:
            if record.ttl > self.ttl:
                record.ttl = self.ttl
        self.records.append((record,time.localtime()))
    
    def read_cache_file(self):
        """ Read the cache file from disk """
        cFile = open("dnsCache", "r")
        jrecords = cFile.readlines()
        for jrecord in jrecords:
            self.records.append(resource_from_json(jrecord))

    def write_cache_file(self):
        """ Write the cache file to disk """
        cFile = open("dnsCache", "w")
        for record in self.records:
            cFile.write(ResourceEncoder.default(record))