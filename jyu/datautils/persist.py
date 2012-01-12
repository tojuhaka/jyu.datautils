# -*- coding: utf-8 -*-

from persistent.list import PersistentList
from persistent.dict import PersistentDict
import persistent

# Convert all the dicts, lists and their children
# to persistent
def to_persistent(data): 
    if not type(data) in (list, dict):
        return data

    if type(data) == list:
        new = PersistentList()
        for item in data:
            new.append(to_persistent(item))
        return new

    if type(data) == dict:
        new = PersistentDict()
        for key, item in data.items():
            new[key] = to_persistent(item)
        return new

# Sideways
def to_normal(data):
    if not isinstance(data, persistent.Persistent):
        return data

    if isinstance(data,persistent.list.PersistentList):
        new = []
        for item in data:
            new.append(to_normal(item))
        return new

    if isinstance(data, persistent.mapping.PersistentMapping):
        new = {}
        for key, item in data.items():
            new[key] = to_normal(item)
        return new
         


