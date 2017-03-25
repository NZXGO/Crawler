# -*- coding: utf-8 -*-
"""
Created on Thu Mar 23 21:03:15 2017

@author: 小甜甜
"""

from pymongo import MongoClient

client = MongoClient('localhost', 27017)

url = 'http://example.webscraping.com/view/United-Kingdom-239'

html = '...***...'
new_html = '................'
db = client.cache
print(db.name)

#插入数据
db.webpage.insert_one({'url':url, 'html':html})
#print(db.webpage)
#查询数据
row = db.webpage.find_one({'url':url})
if row is not None:
    print(row['html'])

#修改数据 upsert=True表示查询不到该数据就创建一条新数据
db.webpage.update_one({'url':url}, {'$set':{'html':new_html}}, upsert=True)
    

#遍历数据
for row in db.webpage.find():
    print(row)
    #删除数据
    #db.webpage.delete_one(row)