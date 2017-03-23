# -*- coding: utf-8 -*-
"""
Created on Thu Mar 23 15:30:54 2017

@author: 小甜甜
"""

import re
import urlparse

url = 'http://example.webscraping.com/view/United-Kingdom-239'
#windows文件系统非法文件名字符
filename =  re.sub('[\/?:*><|]', '_', url)
print(filename)
#for segment in filename.split('_'):
#    print(segment)

filename = '_'.join(segment[:255] for segment in filename.split('_'))
print(filename)


components = urlparse.urlsplit('http://example.webscraping.com/index/')
print(components)
path = components.path
if not path:
    path = '/index.html'
elif path.endswith('/'):
    path += 'index.html'
filename = components.netloc + path + components.query
print(filename)
filename =  re.sub('[\/?:*><|]', '_', filename)
print(filename)
#for segment in filename.split('_'):
#    print(segment)

filename = '_'.join(segment[:255] for segment in filename.split('_'))
print(filename)