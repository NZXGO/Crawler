# -*- coding: utf-8 -*-
"""
Created on Sat Mar 25 20:49:36 2017

@author: 小甜甜
"""

from pymongo import MongoClient

class MongoCache:
    
    def __init__(self):
        self.client = MongoClient('localhost', 27017)
        self.db = self.client.cache
        print('.....Start Database.....')
        
        
    def __getitem__(self, url):
        
        row = self.db.webpage.find_one({'_id':url})
        if row is None:
            raise KeyError(url + ' does not exist, and need download again!!!')
        else:
            return row['html']
        
        
    def __setitem__(self, url, html):
        
        self.db.webpage.update_one({'_id':url}, {'$set':{'html':html}}, upsert=True)
