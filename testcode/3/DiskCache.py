# -*- coding: utf-8 -*-
"""
Created on Thu Mar 23 17:34:07 2017

@author: 小甜甜
"""

from __future__ import print_function, division
import re
import os
import urlparse
import pickle

class DiskCache:
    
    def __init__(self, cache_dir='cache', max_length=255):
        self.cache_dir = cache_dir
        self.max_length = max_length
        
    def url_to_path(self, url):
        components = urlparse.urlsplit(url)
        
        path = components.path
        if not path:
            path = '/index.html'
        elif path.endswith('/'):
            path += '/index.html'
        filename = components.netloc + path + components.query
        
        filename = re.sub('[\/?:*><|]', '_', filename)
        filename = '_'.join(segment[:255] for segment in filename.split('_'))
        return os.path.join(self.cache_dir, filename)
    
    def __getitem__(self, url):
        path = self.url_to_path(url)
        if os.path.exists(path):
            with open(path, 'rb') as fp:
                return pickle.load(fp)
        else:
            raise KeyError(url + ' does not exist, and need download again!!!')
    
    def __setitem__(self, url, result):
        
        path = self.url_to_path(url)
        folder = os.path.dirname(path)
        if not os.path.exists(folder):
            os.makedirs(folder)
        with open(path, 'wb') as fp:
            fp.write(pickle.dumps(result))
        