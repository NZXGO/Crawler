# -*- coding: utf-8 -*-
"""
Created on Tue Mar 21 16:14:51 2017
解析robot.txt文件，判断该用户代理是否合法
@author: 小甜甜
"""

import robotparser

rp = robotparser.RobotFileParser()
rp.set_url('http://example.webscraping.com/robots.txt')
rp.read()
url = 'http://example.webscraping.com'
user_agent = 'BadCrawler'
print( rp.can_fetch(user_agent, url) )

user_agent = 'GoodCrawler'
print( rp.can_fetch(user_agent, url) )

user_agent = 'tt'
print( rp.can_fetch(user_agent, url) )