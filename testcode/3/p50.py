# -*- coding: utf-8 -*-
"""
Created on Thu Mar 23 21:03:15 2017

@author: 小甜甜
"""

from pymongo import MongoClient

client = MongoClient('localhost', 27017)

url = 'http://example.webscraping.com/view/United-Kingdom-239'

html = '...'

db = client.cache
print(db.name)
db.webpage.insert_one({'url':url, 'html':html})
print(db.webpage)
print(db.webpage.find_one(url))
