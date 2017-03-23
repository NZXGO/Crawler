# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 14:19:55 2017

@author: 小甜甜
"""

from __future__ import print_function, division
import urllib2
import urlparse
import datetime
import time
import random


class Throttle:
    """
        下载延迟类
    """
    def __init__(self, delay):
        self.delay = delay
        self.demains = {}
        
    def wait(self, url):
        """
        这种做法有点叼啊，应对那种分布式的服务器
        """
        #获取服务器位置信息
        domain = urlparse.urlparse(url).netloc
        last_accessed = self.demains.get(domain)
        
        if self.delay > 0 and last_accessed is not None:
            sleep_secs = self.delay - (datetime.datetime.now()-last_accessed).seconds
            if sleep_secs > 0:
                time.sleep(sleep_secs)                         
        self.demains[domain] = datetime.datetime.now()

class DownLoader:
    
    def __init__(self, delay=1, user_agent='tt', proxies=None,
                 num_retries=1, cache=None):
        self.throttle = Throttle(delay)
        self.user_agent = user_agent
        self.proxies = proxies
        self.num_retries = num_retries
        self.cache = cache

    def download(self, url, headers, proxy, num_retries):
        print( 'Downloading:', url )
        request = urllib2.Request(url, headers=headers) 
        opener = urllib2.build_opener()
        code = 0
        if proxy:
            proxy_params = {urlparse.urlparse(url).scheme: proxy}
            opener.add_handler(urllib2.ProxyHandler(proxy_params))
        try:
            html = opener.open(request).read()
        except urllib2.URLError as e:
            print( 'Download error', e.reason )
            html = None
            if hasattr(e, 'code'):
                code = e.code
                if 500 <= e.code <600:
                    if num_retries > 0:
                        #recursively retry 5xx HTTP errors
                        return self.download(url, headers, proxy, num_retries-1)
            
        return {'html':html, 'code':code }
        
    def __call__(self, url):
        result = None
        if self.cache:
            
            try:
                result = self.cache[url]
            except KeyError:
                pass
            else:
                if self.num_retries>0 and 500<=result['code']<600:
                    result = None
        
        if result is None:
            self.throttle.wait(url)
            proxy = random.choice(self.proxies) if self.proxies else None
            headers = {'User-agent': self.user_agent}
            result = self.download(url, headers, proxy, self.num_retries)
            if self.cache:
                self.cache[url] = result
        
        return result['html']
        
                             
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        